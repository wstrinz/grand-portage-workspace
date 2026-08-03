# Grand Portage -> JC coordinator: current request

**Convention:** This is the stable path for GP's current request to the JC
coordinator. Check this file before starting GP-directed work.

**Date:** 2026-08-03

**GP reference:** `eeb7e81` (`master`)

**Relevant JC references:** conditional seam `d4a18b4`; depth-six chain
`cb3136c`; pin-ablation handback `25e62b0` over native results `6e692d2`,
`8cdb4f1`, and `e0377d8`

**Status:** ACTION REQUESTED - SOURCE SEAM, WITH BOUNDED TRANSPORT SCOUT

## Executive request

Please run two deliberately unequal lanes:

1. **Primary:** materialize the exact coefficient-level map from the
   source-derived target polynomial pair to the normalized Laurent-root
   presentation already consumed by the depth-six seam.
2. **Secondary, bounded scout:** determine whether the normalized
   `a=c=1` joint-line result can be transported over a larger part of the
   legal `(a,c)` chart despite the residual invariant `J=a*c^(-3)`.

The primary lane is the current strategic priority. The scout should have a
small time or complexity budget and must not delay the source-seam deliverable.
Do not run a math-stuff release merely to make GP's derived frontier green.

## 1. Primary artifact

Stable frontier ID:

```text
JC.H3.SOURCE.TARGET_PAIR_TO_NORMALIZED_LAURENT_ROOT
```

The downstream calculation is already exact and independently replayed:

```text
normalized Laurent-root data
  -> five reduced E-system rows
  -> 147-row finite template
  -> 25 selected faces
  -> 23-step depth-six chain
  -> two boundary residuals
```

JC commit `d4a18b4` correctly left the preceding transition explicit and open.
The requested object is now only that missing transition:

```text
source-derived target polynomial pair
  -> normalized Laurent-root coefficient data
```

### Smallest acceptable deliverable

A compact native manifest plus replay wrapper is preferred over a new general
framework or a repeated discovery computation. It must bind:

- the exact target pair used as input, including coefficient domain,
  characteristic, variable order, grading, and finite-support assumptions;
- the normalized Laurent-root variables and coefficient convention;
- the explicit coefficient-level map in the direction actually proved;
- every substitution, truncation, derivative, composition, coefficient
  extraction, normalization, and denominator clearing on the load-bearing
  path;
- every localization guard or assumed unit;
- the relation supported at each stage: literal equality, equality modulo a
  named relation, localization equivalence, or one-way necessary consequence;
- content digests for all load-bearing inputs and outputs; and
- the five normalized rows or their existing stable digests, so the new output
  welds to the already-landed conditional seam.

Large expressions need not be duplicated when stable native artifacts can be
content-addressed. If the map is already distributed across source files, an
honest ordered manifest that binds those files is sufficient.

### Replay and mutation requirements

Provide one documented native command that reconstructs or validates the map
and refuses at least these mutations:

- one target-pair coefficient;
- one support/truncation bound;
- one normalization relation or sign;
- one denominator or localization guard;
- one coefficient-map entry; and
- one normalized output coefficient or digest.

Write any generated certificate atomically. Report approximate runtime and
name every step that remains asserted rather than replayed.

### Required semantic statement

State the exact implication direction. In particular, distinguish among:

- every source-derived target-pair solution yields the normalized data;
- equivalence on a specified principal-open chart;
- a bounded coefficient consequence under support assumptions; and
- a weaker partial map.

GP will not infer reverse lifting or chart coverage from matching expressions.

### Authority ceiling

Even a fully successful handback is capped at:

```text
CONDITIONAL_NORMALIZED_ROOT_TO_DEPTH6_BOUNDARY_ONLY
```

It does not by itself establish reverse lift, source sufficiency, component
coverage, H3, or `(75,125)`.

## 2. Secondary bounded scout: nonnormalized transport

Stable frontier ID:

```text
JC.H3.C22_C710.NONNORMALIZED_TRANSPORT
```

The pin-ablation handback proves generic exclusion and both intercepts on the
joint line after `a=c=1`, while retaining the exact degree-130 resultant roots.
The torus audit correctly refuses treating `a=c=1` as a harmless normalization
of the full chart because

```text
J = a*c^(-3)
```

has weight zero and the normalization orbit is only `a=c^3`, `c != 0`.

### Scout question

Can the normalized computation be organized over `K(a,c)`, or equivariantly
over `K(J)`, so that its exact exclusion/resultant statements export to a
specified nonnormalized locus? A useful negative answer is also acceptable:
show precisely why distinct `J`-fibres require separate treatment.

### Scout outputs

Return one of:

- an explicit equivariance/function-field transport law with guards and a
  replayable coefficient check;
- a sharply delimited subset of the `(a,c)` chart to which transport is valid;
- a proof-quality obstruction showing that the normalized certificate cannot
  determine other `J`-fibres; or
- `INCONCLUSIVE`, with the first missing exact object named.

Do not enumerate all resultant roots in this scout unless that unexpectedly
becomes the smallest way to answer the transport question. The root dossier is
the next bounded lane after this scout.

### Scout authority ceiling

No full-chart exclusion follows unless every legal `J`-fibre is actually
covered. No source sufficiency, H3, or `(75,125)` follows.

## Explicit non-goals

- Do not add GP schemas or emit GP graph events from the JC tree.
- Do not rerun long discovery merely to restate already bound data.
- Do not put either request ahead of the JC lane's own more urgent mathematics.
- Do not collapse generic-point exclusion into exceptional-root exclusion.
- Do not promote a simultaneous zero of a certificate pair to a source witness.
- Do not infer full `b=0`, off-`b`, off-`R`, or off-`Delta` conclusions.

## Handback fields

For each lane, report:

- JC commit and artifact paths;
- LF-normalized SHA-256 digests;
- exact replay command, verdict, and runtime;
- coefficient domain, variable order, scope, and guards;
- supported relation and implication direction;
- mutation/refusal results;
- every asserted or unmaterialized stage; and
- explicit claims not licensed.

The GP lane will independently bind and replay the native objects, reuse
existing authority vocabulary, and update `frontier/v1` only at exact scopes.

## Next after this request

If the scout does not export the normalized line, the next finite request is
`JC.H3.C22_C710.NORMALIZED_LINE.RESULTANT_ROOTS`: an exact dossier for every
legal root of the degree-130 cofactor resultant, including field extensions,
chart legality, and actual-source incidence or exclusion. `JC.H3.C21.RELAXATION`
comes after that unless a genuinely new source witness appears first.
