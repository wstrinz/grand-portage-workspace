# Phase 0 status - 2026-09-27

G0 is not yet evaluated; Phase 0 is in progress.

## Verified here

- Approved backbrief and F: workspace; local repository has no remote.
- Separate oracle copy on F:, pinned at ac4155787207e2847d248cffed7be871d5dcd577; original source checkout unchanged.
- 113 source-pointed neutral cases (31 acceptance controls, 82 refusals), schema validator and reproducible layer-specific oracle adapter.
- Latest replay: 106 agreements, four known conservative differences, one diagnostic observation, one pending projection, one unsupported dimension-credit case.
- First-batch focused runs passed 95 tests with one live-CAS case excluded; the second batch passed 54 focused tests; the third passed 75 plus three adapter controls; the fourth passed 19 with two companion checks deselected; the fifth passed 12 with two companion checks deselected and two diagnostic controls; the sixth passed all 15 p-axis tests. These runs may overlap and are not the full release suite.
- Source and history indexes plus a partial-review ledger generated. Five deleted test files have been read; seam, formalization and p-axis checks have bounded extractions. Source-ladder and depth-six extraction is queued. Another 24 deleted files remain unread. Semantic coverage remains incomplete.
- Freeze documentation patch prepared and git-apply checked, not applied or published.
- Existing Lean 4.32.1/Lake executables inspected successfully; no kernel spike code.

## Next work and dependencies

- 0a: resolve pending projections, review the remaining sources/history, split compound incidents into minimal cases and replay the additional routes. See PHASE-0A-BATCH-6.md and corpus/REVIEW-COVERAGE.json.
- 0b: concrete JC/GP paths approved; other campaign directories discovered but not yet confirmed. Await remaining manifest paths, optional campaign scope and exclusions. No campaign harvesting has started.
- 0c: corpus-first restriction remains; agree a measurable effort cap before the deferred spike. See ENVIRONMENT.md.
- 0d: reviewable freeze patch and known-issues document ready under freeze-v0.37.1/. No public mutation or publication performed.

The chat's default directory still points to C:. Continue explicitly in F:\repos\grandportage-0.50 and keep practical outputs there.
