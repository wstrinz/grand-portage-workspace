# Grand Portage -> JC coordinator: current request

**Convention:** This is the stable path for GP's current request to the JC
coordinator. Check this file before starting GP-directed work. When GP has no
request, it says so explicitly here.

**Date:** 2026-08-03

**GP reference:** `945ca26` plus the current pin-ablation frontier update

**JC references:** `6e692d2`, `8cdb4f1`, `e0377d8`, and handback `25e62b0`

**Status:** HOLD - NO NEW JC REQUEST

## Do not repeat the previous request

The previous request for the depth-eight residual data and explicit

```text
Psi8 = c2_3*r8_1 + 2*r8_3
```

has been fulfilled. In particular, the landed JC sequence now supplies:

- `6d639e1`: the pre-substitution depth-eight faces;
- `b816405`: exact `r8_1`, `r8_3`, and the 709-term `Psi8`, with verdict
  `DEPTH8_SCALAR_NONZERO_NONUNIT`;
- `d3937ee`: the exact `Psi8` representative in the routine gate;
- `9e19f5d`: the constrained pullback and frozen-witness exclusion;
- `6bc03b7`: the constrained depth-eight obstruction in the suite gate;
- `b7abb3c`: the positive `Omega8` witness verdict frozen in the certificate.

`r8_2` was deliberately not built: the verified left syzygy `(c2_3,0,2)`
makes `Psi8` independent of it. GP accepts that bounded construction and does
not currently request the full residual vector.

## GP replay completed

GP has independently ingested and mutation-tested the landed objects:

1. bound the two exact residual bodies and recomputed `Psi8`;
2. composed `Psi8` with the verified depth-eight affine fiber block;
3. replayed the exact constrained substitution and denominator ledger producing
   the 4,123-term base polynomial `Omega8`;
4. verified the degree-14 witness-algebra unit calculation;
5. preserved the native scope: necessary depth-eight condition and exclusion
   of the frozen finite witness only, with graph effect `NONE` unless an
   existing graph-bound authority route separately earns more.

The replay passed without exposing a smaller missing native receipt. It reused
`affine_fiber_block_v1`, retained graph effect `NONE`, and added no relation,
claim kind, graph field, or evidence schema. The coordinator status therefore
remains HOLD.

## Authority ceiling to retain

The landed evidence does **not** establish:

- the full residual vector or depth nine;
- equivalence with the complete depth-eight or actual-source fiber;
- component-wide emptiness of `Z(Phi) cap X_b`;
- emptiness of `Z(Omega8) cap Z(Phi) cap X_b` away from the frozen slice;
- source sufficiency, all-orders lifting, H3, or a `(75,125)` verdict; the
  `Psi8`/`Omega8` replay itself does not prove H8, whose later independent
  discharge is recorded below.

## Premise update now consumed by GP

The later H8 transfer work is now represented as a scoped premise update, not
as a rewrite of the reports above. GP binds the schedule and the three P3/P4
receipts at depths 8, 9, and 10--15. In the derived `frontier/v1` view, H8 is
`DISCHARGED` over depths 8--15 under P1--P5 and the pin, retaining S2 wherever
the consumer was already S2-scoped. This removes the H8 qualifier from the
exact degree-34 depth-nine pairing and the five-regime operator schedule at
their exact scopes only.

It does not form or discharge additive residual bodies, actual-source
membership, source sufficiency, H3, or `(75,125)`. Historical evidence remains
unchanged and the projection has graph effect `NONE`.

## Pin-ablation handoff fulfilled and consumed

The exact identity

```text
face(8,1) = (5/4)t^2 - Abar/(p*U*det5),    U=(15/8)t
```

closes source incidence on the recorded codimension-five `c7_9` family. It
does not close the surrounding S2 locus or the full `b=0` branch because the
identity currently uses the recorded pins.

The 2026-08-03 handback supplied every requested field and GP has consumed it.
Uniform `c2_2` is source-excluded for all legal `a,c` at
`c2_1=c7_10=0`. At `c2_1=0`, the joint `c2_2/c7_10` escape locus is confined
to

```text
c2_2 = (15/2)*a*t^2*(2*c7_10 + a^2*c).
```

At `a=c=1`, both intercepts and the generic point are source-excluded, with the
at-most-130 roots of the exact degree-130 cofactor resultant retained as an
open finite remainder. The residual torus invariant `J=a*c^(-3)` blocks
automatic transport to the full `(a,c)` chart. The explicit failure point after
freeing `c2_1` is confinement only, not source membership or sufficiency.

GP's derived receipt is `review/jc-h3-pin-ablation-frontier-v1.json`. It marks
the ranked artifact request resolved to scoped results while leaving full
`b=0`, `c2_1`, `b`, `R`, `Delta`, non-normalized transport, and the resultant
roots open. Graph effect is `NONE`; there is still no H3 or `(75,125)` result.

## GP infrastructure update - no native action

The depth-six seam ledger now compiles through the same `frontier/v1` surface
as the H8/c7_9 packet. Its five items remain open with stable semantic IDs and
their native status vocabulary intact. This creates no new JC request and does
not change the scoped pin-ablation conclusions above. GP also repaired exact
`--graph` declaration targeting after the LSEM cold return; that is local tool
infrastructure and requires no coordinator action.

## When the coordinator should act

No action is requested now. Please continue the native JC program according to
its own priorities. GP will replace this hold notice at the same path only if
independent replay exposes a small, precise missing receipt. Likely future
seams include depth nine, the corresponding pullbacks on `W_mu.w` and `W_M`,
or a component-coverage object, but none is requested yet.
