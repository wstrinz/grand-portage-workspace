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
`V(src) subset V(dst)`.  The kernel's opening comment says so and FIVE of the
six types are relaxations in that sense -- and it has never been checked, only
declared.

THE SIXTH IS NOT, AND THIS FILE USED TO SAY IT WAS.  SPECIALIZATION relates the
GENERIC fibre of a scheme over Spec Z to a SPECIAL fibre.  Those are different
fibres, not nested sets: neither contains the other, and the kernel's own
counterexamples prove it -- the Fano plane is empty over Q and nonempty over
F_2, the non-Fano matroid the reverse.  So there is no containment to check,
and `containment` refuses the row rather than computing a confident answer
about a relation that does not exist.

Found by asking how much of the transport table follows from inclusion alone.
Twenty-seven of thirty-six point cells do; three more follow from inclusion in
BOTH directions, which is what an EQUIVALENCE's converse buys; three need a
capability inclusion does not supply.  The last three are SPECIALIZATION's, and
they are weaker than inclusion for the reason above.  A generalisation that
covers five rows and quietly mis-describes the sixth is the shape this project
exists to catch.

For the five that ARE relaxations, the containment was the SIXTH instance of
the pattern this project keeps finding, at the lowest level available: a field
that DETERMINES transport and is taken on the author's word.

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

import hashlib
import os

from . import cas
from . import kernel as K
from . import store as S

VERIFIED = "VERIFIED"
NOT_BY_IDEAL = "NOT_BY_IDEAL"
UNVERIFIED = "UNVERIFIED"


def _pending_ideal(mid, model):
    """The message for a model still waiting on the computation of its ideal.

    ASKED BEFORE THE SOLVER, NOT AFTER.  A constructed model -- a saturation,
    an elimination -- has an ideal that only the CAS knows, and it says so with
    `ideal_pending` rather than by putting a placeholder in `generators`.  The
    placeholder version reached Singular verbatim and came back `expected
    ideal-expression`, an honest error about the wrong thing: nothing had gone
    wrong with the solver, and nothing was wrong with the mathematics.  The
    author simply had not run the program yet, and no layer said so.
    """
    if not model.get("ideal_pending"):
        return None
    return ("%s does not carry an ideal yet -- it is waiting on %s. There is "
            "nothing to reduce modulo until that computation has run and its "
            "generators have been recorded. This is not a failed check; it is "
            "a check that cannot yet be put." % (mid, model["ideal_pending"]))


def containment(graph, eid, timeout=300, _runner=None):
    """Is `I(dst)` inside `I(src)`?  Returns (verdict, why).

    One reduction per generator, stopping at the first that fails, because the
    first failure is the whole answer and the rest cost money.
    """
    e = graph.edges[eid]
    if e.get("type") == K.SPECIALIZATION:
        # NOT A RELAXATION, so there is no containment to test -- and the
        # reduction would have run in characteristic 0 against generators
        # living in characteristic p, producing a confident verdict about a
        # relation that does not exist.
        return UNVERIFIED, (
            "edge %s is a SPECIALIZATION, and that is the one type whose ends "
            "are not nested. The generic fibre and a special fibre of a scheme "
            "over Spec Z are DIFFERENT FIBRES: neither contains the other, and "
            "this kernel's own counterexamples say so -- the Fano plane is "
            "empty over Q and nonempty over F_2, the non-Fano matroid the "
            "reverse.\n"
            "  So `V(src) subset V(dst)` is not what this edge asserts, and "
            "there is nothing here for a reduction to establish. The four "
            "existence cells on this row are already False for exactly this "
            "reason." % eid)
    src, dst = graph.models.get(e["src"]), graph.models.get(e["dst"])
    if not src or not dst:
        return UNVERIFIED, "an endpoint is not a declared model"
    pending = _pending_ideal(e["src"], src) or _pending_ideal(e["dst"], dst)
    if pending:
        return UNVERIFIED, pending
    if src.get("generators") is None or dst.get("generators") is None:
        return UNVERIFIED, "one endpoint carries no ideal"
    ring = src.get("ring_vars") or []
    if not ring:
        return UNVERIFIED, "the source model declares no ring variables"
    ch = src.get("characteristic") or 0
    if (dst.get("characteristic") or 0) != ch:
        return UNVERIFIED, (
            "the endpoints declare different characteristics (%s vs %s). A "
            "reduction happens in ONE ring; comparing ideals across a "
            "characteristic change is what SPECIALIZATION is for, and it is "
            "refused above for the same reason."
            % (ch, dst.get("characteristic") or 0))
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
            characteristic=ch, timeout=timeout, _runner=_runner)
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


AMBIENT = "VERIFIED_AMBIENT"
DERIVED = "VERIFIED_DERIVED"
REFUTED = "REFUTED"


def identity(graph, cid, timeout=300, _runner=None):
    """Does this IDENTITY claim hold at its own model?  Returns (verdict, why).

    AND HERE, UNLIKE `containment`, REFUTATION IS AVAILABLE.  That asymmetry is
    not an inconsistency and it is worth stating plainly, because the module's
    other half spends a docstring refusing to say REFUTED.

        containment   the claim is `V(src) subset V(dst)`, a statement about
                      POINTS.  Reduction tests ideal membership, which is only
                      SUFFICIENT for it -- the containment can hold through the
                      radical -- so a failed reduction proves nothing.

        identity      the claim IS `lhs - rhs` lies in I, a statement about
                      FUNCTIONS.  Reduction modulo a Groebner basis DECIDES
                      ideal membership.  So a failed reduction is not a failed
                      cheap test; it is the answer.

    The difference is the same one the kernel keeps making between points and
    functions -- V(x) and V(x^2) have the same points and different coordinate
    rings -- and it is why a single reduction means different things at the two
    ends of this file.

    The verdicts:

        VERIFIED_AMBIENT   lhs - rhs is 0 in the polynomial ring.  The
                           rewriting never used the model's equations, so
                           `identity_origin: AMBIENT` is now MINTED BY
                           COMPUTATION rather than declared.
        VERIFIED_DERIVED   nonzero, but reduces to 0 modulo I.  It holds here
                           and rests on this model's own equations.
        REFUTED            it does not reduce.  The rewriting is FALSE at the
                           model it was claimed at, which no amount of correct
                           transport typing would ever have surfaced.
        UNVERIFIED         the question could not be put.
    """
    c = graph.claims.get(cid)
    if not c:
        return UNVERIFIED, "no such claim"
    if c.get("kind") != K.IDENTITY:
        return UNVERIFIED, "claim %s is %s, not an IDENTITY" % (cid, c.get("kind"))
    if c.get("lhs") is None or c.get("rhs") is None:
        return UNVERIFIED, (
            "claim %s states its rewriting only in prose. `lhs` and `rhs` are "
            "what makes it a reduction question rather than a reading "
            "question." % cid)
    ring = c.get("ring_vars") or []
    if not ring:
        return UNVERIFIED, "claim %s declares no ring variables" % cid
    model = graph.models.get(c.get("model")) or {}
    # A MODEL WITH NO EQUATIONS IS NOT A MODEL WITH MISSING DATA, and the
    # first version of this guard refused it as though it were.
    #
    # The complaint it answered was real: the REFUTED message named "%s's
    # ideal" at a model that has none, sending a reader to look for equations
    # nobody recorded.  But the fix for a wrong sentence is a right sentence.
    # Refusing to verify turned a wording bug into a false refusal, and it
    # landed on the exact case that motivated the feature -- an SOS Gram
    # identity `mon^T G mon - f = 0` lives in the polynomial ring and needs no
    # ideal at all.  `cas.classify_identity` already says so: "the model
    # imposes nothing, so 'modulo I' is the same question as 'in the ambient
    # ring', and the two agree by construction rather than by accident."
    #
    # So verify either way, and let the PROSE carry the distinction.  With no
    # ideal, DERIVED is unreachable by construction and REFUTED means "not
    # identically zero in the polynomial ring" rather than "false at this
    # model" -- both true, both worth saying, neither a reason to decline.
    # ASK THIS BEFORE `bare`, BECAUSE `bare` WOULD ANSWER IT WRONGLY.
    #
    # Below, a model with no generators is read as "imposes no equations" --
    # correct for an SOS Gram identity in the polynomial ring, and a FALSE
    # LICENCE for a saturation nobody has computed: the rewriting would be
    # reduced against the ambient ring and could come back VERIFIED_AMBIENT at
    # a model whose real ideal is unknown.  The two states spell themselves
    # differently for exactly this reason.
    pending = _pending_ideal(c.get("model"), model)
    if pending:
        return UNVERIFIED, pending
    # ABSENT IS NOT EMPTY, and reading them the same way is a false refutation.
    #
    # `generators: []` means THE AMBIENT SPACE -- the model imposes no
    # equations, so "modulo I" and "in the polynomial ring" are the same
    # question and agree by construction. That reading is right, and the SOS
    # Gram case depends on it.
    #
    # No `generators` key at all means NOBODY RECORDED THE IDEAL, which is a
    # different fact about the graph and not a fact about the model. Seventy-
    # five live models across five campaigns are in that state and NONE
    # declares `[]`, so this is the common case rather than the exotic one.
    #
    # Conflating them is safe in one direction and not the other:
    #
    #   difference is 0 in the polynomial ring  -> AMBIENT, and still SOUND.
    #     That is a statement about the ambient ring; unrecorded equations
    #     cannot make it false. So the SOS case keeps working untouched.
    #   difference is nonzero                   -> REFUTED, and FALSE.
    #     It says the rewriting does not hold at its own model, at
    #     UNSOUND_CONCLUSION, when the rewriting may hold perfectly well
    #     modulo equations the graph never recorded. "Not identically zero in
    #     the polynomial ring" is simply not the question that was asked.
    unrecorded = model.get("generators") is None
    gens = list(model.get("generators") or [])
    bare = not gens
    modulo = ("in the polynomial ring, which is the whole question here "
              "because %s imposes no equations" % c.get("model") if bare
              else "modulo %s's ideal" % c.get("model"))
    origin, evidence = cas.classify_identity(
        ring, lhs=c["lhs"], rhs=c["rhs"], generators=gens,
        characteristic=model.get("characteristic") or 0,
        timeout=timeout, _runner=_runner)
    if origin == K.AMBIENT:
        return AMBIENT, (
            "(%s) - (%s) reduces to 0 in the polynomial ring itself%s. The "
            "rewriting is AMBIENT, and that is now a computed fact rather "
            "than a declared one."
            % (c["lhs"], c["rhs"],
               "" if bare else
               ", before any of %s's equations are imposed" % c.get("model")))
    if origin == K.DERIVED:
        # AND HERE THE VERDICT EARNS A CERTIFICATE.
        #
        # "It reduced to 0" is a claim about a run.  Nobody can recheck it
        # without doing the run again, which means the only real check is
        # trusting the search -- the exact position `UNIT_IDEAL_CERT` was in
        # before its cofactors were captured, and that one produced an erratum.
        #
        # A DERIVED rewriting rests on the model's equations, so `lhs - rhs =
        # sum b_i f_i` and the cofactors ARE the derivation.  Expanding them is
        # arithmetic: no Buchberger, no monomial order, no trust in the search.
        # It is also the bridge to a proof assistant, which can check a
        # polynomial identity and should never run a Groebner engine.
        #
        # THE VERIFIER DOES NOT TRUST ITS OWN LIFT.  It expands what it got
        # back before recording anything, and a mismatch is reported rather
        # than smoothed over -- that is the case the expansion exists to catch.
        target = "(%s) - (%s)" % (c["lhs"], c["rhs"])
        why = ("(%s) - (%s) is nonzero in the polynomial ring but reduces to 0 "
               "modulo %s's ideal, so the rewriting holds in that coordinate "
               "ring and DERIVES from the model's own equations."
               % (c["lhs"], c["rhs"], c.get("model")))
        rep = cas.membership_representation(
            ring, target, gens, characteristic=model.get("characteristic") or 0,
            timeout=timeout, _runner=_runner)
        if not rep["is_member"] or not rep["cofactors"]:
            # Reduction said 0 and the lift found nothing. Not a refutation of
            # the rewriting -- reduction DECIDES membership and it said yes --
            # so the verdict stands and the certificate does not.
            return DERIVED, why + (
                "\n  NO REPRESENTATION WAS RECOVERED, so this verdict rests on "
                "the reduction alone and cannot be rechecked without repeating "
                "it.")
        ok, expanded = cas.check_membership_representation(
            ring, target, gens, rep["cofactors"],
            characteristic=model.get("characteristic") or 0,
            timeout=timeout, _runner=_runner)
        if not ok:
            return UNVERIFIED, (
                "the reduction said (%s) - (%s) lies in %s's ideal, and "
                "expanding the cofactors the CAS returned for it gives a "
                "difference of %s rather than 0.\n"
                "  The search and the arithmetic disagree, and the arithmetic "
                "is the half a reader can check. Nothing is recorded until "
                "they agree."
                % (c["lhs"], c["rhs"], c.get("model"), expanded))
        witness = " + ".join("(%s)*(%s)" % (b, f)
                             for b, f in zip(rep["cofactors"], gens))
        return DERIVED, why + (
            "\n  (%s) - (%s) = %s, expanded and confirmed WITHOUT recomputing "
            "a basis. The derivation is now an artifact rather than a report "
            "of one." % (c["lhs"], c["rhs"], witness)), {
                "cofactors": list(rep["cofactors"]),
                "generators": list(gens), "ring_vars": list(ring),
                "target": target}
    # THE REFUTATION IS THE ONE ANSWER AN UNRECORDED IDEAL CANNOT SUPPORT.
    if unrecorded:
        return UNVERIFIED, (
            "(%s) - (%s) is not identically zero in the polynomial ring, and "
            "%s records no ideal -- so whether the rewriting holds modulo this "
            "model's equations CANNOT BE DECIDED HERE.\n"
            "  This is not a refutation and must not be reported as one. The "
            "model may well impose equations that make it true; nobody wrote "
            "them down. If the model genuinely imposes none -- an identity in "
            "the polynomial ring, an SOS Gram relation -- declare "
            "`generators: []` and the same question becomes answerable, and "
            "the answer will be AMBIENT."
            % (c["lhs"], c["rhs"], c.get("model")))
    # A REFUTATION AT AN OPEN MODEL IS THE ONE A READER WILL ARGUE WITH, so
    # answer the argument here instead of leaving them to make it.
    #
    # `localize` emits a model carrying the SAME ideal plus `open_conditions`:
    # the restriction is a condition on POINTS and adds no equations.  So a
    # rewriting that only becomes true once f is inverted really is false at
    # this model, and a reader who expected otherwise wanted the OTHER
    # construction -- the saturation, where "some power of f kills it into I"
    # is precisely what membership means.  Both readings are defensible; only
    # one of them is the model in front of them, and the message should say
    # which.  (lean/GrandPortage/Localization.lean separates the two.)
    opens = [str(o) for o in (model.get("open_conditions") or [])]
    hint = "" if not opens else (
        "\n  NOTE THAT %s IS AN OPEN LOCUS, carrying the condition%s %s. That "
        "restricts its POINTS and adds no equations -- its ideal is the "
        "source's, unchanged -- so inverting %s is not available here. If the "
        "rewriting holds only after inverting it, the model you want is the "
        "closure of that open locus, whose ideal is the saturation; an "
        "identity there is DERIVED and does not transport back."
        % (c.get("model"), "" if len(opens) == 1 else "s",
           ", ".join(opens), opens[0]))
    return REFUTED, (
        "(%s) - (%s) does not reduce to 0 %s -- it reduces to %s.\n"
        "  THIS ONE IS A REFUTATION, unlike a failed containment. %s So the "
        "rewriting is false where it was claimed, and every transport that "
        "carried it carried something untrue.%s"
        % (c["lhs"], c["rhs"], modulo,
           (evidence or {}).get("reduced_modulo_ideal", "a nonzero form"),
           ("The claim is that the difference is identically zero, and that "
            "is decided by normalising it." if bare else
            "The claim is that the difference lies in the ideal, and "
            "reduction modulo a Groebner basis DECIDES ideal membership."),
           hint))


ISO_VERIFIED = "VERIFIED"
ISO_NOT_ISO = "NOT_AN_ISOMORPHISM"


def ring_iso(graph, eid, timeout=300, _runner=None):
    """Check an EQUIVALENCE's `ring_iso` against the maps, by reduction.

    THE MOST POWERFUL UNAUDITED BOOLEAN LEFT.  `ring_iso` is what licenses an
    IDENTITY to cross an EQUIVALENCE in either direction, and the kernel's own
    warning is that the evidence usually offered for it is the wrong kind:
    V(x^2) and V(x) have the same single solution and any converse you like,
    and `x = 0` holds in one coordinate ring and is false in the other.  Points
    do not give it.

    WHAT TO CHECK CAME FROM THE FORMALISATION.  `Reflects` -- the awkward half
    -- quantifies over preimages, which is not something a CAS can search for.
    But it is not primitive:

        PullsBack psi I J  and  psi . phi = id   ==>   Reflects phi I J

    so a verified isomorphism is three things a solver CAN do:

        forward   every generator of I, substituted by phi, lies in J
        backward  every generator of J, substituted by psi, lies in I
        roundtrip psi(phi(x)) = x for each ring variable

    None of them is a search.  All three are reductions or substitutions, and
    `cas.classify_identity` already answers exactly that question.

    The edge must carry `forward` and `inverse` as substitutions for this to be
    askable; `check` reports when it declares `ring_iso` and does not.
    """
    e = graph.edges[eid]
    if e.get("type") != K.EQUIVALENCE:
        return UNVERIFIED, "edge %s is %s, not an EQUIVALENCE" % (
            eid, e.get("type"))
    fwd, inv = e.get("forward"), e.get("inverse")
    if not fwd or not inv:
        return UNVERIFIED, (
            "edge %s declares no `forward`/`inverse` substitutions, so there "
            "is nothing to reduce. `ring_iso` is a statement about the induced "
            "map on coordinate rings, and without the map it can only be "
            "taken on the author's word -- which is what it has been." % eid)
    src, dst = graph.models.get(e["src"]) or {}, graph.models.get(e["dst"]) or {}
    pending = _pending_ideal(e["src"], src) or _pending_ideal(e["dst"], dst)
    if pending:
        return UNVERIFIED, pending
    if src.get("generators") is None or dst.get("generators") is None:
        return UNVERIFIED, "one endpoint carries no ideal"
    ring = src.get("ring_vars") or []
    ch = src.get("characteristic") or 0
    if (dst.get("characteristic") or 0) != ch:
        return UNVERIFIED, (
            "the endpoints declare different characteristics (%s vs %s); a "
            "substitution between them is not a reduction in one ring"
            % (ch, dst.get("characteristic") or 0))
    if not ring or set(dst.get("ring_vars") or []) != set(ring):
        return UNVERIFIED, (
            "the two models are written in different rings; a substitution "
            "between them needs both variable lists to agree")

    # forward: each generator of I lands in J
    for g in src["generators"]:
        _, ok = cas.substitute_and_reduce(
            ring, g, fwd, list(dst["generators"]), characteristic=ch,
            timeout=timeout, _runner=_runner)
        if not ok:
            return ISO_NOT_ISO, (
                "generator %r of %s does not land in %s's ideal under the "
                "forward map. The map does not CARRY the ideal, so it is not "
                "an isomorphism of coordinate rings whatever it does to points."
                % (g, e["src"], e["dst"]))
    # backward: each generator of J pulls back into I
    for g in dst["generators"]:
        _, ok = cas.substitute_and_reduce(
            ring, g, inv, list(src["generators"]), characteristic=ch,
            timeout=timeout, _runner=_runner)
        if not ok:
            return ISO_NOT_ISO, (
                "generator %r of %s does not pull back into %s's ideal. "
                "Without that the map does not REFLECT, and an identity may "
                "cross one way and not the other -- which is the case "
                "`ring_iso` exists to exclude."
                % (g, e["dst"], e["src"]))
    # roundtrip: psi(phi(v)) = v for each variable
    for v in ring:
        once, _ = cas.substitute_and_reduce(ring, v, fwd, [],
                                            characteristic=ch,
                                            timeout=timeout, _runner=_runner)
        twice, _ = cas.substitute_and_reduce(ring, once, inv, [],
                                             characteristic=ch,
                                             timeout=timeout, _runner=_runner)
        if twice.replace(" ", "") != v:
            return ISO_NOT_ISO, (
                "the maps do not compose to the identity on %r, so `inverse` "
                "is not an inverse. Both ideal checks can pass for a map that "
                "is not invertible, and then only one direction is licensed."
                % v)
    return ISO_VERIFIED, (
        "the forward map carries %s's ideal into %s's, the inverse pulls it "
        "back, and the two compose to the identity on every variable. That is "
        "an isomorphism of COORDINATE RINGS, which is what an IDENTITY needs "
        "and what a bijection on points does not give."
        % (e["src"], e["dst"]))


WITNESS_VERIFIED = "VERIFIED"
WITNESS_REFUTED = "NOT_A_POINT"


def point_witness(graph, cid, timeout=300, _runner=None):
    """Substitute a NONEMPTY claim's exhibited point into its model's equations.

    THE CHEAPEST CHECK IN THE SYSTEM, WITH NO SURFACE FOR THREE RELEASES.
    `cas.check_witness` has existed and worked the whole time; nothing called
    it.  Two check rules and one kernel refusal all promise it by name -- "put
    it in `witness` and `cas_check_witness` will substitute it into the
    generators and tell you" -- and no code path ever did.  That is the fourth
    instance of a capability with no surface (`gp verify` itself, `ring_iso`,
    `unit_ideal`, this), and the gates do not catch it: GATE 3 asks whether a
    message names a command that does not exist, not whether a capability that
    exists is reachable.

    WHY IT MATTERS MORE THAN ITS COST SUGGESTS.  An EMPTY claim must name a
    certificate or the graph will not fold.  A NONEMPTY claim -- where the
    author is LITERALLY HOLDING THE OBJECT, the strongest evidence available
    anywhere in the system -- carried nothing checkable, so a fabricated point
    typed identically to a real one.  A live agent found that unprompted and
    said so plainly: "the graph cannot currently distinguish 'I have the point'
    from 'I claim to have the point'."

    And a REFUTED witness is a false NONEMPTY at its OWN MODEL, which no
    transport typing anywhere downstream would ever have surfaced -- the same
    shape as a REFUTED identity, and the reason both verifiers exist.

        VERIFIED     every generator vanishes at the point.
        NOT_A_POINT  one does not, and it is named with its value.
        UNVERIFIED   the question could not be put.

    STRUCTURED WITNESSES ONLY, via `witness_point`.  The prose `witness` field
    stays legal and stays unchecked -- 25 live records across four campaigns
    are strings like "(x, y) = (1, 2)" and "t = sqrt(3)" -- which is exactly
    the position IDENTITY was in before `lhs`/`rhs`.  The route out is the same
    one: record it structurally and it becomes a question a solver can answer.
    """
    c = graph.claims.get(cid)
    if not c:
        return UNVERIFIED, "no such claim"
    if c.get("kind") != K.NONEMPTY:
        return UNVERIFIED, "claim %s is %s, not a NONEMPTY" % (
            cid, c.get("kind"))
    point = c.get("witness_point")
    if not point:
        return UNVERIFIED, (
            "claim %s gives its point only in prose. `witness_point` -- a "
            "value for each ring variable -- is what makes it an arithmetic "
            "question rather than a reading question." % cid)
    model = graph.models.get(c.get("model")) or {}
    pending = _pending_ideal(c.get("model"), model)
    if pending:
        return UNVERIFIED, pending
    gens = list(model.get("generators") or [])
    if not gens:
        return UNVERIFIED, (
            "%s imposes no equations, so every point of the ambient space lies "
            "on it and there is nothing to substitute into. The claim may well "
            "be true; it is not this check that establishes it."
            % c.get("model"))
    ring = model.get("ring_vars") or c.get("ring_vars") or []
    if not ring:
        return UNVERIFIED, "neither %s nor claim %s declares ring variables" % (
            c.get("model"), cid)
    ok, evidence = cas.check_witness(
        ring, gens, point, characteristic=model.get("characteristic") or 0,
        timeout=timeout, _runner=_runner)
    shown = ", ".join("%s = %s" % (v, point[v]) for v in ring if v in point)
    if ok:
        return WITNESS_VERIFIED, (
            "every generator of %s's ideal vanishes at (%s), so the point is "
            "on the variety and the claim HOLDS AT ITS OWN MODEL. What that "
            "does not settle is where it may travel."
            % (c.get("model"), shown))
    failed = evidence["failed"]
    values = {g["generator"]: g["value"] for g in evidence["generators"]}
    return WITNESS_REFUTED, (
        "the point (%s) does not lie on %s: %s.\n"
        "  THIS ONE IS A REFUTATION. The claim is that the variety has a "
        "point and this is the point offered; substituting it is arithmetic "
        "and it does not vanish. So the NONEMPTY is unsupported at the model "
        "it was claimed at, and every transport that carried it carried "
        "something that was never established."
        % (shown, c.get("model"),
           "; ".join("%s evaluates to %s" % (g, values[g]) for g in failed)))


CERT_VERIFIED = "VERIFIED"
CERT_NOT_UNIT = "NOT_UNIT"


def unit_ideal(graph, cid, timeout=300, _runner=None):
    """Check an EMPTY claim's certificate against the computation, by expansion.

    THE LAST HONOUR-SYSTEM FIELD THAT CARRIES SCOPE, and the one that produced
    the erratum this whole project started from.

    `derive_scope` reads the certificate KIND to decide whether an emptiness
    survives a base change -- which was the fix for a declared `scope`, and
    moved the free choice one field along rather than removing it. Nothing
    relates the label `UNIT_IDEAL_CERT` to any computation. A caller who ran
    something, saw `1`, and typed the name gets the same scope as a caller who
    typed the name.

    WHAT MAKES THIS DIFFERENT FROM RE-RUNNING THE SEARCH.  The expensive step
    found cofactors `a_i` with `sum a_i f_i = 1`. Confirming that is one
    expansion -- no Buchberger, no monomial order, no trust in the search. The
    checker shares no code path with the thing it checks, which is the whole
    idea behind a certifying algorithm, and it is also the clean bridge to a
    proof assistant: Lean can check a polynomial identity and should never
    have to run a Groebner engine.

    Three verdicts:

        VERIFIED    cofactors found AND their expansion is 1
        NOT_UNIT    the ideal is not the unit ideal.  NOT a failed check --
                    the claim's certificate is simply not this one
        UNVERIFIED  the question could not be put
    """
    c = graph.claims.get(cid)
    if not c:
        return UNVERIFIED, "no such claim", None
    if c.get("kind") != K.EMPTY:
        return UNVERIFIED, "claim %s is %s, not EMPTY" % (cid, c.get("kind")), None
    # THIS VERIFIER ANSWERS ONE QUESTION AND IT IS NOT EVERY CLAIM'S QUESTION.
    #
    # It ran on ANY EMPTY claim carrying ANY certificate, and reported NOT_UNIT
    # -- "UNIT_IDEAL_CERT is not the certificate this claim has" -- about a
    # live claim that had never said it was. That claim declares
    # NONSQUARE_CLASS, and it is CORRECT: its ideal reduces to `t^2-3`, which
    # is exactly what a nonsquare-class argument looks like, empty over Q and
    # not over Q(sqrt 3).
    #
    # So the verifier refuted a certificate the author never claimed, and the
    # sentence it used to do it was already in the docstring above: NOT_UNIT
    # means "the claim's certificate is simply not this one", which only parses
    # if the claim said it was.
    #
    # Harmless while nothing read the verdict. The moment `check` began acting
    # on it, it became a false UNSOUND_PREMISE against a sound claim -- which
    # is how this was found, one command after wiring the two together.
    if c.get("certificate") != "UNIT_IDEAL_CERT":
        return UNVERIFIED, (
            "claim %s cites %s, and this verifier only decides "
            "UNIT_IDEAL_CERT. Expanding cofactors for `1` says nothing about "
            "whether a nonsquare class, a degree count or a cited theorem "
            "closes an emptiness; those are different arguments and want "
            "different checkers."
            % (cid, c.get("certificate") or "no certificate")), None
    model = graph.models.get(c.get("model")) or {}
    gens, ring = model.get("generators"), model.get("ring_vars")
    if not gens or not ring:
        return UNVERIFIED, (
            "model %s carries no ideal to expand -- a certificate about an "
            "ideal needs the ideal recorded, not only named"
            % c.get("model")), None

    ch = model.get("characteristic") or 0
    rep = cas.unit_ideal_representation(ring, list(gens), characteristic=ch,
                                        timeout=timeout, _runner=_runner)
    if not rep["is_unit"]:
        return CERT_NOT_UNIT, (
            "%s's ideal reduces to %s, not 1, so it is not the unit ideal and "
            "UNIT_IDEAL_CERT is not the certificate this claim has.\n"
            "  That is a statement about the CERTIFICATE and not about the "
            "emptiness: a model can be empty for other reasons, established by "
            "other means."
            % (c.get("model"), ", ".join(rep["basis"]))), None

    ok, expanded = cas.check_unit_ideal_representation(
        ring, list(gens), rep["cofactors"], characteristic=ch,
        timeout=timeout, _runner=_runner)
    witness = " + ".join("(%s)*(%s)" % (a, f)
                         for a, f in zip(rep["cofactors"], gens))
    if not ok:
        return CERT_NOT_UNIT, (
            "the CAS returned cofactors for %s, and expanding them gives %s "
            "rather than 1.\n"
            "  This is the case the expansion exists to catch: the search said "
            "one thing and the arithmetic says another, and the arithmetic is "
            "the half a reader can check."
            % (c.get("model"), expanded), None)

    return CERT_VERIFIED, (
        "1 = %s, expanded and confirmed WITHOUT recomputing a basis. The "
        "certificate is now a computation rather than a name."
        % witness), {"cofactors": list(rep["cofactors"]),
                     "generators": list(gens), "ring_vars": list(ring)}


def _verdict_event(subject, of, verdict, why, representation=None):
    # Content-addressed id, so re-verifying an unchanged thing with an
    # unchanged answer is an IDEMPOTENT redeclaration and the fold absorbs it.
    # Re-verifying after something changed produces a different id and both
    # verdicts stay in the log, which is what makes `gp history` able to show
    # that the answer moved.
    digest = hashlib.sha1(
        ("%s|%s|%s|%s" % (subject, of, verdict, why)).encode("utf-8")
    ).hexdigest()[:12]
    ev = {"ev": S.EV_VERDICT, "id": "v.%s.%s" % (of, digest),
          "subject": subject, "of": of, "verdict": verdict, "why": why}
    if representation:
        ev["representation"] = representation
    return ev


def verify_all(root=".", timeout=300, _runner=None, record=True):
    """Verify every checkable edge AND claim, and RECORD the answers.

    RECORDING WAS THE STATED POINT AND DID NOT HAPPEN.  This function's own
    docstring promised the results were "appended as a supersession of the
    edge, so the log stays append-only and `gp history` shows that the check
    happened".  A live session measured it: the graph file was byte-identical
    before and after, and there was no `append` anywhere in the module.  It
    also iterated edges only, so the claim half had no batch entry point at
    all.  Both are fixed here.

    The answers go in as `verdict` events rather than as supersessions of the
    thing verified.  A supersession says the record CHANGED; a verdict says
    somebody CHECKED it, and the claim itself is untouched by having been
    examined.  Conflating those would make `gp history` report every
    verification as an amendment to the mathematics.

    Recording is the point.  A verification that lives in a terminal scrollback
    is a verification nobody can act on next week, and this project's whole
    claim is that the graph is the state.
    """
    path = S.graph_path(root)
    graph = S.load(path)
    results, events = [], []

    def run(subject, oid, fn):
        """One object, and a failure here must not cost the other twenty.

        A live campaign lost a whole run to this: one claim naming a symbol
        the ring did not have raised out of `classify_identity`, the batch
        aborted, `S.append` never ran, and FOUR CLAIMS AND TWELVE EDGES that
        had already verified were discarded.  `gp check` had reported that
        exact claim politely one command earlier.
        """
        rep = None
        try:
            out = fn()
        except cas.CASError as exc:
            verdict, why = UNVERIFIED, (
                "the CAS could not answer for this object, and the rest of the "
                "run continued:\n  %s" % exc)
        else:
            verdict, why = out[0], out[1]
            # THE CERTIFICATE, IF THE VERIFIER MINTED ONE -- and this line is
            # why it now survives.  `unit_ideal` has returned cofactors as a
            # third element since it was written, and the call site sliced them
            # off with `[:2]`. So the expensive part ran, the representation
            # was built, the expansion confirmed it, and the graph kept only
            # the word VERIFIED. The one artifact a reader could have rechecked
            # without trusting the search was computed and dropped.
            rep = out[2] if len(out) > 2 else None
        results.append((subject, oid, verdict, why))
        events.append(_verdict_event(subject, oid, verdict, why, rep))

    for eid in sorted(graph.edges):
        e = graph.edges[eid]
        # SUPERSEDED RECORDS ARE NOT IN THE GRAPH as far as `check` is
        # concerned, and `verify` disagreed -- it filtered only on the verdict
        # field.  So a claim corrected by supersession kept being re-verified,
        # and kept re-raising the error that had motivated the correction.
        if e.get("superseded_by"):
            continue
        src, dst = graph.models.get(e["src"]), graph.models.get(e["dst"])
        if not src or not dst:
            continue
        if (not e.get("containment")
                and src.get("generators") is not None
                and dst.get("generators") is not None):
            run("edge", eid, lambda eid=eid: containment(
                graph, eid, timeout=timeout, _runner=_runner))
        # RING_ISO HAD NO SURFACE AT ALL.  It worked, it caught a planted
        # false EQUIVALENCE in a live campaign, and it was reachable only by
        # importing the module from Python -- the same defect `gp verify`
        # itself had two days earlier.
        if (e.get("type") == K.EQUIVALENCE and e.get("ring_iso")
                and e.get("forward") and not e.get("ring_iso_verdict")):
            run("ring_iso", eid, lambda eid=eid: ring_iso(
                graph, eid, timeout=timeout, _runner=_runner))

    for cid in sorted(graph.claims):
        c = graph.claims[cid]
        if c.get("superseded_by"):
            continue
        if (c.get("kind") == K.IDENTITY and not c.get("identity_verdict")
                and c.get("lhs") is not None and c.get("rhs") is not None):
            # Silent where the rewriting was never recorded.  An unstructured
            # IDENTITY is not a failed verification, it is an unasked
            # question, and `check` reports that hole.
            run("claim", cid, lambda cid=cid: identity(
                graph, cid, timeout=timeout, _runner=_runner))
        # ONLY the kind this verifier decides. Running it on every certificate
        # spent a solver call to produce a refutation of something nobody
        # claimed.
        if (c.get("kind") == K.EMPTY
                and c.get("certificate") == "UNIT_IDEAL_CERT"
                and not c.get("certificate_verdict")):
            # NO `[:2]` -- that slice is what threw the cofactors away.
            run("certificate", cid,
                lambda cid=cid: unit_ideal(graph, cid, timeout=timeout,
                                           _runner=_runner))
        # THE OTHER HALF OF THE EXISTENCE STORY, and the last of the four
        # capabilities that worked and could not be reached.  Silent on a prose
        # witness for the same reason as an unstructured IDENTITY: that is an
        # unasked question, not a failed one, and `check` is where the hole
        # gets reported.
        if (c.get("kind") == K.NONEMPTY and c.get("witness_point")
                and not c.get("witness_verdict")):
            run("witness", cid, lambda cid=cid: point_witness(
                graph, cid, timeout=timeout, _runner=_runner))

    if record and events:
        # ROOT, not the graph path.  `append` resolves `.portage/graph.jsonl`
        # itself, so passing the resolved path built
        # `.portage/graph.jsonl/.portage` and crashed -- on the ONE line the
        # suite never reached, because every test called `verify_all` with
        # `record=False` or a fixture that produced no events.
        S.append(events, root)
    return results
