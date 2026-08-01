# JC actual-source depth-6 boundary assay

This isolated adapter consumes the frozen JC receipt
`f2_h3_source_depth6_receipt.json` at SHA-256
`3c9954943d94faf8122ef556aa7248454d3d3d03e460747c6d55c0d3bc4a1464`.
It does not modify the sibling `math-stuff` checkout.

The native receipt contains two different grades of evidence:

- full sparse maps for the 3,262-term `R2B` residual and the 6,124-term
  `beta` residual;
- term counts and SHA-256 commitments, but not polynomial bodies, for the 33
  preceding top/depth-1--6 solve values.

`adapter.py` preserves that distinction. It independently decodes both sparse
maps, recomputes their native canonical digests, checks the exact
`-5*c2_3*c8_7*t` witness, checks that `beta` remains nonzero after
`c4_5 = c2_3^2/4`, and freezes a portable GP projection under
`fixtures/jc_source_depth6/boundary_v1.json`.

It then constructs two exact graph components using the existing
`mapped_ring_iso_v1` proof format:

1. On `alpha != 0`, adjoining `alpha*GP_INV_alpha-1` makes
   `alpha*c7_5+beta=0` equivalent to the translated coordinate
   `c7_5+GP_INV_alpha*beta=0`.
2. On `c2_3^2-4*c4_5=0`, the same equation is exactly `beta=0`, and `c7_5`
   remains free.

Both equivalences verify by direct cofactor expansion without Singular. The
large `beta` polynomial is represented through a fresh `GP_BETA` alias plus
one exact sparse alias equation; this keeps the coordinate maps small while
binding them to the complete polynomial.

## Landed chain replay

JC commit `cb3136c` supplies the missing bodies and ordered transitions in
`f2_h3_source_depth6_chain_certificate.json.gz`. GP retains a byte-identical
copy as `fixtures/jc_source_depth6/chain_v1.json.gz`; its canonical
uncompressed SHA-256 is
`d5ed44977e1f39312fbd2d30a286f686a0cd26d55dba237420a7a3d2bf513f15`.

`chain_adapter.py` is an independent consumer rather than an import of the JC
verifier. Its routine gate checks all 25 face/value digests, 23 ordered state
transitions, unit witnesses and solve identities. It additionally proves that
the ten starting bodies are exactly the solutions in GP's verified top- and
second-face fixtures and that the two outputs are exactly the existing `R2B`
and `alpha*c7_5+beta` boundary projection. `--full-replay` recomputes every
ambient face substitution and explicit `15*t^3+1` cofactor; it currently takes
about 80 seconds on the development machine.

The full independent replay is green. Its authority is nevertheless
`graph_effect: NONE`: the certificate binds the 25 extracted face tables by
digest but does not itself derive those tables from the raw E-system rows.
That source-extraction seam is now the first unresolved boundary.

## Deliberate refusals

The graph contains no edge from the actual-source E-system. The landed chain
proves much more than the earlier digest-only receipt, but a digest-bound face
table is still not a proof that the raw source row extracts to that table.
Therefore this assay grants no:

- actual-source coefficient-extraction authority;
- checked cover joining the generic and discriminant graph components;
- actual-source membership, depth-7, H3, or `(75,125)` conclusion.

The next honest source-composition input is a bounded face-extraction
certificate from raw E-system rows to these 25 exact face bodies. No new graph
edge or claim kind is needed unless that live certificate proves otherwise.

## Review-surface measurement

A persisted five-model/two-edge campaign folds with zero findings, and
`gp show` now summarizes the structured generators instead of dumping or
crashing on them. A full pretty projection measured about 56 MB and the static
explorer about 9 MB because the read model repeats the large generator payloads.
Those temporary artifacts were not checked in. Projection interning or
structured-polynomial summaries should be addressed before publishing a review
packet for this assay; the frozen 4.6 MB evidence fixture remains the canonical
review input.
## Run

```powershell
python experiments/jc_h3_source_depth6/adapter.py
python experiments/jc_h3_source_depth6/chain_adapter.py
python experiments/jc_h3_source_depth6/chain_adapter.py --full-replay
python -m pytest -q tests/test_jc_source_depth6_authority.py
python -m pytest -q tests/test_jc_source_depth6_chain.py
```

To build a disposable persisted campaign and record both equivalence verdicts:

```powershell
python experiments/jc_h3_source_depth6/adapter.py `
  --campaign-root PATH --record
python -m grandportage.cli --root PATH check
python -m grandportage.cli --root PATH show
```
