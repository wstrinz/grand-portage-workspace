"""Discharge moves: from a refused edge to a named work item.

This is the part that makes a campaign drive itself, and it is worth being
precise about how little intelligence is involved.  It is a lookup table.

A typed failure is localized and named: "edge E8 is BASE_EXTENSION and the
emptiness it carries has a field-relative certificate" is not a vague sense
that something is off, it is a work item with an address.  Each table cell has
a canonical next move, so the loop is:

    compute -> type the step -> checker localizes the refusal ->
    look up the move -> dispatch -> repeat

That is a work queue derived from a type error, which is how a build system
with autofix behaves.  What makes it work is that the failure is specific
enough to name the move; vague failures do not generate work.

The honest limit, and it should be read every time this module is quoted: THIS
ROUTES ATTENTION TO WHERE AN EQUATION IS MISSING.  IT DOES NOT FIND THE
EQUATION.  Every actual advance in the source campaign was an equation, and the
only claim here is that a typed graph shortens the search for which one.
"""

from . import kernel as K

_GENERIC = ("Re-examine this step: the transport it needs is not licensed by "
            "the type it was given.  Either the type is wrong (prove the "
            "stronger relation) or the step is wrong (do not take it).")

# (edge type, direction, claim kind) -> the canonical next move.
MOVES = {
    (K.BASE_EXTENSION, K.ALONG, K.EMPTY): (
        "Produce a certificate that BASE-CHANGES -- exhibit 1 in the ideal over "
        "the base field, or a resultant nonzero in the base field -- and the "
        "emptiness transports unchanged.  If no such certificate exists, the "
        "claim is a fact about {src_field} only: restate it at that scope and "
        "stop consuming it as geometric emptiness.  Check whether the target "
        "model has points over the larger field before spending anything: if "
        "it does, the conclusion is not merely unproved, it is false."),
    (K.BASE_EXTENSION, K.AGAINST, K.NONEMPTY): (
        "A point over the larger field need not descend.  Exhibit a point with "
        "coordinates in the smaller field, or accept the witness as a statement "
        "about the larger field alone.  If descent is what you need, the "
        "obstruction is usually a square class or a Galois cocycle -- name it."),
    (K.BASE_EXTENSION, K.ALONG, K.PREDICATE): (
        "A predicate proved over the small field need not hold over the "
        "extension.  Re-derive it over the extension, or show it is defined by "
        "equations with coefficients in the base and is stable under the "
        "Galois action."),

    (K.NECESSARY_CONDITION, K.ALONG, K.PREDICATE): (
        "The predicate holds in the tighter model; you are importing it into "
        "the looser one.  Either re-derive it in the target model from that "
        "model's own equations, or exhibit the converse and retype the edge "
        "EQUIVALENCE.  Until one of those, the predicate is a fact about "
        "{src} and every conclusion drawn from it in {dst} is unsound."),
    (K.NECESSARY_CONDITION, K.AGAINST, K.NONEMPTY): (
        "The witness lives in the relaxation, not in the source.  Lift it to "
        "{dst} explicitly -- that means satisfying the conditions the edge "
        "DROPS ({drops}) -- or read it as what it soundly is: a hard stop on "
        "emptiness spend for {src} and nothing more."),
    (K.NECESSARY_CONDITION, K.ALONG, K.EMPTY): (
        "Emptiness of the tighter model says nothing about the looser one; the "
        "looser model is where the counterexamples would live.  If you need "
        "{dst} closed, find an equation that holds in {dst}."),

    (K.IMAGE_CLOSURE, K.AGAINST, K.NONEMPTY): (
        "ARTIFACT-CANDIDATE, not a solver-time problem.  A point of the "
        "Zariski closure need not lift to the image (Chevalley).  Either "
        "exhibit a lift, or refine the model by the open conditions that cut "
        "the constructible image out of its closure.  Do not buy more solver "
        "time for this cell: no monomial order and no amount of RAM can turn "
        "a closure point into a preimage."),
    (K.IMAGE_CLOSURE, K.ALONG, K.PREDICATE): (
        "Only Zariski-CLOSED conditions extend from an image to its closure.  "
        "Show the predicate is closed (it is cut out by equations, with no "
        "strict inequality and no nonvanishing side condition) and declare it "
        "so, or restrict the conclusion to the image itself."),

    (K.IMAGE_CLOSURE, K.ALONG, K.EMPTY): (
        "The kernel refuses this cell generically, from V(src) subset V(dst) "
        "alone.  See KNOWN_CONSERVATISM: closure of the empty set is empty, so "
        "the step is in fact sound and this is a deliberate false refusal on an "
        "unreachable cell.  If you have genuinely computed the constructible "
        "image and found it empty, record it as a note and override."),

    (K.SPECIALIZATION, K.ALONG, K.EMPTY): None,     # filled below
    (K.SPECIALIZATION, K.AGAINST, K.EMPTY): None,
    (K.SPECIALIZATION, K.ALONG, K.NONEMPTY): None,
    (K.SPECIALIZATION, K.AGAINST, K.NONEMPTY): None,
    (K.SPECIALIZATION, K.ALONG, K.PREDICATE): None,
    (K.SPECIALIZATION, K.AGAINST, K.PREDICATE): None,
}

_SPECIALIZATION_MOVE = (
    "NO relaxation type carries an existence statement across a change of "
    "characteristic, and that is a theorem, not a gap in this table: Fano is "
    "empty over Q and nonempty over F_2, non-Fano is the reverse, so all four "
    "existence cells have explicit counterexamples.  Redo the computation in "
    "the target characteristic, or produce a good-reduction / flatness "
    "argument at this prime that makes the step an EQUIVALENCE.  A mod-p run "
    "is RECONNAISSANCE: it may direct effort, it may never close a case.")

for _key in list(MOVES):
    if MOVES[_key] is None:
        MOVES[_key] = _SPECIALIZATION_MOVE

_IDENTITY_MOVE = (
    "Rewriting a dictionary across this edge needs a DENOMINATOR-FREE map, and "
    "this edge's map is {map_kind}.  Either exhibit the rewriting as a "
    "polynomial transform (in the source campaign the row transform was "
    "polynomial and that single attribute separated the sound leg from the "
    "unsound one), or clear denominators and record what that costs.")

# Rule-level moves, for findings that are not a transport refusal.
RULE_MOVES = {
    "TAINT": (
        "This model was BUILT by a step the type system refuses, so every "
        "conclusion drawn inside it is suspect even where its own transport is "
        "licensed.  Discharge the building inference first -- that is the only "
        "repair.  Re-deriving the downstream claims in an untainted model is "
        "the fallback, and it is a full redo, not a patch."),
    "COVERAGE": (
        "Declare a component on axis {axis} at {missing}, or state positively "
        "that the model imposes nothing there and accept that conclusions read "
        "at those indices are unbounded.  Look first at what the model already "
        "imposes and reads there -- the missing condition is usually visible in "
        "the divisor of a gauge the model uses but does not constrain."),
    "REFINEMENT-TYPE": (
        "A refinement (src = dst + equations) is a NECESSARY_CONDITION edge "
        "read AGAINST the arrow.  Retype it, or -- if it is genuinely not a "
        "refinement -- drop the `refinement` flag and say what the step really "
        "does."),
    K.UNTYPED: (
        "Name the relaxation.  What does this step LOSE?  Nothing -> "
        "EQUIVALENCE (and you must be able to exhibit the converse).  "
        "Equations -> NECESSARY_CONDITION.  A larger coefficient field -> "
        "BASE_EXTENSION.  An elimination or a projection -> IMAGE_CLOSURE.  "
        "A change of characteristic -> SPECIALIZATION.  Until it is named, no "
        "conclusion crosses this edge."),
}

# The discharge for TRAFFIC over an untyped edge, as opposed to the untyped
# edge itself.
#
# The first version offered only "name the relaxation", and a first-time user
# pointed out that this is THE ONE EXIT THAT IS CLOSED BY CONSTRUCTION: if they
# could name the relaxation there would be no obligation to record.  They were
# doing something the design intends -- recording a residual obligation AS a
# type error, which is exactly the shape of the four obligations already in
# their graph -- and the tool answered with a wall whose only signposted door
# was locked.
#
# So both moves are named.  The order matters: typing it is still the real
# repair, and accepting is explicitly framed as carrying a debt in the open
# rather than as making a warning go away.
_UNTYPED_TRAFFIC_MOVE = (
    "You have drawn a conclusion across a step whose relaxation is not named, "
    "so nothing licenses it.  TWO legitimate moves:\n"
    "  (1) TYPE THE EDGE, if you can.  What does {src} -> {dst} LOSE?  "
    "Nothing (converse exhibitable) -> EQUIVALENCE.  Equations -> "
    "NECESSARY_CONDITION.  A larger field -> BASE_EXTENSION.  An elimination "
    "or projection -> IMAGE_CLOSURE.  A change of characteristic -> "
    "SPECIALIZATION.  Getting the DIRECTION right is part of this and is a "
    "real claim about which model holds more information.\n"
    "  (2) CARRY IT DELIBERATELY.  If the point of recording this was to put a "
    "residual obligation ON THE RECORD as a type error -- a legitimate and "
    "intended use -- accept it with a reason:\n"
    "        gp accept --only {fid} -m \"<why it cannot be typed yet>\"\n"
    "      It stops blocking, stays visible in `gp check` forever, and the "
    "reason lands in a file a reviewer reads.  This is carrying a debt in the "
    "open, NOT clearing it.\n"
    "  The edge already records why it is untyped: {debt_why}")

# Cells where the kernel is knowingly stricter than the mathematics, kept as
# data so that "we refuse this soundly" and "we refuse this out of caution" are
# never confused, and so that removing one is a deliberate act.
KNOWN_CONSERVATISM = [
    {
        "cell": (K.IMAGE_CLOSURE, K.ALONG, K.EMPTY),
        "kernel_says": False,
        "truth": "sound -- the closure of the empty set is empty",
        "why_kept": (
            "The cell is derived from the generic inclusion V(src) subset "
            "V(dst), which does not license ALONG-EMPTY for any lossy type.  "
            "Special-casing it would make the closure row inconsistent with "
            "the rule the other rows follow, for a cell that is unreachable in "
            "practice: asserting the constructible image is empty requires "
            "computing the constructible image, which is the thing nobody "
            "computes.  Inherited from whetstone_dag.py unchanged so that the "
            "retrodiction gate stays an exact regression."),
    },
]


def discharge_for(rule_or_type, direction=None, kind=None, graph=None,
                  edge=None, axis=None, missing=None, fid=None,
                  traffic=False):
    """The canonical next move for a finding.  Never returns empty.

    `traffic=True` means "a conclusion was drawn ACROSS this edge", as opposed
    to "this edge exists and is untyped".  The two need different advice and
    conflating them is what produced a discharge naming only the closed exit.
    """
    if rule_or_type == K.UNTYPED and traffic:
        move = _UNTYPED_TRAFFIC_MOVE
    elif rule_or_type in RULE_MOVES:
        move = RULE_MOVES[rule_or_type]
    else:
        move = MOVES.get((rule_or_type, direction, kind))
        if move is None and kind == K.IDENTITY:
            move = _IDENTITY_MOVE
        if move is None:
            move = _GENERIC

    fields = {
        "src": "(source)", "dst": "(target)", "drops": "(undeclared)",
        "map_kind": "(unknown)", "src_field": "its own field",
        "axis": axis or "(axis)",
        "missing": ", ".join(str(m) for m in (missing or [])) or "(indices)",
        "fid": fid or "<finding id>",
        "debt_why": "(none recorded)",
    }
    if edge:
        fields["src"] = edge.get("src", fields["src"])
        fields["dst"] = edge.get("dst", fields["dst"])
        fields["map_kind"] = edge.get("map_kind", fields["map_kind"])
        drops = edge.get("drops") or []
        fields["drops"] = "; ".join(drops) if drops else "(none declared)"
        fields["debt_why"] = edge.get("debt_why") or "(none recorded)"
        if graph is not None:
            srcm = graph.models.get(edge.get("src")) or {}
            fields["src_field"] = srcm.get("field") or "its own field"
    try:
        return move.format(**fields)
    except (KeyError, IndexError):
        return move
