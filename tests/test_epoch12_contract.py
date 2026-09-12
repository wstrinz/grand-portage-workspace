"""Executable answer keys frozen before epoch-12 graph integration."""

from copy import deepcopy

import pytest

from grandportage import field as E
from grandportage import ordered_sos as SOS


def test_concrete_extension_is_not_universal_instantiation():
    assert E.concrete_extension("Q", "R").allowed
    assert E.concrete_extension("R", "C").allowed
    assert not E.concrete_extension("R", "Q").allowed
    assert not E.concrete_extension("R", "ANY_ORDERED").allowed
    assert not E.concrete_extension("ANY_ORDERED", "R").allowed


def test_ordered_and_characteristic_zero_reach_have_distinct_targets():
    ordered = {"kind": "ORDERED"}
    assert E.instantiate(ordered, "Q").allowed
    assert E.instantiate(ordered, "R").allowed
    assert not E.instantiate(ordered, "C").allowed
    assert not E.instantiate(ordered, "F_2").allowed

    char_zero = {"kind": "CHAR_0"}
    assert E.instantiate(char_zero, "Q").allowed
    assert E.instantiate(char_zero, "R").allowed
    assert E.instantiate(char_zero, "C").allowed
    assert not E.instantiate(char_zero, "F_2").allowed


def test_field_specific_and_none_never_generalize():
    finite = {"kind": "FIELD_SPECIFIC", "field": "F_2"}
    assert E.instantiate(finite, "F_2").allowed
    assert not E.instantiate(finite, "Q").allowed
    assert not E.instantiate({"kind": "NONE"}, "Q").allowed
    with pytest.raises(E.FieldError, match="concrete field"):
        E.validate_reach({"kind": "FIELD_SPECIFIC", "field": "ANY_CHAR_0"})


def test_exact_identity_reach_is_model_bound_not_a_global_boolean():
    assert E.reach_for_exact_identity("Q") == {"kind": "CHAR_0"}
    assert E.reach_for_exact_identity("F_2") == {
        "kind": "FIELD_SPECIFIC", "field": "F_2"}


def test_compute_alias_agrees_or_refuses():
    assert E.model_compute_in({"compute_in": "Q"}) == "Q"
    assert E.model_compute_in({"coefficient_domain": "F_3"}) == "F_3"
    assert E.model_compute_in({"compute_in": "Q",
                               "coefficient_domain": "Q"}) == "Q"
    with pytest.raises(E.FieldError, match="identical"):
        E.model_compute_in({"compute_in": "Q",
                            "coefficient_domain": "F_3"})


def test_point_context_retains_universe_and_selected_embedding():
    q = {"about": "Q", "point_universe": "BASE"}
    r = {"about": "R", "point_universe": "BASE"}
    assert E.compatible_point_context(q, r).allowed

    closure = {"about": "Q", "point_universe": "ALGEBRAIC_CLOSURE"}
    assert not E.compatible_point_context(closure, r).allowed

    selected = {"about": "Q", "point_universe": "BASE",
                "embedding": {"kind": "REAL", "root": "+"}}
    swapped = deepcopy(selected)
    swapped["embedding"]["root"] = "-"
    assert not E.compatible_point_context(selected, swapped).allowed


def _model(generator="x^2+1"):
    return {
        "id": "M", "about": "ANY_ORDERED", "compute_in": "Q",
        "coefficient_domain": "Q", "characteristic": 0,
        "point_universe": "BASE", "ring_vars": ["x"],
        "generators": [generator],
    }


def _certificate():
    return {
        "method": SOS.METHOD,
        "ring_vars": ["x"],
        "generators": ["x^2+1"],
        "squares": ["x"],
        "cofactors": ["-1"],
    }


def test_rational_sos_replays_without_search_and_earns_ordered_answer_key():
    receipt = SOS.verify(_model(), _certificate())
    assert receipt["method"] == SOS.METHOD
    assert receipt["squares"] == ["x"]
    assert E.instantiate({"kind": "ORDERED"}, "Q").allowed
    assert E.instantiate({"kind": "ORDERED"}, "R").allowed
    assert not E.instantiate({"kind": "ORDERED"}, "C").allowed


def test_false_or_detached_ordered_certificates_refuse():
    false = _certificate()
    false["cofactors"] = ["1"]
    with pytest.raises(SOS.OrderedSOSError, match="invalid"):
        SOS.verify(_model(), false)

    detached = _certificate()
    detached["generators"] = ["x^2+2"]
    with pytest.raises(SOS.OrderedSOSError, match="do not match"):
        SOS.verify(_model(), detached)


def test_ordered_replay_refuses_positive_characteristic_and_bad_shape():
    finite = _model()
    finite.update({"compute_in": "F_2", "coefficient_domain": "F_2",
                   "characteristic": 2})
    with pytest.raises(SOS.OrderedSOSError, match="over Q"):
        SOS.verify(finite, _certificate())

    extra = _certificate()
    extra["search_budget"] = 10
    with pytest.raises(SOS.OrderedSOSError, match="closed"):
        SOS.verify(_model(), extra)
