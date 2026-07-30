"""Singular production, proof persistence, and replay controls."""

import copy
import json
import sys
import time

import pytest

from grandportage import artifacts as A
from grandportage import backend as B
from grandportage import cas
from grandportage import check as C
from grandportage import format as F
from grandportage import groebner_producer as GP
from grandportage import kernel as K
from grandportage import provenance as P
from grandportage import store as S
from grandportage import verify as V


def _raw(program, body, returncode=0, stderr=""):
    return {
        "returncode": returncode,
        "stdout": body + program.completion_marker + "\n",
        "stderr": stderr,
        "aborted": False,
        "abort_reason": None,
        "argv": ["Singular-test"],
    }


def _producer_runner(program, _timeout):
    if program.outputs == ["GP_G", "GP_B"]:
        return _raw(program, """@@GP_G:
GP_G[1]=y^2-x^3
GP_G[2]=u*x-y
GP_G[3]=u*y-x^2
GP_G[4]=u^2-x
@@GP_B:
GP_B[1,1]=0
GP_B[1,2]=0
GP_B[2,1]=0
GP_B[2,2]=1
GP_B[3,1]=0
GP_B[3,2]=0
GP_B[4,1]=1
GP_B[4,2]=u
""")
    assert program.outputs == ["GP_M"]
    return _raw(program, "@@GP_M:\nGP_M[1,1]=1/2\n")


def _backend(runner=_producer_runner):
    return cas.SingularBackend(
        runner=runner, binary_version="Singular 4.2.1"
    )


def _native_cusp_graph():
    graph = S.Graph()
    graph.apply(F.meta_event())
    graph.apply({
        "ev": "model", "id": "SOURCE", "what": "normalization",
        "characteristic": 0, "ring_vars": ["u", "y", "x"],
        "generators": ["u^2-x", "u^3-y"],
    })
    graph.apply({
        "ev": "model", "id": "TARGET", "what": "cusp",
        "characteristic": 0, "ring_vars": ["y", "x"],
        "generators": ["2*y^2-2*x^3"], "eliminated": ["u"],
    })
    graph.apply({
        "ev": "edge", "id": "E", "src": "SOURCE", "dst": "TARGET",
        "type": K.IMAGE_CLOSURE, "map_kind": K.POLYNOMIAL,
        "why": "eliminate the normalization parameter",
        "built_by_operation": "Eliminate",
    })
    return graph


def _produce(backend=None):
    backend = backend or _backend()
    produced = GP.produce_elimination_groebner(
        backend,
        ["u", "y", "x"],
        ["u^2-x", "u^3-y"],
        ["u"],
        ["2*y^2-2*x^3"],
    )
    return backend, produced


def test_cas_program_order_is_closed_rendered_and_fingerprinted():
    common = dict(
        dialect=cas.SINGULAR, ring="R", ring_vars=["x"],
        decls=[("I", "ideal", "x")], body=[], outputs=["I"],
    )
    dp = cas.CASProgram(ordering="dp", **common)
    lp = cas.CASProgram(ordering="lp", **common)

    assert "ring R = 0,(x),dp;" in dp.text
    assert "ring R = 0,(x),lp;" in lp.text
    assert dp.semantic_fingerprint != lp.semantic_fingerprint
    with pytest.raises(ValueError, match="closed Singular order"):
        cas.CASProgram(ordering="lp; execute", **common)


def test_windows_wsl_command_places_singular_under_an_inner_timeout():
    wrapped = cas._limited_argv(
        ["wsl.exe", "--", "Singular", "-q"], 7
    )
    if cas.os.name == "nt":
        assert wrapped[:7] == [
            "wsl.exe", "--", "timeout", "--signal=KILL",
            "--kill-after=2s", "7s", "Singular",
        ]
    else:
        assert wrapped == ["wsl.exe", "--", "Singular", "-q"]


def test_backend_output_is_bounded_and_overflow_aborts(monkeypatch):
    monkeypatch.setattr(cas, "_MAX_STDOUT_BYTES", 128)
    monkeypatch.setattr(cas, "_MAX_STDERR_BYTES", 128)
    monkeypatch.setattr(cas, "_argv", lambda: [
        sys.executable, "-c",
        "import sys; sys.stdout.write('x' * 10000); sys.stdout.flush()",
    ])
    program = type("Program", (), {"text": ""})()

    result = cas._run_subprocess(program, timeout=10)

    assert result["returncode"] == 125
    assert result["aborted"] is True
    assert result["abort_reason"] == "output limit"
    assert len(result["stdout"].encode("utf-8")) <= 128
def test_ring_identifier_cannot_be_redeclared():
    with pytest.raises(cas.IdentifierCollision, match="SHADOWS"):
        cas.CASProgram(
            cas.SINGULAR, ring="R", ring_vars=["x"],
            decls=[("R", "matrix", "0")], body=[], outputs=["R"],
        )


def test_strict_matrix_parser_pins_orientation_and_full_coverage():
    value = [
        "M[1,1]=1", "M[1,2]=2", "M[2,1]=3", "M[2,2]=4",
    ]
    assert GP._strict_matrix(value, "M", 2, 2, ["x"], 0) == [
        ["1", "2"], ["3", "4"],
    ]
    with pytest.raises(cas.CASError, match="exactly its 2-by-2"):
        GP._strict_matrix(value[:-1], "M", 2, 2, ["x"], 0)


def test_hostile_basis_output_is_rejected_before_reuse():
    def hostile(program, _timeout):
        assert program.outputs == ["GP_G", "GP_B"]
        return _raw(program, """@@GP_G:
GP_G[1]=x; execute("quit")
@@GP_B:
GP_B[1,1]=1
GP_B[1,2]=0
""")

    backend = _backend(hostile)
    with pytest.raises(cas.CASError, match="exact polynomial language"):
        GP.produce_elimination_groebner(
            backend, ["u", "x"], ["u-x", "x"], ["u"], ["x"]
        )
    assert backend.execution_count == 1


def test_producer_builds_the_checked_cusp_proof_and_binds_final_artifact():
    backend, produced = _produce()

    assert produced["checked"]["critical_pair_count"] == 6
    assert produced["proof"]["source_in_basis"] == [
        ["0", "0", "0", "1"], ["0", "1", "0", "u"],
    ]
    assert produced["proof"]["retained_in_target"] == [["1/2"]]
    assert len(backend.executions) == 2
    assert all(run.program.ordering == "lp" for run in backend.executions)
    assert json.loads(backend.executions[-1].artifact.certificate) == (
        produced["proof"])
    assert "ordering lp" not in backend.executions[0].artifact.program_text
    assert ",lp;" in backend.executions[0].artifact.program_text


def test_phase_two_failure_leaves_no_certificate_authority():
    def fail_second(program, timeout):
        if program.outputs == ["GP_G", "GP_B"]:
            return _producer_runner(program, timeout)
        return _raw(
            program, "@@GP_M:\n", returncode=1, stderr="phase two failed"
        )

    backend = _backend(fail_second)
    with pytest.raises(cas.CASError):
        _produce(backend)
    assert len(backend.executions) == 2
    assert all(run.artifact.certificate is None for run in backend.executions)


def test_persisted_groebner_verdict_opens_only_exact_contraction():
    graph = _native_cusp_graph()
    backend, produced = _produce()
    verdict, why, representation = V.elimination_groebner(
        graph, "E", produced["proof"]
    )
    event = V._verdict_event(
        graph, "elimination", "E", verdict, why, representation,
        execution=backend.provenance(),
        verifier="verify.elimination_groebner",
    )
    graph.apply(event)
    graph.edges["E"]["output_verdict"] = V.OP_SOUND

    # This explanation is CLI output. Keep it printable on strict legacy
    # Windows streams (the W7 live run exposed a post-verification cp1252
    # crash when mathematical subset/intersection glyphs were used here).
    why.encode("ascii")

    assert graph.verdicts[event["id"]]["current"] is True
    assert graph.edges["E"]["contraction_verdict"] == V.GROEBNER_VERIFIED
    assert C.effective_exact_contraction(graph.edges["E"])
    assert not C.effective_geometric_closure(graph.edges["E"])
    assert not C.effective_image_complete(graph.edges["E"])


def test_recomputed_fingerprint_cannot_turn_a_false_proof_into_authority():
    graph = _native_cusp_graph()
    backend, produced = _produce()
    verdict, why, representation = V.elimination_groebner(
        graph, "E", produced["proof"]
    )
    event = V._verdict_event(
        graph, "elimination", "E", verdict, why, representation,
        execution=backend.provenance(),
        verifier="verify.elimination_groebner",
    )
    event = copy.deepcopy(event)
    event["representation"]["proof"]["critical_pairs"][0]["reducers"][0] = "0"
    event["input_fingerprint"] = P.input_fingerprint(
        graph, "elimination", "E", event["representation"]
    )
    event["id"] = "v.E.%s" % P.event_digest(event)

    with pytest.raises(S.GraphError, match="exact checker"):
        graph.apply(event)


def test_artifact_audit_binds_final_producer_proof(tmp_path):
    root = str(tmp_path)
    graph = _native_cusp_graph()
    backend, produced = _produce()
    verdict, why, representation = V.elimination_groebner(
        graph, "E", produced["proof"]
    )
    A.persist_all(root, backend.execution_artifacts())
    event = V._verdict_event(
        graph, "elimination", "E", verdict, why, representation,
        execution=backend.provenance(),
        verifier="verify.elimination_groebner",
    )
    graph.apply(event)
    assert A.audit_graph(root, graph) == []

    event["representation"]["proof"]["basis"][0] = "x"
    assert any("does not match the verdict proof" in problem
               for problem in A.audit_graph(root, graph))
@pytest.mark.live
def test_real_singular_end_to_end_produces_the_checked_cusp_certificate():
    backend = cas.SingularBackend()
    produced = GP.produce_elimination_groebner(
        backend,
        ["u", "y", "x"],
        ["u^2-x", "u^3-y"],
        ["u"],
        ["2*y^2-2*x^3"],
        timeout=120,
    )

    assert produced["checked"]["critical_pair_count"] == 6
    assert produced["proof"]["retained_in_target"] == [["1/2"]]
    assert len(backend.executions) == 2
    assert all(",lp;" in run.artifact.program_text
               for run in backend.executions)
@pytest.mark.live
def test_real_wrapper_persists_checked_authority_and_both_artifacts(tmp_path):
    root = str(tmp_path)
    S.append([
        {"ev": "model", "id": "SOURCE", "what": "normalization",
         "characteristic": 0, "ring_vars": ["u", "y", "x"],
         "generators": ["u^2-x", "u^3-y"]},
        {"ev": "model", "id": "TARGET", "what": "cusp",
         "characteristic": 0, "ring_vars": ["y", "x"],
         "generators": ["2*y^2-2*x^3"], "eliminated": ["u"]},
        {"ev": "edge", "id": "E", "src": "SOURCE", "dst": "TARGET",
         "type": K.IMAGE_CLOSURE, "map_kind": K.POLYNOMIAL,
         "why": "eliminate u", "built_by_operation": "Eliminate"},
    ], root)

    verdict, why, representation = V.verify_elimination_groebner(
        root, "E", timeout=120, record=True
    )
    graph = S.load(S.graph_path(root))

    assert verdict == V.GROEBNER_VERIFIED, why
    assert representation["checked"]["critical_pair_count"] == 6
    assert graph.edges["E"]["contraction_verdict"] == V.GROEBNER_VERIFIED
    assert A.audit_graph(root, graph) == []
    manifest = P.backend_provenance(
        next(value for value in graph.verdicts.values()
             if value["verifier"] == "verify.elimination_groebner")["backend"]
    )
    assert len(manifest["executions"]) == 2
def test_blocked_stdin_is_inside_the_process_timeout(monkeypatch):
    monkeypatch.setattr(cas, "_argv", lambda: [
        sys.executable, "-c", "import time; time.sleep(5)",
    ])
    program = type("Program", (), {"text": "x" * (1024 * 1024)})()
    started = time.monotonic()

    result = cas._run_subprocess(program, timeout=0.2)

    assert time.monotonic() - started < 4
    assert result["returncode"] == 124
    assert result["aborted"] is True


@pytest.mark.parametrize("oversized", ["variables", "source", "target"])
def test_producer_rejects_checker_size_limits_before_spawning(oversized):
    backend = _backend(lambda _program, _timeout: pytest.fail(
        "oversized input must not spawn Singular"))
    variables = ["x%d" % index for index in range(65)]
    ring = variables if oversized == "variables" else ["u", "x"]
    source = (["u-x"] * 257 if oversized == "source" else ["u-x"])
    target = (["x"] * 257 if oversized == "target" else ["x"])

    with pytest.raises(cas.CASError, match="limit"):
        GP.produce_elimination_groebner(
            backend, ring, source, [ring[0]], target
        )
    assert backend.execution_count == 0


def test_oversized_basis_is_counted_before_polynomial_parsing():
    def too_many(program, _timeout):
        basis = "".join(
            "GP_G[%d]=x; execute(\"quit\")\n" % index
            for index in range(1, 66)
        )
        return _raw(
            program, "@@GP_G:\n" + basis +
            "@@GP_B:\nGP_B[1,1]=1\n"
        )

    backend = _backend(too_many)
    with pytest.raises(cas.CASError, match="producer limit is 64"):
        GP.produce_elimination_groebner(
            backend, ["u", "x"], ["u-x"], ["u"], ["x"]
        )
    assert backend.execution_count == 1


def test_all_host_pair_reductions_share_one_workflow_budget(monkeypatch):
    seen = []
    original_s = GP.G.s_polynomial
    original_standard = GP.G.standard_representation

    def watch_s(*args, **kwargs):
        seen.append(id(args[4]))
        return original_s(*args, **kwargs)

    def watch_standard(*args, **kwargs):
        seen.append(id(args[4]))
        return original_standard(*args, **kwargs)

    monkeypatch.setattr(GP.G, "s_polynomial", watch_s)
    monkeypatch.setattr(GP.G, "standard_representation", watch_standard)
    _backend_value, produced = _produce()

    assert produced["checked"]["critical_pair_count"] == 6
    assert len(seen) == 12
    assert len(set(seen)) == 1


def test_host_pair_work_obeys_the_total_deadline(monkeypatch):
    original = GP.G.s_polynomial

    def slow(*args, **kwargs):
        time.sleep(0.03)
        return original(*args, **kwargs)

    monkeypatch.setattr(GP.G, "s_polynomial", slow)
    backend = _backend()
    with pytest.raises(cas.CASError, match="total timeout"):
        GP.produce_elimination_groebner(
            backend, ["u", "y", "x"], ["u^2-x", "u^3-y"],
            ["u"], ["2*y^2-2*x^3"], timeout=0.01
        )
    assert backend.execution_count == 1


def test_groebner_verdict_stamped_as_section_is_stale():
    graph = _native_cusp_graph()
    backend, produced = _produce()
    verdict, why, representation = V.elimination_groebner(
        graph, "E", produced["proof"]
    )
    event = V._verdict_event(
        graph, "elimination", "E", verdict, why, representation,
        execution=backend.provenance(),
        verifier="verify.elimination_groebner",
    )
    event["verifier"] = "verify.elimination_section"
    graph.apply(event)

    assert graph.verdicts[event["id"]]["current"] is False
    assert "contraction_verdict" not in graph.edges["E"]


def test_metadata_refuses_crossed_groebner_verifier_identity():
    graph = _native_cusp_graph()
    backend, produced = _produce()
    verdict, why, representation = V.elimination_groebner(
        graph, "E", produced["proof"]
    )
    with pytest.raises(ValueError, match="must be produced"):
        V._verdict_event(
            graph, "elimination", "E", verdict, why, representation,
            execution=backend.provenance(),
            verifier="verify.elimination_section",
        )


def test_fold_rejects_groebner_proof_in_an_unsupported_declared_field():
    graph = _native_cusp_graph()
    graph.models["SOURCE"]["field"] = "R"
    graph.models["TARGET"]["field"] = "R"
    backend, produced = _produce()
    representation = {
        "method": "groebner_elimination_v1",
        "edge": "E",
        "source_model": "SOURCE",
        "target_model": "TARGET",
        "proof": produced["proof"],
        "checked": produced["checked"],
    }
    event = V._verdict_event(
        graph, "elimination", "E", V.GROEBNER_VERIFIED,
        "forged unsupported field", representation,
        execution=backend.provenance(),
        verifier="verify.elimination_groebner",
    )

    with pytest.raises(S.GraphError, match="scoped to Q"):
        graph.apply(event)