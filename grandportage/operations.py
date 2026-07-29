"""Structured operations: the program and the transport relation from one value.

THE POINT IS NOT ACCURACY.  Experiment B measured hand-declared relation types
across 57 live edges and found them 88% correct, with most of the remaining
errors in places no constructor can reach -- five of thirteen were edges where
NO OPERATION HAPPENED and the author correctly determined that nothing relates
the two models.  So "callers get the type wrong" does not, on its own, pay for
this layer.

What pays for it is that the caller stops writing the same thing twice.  A
constructor takes what the mathematician already knows -- which variables,
which polynomial -- and derives the target model, the edge, the CAS program and
the verification plan from it.  Typing becomes the thing that saves work rather
than the tax you pay afterwards.

WHY THESE THREE AND NOT SIXTEEN.  Experiment B named them:

    Localize / SaturateClosure   the two that actually got confused, with
                                 NECESSARY_CONDITION and with each other
    Eliminate                    zero observed mislabels, worst consequence
                                 when wrong

`AddEquations` and `DropEquations` have 27 live instances and zero mislabels.
The caller gets those right every time, so a constructor there buys nothing and
was not built.

THE DISTINCTION THAT MOTIVATED THE FIRST TWO, stated once because getting it
wrong is what the corpus shows people do:

    Localize(I, f)          the OPEN locus D(f): THE SAME IDEAL, with a
                            condition on POINTS.  Its points are points of
                            V(I) with f != 0, so going back to V(I) DROPS AN
                            INEQUALITY and no equation.
                            -> RESTRICTION

    SaturateClosure(I, f)   the CLOSURE of that open locus, back in the
                            ambient space.  I : f^oo contains I, so the
                            saturated model is cut by MORE EQUATIONS, and
                            going back to V(I) drops them.
                            -> NECESSARY_CONDITION

Same input, same intuition ("the part where f is nonzero"), two different
models and two different edge types.  A live campaign typed both as
NECESSARY_CONDITION; one of those was right by accident.
"""

from . import cas
from . import kernel as K

# What each constructor emits as its transport relation.  Written as a table so
# the derivation is inspectable rather than buried in three functions -- the
# whole claim of this module is that the type is DERIVED, and a reader should
# be able to check that claim without reading the code that acts on it.
DERIVES = {
    "Localize": (K.RESTRICTION,
                 "the open locus D(f) is cut out by the same ideal together "
                 "with a condition on points, so returning to the ambient "
                 "model drops the inequality f != 0 and no equation"),
    "SaturateClosure": (K.NECESSARY_CONDITION,
                        "I : f^oo contains I, so the saturated model is cut "
                        "by more equations; returning to the ambient model "
                        "drops them"),
    "Decompose": (K.NECESSARY_CONDITION,
                  "a component of a factorizing decomposition carries the "
                  "parent's equations and more, so returning to the parent "
                  "drops the equations that single this piece out"),
    "Eliminate": (K.IMAGE_CLOSURE,
                  "elimination returns the ideal of the ZARISKI CLOSURE of "
                  "the projection, which is not the image: a point of the "
                  "closure need not lift"),
}


class Operation(object):
    """What a constructor returns: events, a program, and what to verify.

    Deliberately a plain value.  It is not applied to a graph here, because a
    tool that both decides a relation and writes it leaves nobody holding the
    claim -- the same reason `cas.classify_identity` touches the graph not at
    all.  The caller sends `events` through the ordinary write path, where
    every existing guard still applies.
    """

    __slots__ = ("kind", "events", "program", "verify_hint", "derivation")

    def __init__(self, kind, events, program, verify_hint, derivation):
        self.kind = kind
        self.events = events
        self.program = program
        self.verify_hint = verify_hint
        self.derivation = derivation


def execute(op, timeout=300, _runner=None):
    """Run a pending constructor program and return completed events.

    Saturation and elimination cannot know their target ideal before the CAS
    answers. Their constructors therefore emit `ideal_pending`; this function
    turns that pending value into generators before anything is written. It
    returns another plain Operation, preserving the rule that construction and
    graph mutation are separate decisions.
    """
    if op.kind not in ("SaturateClosure", "Eliminate"):
        return op
    result = (_runner or cas._run_subprocess)(op.program, timeout)
    if result["aborted"]:
        raise cas.CASError("the %s operation aborted: %s"
                           % (op.kind, result.get("abort_reason") or "unknown"))
    if result["returncode"] != 0:
        raise cas.CASError("the %s operation exited %s:\n%s"
                           % (op.kind, result["returncode"],
                              result["stderr"][-1500:]))
    if "? error" in result["stdout"] + result["stderr"]:
        raise cas.CASError("the %s operation reported a CAS error:\n%s"
                           % (op.kind, result["stdout"][-1500:]))
    values = cas._parse_outputs(result["stdout"], op.program.outputs)
    raw = values[op.program.outputs[0]]
    rows = raw if isinstance(raw, list) else [raw]
    generators = [row.split("=", 1)[-1].strip() for row in rows]
    generators = [g for g in generators if g and g != "0"]

    events = [dict(ev) for ev in op.events]
    pending = [ev for ev in events
               if ev.get("ev") == "model" and ev.get("ideal_pending")]
    if len(pending) != 1:
        raise cas.CASError(
            "%s expected exactly one pending model, found %d"
            % (op.kind, len(pending)))
    pending[0].pop("ideal_pending")
    pending[0]["generators"] = generators
    return Operation(
        op.kind, events, op.program,
        "the computed ideal is recorded; run `gp verify` to check the edge's "
        "containment and operation output independently",
        op.derivation)


def _ideal(generators):
    """An ideal declaration that survives having no generators.

    `",".join([])` is the empty string, so an empty ideal emitted
    `ideal GP_I = ;` -- a syntax error.  And the empty case is not exotic: it
    is the AMBIENT SPACE, which is exactly the motivating use of `localize`.
    "The smooth locus of the parameter plane" is the plane itself with an
    inequality, and a live campaign hit that on its first try.
    """
    return ",".join(generators) if generators else "0"


def _model(mid, what, ring_vars, generators, **extra):
    """`generators=None` means the ideal is COMPUTED, not that there is none.

    The distinction is carried by omitting the key rather than by an empty
    list, because an empty list is a real and different model -- the ambient
    space -- and `_ideal` above exists precisely to emit it.  A caller passing
    None should pass `ideal_pending` as well, saying what will fill it.  That
    is not enforced in the store: most models in a real graph carry no algebra
    at all, and refusing them would be a much larger change than this.  What
    IS enforced there is that the two are not declared together.
    """
    ev = {"ev": "model", "id": mid, "what": what,
          "ring_vars": list(ring_vars)}
    if generators is not None:
        ev["generators"] = list(generators)
    ev.update(extra)
    return ev


def _edge(eid, src, dst, kind, why_extra=""):
    etype, why = DERIVES[kind]
    return {"ev": "edge", "id": eid, "src": src, "dst": dst, "type": etype,
            "map_kind": (K.IDENTITY_MAP if etype == K.RESTRICTION
                         else K.POLYNOMIAL),
            "why": (why + ("  " + why_extra if why_extra else "")),
            "built_by_operation": kind}


def localize(src, f, produces, ring_vars, generators, characteristic=0):
    """The open locus where `f` does not vanish -- SAME IDEAL, fewer points.

    Emits a RESTRICTION, because the ideal does not change: only the
    inequality does.  `map_kind` is IDENTITY_MAP for the same reason -- a
    restriction changes no coordinates, so there is no substitution that
    could introduce a denominator.

    THE PROSE HERE USED TO SAY "with f inverted", WHICH IS A DIFFERENT
    CONSTRUCTION FROM THE ONE THE CODE PERFORMS.  Two readings of "restrict to
    where f is nonzero" were written a day apart and never reconciled:

        (a) the same ring and ideal, with an open condition on POINTS
        (b) the localized algebra A_f, a genuinely different coordinate ring

    This function has always emitted (a) -- `generators` is copied across
    untouched, three lines below -- while describing itself as (b).  The
    difference is not cosmetic: `lean/GrandPortage/Localization.lean` exhibits
    an element zero in the localization and nonzero in the ring (`3` at `2`
    modulo `(6)`; in polynomials, `y` in `k[x,y]/(xy)` localized at `x`), so
    under (b) an IDENTITY here would NOT transport back to the source and the
    unconditional RESTRICTION/ALONG/IDENTITY cell would need a gate.

    (a) is also the reading the rest of the system is built on.  Every one of
    RESTRICTION's six point-cells is an instance of one generic theorem about
    `Refines` between two models over a COMMON point set; reading (b) changes
    the ring, so the two ends stop being comparable that way and the whole
    column would have to be re-earned rather than inherited.

    If you want (b), you want `saturate_closure`: `I : f^oo` is exactly the set
    of things some power of `f` kills into `I`, which is exactly what becomes
    zero in `A_f`.  It emits NECESSARY_CONDITION, and an identity there is
    DERIVED -- which the kernel already refuses to transport ALONG.  The two
    constructors were always the two readings.
    """
    ev_model = _model(
        produces,
        "the open locus of %s where %s does not vanish -- the same equations, "
        "restricted to the points where %s is invertible" % (src, f, f),
        ring_vars, generators, open_conditions=[f])
    ev_edge = _edge("E-%s" % produces, produces, src, "Localize",
                    "The dropped condition is %s != 0." % f)
    prog = cas.CASProgram(
        cas.SINGULAR, ring="GP_R", ring_vars=list(ring_vars),
        decls=[("GP_I", "ideal", _ideal(generators)),
               ("GP_S", "ideal", "std(GP_I)")],
        body=[], outputs=["GP_S"], characteristic=characteristic)
    return Operation(
        "Localize", [ev_model, ev_edge], prog,
        "nothing to reduce: the ideal is unchanged by localisation, and the "
        "open condition is not an ideal-membership question",
        DERIVES["Localize"][1])


def saturate_closure(src, f, produces, ring_vars, generators,
                     characteristic=0):
    """The CLOSURE of the open locus, back in the ambient space.

    Emits a NECESSARY_CONDITION, because `I : f^oo` contains `I` -- the
    saturated model carries more equations, so returning to the source drops
    them.  This is the constructor that a live campaign conflated with
    `localize`, and the two produce different edge types from the same words.

    IT IS ALSO THE ONE THAT MEANS "f INVERTED".  `I : f^oo` is exactly the set
    of elements some power of `f` carries into `I`, which is exactly what dies
    in the localized algebra `A_f`.  So the reading `localize` used to CLAIM
    is the reading this function DELIVERS -- and delivers soundly, because an
    identity here is DERIVED and NECESSARY_CONDITION/ALONG/IDENTITY refuses to
    transport a DERIVED rewriting back.  No new gate was needed; the two
    constructors were always the two readings.
    """
    ev_model = _model(
        produces,
        "the Zariski closure of the part of %s where %s does not vanish"
        % (src, f),
        ring_vars, None,
        saturated_at=f,
        ideal_pending="the saturation %s : %s^oo, which is what this "
                      "operation's program computes" % (src, f))
    ev_edge = _edge("E-%s" % produces, produces, src, "SaturateClosure",
                    "Saturating at %s removes the components lying inside "
                    "V(%s)." % (f, f))
    # SATURATION BY ELIMINATION, because `sat` LIVES IN A LIBRARY THIS BOUNDARY
    # WILL NOT LOAD.
    #
    # The first version emitted `sat(GP_I,GP_F)[1]`, which Singular answers
    # with "`int` expected while building `sat(`" -- the symbol is in
    # `elim.lib`, and `LIB` is in the dialect's FORBIDDEN set precisely so no
    # program can pull in arbitrary code.  So this constructor could never have
    # run, and a live campaign found that by trying to use it.
    #
    # I tested `eliminate` against a real solver and did not test this one.
    # The identity below needs no library:
    #
    #     I : f^oo  =  (I + (1 - t*f)) ∩ R,  eliminating t
    #
    # Verified against Singular on cases with known answers -- sat((xy), x) = (y)
    # and sat((x^2y, xy^2), x) = (y) -- before being trusted here.
    tvar = "GP_T"
    prog = cas.CASProgram(
        cas.SINGULAR, ring="GP_R", ring_vars=[tvar] + list(ring_vars),
        decls=[("GP_I", "ideal",
                _ideal(list(generators) + ["1-%s*(%s)" % (tvar, f)])),
               ("GP_E", "ideal", "eliminate(GP_I,%s)" % tvar),
               ("GP_OUT", "ideal", "std(GP_E)")],
        body=[], outputs=["GP_OUT"], characteristic=characteristic)
    return Operation(
        "SaturateClosure", [ev_model, ev_edge], prog,
        "the target's generators come back from the run; once recorded, "
        "`gp verify` can check I(src) inside I(dst) by reduction",
        DERIVES["SaturateClosure"][1])


def decompose(src, ring_vars, generators, produces="%s_C%d",
              characteristic=0, timeout=300, _runner=None):
    """Split a model into a COVER of simpler pieces, with the cover proved.

    THE ONE CONSTRUCTOR THAT MUST RUN THE CAS TO KNOW WHAT IT EMITS.  The other
    three know their target before any computation: a localisation keeps the
    ideal, a saturation and an elimination each produce exactly one model whose
    generators arrive later.  A decomposition does not even know HOW MANY
    models it makes until `facstd` answers.

    That does not breach this module's rule.  The rule is that a constructor
    does not WRITE -- "a tool that both decides a relation and writes it leaves
    nobody holding the claim" -- and this one still returns plain events for
    the caller to send through the ordinary path.  `cas.classify_identity` runs
    a solver and touches no graph for the same reason.

    IT ALSO EMITS ITS OWN COMPLETENESS PREMISE, which no other constructor
    does, and that is the point of building it now rather than earlier.  A
    partition needs an `exhaustive` claim or the graph will not fold, and until
    `verify.partition_exhaustiveness` existed that claim was prose. Here it is
    a claim a verifier DECIDES -- and for a minted cover it decides VERIFIED by
    construction, because `facstd` guarantees `V(I) = union V(I_j)`.

    So the events are: one model per piece CARRYING ITS OWN IDEAL, one
    NECESSARY_CONDITION per piece pointing back at the parent, the
    completeness claim, and the partition binding them.

    AN IDEAL THAT DOES NOT FACTOR RETURNS NO EVENTS AT ALL.  Check for that --
    it is a common answer rather than a failure, and the alternative was a
    one-branch partition the store correctly refuses.  It is also NOT a proof
    of irreducibility: `facstd` gives a cover, and nothing inside this boundary
    decides primality.
    """
    pieces = cas.factorizing_decomposition(
        ring_vars, generators, characteristic=characteristic,
        timeout=timeout, _runner=_runner)
    prog = cas.CASProgram(
        cas.SINGULAR, ring="GP_R", ring_vars=list(ring_vars),
        decls=[("GP_I", "ideal", _ideal(generators)),
               ("GP_L", "list", "facstd(GP_I)")],
        body=[], outputs=["GP_L"], characteristic=characteristic)
    # ONE PIECE IS NOT A DECOMPOSITION, and the store says so better than this
    # comment could: "a split into one piece is just the parent". Emitting a
    # component model identical to the parent plus an edge from it to itself
    # would be noise carrying a partition the graph correctly refuses.
    #
    # `events` is EMPTY here, deliberately, and a caller must check for that.
    # "This ideal does not factor" is a real answer and a common one -- an
    # irreducible curve gives it every time -- so it is neither an error nor
    # something to paper over with a one-branch partition.
    if len(pieces) < 2:
        return Operation(
            "Decompose", [], prog,
            "nothing to verify: no events were emitted",
            "%s's ideal did not factor, so there is no case analysis to make. "
            "That is a statement about what `facstd` could split, NOT a proof "
            "of irreducibility -- a cover is not a primary decomposition, and "
            "nothing inside this CAS boundary can decide primality." % src)
    ids = [produces % (src, i) if "%" in produces else "%s%d" % (produces, i)
           for i in range(len(pieces))]
    events = []
    for bid, gens in zip(ids, pieces):
        events.append(_model(
            bid, "the component of %s cut out by %s" % (src, ", ".join(gens)),
            ring_vars, gens, component_of=src))
        events.append(_edge("E-%s" % bid, bid, src, "Decompose",
                            "This piece adds %s." % ", ".join(gens)))
    cover = "CL-%s-COVER" % src
    events.append({
        "ev": "claim", "id": cover, "model": src, "kind": K.PREDICATE,
        "statement": ("every point of %s lies on one of the %d components "
                      "%s" % (src, len(ids), ", ".join(ids))),
        # RAN, not READ: `facstd` computed this and `gp verify` re-decides it.
        "established_by": "RAN", "ladder": "exact-checked"})
    events.append({
        "ev": "partition", "id": "P-%s" % src, "parent": src,
        "branches": list(ids), "exhaustive": cover,
        "why": "a factorizing decomposition of %s's ideal" % src})
    return Operation(
        "Decompose", events, prog,
        "`gp verify` re-decides the cover from the recorded ideals, by "
        "intersecting the components and testing radical membership against "
        "the parent -- so the completeness premise is checked rather than "
        "taken from the tool that produced it",
        DERIVES["Decompose"][1])


def eliminate(src, variables, produces, ring_vars, generators,
              characteristic=0):
    """Project away `variables`; what comes back is the CLOSURE of the image.

    THE CELL WHERE BEING WRONG COSTS MOST, which is why it is here despite
    zero observed mislabels in the corpus.  The hyperbola shows it in one
    line: eliminating `y` from `xy = 1` gives the zero ideal, so the closure
    is all of `A^1`, and `x = 0` is a point of the closure with no preimage.
    The CAS is right; the unsupported step is reading the closure as the
    image.

    The emitted edge is IMAGE_CLOSURE, whose AGAINST/NONEMPTY cell refuses a
    witness precisely so that reading cannot happen silently.
    """
    remaining = [v for v in ring_vars if v not in set(variables)]
    if not remaining:
        raise ValueError(
            "eliminating %s leaves no variables; there is no target model to "
            "project onto" % ", ".join(variables))
    ev_model = _model(
        produces,
        "the Zariski closure of the image of %s after eliminating %s"
        % (src, ", ".join(variables)),
        remaining, None,
        eliminated=list(variables),
        ideal_pending="the elimination ideal of %s after removing %s, which "
                      "is what this operation's program computes"
                      % (src, ", ".join(variables)))
    ev_edge = _edge("E-%s" % produces, src, produces, "Eliminate",
                    "Eliminated: %s." % ", ".join(variables))
    prog = cas.CASProgram(
        cas.SINGULAR, ring="GP_R", ring_vars=list(ring_vars),
        decls=[("GP_I", "ideal", _ideal(generators)),
               ("GP_E", "ideal",
                "eliminate(GP_I,%s)" % "*".join(variables)),
               ("GP_OUT", "ideal", "std(GP_E)")],
        body=[], outputs=["GP_OUT"], characteristic=characteristic)
    return Operation(
        "Eliminate", [ev_model, ev_edge], prog,
        "a NONEMPTY at the target does NOT give a witness at the source; if "
        "you need one, exhibit a lift explicitly",
        DERIVES["Eliminate"][1])
