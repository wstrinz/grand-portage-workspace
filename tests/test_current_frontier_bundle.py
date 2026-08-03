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
        "receipts": 3, "items": 20, "open": 12,
        "resolved": 8, "overlap_resolutions": 2}
    assert items["JC.H3.B0.SOURCE.EXCLUSION"]["receipts"] == [
        "h8-c79", "pin-ablation"]
    assert items["JC.H3.C79.SOURCE.FACE81.PIN_ABLATION"][
        "status"] == "RESOLVED_TO_SCOPED_RESULTS"
    assert "JC.H3.SOURCE.TARGET_PAIR_TO_NORMALIZED_LAURENT_ROOT" in report[
        "open_items"]
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
