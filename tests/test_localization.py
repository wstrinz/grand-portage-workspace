"""Principal-open localization certificates and adversarial controls."""

import copy
import json

import pytest

from grandportage import cli
from grandportage import groebner as G
from grandportage import localization as L


def _spec():
    return {
        "schema": L.SCHEMA,
        "characteristic": 0,
        "ring_vars": ["q", "t", "y"],
        "generators": ["q*t*y"],
        "guards": ["q", "t"],
        "expression": {
            "numerator": "y",
            "denominator_powers": [2, 1],
        },
        "certificate": {
            "localization_powers": [1, 1],
            "membership_target": "q*t*y",
            "cofactors": ["1"],
        },
    }


def test_exact_guard_monomial_certifies_localized_membership_only():
    report = L.verify(_spec())

    assert report["verdict"] == L.VERIFIED
    assert report["licenses"] == [
        "identity_in_declared_localization_only"
    ]
    assert report["normalized"]["expression"] == {
        "numerator": "y",
        "denominator_powers": [2, 1],
    }
    assert report["normalized"]["certificate"]["membership_target"] == (
        "q*t*y"
    )
    assert report["checked"]["generator_count"] == 1


def test_same_identity_without_the_needed_guard_power_is_rejected():
    spec = _spec()
    spec["certificate"]["localization_powers"] = [0, 1]

    with pytest.raises(L.LocalizationError, match="expected t\\*y"):
        L.verify(spec)


def test_wrong_cofactor_is_rejected_by_exact_expansion():
    spec = _spec()
    spec["certificate"]["cofactors"] = ["2"]

    with pytest.raises(L.LocalizationError, match="wrong polynomial"):
        L.verify(spec)


@pytest.mark.parametrize("mutate, message", [
    (lambda spec: spec.update({"guards": ["q", "q+0"]}),
     "remain distinct"),
    (lambda spec: spec.update({"guards": ["0"]}),
     "zero polynomial cannot be inverted"),
    (lambda spec: spec["expression"].update({"denominator_powers": [1]}),
     "one power per guard"),
    (lambda spec: spec["certificate"].update({
        "localization_powers": [65, 0]}),
     "0 through 64"),
    (lambda spec: spec.update({"surprise": True}),
     "unknown field"),
])
def test_certificate_surface_is_closed_and_bounded(mutate, message):
    spec = _spec()
    mutate(spec)
    with pytest.raises(L.LocalizationError, match=message):
        L.verify(spec)


def test_denominator_scope_is_bound_into_the_report_fingerprint():
    first = L.verify(_spec())
    changed = _spec()
    changed["expression"]["denominator_powers"] = [3, 1]
    second = L.verify(changed)

    assert first["spec_fingerprint"] != second["spec_fingerprint"]


def test_cli_prints_narrow_authority_and_can_emit_json(tmp_path, capsys):
    path = tmp_path / "localization.json"
    path.write_text(json.dumps(_spec()), encoding="utf-8")

    assert cli.main([
        "verify-localization-membership", "--spec", str(path),
    ]) == 0
    text = capsys.readouterr().out
    assert L.VERIFIED in text
    assert "no ambient identity or point transport" in text

    assert cli.main([
        "verify-localization-membership", "--spec", str(path), "--json",
    ]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["licenses"] == [
        "identity_in_declared_localization_only"
    ]


def test_mutating_the_recorded_target_does_not_survive():
    spec = copy.deepcopy(_spec())
    spec["certificate"]["membership_target"] = "q*y"

    with pytest.raises(L.LocalizationError, match="expected q\\*t\\*y"):
        L.verify(spec)


def test_sparse_generator_and_target_verify_without_infix_reparsing():
    spec = _spec()
    sparse = G.encode_sparse_polynomial(G.parse_polynomial(
        "q*t*y", spec["ring_vars"]
    ))
    spec["generators"] = [sparse]
    spec["certificate"]["membership_target"] = sparse

    report = L.verify(spec)

    assert report["verdict"] == L.VERIFIED
    assert report["normalized"]["generators"] == [sparse]


def test_sparse_zero_guard_is_still_refused():
    spec = _spec()
    spec["guards"] = [{
        "schema": G.SPARSE_POLYNOMIAL_SCHEMA, "terms": [],
    }]
    with pytest.raises(L.LocalizationError, match="zero polynomial"):
        L.verify(spec)
