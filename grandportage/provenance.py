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

from . import backend as B
from . import format as F
from . import kernel as K


BACKEND = "singular"

# Increment one entry whenever that verifier's meaning or implementation
# changes in a way that requires stored answers to be recomputed.  Keeping
# these independent avoids invalidating every verdict when one checker changes.
VERIFIERS = {
    "claim": ("verify.identity", 2),
    "edge": ("verify.containment", 2),
    "certificate": ("verify.unit_ideal", 2),
    "ring_iso": ("verify.ring_iso", 2),
    "witness": ("verify.point_witness", 2),
    "operation": ("verify.operation_output", 2),
    "partition": ("verify.partition_exhaustiveness", 2),
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


def event_fingerprint(value):
    """Stable SHA-256 for an execution trace or other provenance payload."""
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def event_digest(event):
    """Content address one complete verdict event, excluding only its id."""
    payload = {key: value for key, value in event.items() if key != "id"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16]


_BACKEND_PREFIX = "gp-backend-v2:"
BACKEND_PROVENANCE_PREFIX = _BACKEND_PREFIX
_SYMBOL = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _active_model(graph, mid):
    model = graph.models.get(mid)
    return model if model and not model.get("superseded_by") else None


def _eligible_structural_containment(graph, eid):
    edge = graph.edges.get(eid)
    if (not edge or edge.get("superseded_by")
            or K.is_mapped_equivalence(edge)
            or edge.get("type") == K.SPECIALIZATION):
        return False
    source = _active_model(graph, edge.get("src"))
    target = _active_model(graph, edge.get("dst"))
    if not source or not target:
        return False
    if (source.get("ideal_pending") or target.get("ideal_pending")
            or source.get("generators") is None
            or target.get("generators") is None):
        return False
    ring = source.get("ring_vars") or []
    if (not ring or "characteristic" not in source
            or "characteristic" not in target
            or source["characteristic"] != target["characteristic"]
            or set(target.get("ring_vars") or []) != set(ring)):
        return False
    return target["generators"] == []


def _eligible_structural_operation(graph, event):
    edge = graph.edges.get(event.get("of"))
    if not edge or edge.get("superseded_by"):
        return False
    kind = edge.get("built_by_operation")
    if kind not in ("SaturateClosure", "Eliminate"):
        return False
    built_id = edge.get("src") if kind == "SaturateClosure" else edge.get("dst")
    source_id = edge.get("dst") if kind == "SaturateClosure" else edge.get("src")
    built = _active_model(graph, built_id)
    source = _active_model(graph, source_id)
    if not built or not source:
        return False
    if (built.get("ideal_pending") or source.get("ideal_pending")
            or built.get("generators") is None
            or source.get("generators") is None):
        return False
    if (not (source.get("ring_vars") or [])
            or "characteristic" not in source
            or "characteristic" not in built
            or source["characteristic"] != built["characteristic"]):
        return False
    generators = built["generators"]
    if kind == "SaturateClosure" and not built.get("saturated_at"):
        return False
    if kind == "Eliminate":
        ring = source.get("ring_vars") or []
        eliminated = built.get("eliminated")
        if (not isinstance(eliminated, list) or not eliminated
                or len(eliminated) != len(set(eliminated))
                or any(variable not in ring for variable in eliminated)):
            return False
        if (built.get("ring_vars") or []) != [
                variable for variable in ring
                if variable not in set(eliminated)]:
            return False
    if event.get("verdict") == "VERIFIED":
        return generators == []
    if (event.get("verdict") != "NOT_THE_STATED_OUTPUT"
            or kind != "Eliminate"):
        return False
    kept = set(built.get("ring_vars") or [])
    return bool(generators) and all(
        any(symbol not in kept for symbol in _SYMBOL.findall(str(generator)))
        for generator in generators
    )


def _allows_empty_structural_trace(graph, event):
    """Recognize eligible verifier-native decisions with no backend run."""
    if event.get("verdict") == "UNVERIFIED":
        return True
    if event.get("subject") == "edge" and event.get("verdict") == "VERIFIED":
        return _eligible_structural_containment(graph, event.get("of"))
    if event.get("subject") == "operation":
        return _eligible_structural_operation(graph, event)
    return False

def encode_backend_provenance(execution):
    """Encode a versioned manifest inside the format-1 `backend` string."""
    if not isinstance(execution, dict):
        raise ValueError("execution provenance must be an explicit manifest")
    return _BACKEND_PREFIX + json.dumps(
        execution, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )


def backend_provenance(value, current_only=True):
    """Decode and validate a v2 backend descriptor, or return ``None``."""
    if not isinstance(value, str) or not value.startswith(_BACKEND_PREFIX):
        return None
    try:
        manifest = json.loads(value[len(_BACKEND_PREFIX):])
    except (TypeError, ValueError):
        return None
    if not isinstance(manifest, dict):
        return None
    required = {
        "schema", "contract", "implementation", "implementation_version",
        "protocol_version", "binary_version", "executions",
        "trace_fingerprint",
    }
    if set(manifest) != required:
        return None
    if manifest["schema"] != 2:
        return None
    if (not isinstance(manifest["contract"], str)
            or not manifest["contract"]
            or not isinstance(manifest["implementation"], str)
            or not manifest["implementation"]
            or type(manifest["implementation_version"]) is not int
            or manifest["implementation_version"] < 1
            or type(manifest["protocol_version"]) is not int
            or manifest["protocol_version"] < 1):
        return None
    if current_only and (
            manifest["contract"] != B.SINGULAR_CONTRACT
            or manifest["implementation"] != B.SINGULAR_IMPLEMENTATION
            or manifest["implementation_version"]
            != B.SINGULAR_IMPLEMENTATION_VERSION
            or manifest["protocol_version"] != B.BACKEND_PROTOCOL_VERSION):
        return None
    version = manifest["binary_version"]
    if (not isinstance(version, str) or not version.strip()
            or version.startswith("unavailable:")
            or version in ("unreported", "test-double")):
        return None
    trace = manifest["executions"]
    if (not isinstance(trace, list)
            or not all(B.valid_execution_trace_entry(entry)
                       for entry in trace)):
        return None
    expected = B.semantic_fingerprint("backend_execution_trace", trace)
    if manifest["trace_fingerprint"] != expected:
        return None
    return manifest


def metadata(graph, subject, of, execution=None):
    """Provenance fields attached to a newly computed verdict event."""
    if execution is None:
        raise ValueError(
            "verdict v2 needs explicit execution provenance; an absent run "
            "cannot be replaced by a fabricated empty trace"
        )
    verifier, verifier_version = VERIFIERS[subject]
    return {
        "verifier": verifier,
        "verifier_version": verifier_version,
        "kernel_epoch": F.KERNEL_EPOCH,
        "backend": encode_backend_provenance(execution),
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
    manifest = backend_provenance(event.get("backend"))
    if manifest is None:
        return False, "backend execution provenance is absent or invalid"
    if (not manifest["executions"]
            and not _allows_empty_structural_trace(graph, event)):
        return False, (
            "authoritative %s verdict lacks a backend execution trace and "
            "is not a verifier-native structural decision" % subject)
    fingerprint = event.get("input_fingerprint")
    if not isinstance(fingerprint, str) or not _FINGERPRINT_RE.match(fingerprint):
        return False, "input fingerprint is malformed"
    if fingerprint != input_fingerprint(graph, subject, event.get("of")):
        return False, "verifier input fingerprint does not match"
    return True, "current"
