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
