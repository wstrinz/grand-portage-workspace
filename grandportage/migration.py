"""Explicit, non-destructive graph-format migration."""

import hashlib
import json
import os

from . import format as F
from . import store as S


def _destination(source):
    stem, ext = os.path.splitext(source)
    return stem + ".epoch1" + (ext or ".jsonl")


def _native_record(raw, source_fingerprint):
    """Return (closed epoch-1 record, audit actions) for one legacy record."""
    if not isinstance(raw, dict):
        raise S.GraphError("epoch-0 event is not an object")
    kind = raw.get("ev")
    if kind == F.META_EVENT:
        raise S.GraphError(
            "epoch-0 source contains a misplaced `meta`; refusing to infer "
            "where its format changes")
    if kind not in F.EVENT_FIELDS:
        raise S.GraphError("cannot migrate unknown event kind %r" % kind)

    source = dict(raw)
    actions = []
    if "ring_isomorphism" in source:
        source.pop("ring_isomorphism")
        if kind == "edge":
            source["ring_iso"] = False
        actions.append({
            "field": "ring_isomorphism",
            "action": "removed; epoch 1 never promotes the legacy alias",
        })

    out = F.import_epoch0_event(source)
    if "witness" in source:
        actions.append({
            "field": "witness",
            "action": ("renamed to strictness_witness"
                       if "strictness_witness" not in source
                       else "dropped; explicit strictness_witness retained"),
        })
    if "zariski_dense" in source:
        actions.append({
            "field": "zariski_dense",
            "action": "dropped; retracted and non-licensing in epoch 1",
        })

    for field in sorted(F.LICENSING_BOOLEANS.get(kind, set())):
        if field in source and not isinstance(source[field], bool):
            actions.append({
                "field": field,
                "action": "malformed legacy truthy value normalized to false",
            })

    unknown = sorted(set(out) - F.EVENT_FIELDS[kind])
    for field in unknown:
        out.pop(field)
        actions.append({
            "field": field,
            "action": "dropped; not in the closed epoch-1 schema",
        })

    if kind == "verdict":
        defaults = {
            "verifier": "legacy.import",
            "verifier_version": 1,
            "kernel_epoch": 0,
            "backend": "legacy",
            "input_fingerprint": source_fingerprint,
        }
        for field, value in defaults.items():
            if field not in out:
                out[field] = value
                actions.append({
                    "field": field,
                    "action": "added legacy provenance; verdict remains inactive",
                })

    return out, actions


def migrate_epoch1(paths, dry_run=False, output=None):
    """Write epoch-1 graphs and audit reports beside epoch-0 originals.

    Returns a list of report dictionaries.  The source is never replaced.
    """
    if output and len(paths) != 1:
        raise S.GraphError("--epoch1-output requires exactly one source graph")
    reports = []
    for source in paths:
        if S.is_native_graph(source):
            raise S.GraphError("%s is already an epoch-1 graph" % source)
        with open(source, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        fingerprint = "sha256:" + digest
        destination = output or _destination(source)
        audit_path = destination + ".audit.json"
        if os.path.exists(destination) or os.path.exists(audit_path):
            raise S.GraphError(
                "migration output already exists; refusing to overwrite:\n  %s"
                % (destination if os.path.exists(destination) else audit_path))

        converted = [F.meta_event()]
        changes = []
        for raw, lineno in S._raw_events(source):
            event, actions = _native_record(raw, fingerprint)
            converted.append(event)
            if actions:
                changes.append({
                    "line": lineno,
                    "event": raw.get("id"),
                    "kind": raw.get("ev"),
                    "actions": actions,
                })

        # The migration is not successful unless its own output crosses the
        # strict native fold boundary.
        S.Graph().apply_all([
            (event, destination, n)
            for n, event in enumerate(converted, 1)
        ]).validate()

        report = {
            "source": os.path.abspath(source),
            "source_sha256": fingerprint,
            "destination": os.path.abspath(destination),
            "audit": os.path.abspath(audit_path),
            "created_with": F.created_with(),
            "graph_format": F.GRAPH_FORMAT,
            "kernel_epoch": F.KERNEL_EPOCH,
            "events": len(converted) - 1,
            "changes": changes,
            "dry_run": bool(dry_run),
        }
        if not dry_run:
            parent = os.path.dirname(destination)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent)
            with open(destination, "x", encoding="utf-8") as fh:
                for event in converted:
                    fh.write(json.dumps(event, sort_keys=True) + "\n")
            with open(audit_path, "x", encoding="utf-8") as fh:
                json.dump(report, fh, indent=2, sort_keys=True)
                fh.write("\n")
        reports.append(report)
    return reports
