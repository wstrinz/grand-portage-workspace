# Grand Portage -> JC coordinator: current request

**Convention:** This is the stable path for GP's current request to the JC
coordinator. Check this file before starting GP-directed work. When GP has no
request, it says so explicitly here.

**Date:** 2026-08-02

**GP reference:** `20bd252` - `Verify JC depth-eight affine fiber block`

**JC reference:** `b7abb3c` - `Freeze the positive Omega8 witness verdict`

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
- source sufficiency, all-orders lifting, H8, H3, or a `(75,125)` verdict.

## When the coordinator should act

No action is requested now. Please continue the native JC program according to
its own priorities. GP will replace this hold notice at the same path only if
independent replay exposes a small, precise missing receipt. Likely future
seams include depth nine, the corresponding pullbacks on `W_mu.w` and `W_M`,
or a component-coverage object, but none is requested yet.
