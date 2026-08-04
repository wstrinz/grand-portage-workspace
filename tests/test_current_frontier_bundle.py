import json
import os
from pathlib import Path

import pytest

from grandportage import frontier_bundle as B


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "fixtures" / "frontier" / "current_v1.json"


def _items(report):
    return {item["id"]: item for item in report["items"]}


def test_current_bundle_has_one_explicit_research_boundary():
    report = B.build_path(MANIFEST)
    items = _items(report)

    assert report["counts"] == {
        "receipts": 4, "items": 23, "open": 11,
        "resolved": 12, "overlap_resolutions": 6}
    assert items["JC.H3.B0.SOURCE.EXCLUSION"]["receipts"] == [
        "h8-c79", "pin-ablation"]
    assert items["JC.H3.C79.SOURCE.FACE81.PIN_ABLATION"][
        "status"] == "RESOLVED_TO_SCOPED_RESULTS"
    assert "JC.H3.SOURCE.TARGET_PAIR_TO_NORMALIZED_LAURENT_ROOT" in report[
        "open_items"]
    assert items["JC.H3.D6.R6.NONMONOMIAL_FRAME"]["status"] == (
        "DISCHARGED_PREMISE_FREE_AS_CONSUMED")
    assert items["JC.H3.D6.R7_PRIME.SIGMA_BUDGET"]["status"] == (
        "PROVED_NATIVE_UNCONDITIONAL")
    assert items["JC.H3.C22_C710.NONNORMALIZED_TRANSPORT"]["status"] == (
        "RESOLVED_TO_GENERIC_AND_FINITE_REMAINDER")
    assert "JC.H3.C22_C710.EXCEPTIONAL_J_FIBERS" in report["open_items"]
    assert "JC.H3.D6.R7.75_125_IDENTIFICATION" in report["open_items"]
    assert report["graph_effect"] == "NONE"


def test_current_bundle_refuses_implicit_last_writer_wins(tmp_path):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["root"] = os.path.relpath(ROOT, tmp_path)
    manifest["resolutions"] = []
    path = tmp_path / "current.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(B.FrontierBundleError, match="explicit resolution"):
        B.build_path(path)


def test_current_bundle_refuses_false_scope_agreement(tmp_path):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["root"] = os.path.relpath(ROOT, tmp_path)
    manifest["resolutions"][0]["scope_id"] = "JC.H3.B0.NOT_THE_SCOPE"
    path = tmp_path / "current.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(B.FrontierBundleError, match="incompatible exact scopes"):
        B.build_path(path)


def test_current_checked_review_receipt_regenerates_exactly():
    expected = json.loads((ROOT / "review" /
                           "frontier-current-v1.json").read_text(
                               encoding="utf-8"))

    assert expected == B.review_receipt(B.build_path(MANIFEST))


def test_support_seam_supersessions_preserve_the_named_remainders():
    items = _items(B.build_path(MANIFEST))

    r6 = items["JC.H3.D6.R6.NONMONOMIAL_FRAME"]
    assert r6["replacements"] == ["JC.H3.D6.R7_PRIME.SIGMA_BUDGET"]
    transport = items["JC.H3.C22_C710.NONNORMALIZED_TRANSPORT"]
    assert transport["replacements"] == [
        "JC.H3.C22_C710.EXCEPTIONAL_J_FIBERS",
        "JC.H3.C22_C710.NONNORMALIZED_TRANSPORT.GENERIC_J",
    ]
