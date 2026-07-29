"""M2 backend contract and semantic golden corpus."""

import pytest

from grandportage import backend as B
from grandportage import cas
from grandportage import kernel as K
from grandportage import provenance as P
from grandportage import store as S
from grandportage import verify as V


def _raw(stdout, *, returncode=0, aborted=False, stderr=""):
    return {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "aborted": aborted,
        "abort_reason": "timeout" if aborted else None,
        "argv": ["Singular-test-double"],
    }


def _program(characteristic=0, outputs=None):
    outputs = outputs or ["GP_G"]
    return cas.CASProgram(
        cas.SINGULAR,
        ring="GP_R",
        ring_vars=["x"],
        decls=[("GP_G", "ideal", "std(ideal(x))")],
        body=[],
        outputs=outputs,
        characteristic=characteristic,
    )


def test_execution_artifact_snapshots_program_backend_raw_and_parsed_output():
    program = _program()
    backend = cas.SingularBackend(
        runner=lambda _program, _timeout: _raw("@@GP_G:\nGP_G[1]=x\n"),
        binary_version="Singular 9.9-test",
    )

    result = backend.execute(
        program,
        semantic_input={"operation": "basis", "generators": ["x"]},
    )
    values = cas._parse_result(result, program.outputs)
    artifact = result.artifact

    assert result["program"] is program
    assert artifact.backend.binary_version == "Singular 9.9-test"
    assert artifact.backend.implementation == "grandportage.cas.SingularBackend"
    assert artifact.program_text == program.text
    assert artifact.program_fingerprint == B.text_fingerprint(program.text)
    assert artifact.semantic_input_fingerprint.startswith("sha256:")
    assert artifact.stdout == "@@GP_G:\nGP_G[1]=x\n"
    assert artifact.stdout_fingerprint == B.text_fingerprint(artifact.stdout)
    assert artifact.stderr_fingerprint == B.text_fingerprint(artifact.stderr)
    assert artifact.parsed_output is not None
    assert values == {"GP_G": "GP_G[1]=x"}

    result["stdout"] = "mutated legacy dictionary"
    program.body.append("// mutated after execution")
    assert artifact.stdout == "@@GP_G:\nGP_G[1]=x\n"
    assert "// mutated" not in artifact.program_text


def test_parse_uses_the_frozen_stdout_not_a_mutated_legacy_field():
    program = _program()
    backend = cas.SingularBackend(
        runner=lambda _program, _timeout: _raw("@@GP_G:\nGP_G[1]=x\n"),
        binary_version="test",
    )
    result = backend.execute(program)
    result["stdout"] = "@@GP_G:\nGP_G[1]=not_the_run\n"

    values = cas._parse_result(result, program.outputs)

    assert values == {"GP_G": "GP_G[1]=x"}
    assert "not_the_run" not in result.artifact.parsed_output


def test_a_runner_cannot_smuggle_in_a_foreign_execution_artifact():
    program = _program()
    first = cas.SingularBackend(
        runner=lambda _program, _timeout: _raw("@@GP_G:\nGP_G[1]=x\n"),
        binary_version="first",
    ).execute(program)
    second = cas.SingularBackend(
        runner=lambda _program, _timeout: first,
        binary_version="second",
    )

    with pytest.raises(TypeError, match="pre-wrapped BackendExecution"):
        second.execute(_program(characteristic=2))

    assert second.executions == []


def test_verify_all_uses_semantic_backend_methods_not_cas_programs(tmp_path):
    S.append([
        {
            "ev": "model", "id": "M", "what": "the origin",
            "characteristic": 0, "ring_vars": ["x"], "generators": ["x"],
        },
        {
            "ev": "claim", "id": "C", "model": "M", "kind": K.IDENTITY,
            "statement": "x vanishes", "lhs": "x", "rhs": "0",
            "ring_vars": ["x"], "identity_origin": K.DERIVED,
            "established_by": "RAN", "ladder": "exact-checked",
        },
    ], str(tmp_path))

    class SemanticOnly(cas.SingularBackend):
        def __init__(self):
            super().__init__(runner=lambda *_args: None,
                             binary_version="test-double")
            self.calls = []

        def execute(self, *_args, **_kwargs):
            raise AssertionError("semantic verifier passed a CASProgram")

        def classify_identity(self, *_args, **_kwargs):
            self.calls.append("classify_identity")
            return K.DERIVED, {"difference": "x", "reduced_modulo_ideal": "0"}

        def membership(self, *_args, **_kwargs):
            self.calls.append("membership")
            return {"is_member": True, "cofactors": ["1"], "reduced": "0"}

        def check_membership(self, *_args, **_kwargs):
            self.calls.append("check_membership")
            return True, "0"

    backend = SemanticOnly()
    assert backend.identity.implementation.endswith(".<locals>.SemanticOnly")
    assert backend.can_record_verdicts is False
    with pytest.raises(ValueError, match="record=True requires"):
        V.verify_all(root=str(tmp_path), backend=backend, record=True)
    results = V.verify_all(root=str(tmp_path), backend=backend, record=False)

    assert backend.calls == [
        "classify_identity", "membership", "check_membership"
    ]
    assert [(subject, oid, verdict) for subject, oid, verdict, _ in results] == [
        ("claim", "C", V.DERIVED)
    ]


def test_derived_identity_without_a_replayable_representation_is_unverified():
    graph = S.Graph()
    graph.models["M"] = {
        "id": "M", "characteristic": 0, "ring_vars": ["x"],
        "generators": ["x"],
    }
    graph.claims["C"] = {
        "id": "C", "model": "M", "kind": K.IDENTITY,
        "lhs": "x", "rhs": "0", "ring_vars": ["x"],
    }

    class NoRepresentation(cas.SingularBackend):
        def classify_identity(self, *_args, **_kwargs):
            return K.DERIVED, {"reduced_modulo_ideal": "0"}

        def membership(self, *_args, **_kwargs):
            return {"is_member": True, "cofactors": None, "reduced": "0"}

    verdict, why = V.identity(
        graph, "C", _backend=NoRepresentation(
            runner=lambda *_args: None, binary_version="test"))

    assert verdict == V.UNVERIFIED
    assert "NO REPRESENTATION" in why


def test_verify_all_refuses_to_record_an_injected_runner(tmp_path):
    S.append([
        {
            "ev": "model", "id": "M", "what": "the origin",
            "characteristic": 0, "ring_vars": ["x"], "generators": ["x"],
        },
        {
            "ev": "claim", "id": "C", "model": "M", "kind": K.IDENTITY,
            "statement": "x vanishes", "lhs": "x", "rhs": "0",
            "ring_vars": ["x"], "identity_origin": K.DERIVED,
            "established_by": "RAN", "ladder": "exact-checked",
        },
    ], str(tmp_path))

    def runner(program, _timeout):
        stdout = "".join("@@%s:\n0\n" % output.upper()
                         for output in program.outputs)
        return _raw(stdout)

    with pytest.raises(ValueError, match="injected runners"):
        V.verify_all(root=str(tmp_path), _runner=runner, record=True)
    assert S.load(S.graph_path(str(tmp_path))).verdicts == {}


@pytest.mark.live
def test_verify_all_records_the_real_backend_trace_that_answered(tmp_path):
    S.append([
        {
            "ev": "model", "id": "M", "what": "the origin",
            "characteristic": 0, "ring_vars": ["x"], "generators": ["x"],
        },
        {
            "ev": "claim", "id": "C", "model": "M", "kind": K.IDENTITY,
            "statement": "x vanishes", "lhs": "x", "rhs": "0",
            "ring_vars": ["x"], "identity_origin": K.DERIVED,
            "established_by": "RAN", "ladder": "exact-checked",
        },
    ], str(tmp_path))

    V.verify_all(root=str(tmp_path), record=True, timeout=120)
    verdict = next(iter(S.load(S.graph_path(str(tmp_path))).verdicts.values()))
    manifest = P.backend_provenance(verdict["backend"])

    assert verdict["current"] is True
    assert manifest["contract"] == "singular"
    assert manifest["binary_version"] != "test-double"
    assert manifest["implementation"] == B.SINGULAR_IMPLEMENTATION
    assert manifest["executions"]
    assert all(B.valid_execution_trace_entry(entry)
               for entry in manifest["executions"])


def test_characteristic_is_part_of_the_semantic_program_fingerprint():
    assert (
        _program(characteristic=0).semantic_fingerprint
        != _program(characteristic=2).semantic_fingerprint
    )


def test_multi_output_parse_is_atomic_on_an_empty_second_marker():
    program = _program(outputs=["GP_G", "GP_M"])
    backend = cas.SingularBackend(
        runner=lambda _program, _timeout: _raw(
            "@@GP_G:\nGP_G[1]=1\n@@GP_M:\n"
        ),
        binary_version="test",
    )
    result = backend.execute(program)

    with pytest.raises(cas.CASError):
        cas._parse_result(result, program.outputs)

    assert result.artifact.parsed_output is None
    assert "parsed_values" not in result


def test_truncated_facstd_component_is_not_an_empty_ideal():
    backend = cas.SingularBackend(
        runner=lambda _program, _timeout: _raw(
            "@@GP_L:\n[1]:\n_[1]=x\n[2]:\n"
        ),
        binary_version="test",
    )

    with pytest.raises(cas.CASError, match="truncated facstd output"):
        backend.factorizing_decomposition(["x"], ["x"])


def test_named_saturation_and_elimination_keep_the_exact_executed_program():
    seen = []

    def runner(program, _timeout):
        seen.append(program)
        return _raw("@@GP_OUT:\nGP_OUT[1]=y\n")

    backend = cas.SingularBackend(runner=runner, binary_version="test")
    saturated = backend.saturate(["x", "y"], ["x^9*y"], "x")
    eliminated = backend.eliminate(
        ["x", "y", "z"], ["z", "x*(y-x^2)"], ["z"]
    )

    assert saturated["generators"] == ["y"]
    assert eliminated["ring_vars"] == ["x", "y"]
    assert eliminated["generators"] == ["y"]
    assert saturated["program"] is seen[0]
    assert eliminated["program"] is seen[1]
    assert saturated["execution"]["program"] is seen[0]
    assert eliminated["execution"]["program"] is seen[1]


def _assert_member(backend, ring, target, generators, characteristic=0):
    answer = backend.membership(
        ring, target, generators, characteristic=characteristic, timeout=120
    )
    assert answer["is_member"], answer
    ok, expanded = backend.check_membership(
        ring, target, generators, answer["cofactors"],
        characteristic=characteristic, timeout=120,
    )
    assert ok, expanded


@pytest.mark.live
def test_golden_characteristic_dependent_membership():
    backend = cas.SingularBackend()

    over_q = backend.membership(
        ["x"], "x^2+1", ["x+1"], characteristic=0, timeout=120
    )
    over_f2 = backend.membership(
        ["x"], "x^2+1", ["x+1"], characteristic=2, timeout=120
    )

    assert over_q["is_member"] is False
    assert over_q["reduced"] == "2"
    assert over_f2["is_member"] is True
    assert backend.executions[-1].artifact.certificate is not None
    _assert_member(
        backend, ["x"], "x^2+1", ["x+1"], characteristic=2
    )

    for generators in (
        ["x+y", "x-y"],
        ["y-x", "-(x+y)"],
    ):
        answer = backend.membership(
            ["x", "y"], "3*x+y", generators, timeout=120
        )
        assert answer["is_member"], answer
        ok, expanded = backend.check_membership(
            ["x", "y"], "3*x+y", generators, answer["cofactors"],
            timeout=120,
        )
        assert ok, expanded
        wrong, _ = backend.check_membership(
            ["x", "y"], "3*x+y", generators,
            list(reversed(answer["cofactors"])), timeout=120,
        )
        assert wrong is False


@pytest.mark.live
def test_golden_saturation_beyond_the_old_witness_bound():
    backend = cas.SingularBackend()
    answer = backend.saturate(
        ["x", "y"], ["x^9*y"], "x", characteristic=0, timeout=120
    )

    _assert_member(backend, ["x", "y"], "y", answer["generators"])
    for generator in answer["generators"]:
        _assert_member(backend, ["x", "y"], generator, ["y"])

    for exponent in range(9):
        probe = backend.membership(
            ["x", "y"], "x^%d*y" % exponent, ["x^9*y"], timeout=120
        )
        assert probe["is_member"] is False
    _assert_member(backend, ["x", "y"], "x^9*y", ["x^9*y"])


@pytest.mark.live
def test_golden_non_involution_pullback_and_compact_elimination():
    backend = cas.SingularBackend()

    reduced, zero = backend.pullback_reduce(
        ["x"], "x-1", {"x": "x+1"}, generators=["x"], timeout=120
    )
    assert zero, reduced
    reduced, zero = backend.pullback_reduce(
        ["x"], "x", {"x": "x-1"}, generators=["x-1"], timeout=120
    )
    assert zero, reduced

    eliminated = backend.eliminate(
        ["x", "y", "z"], ["z", "x*(y-x^2)"], ["z"], timeout=120
    )
    assert all("z" not in generator for generator in eliminated["generators"])
    _assert_member(
        backend, ["x", "y"], "x^3-x*y", eliminated["generators"]
    )
    for generator in eliminated["generators"]:
        _assert_member(
            backend, ["x", "y"], generator, ["x^3-x*y"]
        )


@pytest.mark.live
def test_golden_geometric_hole_and_overlapping_decomposition():
    backend = cas.SingularBackend()

    covered, evidence = backend.partition_cover(
        ["x"], ["x^2+1"], [["x^2+1", "x"], ["x^2+1", "x-1"]],
        timeout=120,
    )
    assert covered is False
    assert evidence["uncovered"]
    _assert_member(backend, ["x"], "1", evidence["uncovered"])
    for generator in evidence["uncovered"]:
        _assert_member(backend, ["x"], generator, ["1"])

    pieces = backend.factorizing_decomposition(
        ["x", "y"], ["x*y*(x-y)"], timeout=120
    )
    assert len(pieces) == 3
    for piece in pieces:
        _assert_member(backend, ["x", "y"], "x*y*(x-y)", piece)
        is_origin, evidence = backend.evaluate_point(
            ["x", "y"], piece, {"x": 0, "y": 0}, timeout=120
        )
        assert is_origin, evidence
    covered, evidence = backend.partition_cover(
        ["x", "y"], ["x*y*(x-y)"], pieces, timeout=120
    )
    assert covered, evidence

    one_piece = backend.factorizing_decomposition(
        ["x", "y"], ["x^2+y", "y^2+x"], timeout=120
    )
    assert len(one_piece) == 1
    input_ideal = ["x^2+y", "y^2+x"]
    returned_ideal = one_piece[0]
    for generator in input_ideal:
        _assert_member(backend, ["x", "y"], generator, returned_ideal)
    for generator in returned_ideal:
        _assert_member(backend, ["x", "y"], generator, input_ideal)
    _assert_member(
        backend, ["x", "y"], "y*(y^3+1)", returned_ideal
    )
    assert backend.membership(
        ["x", "y"], "y", returned_ideal, timeout=120
    )["is_member"] is False
    assert backend.membership(
        ["x", "y"], "y^3+1", returned_ideal, timeout=120
    )["is_member"] is False
