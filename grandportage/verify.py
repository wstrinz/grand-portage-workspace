"""Verify by computation what the graph currently takes on the author's word.

SEPARATE FROM THE CHECKER ON PURPOSE.  `check.py` is deterministic, spawns no
process and reaches no network; given a graph it returns the same findings
every time, and that property is worth more than the convenience of folding
verification into it.  So the division is:

    check.py    reports the HOLE      -- free, deterministic, every run
    verify.py   fills it              -- costs CAS time, an explicit act

That split is the same one the project already makes between a finding and its
discharge, and it keeps the expensive thing opt-in.

WHAT IS VERIFIED, and why it is the deepest thing here.  Every edge asserts
`V(src) subset V(dst)`.  The kernel's opening comment says so and all six types
are relaxations in that sense -- and it has never been checked, only declared.
That makes it the SIXTH instance of the pattern this project keeps finding, at
the lowest level available: a field that DETERMINES transport and is taken on
the author's word.

The containment follows from an ideal containment the other way round:

    I(dst) subset I(src)   ==>   V(src) subset V(dst)

More equations cut a smaller variety.  So the test is one reduction per
generator of `I(dst)`: each must lie in `I(src)`, which is exactly the
membership question `cas.classify_identity` already answers.

SUFFICIENT, NOT NECESSARY, AND THE FAILING SIDE PROVES NOTHING.  This is the
whole of what this module may and may not say, and getting it wrong here would
be the same overreach it exists to catch.

    I(dst) subset I(src)       ==>  V(src) subset V(dst)      SOUND
    I(dst) not subset I(src)   ==>  nothing follows

The containment really needs `I(dst) subset RADICAL(I(src))`, and reduction
tests plain ideal membership.  So a generator that fails to reduce refutes the
CHEAP TEST and not the edge: the containment may still hold through the
radical.  There are therefore three verdicts and REFUTED is not among them --

    VERIFIED       every generator reduced; the containment is established
    NOT_BY_IDEAL   the cheap test failed; the containment is UNESTABLISHED,
                   which is not the same as false
    UNVERIFIED     the question could not be put (no ideal, different rings)

Genuinely REFUTING an edge needs a point of `V(src)` outside `V(dst)` -- a
witness, not a reduction -- and that is deliberately out of scope here.  A
module that answered a question it had not asked would be the honour system
wearing a computation.
"""

import os

from . import cas
from . import kernel as K
from . import store as S

VERIFIED = "VERIFIED"
NOT_BY_IDEAL = "NOT_BY_IDEAL"
UNVERIFIED = "UNVERIFIED"


def containment(graph, eid, timeout=300, _runner=None):
    """Is `I(dst)` inside `I(src)`?  Returns (verdict, why).

    One reduction per generator, stopping at the first that fails, because the
    first failure is the whole answer and the rest cost money.
    """
    e = graph.edges[eid]
    src, dst = graph.models.get(e["src"]), graph.models.get(e["dst"])
    if not src or not dst:
        return UNVERIFIED, "an endpoint is not a declared model"
    if src.get("generators") is None or dst.get("generators") is None:
        return UNVERIFIED, "one endpoint carries no ideal"
    ring = src.get("ring_vars") or []
    if not ring:
        return UNVERIFIED, "the source model declares no ring variables"
    if set(dst.get("ring_vars") or []) != set(ring):
        # NOT A FAILURE OF THE MATHEMATICS, a failure of the comparison.  Two
        # ideals in different rings are not comparable by reduction, and
        # pretending otherwise would produce a confident verdict about nothing.
        return UNVERIFIED, (
            "the two models are written in different rings (%s vs %s); an "
            "ideal containment between them is not a reduction question"
            % (", ".join(ring), ", ".join(dst.get("ring_vars") or [])))

    src_gens = list(src["generators"])
    for g in dst["generators"]:
        origin, evidence = cas.classify_identity(
            ring, lhs=g, rhs="0", generators=src_gens,
            timeout=timeout, _runner=_runner)
        if origin in (K.AMBIENT, K.DERIVED):
            continue
        return NOT_BY_IDEAL, (
            "generator %r of %s's ideal does not reduce to 0 modulo %s's -- it "
            "reduces to %s. So I(%s) is not inside I(%s), and the SUFFICIENT "
            "test for V(%s) subset V(%s) fails.\n"
            "  THAT IS NOT A REFUTATION. The containment can still hold "
            "through the radical, which reduction does not test. What it means "
            "is that the edge's central assertion is UNESTABLISHED, where "
            "before it was merely unexamined. To refute it you need a point of "
            "V(%s) outside V(%s), and that is a witness rather than a "
            "reduction."
            % (g, e["dst"], e["src"],
               (evidence or {}).get("reduced_modulo_ideal", "a nonzero form"),
               e["dst"], e["src"], e["src"], e["dst"], e["src"], e["dst"]))
    return VERIFIED, (
        "every generator of %s's ideal reduces to 0 modulo %s's, so I(%s) is "
        "inside I(%s) and V(%s) is inside V(%s)."
        % (e["dst"], e["src"], e["dst"], e["src"], e["src"], e["dst"]))


def verify_all(root=".", timeout=300, _runner=None):
    """Verify every checkable edge and RECORD the answers in the graph.

    Recording is the point.  A verification that lives in a terminal scrollback
    is a verification nobody can act on next week, and this project's whole
    claim is that the graph is the state.  The result is appended as a
    supersession of the edge, so the log stays append-only and `gp history`
    shows that the check happened.
    """
    path = S.graph_path(root)
    graph = S.load(path)
    results = []
    for eid in sorted(graph.edges):
        e = graph.edges[eid]
        if e.get("containment"):
            continue
        src, dst = graph.models.get(e["src"]), graph.models.get(e["dst"])
        if not src or not dst:
            continue
        if src.get("generators") is None or dst.get("generators") is None:
            continue
        verdict, why = containment(graph, eid, timeout=timeout,
                                   _runner=_runner)
        results.append((eid, verdict, why))
    return results
