"""Version and fingerprint the inputs behind computed verifier verdicts.

A stored ``VERIFIED`` is executable trust.  It must therefore say which
verifier produced it, which kernel semantics interpreted it, which backend ran
it, and exactly which graph records were presented as input.  Otherwise a
verdict produced by yesterday's buggy verifier remains authoritative forever.

This module deliberately owns only verifier provenance.  Graph-format
versioning lives in :mod:`grandportage.format`; the store calls
``current_verdict`` while folding and projects a verdict into the effective
graph only when this module says it is current.
"""

import hashlib
import json
import re

from . import format as F


BACKEND = "singular"

# Increment one entry whenever that verifier's meaning or implementation
# changes in a way that requires stored answers to be recomputed.  Keeping
# these independent avoids invalidating every verdict when one checker changes.
VERIFIERS = {
    "claim": ("verify.identity", 1),
    "edge": ("verify.containment", 1),
    "certificate": ("verify.unit_ideal", 1),
    "ring_iso": ("verify.ring_iso", 1),
    "witness": ("verify.point_witness", 1),
    "operation": ("verify.operation_output", 1),
    "partition": ("verify.partition_exhaustiveness", 1),
}

_FINGERPRINT_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

# Verdict projection mutates the folded target.  None of those computed fields
# may feed its own input fingerprint, or a verdict would become stale at the
# instant it was applied.
_COMPUTED_FIELDS = {
    "identity_verdict", "identity_why",
    "containment", "containment_why",
    "certificate_verdict", "certificate_why",
    "ring_iso_verdict", "ring_iso_why",
    "witness_verdict", "witness_why",
    "output_verdict", "output_why",
    "exhaustive_verdict", "exhaustive_why",
    "representation",
}

# Lifecycle annotations are derived only after the event fold.  Active objects
# have none when verified; including them would make fingerprints depend on
# whether supersession resolution happened before or after an otherwise
# identical read.
_LIFECYCLE_FIELDS = {
    "superseded_by", "retracted_by", "withdrawn_by",
}


def _semantic(record):
    """Return the declared, verifier-relevant form of one folded record."""
    if record is None:
        return None
    return {
        key: value
        for key, value in record.items()
        if key not in _COMPUTED_FIELDS and key not in _LIFECYCLE_FIELDS
    }


def input_payload(graph, subject, of):
    """The complete graph input consumed by one verifier subject.

    The payload names records, rather than selecting a hand-maintained subset
    of fields.  Adding a new declaration field therefore invalidates old
    verdicts conservatively until the verifier is rerun.
    """
    if subject in ("edge", "ring_iso", "operation"):
        edge = graph.edges.get(of)
        return {
            "subject": subject,
            "of": of,
            "edge": _semantic(edge),
            "src": _semantic(graph.models.get(edge.get("src"))) if edge else None,
            "dst": _semantic(graph.models.get(edge.get("dst"))) if edge else None,
        }
    if subject in ("claim", "certificate", "witness"):
        claim = graph.claims.get(of)
        return {
            "subject": subject,
            "of": of,
            "claim": _semantic(claim),
            "model": (
                _semantic(graph.models.get(claim.get("model")))
                if claim else None
            ),
        }
    if subject == "partition":
        partition = graph.partitions.get(of)
        branches = partition.get("branches") or [] if partition else []
        return {
            "subject": subject,
            "of": of,
            "partition": _semantic(partition),
            "parent": (
                _semantic(graph.models.get(partition.get("parent")))
                if partition else None
            ),
            "branches": [
                {"id": bid, "model": _semantic(graph.models.get(bid))}
                for bid in branches
            ],
        }
    raise ValueError("unknown verdict subject %r" % subject)


def input_fingerprint(graph, subject, of):
    """Stable SHA-256 of the canonical semantic verifier input."""
    encoded = json.dumps(
        input_payload(graph, subject, of),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def event_digest(event):
    """Content address one complete verdict event, excluding only its id."""
    payload = {key: value for key, value in event.items() if key != "id"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


def metadata(graph, subject, of):
    """Provenance fields attached to a newly computed verdict event."""
    verifier, verifier_version = VERIFIERS[subject]
    return {
        "verifier": verifier,
        "verifier_version": verifier_version,
        "kernel_epoch": F.KERNEL_EPOCH,
        "backend": BACKEND,
        "input_fingerprint": input_fingerprint(graph, subject, of),
    }


def current_verdict(graph, event):
    """Return ``(is_current, reason)`` for a stored verdict event.

    Missing metadata is the epoch-0 form.  It remains valid log history but is
    deliberately inactive.  Mismatches are handled the same way: stale
    evidence must never overwrite a current verdict or license transport.
    """
    if getattr(graph, "graph_format", 0) != F.GRAPH_FORMAT:
        return False, "epoch-0 verdicts are compatibility history only"
    subject = event.get("subject")
    if subject not in VERIFIERS:
        return False, "unknown verifier subject"
    expected_verifier, expected_version = VERIFIERS[subject]
    required = (
        "verifier", "verifier_version", "kernel_epoch",
        "backend", "input_fingerprint",
    )
    missing = [field for field in required if event.get(field) is None]
    if missing:
        return False, "legacy verdict lacks %s" % ", ".join(missing)
    if event.get("verifier") != expected_verifier:
        return False, "verifier identity does not match"
    if event.get("verifier_version") != expected_version:
        return False, "verifier version does not match"
    if event.get("kernel_epoch") != F.KERNEL_EPOCH:
        return False, "kernel epoch does not match"
    if event.get("backend") != BACKEND:
        return False, "backend does not match"
    fingerprint = event.get("input_fingerprint")
    if not isinstance(fingerprint, str) or not _FINGERPRINT_RE.match(fingerprint):
        return False, "input fingerprint is malformed"
    if fingerprint != input_fingerprint(graph, subject, event.get("of")):
        return False, "verifier input fingerprint does not match"
    return True, "current"
