"""Pinned historical recurrence and finite-quotient residual controls."""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "oracle/history/checkout"
PIN = "7991c9052f13e8dcaa78b5eae36f31663e080c1e"
MODULE_PATHS = {
    "zero_endpoint": "jc_h3_adjoint_recurrence/adapter.py",
    "finite_unit": "jc_h3_b0_free_plane/depth8_residual_adapter.py",
    "false_gcd_claim": "jc_h3_b0_free_plane/depth8_residual_adapter.py",
}


def _load(control):
    path = HISTORY / "experiments" / MODULE_PATHS[control]
    spec = importlib.util.spec_from_file_location(
        "historical_residual_" + control, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _fixture(module, digest):
    raw = module.DEFAULT_FIXTURE.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != digest or actual != module.EXPECTED_FIXTURE_SHA256:
        raise ValueError("Historical fixture SHA-256 mismatch")
    return json.loads(raw.decode("utf-8"))


def _zero_endpoint(case, module, fixture):
    d = case["inputs"]
    _, baseline = module.validate_fixture_value(copy.deepcopy(fixture))
    if (baseline["domain_start"] != d["domain_start"]
            or baseline["endpoint_depth"] != d["endpoint_depth"]
            or baseline["zero_from"] != d["zero_from"]
            or baseline["cutoff_gap"] != d["claimed_minimal_shift"]):
        raise ValueError("Recurrence case differs from pinned baseline")
    zero = next(entry["value"] for regime in fixture["native_certificate"]["regimes"]
                for entry in regime["matrix"] if entry["value"]["terms"] == 0)
    if zero["sparse"]["terms"]:
        raise ValueError("Zero template is not zero")
    endpoint = [regime for regime in fixture["native_certificate"]["regimes"]
                if d["endpoint_depth"] in regime["depths"]]
    if len(endpoint) != 1:
        raise ValueError("Endpoint regime is ambiguous")
    for entry in endpoint[0]["matrix"]:
        entry["value"] = copy.deepcopy(zero)
    regimes = module._decode_regimes(fixture["native_certificate"])
    endpoint_nonzero = any(module._padded_at(d["endpoint_depth"], regimes).values())
    tail_zero = all(not any(module._padded_at(depth, regimes).values())
                    for depth in range(d["zero_from"], d["zero_from"] + 12))
    prior_shift_annihilates = all(
        not any(module._padded_at(depth + d["claimed_minimal_shift"] - 1,
                                  regimes).values())
        for depth in range(d["domain_start"], d["zero_from"] + 4))
    if endpoint_nonzero or not tail_zero or not prior_shift_annihilates:
        raise ValueError("Endpoint mutation did not produce the intended arithmetic")
    try:
        module.validate_fixture_value(fixture)
    except module.RecurrenceEvidenceError as exc:
        failure = str(exc)
        if not failure.startswith(("J4:", "A2:")):
            raise
        return {
            "observed_verdict": "REFUSE", "reason": failure,
            "baseline_minimal_eighth_shift_checked": True,
            "mutated_endpoint_nonzero": endpoint_nonzero,
            "mutated_tail_zero": tail_zero,
            "mutated_seventh_shift_annihilates": prior_shift_annihilates,
            "graph_effect": "NONE", "external_execution": False,
        }
    raise ValueError("Zeroed endpoint unexpectedly validated")


def _finite_unit(case, module, fixture):
    d = case["inputs"]
    if (d["quotient"] != "K[Z]/(r_final)"
            or d["base_field"] != "Q[t]/(15*t^3+1)"
            or d["unit_element"] != "Omega8"):
        raise ValueError("Unknown finite quotient interpretation")
    witness = fixture["pullback_certificate"]["witness"]
    if witness["gcd_with_r_final_degree"] != 0:
        raise ValueError("Pinned witness does not report coprimality")
    if d["control"] == "finite_unit":
        if d["claimed_gcd_degree"] != 0:
            raise ValueError("Positive case changes the gcd claim")
        checked = module.validate_fixture_value(fixture)
        found = checked["witness"]
        if not found["omega_unit"] or found["gcd_degree"] != 0:
            raise ValueError("Historical finite unit replay did not verify")
        return {
            "observed_verdict": "ACCEPT",
            "reason": "Historical exact quotient replay verifies gcd degree zero.",
            "checked_witness": found,
            "graph_effect": "NONE", "parent_exclusion": False,
            "external_execution": False,
        }
    if d["control"] != "false_gcd_claim" or d["claimed_gcd_degree"] != 1:
        raise ValueError("Unknown finite quotient mutation")
    baseline = module.validate_fixture_value(copy.deepcopy(fixture))
    actual_gcd_degree = baseline["witness"]["gcd_degree"]
    if actual_gcd_degree != 0:
        raise ValueError("Pinned exact quotient replay differs from the control")
    witness["gcd_with_r_final_degree"] = d["claimed_gcd_degree"]
    try:
        module.validate_fixture_value(fixture)
    except module.Depth8ResidualEvidenceError as exc:
        failure = str(exc)
        if not failure.startswith("W5:"):
            raise
        return {
            "observed_verdict": "REFUSE", "reason": failure,
            "claimed_gcd_degree": d["claimed_gcd_degree"],
            "actual_gcd_degree": actual_gcd_degree,
            "arithmetic_replay_reached": True,
            "outer_fixture_digest_rejection": False,
            "graph_effect": "NONE", "parent_exclusion": False,
            "external_execution": False,
        }
    raise ValueError("False finite gcd claim unexpectedly validated")


def probe(case, route):
    if route["historical_commit"] != PIN:
        raise ValueError("Wrong historical revision")
    d = case["inputs"]
    control = d["control"]
    if control not in MODULE_PATHS:
        raise ValueError("Unknown historical residual control")
    module = _load(control)
    fixture = _fixture(module, d["fixture_sha256"])
    if control == "zero_endpoint":
        return _zero_endpoint(case, module, fixture)
    return _finite_unit(case, module, fixture)
