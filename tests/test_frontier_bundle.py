import hashlib
import json
from pathlib import Path

import pytest

from grandportage import cli
from grandportage import frontier_bundle as B


def _receipt(observations):
    return {
        "schema": "test-frontier-review/v1",
        "authority": "DERIVED_READ_MODEL_ONLY",
        "graph_effect": "NONE",
        "history": {"input_fingerprint": "sha256:test"},
        "item_observations": observations,
        "open_items": [item["id"] for item in observations
                       if item["state"] == "OPEN"],
    }


def _observation(identifier, state="OPEN", status="OPEN",
                 scope="scope.exact"):
    return {"id": identifier, "scope_id": scope,
            "state": state, "status": status}


def _write_bundle(tmp_path, receipts, resolutions=()):
    bindings = []
    for receipt_id, value in receipts.items():
        path = tmp_path / (receipt_id + ".json")
        path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n",
                        encoding="utf-8")
        digest = hashlib.sha256(
            path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        bindings.append({"id": receipt_id, "path": path.name,
                         "digest_algo": B.DIGEST_ALGO, "sha256": digest})
    manifest = tmp_path / "bundle.json"
    manifest.write_text(json.dumps({
        "schema": B.INPUT_SCHEMA,
        "receipts": bindings,
        "resolutions": list(resolutions),
    }), encoding="utf-8")
    return manifest


def _agree(identifier="A", receipts=("old", "new"),
           scope="scope.exact"):
    return {"id": "resolution.agree", "item_id": identifier,
            "mode": "AGREE_OPEN", "scope_id": scope,
            "receipts": list(receipts), "reason": "exact agreement"}


def _supersede(identifier="A"):
    return {"id": "resolution.supersede", "item_id": identifier,
            "mode": "SUPERSEDE", "scope_id": "scope.exact",
            "prior_receipts": ["old"], "current_receipt": "new",
            "current_status": "RESOLVED", "replacements": ["B"],
            "reason": "new scoped result replaces the artifact request"}


def test_duplicate_open_item_requires_explicit_exact_agreement(tmp_path):
    receipts = {name: _receipt([_observation("A")])
                for name in ("old", "new")}
    manifest = _write_bundle(tmp_path, receipts)

    with pytest.raises(B.FrontierBundleError, match="explicit resolution"):
        B.build_path(manifest)

    report = B.build_path(_write_bundle(
        tmp_path, receipts, [_agree()]))
    assert report["open_items"] == ["A"]
    assert report["items"][0]["receipts"] == ["new", "old"]


def test_agreement_refuses_scope_or_status_conflicts(tmp_path):
    receipts = {
        "old": _receipt([_observation("A")]),
        "new": _receipt([_observation("A", scope="scope.other")]),
    }
    with pytest.raises(B.FrontierBundleError, match="incompatible exact scopes"):
        B.build_path(_write_bundle(tmp_path, receipts, [_agree()]))

    receipts["new"] = _receipt([_observation("A", status="OPEN_OTHER")])
    with pytest.raises(B.FrontierBundleError, match="statuses conflict"):
        B.build_path(_write_bundle(tmp_path, receipts, [_agree()]))


def test_supersession_replaces_open_task_with_bounded_results(tmp_path):
    receipts = {
        "old": _receipt([_observation("A")]),
        "new": _receipt([
            _observation("A", state="CLOSED", status="RESOLVED"),
            _observation("B", status="OPEN_FINITE_REMAINDER"),
        ]),
    }
    report = B.build_path(_write_bundle(
        tmp_path, receipts, [_supersede()]))
    items = {item["id"]: item for item in report["items"]}

    assert report["open_items"] == ["B"]
    assert items["A"]["status"] == "RESOLVED"
    assert items["A"]["supersedes_receipts"] == ["old"]
    assert items["A"]["replacements"] == ["B"]


def test_supersession_refuses_unproved_status_or_missing_replacement(tmp_path):
    receipts = {
        "old": _receipt([_observation("A")]),
        "new": _receipt([_observation(
            "A", state="CLOSED", status="SOMETHING_ELSE")]),
    }
    with pytest.raises(B.FrontierBundleError, match="status disagrees"):
        B.build_path(_write_bundle(tmp_path, receipts, [_supersede()]))

    receipts["new"] = _receipt([
        _observation("A", state="CLOSED", status="RESOLVED")])
    with pytest.raises(B.FrontierBundleError, match="replacement is absent"):
        B.build_path(_write_bundle(tmp_path, receipts, [_supersede()]))


def test_supersession_refuses_current_as_prior_or_self_replacement(tmp_path):
    receipts = {
        "old": _receipt([_observation("A")]),
        "new": _receipt([
            _observation("A", state="CLOSED", status="RESOLVED"),
            _observation("B"),
        ]),
    }
    resolution = _supersede()
    resolution["prior_receipts"].append("new")
    with pytest.raises(B.FrontierBundleError, match="current receipt as prior"):
        B.build_path(_write_bundle(tmp_path, receipts, [resolution]))

    resolution = _supersede()
    resolution["replacements"] = ["A"]
    with pytest.raises(B.FrontierBundleError, match="distinct replacement"):
        B.build_path(_write_bundle(tmp_path, receipts, [resolution]))


def test_receipt_digest_mutation_refuses(tmp_path):
    manifest = _write_bundle(
        tmp_path, {"only": _receipt([_observation("A")])})
    (tmp_path / "only.json").write_text("{}", encoding="utf-8")

    with pytest.raises(B.FrontierBundleError, match="digest changed"):
        B.build_path(manifest)


def test_lf_normalized_digest_survives_crlf_checkout(tmp_path):
    manifest = _write_bundle(
        tmp_path, {"only": _receipt([_observation("A")])})
    path = tmp_path / "only.json"
    lf = path.read_bytes().replace(b"\r\n", b"\n")
    path.write_bytes(lf.replace(b"\n", b"\r\n"))

    assert B.build_path(manifest)["open_items"] == ["A"]


def test_bundle_is_deterministic_and_cli_exposes_same_surface(tmp_path, capsys):
    receipts = {
        "z": _receipt([_observation("Z")]),
        "a": _receipt([_observation("A")]),
    }
    manifest = _write_bundle(tmp_path, receipts)
    first = B.build_path(manifest)
    second = B.build_path(manifest)

    assert B.canonical_json(first) == B.canonical_json(second)
    assert first["open_items"] == ["A", "Z"]
    assert cli.main(["frontier-bundle", str(manifest), "--compact"]) == 0
    assert json.loads(capsys.readouterr().out) == first
