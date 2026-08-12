# JC closeout and Grand Portage restart roadmap

**Assessment date:** 2026-08-12
**Grand Portage baseline:** `master` at `7381245` (`v0.23.0` plus Portage
Command v0), with only an unrelated untracked `uv.lock`.
**JC baseline inspected:** `math-stuff/main` now refreshed to `1bbdec4`, with active and
untracked campaign work present.  The only authoritative live coordination
source is `d2_plane_72_108/CURRENT.md`.

This note is a planning artifact. It has no mathematical authority and no
graph effect.

## Decision

Grand Portage can usefully help the current JC effort, but its highest-value
contribution is now **campaign closeout and publication integrity**, not another
JC-specific theorem checker.

The `(75,125)` summit remains open. The live campaign has nevertheless reached
a natural publication-grade intermediate result: a sharply typed
counterexample portrait, a zero-sorry conditional end-to-end composition,
compact exact and modular interfaces, and a large collection of exact
mechanism ceilings that explain why many formerly plausible attacks cannot
close their leaves. JC's own publication policy now explicitly permits a
publication flag short of exact S2 closure.

The remaining publication work is bounded:

1. audit every portrait claim against current-head evidence;
2. freshness-replay the formal composition and load-bearing checkers;
3. assemble one replayable evidence/release manifest that separates exact,
   checked, conditional, cited, and reconnaissance material;
4. complete canonical price cards for `S1'`, `S3`, `S4`, `S5`, `A2`, and
   `H-RECIP`;
5. produce the technical report and tagged archival artifact.

Exact S2 closure (`m0 = r = 436`) remains the stronger gold flag. It should
resume only through a genuinely new structural representation, not by adding
CRT primes, reconstruction height, Macaulay degree, RAM, or parallel attacks to
representations whose ceilings are already exact.

## What changed since GP v0.23

GP's checked JC frontier is a faithful snapshot of an older campaign phase. It
still centers `JC.H3.SOURCE.REMAINING_COEFFICIENT_MAP` and the active
`Q_(5,1)=0` hyperplane packet. The authoritative JC campaign has since moved
well beyond that frontier.

The current theorem-facing surface is now six typed leaves:

| leaf | current residual |
|---|---|
| `S1'` | actual pair to indexed row-open/row-zero exclusion |
| `S2` | LOCAL / positive-dimensional infinity kill; the finite-algebra squeeze is the preferred structural route |
| `S3` | `AFF-A` isolated-point kill |
| `S4` | `AFF-B` isolated-point kill on `D(z1)` |
| `S5` | `ENTRY-T` isolated-point kill on `D(z1)`; `z1=0` is exact over `QQ` |
| `S6` | atlas/scope residue: `A2` authority and `H-RECIP` |

Several developments are especially informative for GP's design:

- The campaign's authoritative state is a manually curated, override-capable
  coordination document. Filenames, timestamps, and unions of old frontier
  notes are explicitly non-authoritative.
- A live leaf is described by a triple: its smallest exact object, its next
  accepted object, and the inference/representation that is retired.
- Negative representation theorems are first-class research outputs. They need
  replay and publication treatment even though they close no theorem leaf.
- Evidence grades are irreducibly plural: `PROVED`, `CHECKED`, conditional,
  cited/external, and modular reconnaissance must not be collapsed.
- The campaign has a non-summit terminal condition with explicit publication
  criteria and a slower-burn maintenance policy.
- The useful formal boundary is now often a small finite interface plus native
  binding obligations. Formalization does not discover the missing CAS
  presentation.

Portage Command v0 already handles packets, attempts, useful refutations,
append-only history, and verification debt. It does **not** yet represent this
new campaign state.

## The missing GP object

Build a provisional, profile-driven `campaign-dossier/v0` derived read surface.
It should bind a campaign's canonical authority snapshot and compile the three
views needed at this stage:

1. **Current portrait:** what is proved, checked, conditional, cited, or only
   reconnaissance, with exact scopes and evidence bindings.
2. **Residual/price ledger:** each open leaf's smallest faithful object, best
   measured certificate price, retired representations, next accepted object,
   and explicit resume condition.
3. **Closeout profile:** named terminal criteria such as `PUBLICATION_FLAG` and
   `GOLD_FLAG`, with a fail-closed readiness verdict and exact blockers.

This remains zone 4:

```text
authority: DERIVED_READ_MODEL_ONLY
graph_effect: NONE
```

The dossier must never parse mathematical truth out of arbitrary Markdown.
Each campaign supplies a small explicit adapter/manifest binding canonical
source files, commits, receipts, and replay commands by digest. The source
campaign remains authoritative; GP checks consistency, freshness, coverage,
and presentation.

### Minimum dossier records

**Source snapshot**

- repository identity and commit;
- canonical coordination sources and normalized digests;
- clean/dirty and generated-at state, surfaced rather than hidden;
- prior dossier fingerprint, when extending a published snapshot.

**Portrait claim card**

- stable claim ID and exact scope ID;
- concise proposition;
- grade: `PROVED`, `CHECKED`, `CONDITIONAL`, `CITED`, or
  `RECONNAISSANCE`;
- evidence artifacts and replay commands;
- named assumptions and consumers;
- public-release disposition.

**Leaf price card**

- stable leaf ID and state;
- smallest faithful exact object;
- next accepted object;
- measured price and price basis (dimensions, height, wall/RSS cap, or a named
  structural obstruction);
- retired representations with exact reasons;
- one explicit resume condition;
- theorem-facing downstream role.

**Closeout criterion**

- stable profile and criterion IDs;
- required claim, artifact, replay, price-card, or publication-hygiene class;
- current state and exact blocker;
- whether an open theorem leaf is permitted when it has a complete price card.

**Evidence/release artifact**

- content digest, role, grade, replay, and public/private disposition;
- dependency on external tools or data;
- compact receipt versus regenerable heavy discovery artifact;
- license/provenance note where required.

## Implementation sequence

### Phase 0 — re-establish a trustworthy baseline

1. Keep GP v0.23's existing frontier and packet fixtures as historical frozen
   retrodiction fixtures; do not rewrite them to impersonate current JC.
2. Add a current-head JC dossier adapter and manifest by hand from
   `CURRENT.md`, the publication flag, formal shadow surface, and exact evidence
   list.
3. Make staleness visible: the compiled dossier must report a digest/commit
   mismatch rather than silently presenting an old packet as current.
4. Add a human `gp campaign-dossier` view answering: current portrait, open
   leaves, publication blockers, active allocation, and legal resume triggers.

**Exit condition:** a cold reader can accurately state why JC is not a summit
proof, why it is nevertheless publication-close, and exactly what blocks the
publication flag without reading the campaign transcript.

### Phase 1 — closeout compiler

1. Implement fail-closed dossier normalization and deterministic fingerprints.
2. Add profile evaluation for JC's `PUBLICATION_FLAG` and `GOLD_FLAG` without
   hard-coding JC vocabulary into the compiler.
3. Reject theorem support by `RECONNAISSANCE` evidence; allow reconnaissance
   and mechanism ceilings as separately typed publication artifacts.
4. Require every unresolved leaf admitted by a short-of-summit profile to have
   a complete price card and resume condition.
5. Generate the dependency-card table, leaf-price table, replay matrix, and
   exact blocker list from the same fingerprinted dossier.

**Exit condition:** readiness is determined mechanically from explicit cards;
an unpriced leaf, stale authority source, missing replay, or grade laundering
keeps the profile not ready.

### Phase 2 — archival release builder

1. Assemble a content-addressed release manifest of compact receipts,
   deterministic checkers, Lean modules/theorem names, axiom-audit outputs, and
   external assumptions.
2. Keep heavy discovery artifacts, logs, local paths, scratch data, and
   third-party sources out of the public payload unless explicitly licensed and
   required.
3. Generate checksums and a clean-clone replay plan; make environment-dependent
   and long-running checks explicit lanes.
4. Export machine-readable provenance, preferably RO-Crate only after the
   native manifest is stable.

**Exit condition:** a clean checkout can verify the advertised compact package
and can see, without inference, which claims remain conditional.

### Phase 3 — maintenance and successor campaigns

1. Represent the slower-burn rule as advisory campaign policy: at most one
   theorem-facing JC lane by default and explicit structural resume triggers.
2. Generate a successor-campaign starter from a dossier: authority sources,
   profile, packet catalog, ledger, replay lanes, and publication policy.
3. Add a handoff view that distinguishes reusable machinery from
   campaign-private adapters.

**Exit condition:** parking JC preserves a precise restart point, and a new
campaign can begin without copying JC-specific semantics into GP's core.

### Phase 4 — generalize before freezing

Run the dossier/closeout flow on at least one non-JC campaign. Use the result to
decide whether claim grades, price cards, and closeout criteria remain one
schema with profiles or need separate typed packet families. Freeze `v1` only
after this transfer test.

## First implementation slice

**Status:** complete. The dossier compiler, CLI, synthetic and current-JC
fixtures, source audit, profile evaluation, adversarial tests, and trust-zone
registration are implemented.

The next coding tranche should be deliberately small:

1. `grandportage/dossier.py` with deterministic validation, fingerprints, and
   profile evaluation;
2. `gp campaign-dossier INPUT.json [--format json|human]`;
3. one synthetic fixture and one current JC fixture;
4. focused adversarial tests for:
   - canonical-source digest or commit drift;
   - duplicate claim/leaf IDs;
   - reconnaissance evidence used as theorem support;
   - an open leaf missing a price or resume condition;
   - a closeout criterion marked complete without its bound artifact/replay;
   - a retired representation with no exact reason;
   - deterministic ordering and fingerprints;
   - graph effect or authority widening;
5. architecture tests preserving the zone-4 dependency direction.

Do not yet build a UI, planner, distributed runner, automatic Markdown parser,
or new mathematical evidence contract. The dossier and closeout compiler are
the immediate credibility gain; release assembly and visualization should
consume them later.

## Archival implementation slice

**Status:** implemented provisionally as `campaign-release/v0`.

The release compiler now computes exact transitive coverage from evaluated
profile references; validates public payload classes, provenance, licensing,
and safe paths; requires replay lanes for load-bearing artifacts; and can
atomically materialize a clean, digest-rechecked bundle with a manifest,
checksums, and replay document. The publication projection now generates the
exact portrait dependency audit and manuscript-ready claim, leaf, retirement,
replay, and blocker tables. The JC fixture is an honest draft: it provides the
portrait-audit and release-manifest placeholders under explicit generator
contracts while leaving the manuscript and all independent policy blockers
intact.

The remaining Phase 2 work is live clean-clone exercise and environment capture
for JC, followed by a non-JC transfer assay before considering RO-Crate or v1.

## Immediate JC handback

GP can contribute four bounded artifacts to JC closeout while the compiler is
being built:

1. a current-head portrait dependency manifest;
2. the canonical six-leaf price-card table;
3. a replay/release manifest separating exact, formal, checked, conditional,
   cited, reconnaissance, and mechanism-ceiling artifacts;
4. a publication-flag report listing only real blockers.

These artifacts should be generated from the JC adapter and reviewed in JC,
not treated as new GP graph authority. They directly satisfy three of the five
publication-flag components and give the manuscript its dependency and methods
tables.

## Allocation recommendation

Use most near-term GP effort on the dossier/closeout and release path. Offer JC
the four handback artifacts above and keep one optional theorem-facing lane only
if it meets JC's own structural resume rule. After the publication flag, use the
same machinery to start a second campaign and test whether Grand Portage's
vision survives outside its exemplar.
