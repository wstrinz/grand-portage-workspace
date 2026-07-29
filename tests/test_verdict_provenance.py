"""Epoch-1 verifier answers are evidence only while their provenance matches."""

import pytest

from grandportage import format as F
from grandportage import kernel as K
from grandportage import provenance as P
from grandportage import store as S
from grandportage import verify as V


def _identity_graph(generator="x"):
    graph = S.Graph()
    graph.apply(F.meta_event())
    graph.apply({
        "ev": "model", "id": "M", "what": "a line",
        "characteristic": 0, "ring_vars": ["x"],
        "generators": [generator],
    })
    graph.apply({
        "ev": "claim", "id": "C", "model": "M", "kind": K.IDENTITY,
        "statement": "x vanishes", "lhs": "x", "rhs": "0",
        "ring_vars": ["x"], "identity_origin": K.DERIVED,
        "established_by": "RAN", "ladder": "exact-checked",
    })
    return graph


def _verdict(graph, verdict="VERIFIED_DERIVED"):
    return V._verdict_event(
        graph, "claim", "C", verdict, "x reduces to zero modulo (x)")


def test_fresh_epoch1_verdict_is_active():
    graph = _identity_graph()
    event = _verdict(graph)

    graph.apply(event)

    assert graph.claims["C"]["identity_verdict"] == "VERIFIED_DERIVED"
    assert graph.verdicts[event["id"]]["current"] is True


def test_legacy_verified_remains_readable_but_inactive():
    graph = S.Graph()
    graph.apply({
        "ev": "model", "id": "M", "what": "a line",
        "characteristic": 0, "ring_vars": ["x"], "generators": ["x"],
    })
    graph.apply({
        "ev": "claim", "id": "C", "model": "M", "kind": K.IDENTITY,
        "statement": "x vanishes", "lhs": "x", "rhs": "0",
        "ring_vars": ["x"], "identity_origin": K.DERIVED,
        "established_by": "RAN", "ladder": "exact-checked",
    })
    event = {
        "ev": "verdict", "id": "v.C.legacy", "subject": "claim",
        "of": "C", "verdict": "VERIFIED_DERIVED",
        "why": "an epoch-0 verifier said so",
    }

    graph.apply(event)

    assert "identity_verdict" not in graph.claims["C"]
    assert graph.verdicts[event["id"]]["current"] is False
    assert "epoch-0" in graph.verdicts[event["id"]]["stale_reason"]


def test_verdict_for_different_semantic_input_is_stale():
    original = _identity_graph("x")
    event = _verdict(original)
    changed = _identity_graph("x^2")

    changed.apply(event)

    assert "identity_verdict" not in changed.claims["C"]
    assert "fingerprint" in changed.verdicts[event["id"]]["stale_reason"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("verifier", "verify.some_old_identity"),
        ("verifier_version", 2),
        ("kernel_epoch", F.KERNEL_EPOCH + 1),
        ("backend", "not-singular"),
    ],
)
def test_mismatched_verifier_kernel_or_backend_is_stale(field, value):
    graph = _identity_graph()
    event = _verdict(graph)
    event[field] = value
    event["id"] = "v.C.mismatch.%s" % field

    graph.apply(event)

    assert "identity_verdict" not in graph.claims["C"]
    assert graph.verdicts[event["id"]]["current"] is False


def _never(*_args, **_kwargs):
    raise AssertionError("a verifier with unknown characteristic ran the CAS")


def _missing_characteristic_graph():
    graph = S.Graph()
    graph.models.update({
        "A": {"id": "A", "ring_vars": ["x"], "generators": ["x"]},
        "B": {"id": "B", "ring_vars": ["x"], "generators": ["x^2"]},
    })
    return graph


def test_identity_declines_unknown_characteristic_before_cas():
    graph = _missing_characteristic_graph()
    graph.claims["C"] = {
        "id": "C", "model": "A", "kind": K.IDENTITY,
        "lhs": "x", "rhs": "0", "ring_vars": ["x"],
    }
    verdict, why = V.identity(graph, "C", _runner=_never)
    assert verdict == V.UNVERIFIED
    assert "no characteristic" in why


@pytest.mark.parametrize("checker", ["containment", "ring_iso", "operation"])
def test_edge_verifiers_decline_unknown_characteristic_before_cas(checker):
    graph = _missing_characteristic_graph()
    if checker == "containment":
        graph.edges["E"] = {
            "id": "E", "src": "A", "dst": "B",
            "type": K.NECESSARY_CONDITION, "map_kind": K.IDENTITY_MAP,
        }
        out = V.containment(graph, "E", _runner=_never)
    elif checker == "ring_iso":
        graph.edges["E"] = {
            "id": "E", "src": "A", "dst": "B", "type": K.EQUIVALENCE,
            "map_kind": K.IDENTITY_MAP,
            "forward": {"x": "x"}, "inverse": {"x": "x"},
        }
        out = V.ring_iso(graph, "E", _runner=_never)
    else:
        graph.edges["E"] = {
            "id": "E", "src": "B", "dst": "A",
            "built_by_operation": "SaturateClosure",
        }
        graph.models["B"]["saturated_at"] = "x"
        out = V.operation_output(graph, "E", _runner=_never)
    assert out[0] == V.UNVERIFIED
    assert "no characteristic" in out[1]


def test_partition_witness_and_certificate_decline_unknown_characteristic():
    graph = _missing_characteristic_graph()
    graph.models["C"] = {
        "id": "C", "ring_vars": ["x"], "generators": ["x-1"],
    }
    graph.partitions["P"] = {
        "id": "P", "parent": "A", "branches": ["B", "C"],
    }
    graph.claims["W"] = {
        "id": "W", "model": "A", "kind": K.NONEMPTY,
        "witness_point": {"x": 0},
    }
    graph.claims["U"] = {
        "id": "U", "model": "A", "kind": K.EMPTY,
        "certificate": "UNIT_IDEAL_CERT",
    }

    results = [
        V.partition_exhaustiveness(graph, "P", _runner=_never),
        V.point_witness(graph, "W", _runner=_never),
        V.unit_ideal(graph, "U", _runner=_never),
    ]
    for verdict, why, *_rest in results:
        assert verdict == V.UNVERIFIED
        assert "no characteristic" in why
