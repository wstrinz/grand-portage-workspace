# Grand Portage v0.28 release record

Version: `0.28.0`

Graph format: `5`

Kernel epoch: `10`

Collected checks: `1445`

v0.28 is an extraction and trial release. It adds no graph relation, claim
kind, graph field, evidence schema, graph format, or kernel-epoch change.

## Landed work

- The signed-off JC campaign tree moved to the optional
  `grandportage-jc-campaign` companion. The core retains neutral contract
  fixtures, generic compilers, the adapter conformance harness, and a narrow
  public-snapshot re-accretion gate.
- A genuinely cold ARR15 packet trial ran once. Its standard outcome is
  `PACKET_DEFECT`: useful work returned, but one declared source digest was
  wrong. The exact report and failure matrix are in this directory.
- Campaign packet compilation now verifies every declared source path and
  LF-normalized digest before emitting a packet.
- `CertificateScope.lean` now proves named stability decisions for every
  runtime builtin certificate. The runtime registry binds all eight names to
  their Lean decision and derived `SCHEME` or `FIELD_RELATIVE` scope.
- Authorized live Singular differential fuzz is restored and reports the
  checked case count and deterministic seed.
- The compact projection was exercised on the 452-record ARR15 graph. It is a
  useful content-addressed digest index, but not yet a semantic review model;
  the separate dogfood memo records that limit.

## Validation

- Core ordinary gate: `1395 passed, 50 deselected` in 44.65 seconds.
- Core live WSL/Singular gate: `50 passed, 1395 deselected` in 358.89
  seconds after the expected sandbox refusal and approved identical rerun.
- Lean: 27 jobs built with no `sorry`; only pre-existing linter warnings.
- Live reference differential: 22 checked cases in 10 seconds with seed
  `270027`, zero divergence. This is bounded fuzz, not exhaustive proof.
- Extracted companion: `357 passed, 9 skipped, 2 deselected` in 248.46 seconds.
- Companion adapter conformance: 14 adapters and 42 mutation controls pass.
- Public-snapshot and neutral Stacks custody controls: 17 pass.

No replay or exhaustive tests remain in the core after campaign extraction;
those lanes belong to the companion.

## Publication gate

The local companion repository has no remote and has not been pushed. Creating
or selecting the public remote remains an explicit external-authority step.
The core and companion should be published in that order so the companion's
pinned Grand Portage dependency remains resolvable.
