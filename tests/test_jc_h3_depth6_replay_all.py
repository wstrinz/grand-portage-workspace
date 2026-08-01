import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "jc_h3_source_depth6" / "replay_all.py"


def _load():
    spec = importlib.util.spec_from_file_location("jc_h3_replay_all_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _envelope(license_name="checked"):
    return {
        "licenses": [license_name],
        "outstanding_premises": ["scope remains bounded"],
    }


def test_fast_gate_replays_welds_and_names_terminal_open_authority():
    module = _load()
    report = module.run_gate(
        full=False, check_native_bindings=True, native_replay=False)

    assert report["overall_verdict"] == (
        "VERIFIED_TO_EXPLICIT_OPEN_OBLIGATION")
    assert report["coverage"] == "WELDS_ONLY_GRAPH_AUTHORITIES_DEFERRED"
    assert [stage["id"] for stage in report["stages"]] == [
        "conditional_source_seam",
        "graded_face_extraction",
        "complete_finite_template",
        "ordered_depth6_chain",
        "boundary_projection_and_strata",
    ]
    assert report["stages"][2]["status"] == "DEFERRED_OPTIONAL"
    assert report["stages"][4]["graph_effect"] == "NONE"
    assert report["first_missing_authority"]["id"] == (
        "target_pair_to_normalized_laurent_root")
    assert "H3 promotion" in report["first_missing_authority"]["blocks"]
    assert report["aggregate_graph_effect"] == "NONE"


def test_gate_refuses_silent_original_source_promotion(monkeypatch):
    module = _load()
    monkeypatch.setattr(module.ORIGINAL, "verify_fixture", lambda **_kwargs: {
        "verdict": "VERIFIED_CONDITIONAL_ESYSTEM_SEAM",
        "strict_original_source_supported": True,
        "missing_stage": module.FIRST_MISSING,
        "evidence_envelope": _envelope(),
    })

    with pytest.raises(module.MilestoneReplayError,
                       match="strict original-source support"):
        module.run_gate()


def test_full_gate_checks_graph_authorities_in_semantic_order(
        monkeypatch, tmp_path):
    module = _load()
    calls = []
    monkeypatch.setattr(module.ORIGINAL, "verify_fixture", lambda **_kwargs: {
        "verdict": "VERIFIED_CONDITIONAL_ESYSTEM_SEAM",
        "strict_original_source_supported": False,
        "missing_stage": module.FIRST_MISSING,
        "evidence_envelope": _envelope("conditional"),
    })
    monkeypatch.setattr(module.FACE, "verify_fixture", lambda **_kwargs: {
        "verdict": "VERIFIED_GRADED_FACE_EXTRACTION_WITH_SOURCE_REPLAY",
        "source_rows": 5,
        "faces": 25,
        "evidence_envelope": _envelope("faces"),
    })
    campaign = {
        "source_generators": 147,
        "selected_generators": 25,
        "ring_variables": 78,
        "authority": {"licenses": ["point inclusion"],
                      "refuses": ["reverse inclusion"]},
    }
    monkeypatch.setattr(
        module.FULL_TEMPLATE, "compile_campaign",
        lambda **_kwargs: calls.append("template") or campaign)
    monkeypatch.setattr(
        module.FULL_TEMPLATE, "graph_from_campaign", lambda _value: "graph")
    monkeypatch.setattr(
        module.V, "containment",
        lambda _graph, _edge: calls.append("containment") or
        (module.V.VERIFIED, "exact subset"))
    monkeypatch.setattr(module.CHAIN, "verify_chain", lambda **_kwargs: {
        "verdict": "VERIFIED_DEPTH6_CHAIN_FULL_REPLAY",
        "solved_steps": 23,
        "residuals_welded": 2,
        "evidence_envelope": _envelope("chain"),
    })
    frozen = tmp_path / "boundary.json"
    frozen.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(module.BOUNDARY, "DEFAULT_FROZEN", frozen)
    monkeypatch.setattr(module.BOUNDARY, "verify_frozen", lambda _value: {
        "verdict": "VERIFIED_FROZEN_DEPTH6_BOUNDARY",
        "evidence_envelope": _envelope("boundary"),
    })
    monkeypatch.setattr(
        module.BOUNDARY, "graph_from_frozen", lambda _value: "boundary graph")
    monkeypatch.setattr(
        module.V, "ring_iso",
        lambda _graph, edge: calls.append(edge) or
        (module.V.ISO_VERIFIED, "exact equivalence"))

    report = module.run_gate(full=True)

    assert calls == [
        "template", "containment", module.BOUNDARY.GENERIC_EDGE,
        module.BOUNDARY.DISCRIMINANT_EDGE,
    ]
    assert report["coverage"] == "ALL_FROZEN_STAGES_AND_COMPLETE_TEMPLATE"
    assert report["stages"][2]["graph_effect"] == "POINT_INCLUSION"
    assert report["stages"][4]["graph_effect"] == "IDENTITY_TRANSPORT"


def test_report_write_is_atomic_and_refuses_unrequested_overwrite(tmp_path):
    module = _load()
    path = tmp_path / "ledger.json"
    report = {"schema": module.SCHEMA, "overall_verdict": "TEST"}

    module._write_report(path, report)
    assert json.loads(path.read_text(encoding="utf-8")) == report
    assert not list(tmp_path.glob("*.tmp"))
    with pytest.raises(module.MilestoneReplayError, match="output exists"):
        module._write_report(path, report)
    replacement = dict(report, overall_verdict="REPLACED")
    module._write_report(path, replacement, force=True)
    assert json.loads(path.read_text(encoding="utf-8")) == replacement


def test_native_replay_preserves_the_open_seam(monkeypatch, tmp_path):
    module = _load()
    verifier = tmp_path / "native.py"
    verifier.write_text("# bound in test\n", encoding="utf-8")
    monkeypatch.setattr(module, "NATIVE_VERIFIER", verifier)
    monkeypatch.setattr(module.subprocess, "run", lambda *_args, **_kwargs:
                        SimpleNamespace(
                            returncode=0, stderr="", stdout=json.dumps({
                                "status": "CONDITIONAL_EXACT_WITH_OPEN_UPSTREAM",
                                "strict_original_source_supported": False,
                                "original_pair_to_normalized_root":
                                    "UNMATERIALIZED_OPEN",
                                "mutation_refusals": 9,
                            })))

    stage = module._run_native_replay()

    assert stage["status"] == "VERIFIED"
    assert stage["graph_effect"] == "NONE"
    assert stage["outstanding_premises"] == [module.FIRST_MISSING]

def test_checked_in_review_ledgers_preserve_mode_and_authority_boundary():
    module = _load()
    review = ROOT / "review"
    full = json.loads((review / "jc-h3-depth6-full-replay-v1.json").read_text(
        encoding="utf-8"))
    native = json.loads((
        review / "jc-h3-depth6-native-replay-v1.json").read_text(
            encoding="utf-8"))

    assert full["schema"] == native["schema"] == module.SCHEMA
    assert full["mode"] == "full"
    assert full["stages"][2]["graph_effect"] == "POINT_INCLUSION"
    assert full["stages"][4]["graph_effect"] == "IDENTITY_TRANSPORT"
    assert native["native_replay_executed"] is True
    assert native["stages"][-1]["licenses"][-1] == (
        "nine_native_mutations_refused")
    assert full["bindings"] == native["bindings"]
    assert full["first_missing_authority"] == native["first_missing_authority"]
    assert full["aggregate_graph_effect"] == native["aggregate_graph_effect"] == (
        "NONE")
