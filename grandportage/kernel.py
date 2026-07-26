"""The transport kernel: the only place mathematical judgement is encoded.

Everything else in Grand Portage is data, bookkeeping or plumbing.  This module
is pure stdlib, imports nothing from the rest of the package, and has no I/O.

The kernel answers exactly one question:

    given an edge between two models, a direction of travel, and a claim,
    is moving that claim across that edge LICENSED?

It does not know what a Groebner basis is, what a matroid is, or what problem
you are working on.  It knows five relaxation types and four claim kinds.

Provenance: this is `whetstone/whetstone_dag.py`'s transport table, lifted out
of the JC(2) campaign it was written against, plus the SPECIALIZATION type that
`whetstone/MATROID_TRANSFER.md` sec.8 showed was forced by a second domain.
"""

# ---------------------------------------------------------------------------
# Edge types.  Edges point TIGHTER -> LOOSER: `src` is the more informative
# model, so V(src) subset V(dst) for every lossy type.  AGAINST = reasoning
# looser -> tighter, which is the direction emptiness travels and the direction
# that closes cells.
# ---------------------------------------------------------------------------
EQUIVALENCE = "EQUIVALENCE"
NECESSARY_CONDITION = "NECESSARY_CONDITION"
BASE_EXTENSION = "BASE_EXTENSION"
IMAGE_CLOSURE = "IMAGE_CLOSURE"
SPECIALIZATION = "SPECIALIZATION"

# Not a relaxation type: an explicitly recorded modelling DEBT.  An edge may be
# declared UNTYPED, but only with a reason, and the checker reports every one of
# them.  This exists so that "we have not typed this step" is a positive
# assertion in the graph rather than a missing row -- MODELLING_GAPS.md sec.4
# requirement 3.  It licenses nothing.
UNTYPED = "UNTYPED"

LOSSY_TYPES = (NECESSARY_CONDITION, BASE_EXTENSION, IMAGE_CLOSURE,
               SPECIALIZATION)
ALL_TYPES = (EQUIVALENCE,) + LOSSY_TYPES
DECLARABLE_TYPES = ALL_TYPES + (UNTYPED,)

ALONG = "ALONG"
AGAINST = "AGAINST"
DIRECTIONS = (ALONG, AGAINST)

# ---------------------------------------------------------------------------
# Claim kinds.
# ---------------------------------------------------------------------------
EMPTY = "EMPTY"          # this model has no points
NONEMPTY = "NONEMPTY"    # this model has a point (usually an exhibited witness)
PREDICATE = "PREDICATE"  # a condition satisfied by every point of this model
IDENTITY = "IDENTITY"    # a rewriting valid in this model's coordinate ring
CLAIM_KINDS = (EMPTY, NONEMPTY, PREDICATE, IDENTITY)

SCHEME = "SCHEME"        # the field-independent emptiness scope

# ---------------------------------------------------------------------------
# Certificate kinds, and whether the emptiness they certify BASE-CHANGES.
#
# This is the mechanism by which the kernel DERIVES an emptiness scope instead
# of trusting the label an author wrote.  1 in I over Q stays 1 in I over K; a
# nonzero rational resultant stays nonzero.  "This quadratic form has no zero
# because its discriminant is a non-square" does NOT survive adjoining the
# square root -- and that single row is the whole of the C08/C20 detection in
# the first domain and the whole of the ML8 detection in the second.
#
# Domains extend this registry through the graph (a `certificate` event); they
# do not edit this dict.
# ---------------------------------------------------------------------------
BUILTIN_CERTIFICATES = {
    "UNIT_IDEAL_CERT": True,            # 1 in I, exhibited over the base
    "NONZERO_RESULTANT": True,          # res in Q^*, hence in K^*
    "EXACT_VALUATION_COLLISION": True,  # an inequality between integers
    "DEGREE_COUNT": True,               # an inequality between integers
    "NONSQUARE_CLASS": False,           # field-relative by construction
    "NO_RATIONAL_POINT_SEARCH": False,  # field-relative by construction
}

# Map kinds.  Needed only for IDENTITY transport: rewriting a dictionary across
# a map is licensed when the map has no denominators.
POLYNOMIAL = "POLYNOMIAL"
RATIONAL = "RATIONAL"
IDENTITY_MAP = "IDENTITY_MAP"
MAP_KINDS = (POLYNOMIAL, RATIONAL, IDENTITY_MAP)

DENOMINATOR_FREE = (POLYNOMIAL, IDENTITY_MAP)

# Conditional rules, resolved by transport() against edge/claim attributes.
_SCHEME_SCOPE = "scheme_scope"
_MAP_POLYNOMIAL = "map_polynomial"
_CLOSED_CONDITION = "closed_condition"

# ===========================================================================
# THE TRANSPORT TABLE.  This is the whole type system.
# ===========================================================================
TRANSPORT = {
    EQUIVALENCE: {
        ALONG:   {EMPTY: True, NONEMPTY: True, PREDICATE: True, IDENTITY: True},
        AGAINST: {EMPTY: True, NONEMPTY: True, PREDICATE: True, IDENTITY: True},
    },
    NECESSARY_CONDITION: {
        # tighter -> looser.  A point of the tighter model is a point of the
        # looser one; nothing else survives this direction.
        ALONG:   {EMPTY: False, NONEMPTY: True, PREDICATE: False,
                  IDENTITY: _MAP_POLYNOMIAL},
        # looser -> tighter.  THIS is the direction that closes cells.
        AGAINST: {EMPTY: True, NONEMPTY: False, PREDICATE: True,
                  IDENTITY: _MAP_POLYNOMIAL},
    },
    BASE_EXTENSION: {
        # src = the model over the SMALL field k; dst = over the BIG field K.
        # NOTE THE REVERSED ASYMMETRY: here it is NONEMPTY that travels freely
        # ALONG (a k-point IS a K-point) and EMPTY that travels only with a
        # certificate.  Anyone who internalised "emptiness always transports"
        # from the other lossy types was primed to get this exactly backwards,
        # which is how the first domain shipped an erratum.
        ALONG:   {EMPTY: _SCHEME_SCOPE, NONEMPTY: True, PREDICATE: False,
                  IDENTITY: True},
        AGAINST: {EMPTY: True, NONEMPTY: False, PREDICATE: True,
                  IDENTITY: True},
    },
    IMAGE_CLOSURE: {
        # src = the true constructible image; dst = its Zariski closure.
        # A Zariski-CLOSED condition on the image does extend to the closure --
        # which is why elimination is a sound way to DERIVE equations even
        # though it is unsound as a source of witnesses.
        ALONG:   {EMPTY: False, NONEMPTY: True, PREDICATE: _CLOSED_CONDITION,
                  IDENTITY: _MAP_POLYNOMIAL},
        # A point of the closure need NOT lift: NONEMPTY does not travel here.
        # That single cell is Chevalley.
        AGAINST: {EMPTY: True, NONEMPTY: False, PREDICATE: True,
                  IDENTITY: _MAP_POLYNOMIAL},
    },
    SPECIALIZATION: {
        # generic fibre <-> special fibre of a scheme over Spec Z: char 0 to
        # char p.  The MAXIMALLY LOSSY type -- it carries no existence
        # statement in either direction.  Pinned by four published matroid
        # facts (MATROID_TRANSFER.md sec.3): Fano is EMPTY over Q and NONEMPTY
        # over F_2, non-Fano is the reverse, so all four existence cells are
        # falsified by explicit counterexamples.  A denominator-free identity
        # still reduces.
        ALONG:   {EMPTY: False, NONEMPTY: False, PREDICATE: False,
                  IDENTITY: _MAP_POLYNOMIAL},
        AGAINST: {EMPTY: False, NONEMPTY: False, PREDICATE: False,
                  IDENTITY: _MAP_POLYNOMIAL},
    },
    UNTYPED: {
        ALONG:   {k: False for k in CLAIM_KINDS},
        AGAINST: {k: False for k in CLAIM_KINDS},
    },
}


class Ruling(object):
    """The kernel's answer.  `rule` names the table cell, so a refusal can be
    routed to a discharge move without re-deriving why it was refused."""

    __slots__ = ("licensed", "reason", "rule", "etype", "direction", "kind")

    def __init__(self, licensed, reason, rule, etype, direction, kind):
        self.licensed = licensed
        self.reason = reason
        self.rule = rule
        self.etype = etype
        self.direction = direction
        self.kind = kind

    def __repr__(self):
        return "<Ruling %s %s/%s/%s>" % (
            "LICENSED" if self.licensed else "REFUSED",
            self.etype, self.direction, self.kind)


class ScopeError(ValueError):
    """An emptiness claim whose declared scope contradicts its certificate."""


def derive_scope(kind, certificate, declared_scope, certificates=None,
                 claim_id="<claim>"):
    """DERIVE an emptiness claim's scope from its certificate.

    This refuses to take the author's word for it, which is the single most
    load-bearing line in the whole system.  A claim whose certificate
    base-changes is SCHEME-scoped whatever the author wrote; a claim whose
    certificate does not base-change MUST carry an explicit field scope, and
    declaring it SCHEME is an error rather than a flag -- you cannot assert
    field-independence on the strength of a field-relative certificate.

    Non-emptiness claims keep whatever scope they declared: `NONEMPTY over R`
    is a fact about R and travels by the transport table, not by derivation.
    """
    certs = BUILTIN_CERTIFICATES if certificates is None else certificates
    if kind != EMPTY:
        return declared_scope
    if certificate is None:
        raise ScopeError(
            "EMPTY claim %s has no certificate.  An emptiness with no "
            "certificate has no derivable scope, and a scope taken on trust "
            "is exactly the failure this kernel exists to refuse." % claim_id)
    if certificate not in certs:
        raise ScopeError(
            "EMPTY claim %s cites unknown certificate kind %r.  Register it "
            "with a `certificate` event declaring whether it base-changes."
            % (claim_id, certificate))
    if certs[certificate]:
        return SCHEME
    if declared_scope in (None, SCHEME):
        raise ScopeError(
            "EMPTY claim %s cites a field-relative certificate (%s) but "
            "declares scope %r.  Name the field the certificate is relative to."
            % (claim_id, certificate, declared_scope))
    return declared_scope


def transport(etype, direction, kind, scope=None, certificate=None,
              map_kind=IDENTITY_MAP, zariski_closed=None):
    """Return a Ruling for moving a claim of `kind` across an edge of `etype`.

    Deliberately takes plain values rather than objects: the kernel must be
    callable from a test, a checker, a mutation harness or an MCP handler
    without any of them agreeing on a class.
    """
    if etype not in TRANSPORT:
        raise KeyError("unknown edge type %r (declarable: %s)"
                       % (etype, ", ".join(DECLARABLE_TYPES)))
    if direction not in DIRECTIONS:
        raise KeyError("unknown direction %r" % (direction,))
    if kind not in CLAIM_KINDS:
        raise KeyError("unknown claim kind %r" % (kind,))

    rule = TRANSPORT[etype][direction][kind]

    def ruling(ok, reason, rulename):
        return Ruling(ok, reason, rulename, etype, direction, kind)

    if etype == UNTYPED:
        return ruling(False,
                      "the edge is declared UNTYPED: no transport is licensed "
                      "across a step whose relaxation type has not been named",
                      "untyped")
    if rule is True:
        return ruling(True, "licensed by %s/%s/%s" % (etype, direction, kind),
                      "table")
    if rule is False:
        return ruling(False, "%s does NOT license %s in the %s direction"
                      % (etype, kind, direction), "table")
    if rule == _SCHEME_SCOPE:
        if scope == SCHEME:
            return ruling(True,
                          "licensed: the emptiness is certificate-backed (%s), "
                          "so it base-changes" % certificate, _SCHEME_SCOPE)
        return ruling(False,
                      "%s licenses EMPTY along the extension only at scope "
                      "SCHEME; this claim has scope %r (certificate %s, which "
                      "does not base-change)"
                      % (BASE_EXTENSION, scope, certificate), _SCHEME_SCOPE)
    if rule == _MAP_POLYNOMIAL:
        if map_kind in DENOMINATOR_FREE:
            return ruling(True, "licensed: the map is denominator-free (%s)"
                          % map_kind, _MAP_POLYNOMIAL)
        return ruling(False,
                      "IDENTITY rewriting needs a denominator-free map; this "
                      "edge's map is %s" % map_kind, _MAP_POLYNOMIAL)
    if rule == _CLOSED_CONDITION:
        if zariski_closed:
            return ruling(True,
                          "licensed: a Zariski-CLOSED condition on the image "
                          "extends to the closure by definition",
                          _CLOSED_CONDITION)
        return ruling(False,
                      "only Zariski-closed conditions extend from an image to "
                      "its closure; this predicate is not declared closed",
                      _CLOSED_CONDITION)
    raise AssertionError("unknown rule %r in the transport table" % (rule,))


def signature(etype):
    """The type's transport signature, as a comparable tuple.

    Used to assert that no two types are the same table wearing a different
    name, and that a proposed new type is actually needed.
    """
    return tuple((d, k, TRANSPORT[etype][d][k])
                 for d in DIRECTIONS for k in CLAIM_KINDS)
