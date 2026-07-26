"""The checker: reads a folded graph, emits findings, decides.

Deterministic, no model in the loop, no solver, no network.  Given a graph it
returns the same findings every time, and `gp check` exits 0 iff there are
none above the configured severity floor.

The checker never grades evidence and the ladder never licenses a transport.
Those are orthogonal axes and conflating them is how a project ends up with an
`independently-audited` predicate imported across an edge that forbids it.
"""

from . import kernel as K
from .discharge import discharge_for

# Severities.  Not every finding is an accusation.
UNSOUND_CONCLUSION = "UNSOUND_CONCLUSION"  # a statement was recorded that the
                                           # graph itself contradicts
UNSOUND_PREMISE = "UNSOUND_PREMISE"        # the conclusion may hold; the route
                                           # does not
TRIAGE = "TRIAGE"                          # nothing was claimed wrongly; the
                                           # type layer only routes the result
DEBT = "DEBT"                              # a hole recorded as a hole

SEVERITY_ORDER = [DEBT, TRIAGE, UNSOUND_PREMISE, UNSOUND_CONCLUSION]
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITY_ORDER)}

# Rule codes.
R_TRANSPORT = "TRANSPORT"
R_TAINT = "TAINT"
R_COVERAGE = "COVERAGE"
R_UNTYPED = "UNTYPED-EDGE"
R_REFINEMENT = "REFINEMENT-TYPE"

EXISTENCE_OPPOSITE = {K.EMPTY: K.NONEMPTY, K.NONEMPTY: K.EMPTY}


class Finding(object):
    __slots__ = ("rule", "fid", "severity", "subject", "detail", "discharge",
                 "trace", "derived_severity", "severity_why")

    def __init__(self, rule, fid, severity, subject, detail, discharge,
                 trace=(), derived_severity=None, severity_why=None):
        self.rule = rule
        self.fid = fid
        self.severity = severity
        self.subject = subject
        self.detail = detail
        self.discharge = discharge
        self.trace = list(trace)
        self.derived_severity = derived_severity or severity
        self.severity_why = severity_why

    @property
    def overridden(self):
        return self.severity != self.derived_severity

    def as_dict(self):
        d = {"rule": self.rule, "id": self.fid, "severity": self.severity,
             "subject": self.subject, "detail": self.detail,
             "discharge": self.discharge}
        if self.trace:
            d["trace"] = [{"edge": e, "direction": dr, "licensed": lic,
                           "reason": rsn} for e, dr, lic, rsn in self.trace]
        if self.overridden:
            d["derived_severity"] = self.derived_severity
            d["severity_why"] = self.severity_why
        return d

    def __repr__(self):
        return "<%s %s %s>" % (self.rule, self.fid, self.severity)


def audit_inference(graph, iid):
    """Walk an inference's path through the kernel.

    Returns (licensed, trace) where trace is [(edge, direction, ok, reason)].
    Every step is recorded, licensed or not, so a report can show the whole
    route rather than only the step that failed.
    """
    inf = graph.inferences[iid]
    claim = graph.claims[inf["claim"]]
    trace, ok = [], True
    for eid, direction in inf["path"]:
        e = graph.edges[eid]
        r = K.transport(e["type"], direction, claim["kind"],
                        scope=claim.get("scope"),
                        certificate=claim.get("certificate"),
                        map_kind=e["map_kind"],
                        zariski_closed=claim.get("zariski_closed"))
        trace.append((eid, direction, r.licensed, r.reason))
        if not r.licensed:
            ok = False
    return ok, trace


def probe(graph, claim_id, edge_id, direction, etype=None, map_kind=None,
          zariski_closed=None):
    """What WOULD happen if this claim crossed this edge in this direction.

    A probe is not an inference: nothing asserts that anyone took this step.
    It exists because the sharpest credibility checks are counterfactual, and
    the prototypes both needed it without naming it.  Two examples, and they
    are the load-bearing controls in their respective domains:

      CONTRAST PAIR.  Push two emptiness claims -- both computed over the same
      small field -- across the SAME edge in the SAME direction.  One is
      licensed and one is not, and the only thing that differs is the
      certificate.  As recorded inferences these two claims travel over
      different edges, so the discrimination is invisible; only the probe
      isolates the certificate as the sole cause.

      NON-VACUITY.  Retype an EQUIVALENCE as NECESSARY_CONDITION and check that
      it would now forbid a transport the equivalence licenses.  If it would
      not, the positive control on that edge proves nothing, because the edge's
      type was never load-bearing for it.

    `etype`, `map_kind` and `zariski_closed` override the declared values, so a
    probe can ask the retyping question without mutating the graph.
    """
    claim = graph.claims[claim_id]
    edge = graph.edges[edge_id]
    return K.transport(
        etype or edge["type"], direction, claim["kind"],
        scope=claim.get("scope"), certificate=claim.get("certificate"),
        map_kind=map_kind or edge["map_kind"],
        zariski_closed=(claim.get("zariski_closed")
                        if zariski_closed is None else zariski_closed))


def contradicting_claims(graph, model_id, kind, exclude=()):
    """Claims at `model_id` asserting the opposite existence statement.

    This is what upgrades a refused transport from "the route does not hold" to
    "the conclusion is FALSE" -- and it is derived from the graph rather than
    graded by hand.  Note it turns on MODEL identity: placing a NONEMPTY claim
    on the model an inference concludes about is itself the modelling act that
    makes the contradiction visible.  No scope lattice is involved and none is
    wanted; the field lives in the model.
    """
    opposite = EXISTENCE_OPPOSITE.get(kind)
    if opposite is None:
        return []
    return sorted(cid for cid, c in graph.claims.items()
                  if c["model"] == model_id and c["kind"] == opposite
                  and cid not in exclude)


def _first_refusal(graph, trace):
    for eid, direction, ok, reason in trace:
        if not ok:
            return graph.edges[eid], direction, reason
    return None, None, None


def check_transport(graph):
    findings = []
    for iid in graph.inference_order:
        inf = graph.inferences[iid]
        ok, trace = audit_inference(graph, iid)
        if ok:
            continue
        edge, direction, reason = _first_refusal(graph, trace)
        counter = contradicting_claims(graph, inf["concludes_at"],
                                       inf["concludes_kind"],
                                       exclude=(inf["claim"],))
        if edge["type"] == K.UNTYPED:
            derived = DEBT
        elif counter:
            derived = UNSOUND_CONCLUSION
        else:
            derived = UNSOUND_PREMISE
        severity = inf.get("severity_override") or derived
        detail = "%s\n  asserted: %s\n  refused : %s" % (
            graph.claims[inf["claim"]]["statement"], inf["asserted"], reason)
        if counter:
            detail += ("\n  contradicted by: %s\n    (%s)"
                       % (", ".join(counter),
                          graph.claims[counter[0]]["statement"]))
        findings.append(Finding(
            R_TRANSPORT, "%s:%s" % (R_TRANSPORT, iid), severity, iid, detail,
            discharge_for(edge["type"], direction, inf["concludes_kind"],
                          graph=graph, edge=edge),
            trace=trace, derived_severity=derived,
            severity_why=inf.get("severity_why")))
    return findings


def check_taint(graph, transport_findings):
    """A licensed conclusion drawn in an illegitimately-constructed model is
    still unsound.  Provenance has to be tracked separately from transport."""
    refused = {f.subject for f in transport_findings if f.rule == R_TRANSPORT}
    findings = []
    for mid in sorted(graph.built_by):
        bad = [b for b in graph.built_by[mid] if b in refused]
        if not bad:
            continue
        downstream = sorted(cid for cid, c in graph.claims.items()
                            if c["model"] == mid)
        findings.append(Finding(
            R_TAINT, "%s:%s" % (R_TAINT, mid), UNSOUND_PREMISE, mid,
            "model %s was BUILT BY a refused inference (%s).  Every claim "
            "drawn in it inherits the defect even where its own transport is "
            "licensed.\n  affected claims: %s"
            % (mid, ", ".join(bad), ", ".join(downstream) or "(none)"),
            discharge_for(R_TAINT, None, None, graph=graph)))
    return findings


def coverage_gaps(graph, model):
    """`touched(axis) \\ declared(model, axis)`, per axis the model claims to cover.

    Ten lines, readable by a human, over an inventory whose every row is
    independently checkable.  Structurally this is a CEGAR signature-closure
    rule: the abstraction's vocabulary must contain every index appearing in
    the concrete object's own impositions and read sites.  It fires on ABSENT
    structure only -- a declared-but-too-weak component is invisible to it, and
    that limitation is a property of the whole coverage tradition, not a bug
    here.
    """
    gaps = {}
    for axis in model.get("coverage_axes", []):
        touched = set()
        for row in model["imposes"] + model["reads"]:
            if row.get("axis") == axis:
                touched.update(row.get("at") or [])
        missing = sorted(touched - set(model["declares"].get(axis, [])))
        if missing:
            gaps[axis] = missing
    return gaps


def check_coverage(graph):
    findings = []
    for mid in sorted(graph.models):
        m = graph.models[mid]
        for axis, missing in sorted(coverage_gaps(graph, m).items()):
            imposing = sorted({r["name"] for r in m["imposes"]
                               if r.get("axis") == axis
                               and set(r.get("at") or []) & set(missing)})
            reading = sorted({r["name"] for r in m["reads"]
                              if r.get("axis") == axis
                              and set(r.get("at") or []) & set(missing)})
            detail = (
                "model %s asserts coverage on axis %r but declares nothing at "
                "%s.\n  declared: %s\n  imposes there: %s\n  reads there   : %s\n"
                "  Where nothing is declared the relaxation is UNBOUNDED: the "
                "model imposes literally nothing at those indices."
                % (mid, axis, ", ".join(missing),
                   ", ".join(m["declares"].get(axis, [])) or "(nothing)",
                   "; ".join(imposing) or "(none)",
                   "; ".join(reading) or "(none)"))
            findings.append(Finding(
                R_COVERAGE, "%s:%s:%s" % (R_COVERAGE, mid, axis),
                UNSOUND_PREMISE, mid, detail,
                discharge_for(R_COVERAGE, None, None, graph=graph,
                              axis=axis, missing=missing)))
    return findings


def check_untyped(graph):
    findings = []
    for eid in sorted(graph.edges):
        e = graph.edges[eid]
        if e["type"] != K.UNTYPED:
            continue
        downstream = sorted(iid for iid in graph.inference_order
                            if any(s[0] == eid
                                   for s in graph.inferences[iid]["path"]))
        findings.append(Finding(
            R_UNTYPED, "%s:%s" % (R_UNTYPED, eid), DEBT, eid,
            "edge %s (%s -> %s) has no declared relaxation type.\n  debt: %s\n"
            "  inferences crossing it: %s"
            % (eid, e["src"], e["dst"], e.get("debt_why"),
               ", ".join(downstream) or "(none yet)"),
            discharge_for(K.UNTYPED, None, None, graph=graph, edge=e)))
    return findings


def check_refinement(graph):
    """Monotonicity is not a fourth type.

    Adding equations gives V(new) subset V(old), which is a NECESSARY_CONDITION
    edge new -> old read AGAINST.  "A closed branch can never reopen under
    refinement" is therefore a theorem about ONE existing type, and a
    refinement edge typed as anything else is a modelling error.
    """
    findings = []
    for eid in sorted(graph.edges):
        e = graph.edges[eid]
        if not e["refinement"] or e["type"] == K.NECESSARY_CONDITION:
            continue
        findings.append(Finding(
            R_REFINEMENT, "%s:%s" % (R_REFINEMENT, eid), UNSOUND_PREMISE, eid,
            "edge %s is declared a refinement (src = dst + equations) but is "
            "typed %s.  A refinement is a NECESSARY_CONDITION edge read "
            "AGAINST the arrow; no other type states that adding equations "
            "cannot reopen a closed branch."
            % (eid, e["type"]),
            discharge_for(R_REFINEMENT, None, None, graph=graph, edge=e)))
    return findings


def run(graph):
    """All rules, in a stable order, most severe first."""
    transport_findings = check_transport(graph)
    findings = (transport_findings
                + check_taint(graph, transport_findings)
                + check_coverage(graph)
                + check_refinement(graph)
                + check_untyped(graph))
    findings.sort(key=lambda f: (-SEVERITY_RANK[f.severity], f.rule, f.fid))
    return findings


def clean_inferences(graph, findings):
    """Inferences the checker did NOT flag.

    Reported because a framework that flags a sound step is a false-positive
    generator and unusable.  The positive controls are the load-bearing half of
    any credibility claim, so they get printed, not assumed.
    """
    flagged = {f.subject for f in findings if f.rule == R_TRANSPORT}
    return [i for i in graph.inference_order if i not in flagged]


def exit_code(findings, floor=UNSOUND_PREMISE):
    """1 iff any finding is at or above `floor`.

    The floor is DEBT-tolerant by default: a recorded hole is a hole you are
    tracking, and blocking on it would push people to stop recording them.
    """
    rank = SEVERITY_RANK[floor]
    return 1 if any(SEVERITY_RANK[f.severity] >= rank for f in findings) else 0
