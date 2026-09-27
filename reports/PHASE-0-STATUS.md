# Phase 0 status — 2026-09-27

G0 is not yet evaluated; Phase 0 is in progress.

## Verified here

- Approved backbrief and F: workspace; local repository has no remote.
- Separate oracle copy on F:, pinned at ac4155787207e2847d248cffed7be871d5dcd577; original source checkout unchanged.
- 50 source-pointed neutral cases (17 acceptance controls, 33 refusals), schema validator and reproducible layer-specific oracle adapter.
- Latest replay: 42 agreements, four known conservative differences, one diagnostic observation, three pending projections.
- 95 focused frozen regression tests passed; one additional live-CAS case excluded. This is not the full release suite.
- Source and history indexes generated; semantic coverage remains incomplete.
- Freeze documentation patch prepared and git-apply checked, not applied or published.
- Existing Lean 4.32.1/Lake executables inspected successfully; no kernel spike code.

## Next work and dependencies

- 0a: resolve pending projections, review the remaining sources/history, split compound incidents into minimal cases and replay the additional routes. See PHASE-0A-BATCH-1.md.
- 0b: concrete JC/GP paths approved; other campaign directories discovered but not yet confirmed. Await remaining manifest paths, optional campaign scope and exclusions. No campaign harvesting has started.
- 0c: corpus-first restriction remains; agree a measurable effort cap before the deferred spike. See ENVIRONMENT.md.
- 0d: reviewable freeze patch and known-issues document ready under freeze-v0.37.1/. No public mutation or publication performed.

The chat's default directory still points to C:. Continue explicitly in F:\repos\grandportage-0.50 and keep practical outputs there.
