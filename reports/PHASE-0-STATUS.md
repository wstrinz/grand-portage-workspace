# Phase 0 status - 2026-09-27

G0 is not yet evaluated; Phase 0 is in progress.

## Verified here

- Approved backbrief and F: workspace; local repository has no remote.
- Separate oracle copy on F:, pinned at ac4155787207e2847d248cffed7be871d5dcd577; original source checkout unchanged.
- 233 source-pointed neutral cases (67 acceptance controls, 166 refusals), schema validator and reproducible layer-specific oracle adapter.
- Latest replay: 226 agreements, four known conservative differences, one diagnostic observation, one pending projection, one unsupported dimension-credit case.
- First-batch focused runs passed 95 tests with one live-CAS case excluded; the second batch passed 54 focused tests; the third passed 75 plus three adapter controls; the fourth passed 19 with two companion checks deselected; the fifth passed 12 with two companion checks deselected and two diagnostic controls; the sixth passed all 15 p-axis tests. The seventh milestone passed 271 selected historical instances (including 24 corrected-harness retries). The eighth slice passed 30 offline current-tree tests with three live tests deselected, plus four constructor-emission controls. The ninth slice passed 93 lifecycle, merge and provenance regressions plus four retry/section order controls. These runs overlap and are not the full release suite.
- Source and history indexes plus a partial-review ledger generated. All 29 deleted test files have been read and all 226 functions dispositioned. Of 197 selected functions, all 271 parametrized instances pass; 29 original functions remain unrun (27 companion-dependent, two live CAS). Semantic coverage remains incomplete.
- Freeze documentation patch prepared and git-apply checked, not applied or published.
- Existing Lean 4.32.1/Lake executables inspected successfully; no kernel spike code.

## Next work and dependencies

- 0a: resolve pending projections, review the remaining sources/history, split compound incidents into minimal cases and replay the additional routes. See PHASE-0A-BATCH-11.md and NEXT-REVIEW-PRIORITIES.md and corpus/REVIEW-COVERAGE.json.
- 0b: concrete JC/GP paths approved; other campaign directories discovered but not yet confirmed. Await remaining manifest paths, optional campaign scope and exclusions. No campaign harvesting has started.
- 0c: corpus-first restriction remains; agree a measurable effort cap before the deferred spike. See ENVIRONMENT.md.
- 0d: reviewable freeze patch and known-issues document ready under freeze-v0.37.1/. No public mutation or publication performed.

The chat's default directory still points to C:. Continue explicitly in F:\repos\grandportage-0.50 and keep practical outputs there.

Current lifecycle finding: two current identity receipts can produce different active fields under reversed branch merge order, although both receipts remain retained. The proposed 0.50 policy is not settled; see LIFECYCLE-DESIGN-FINDINGS.md and RETRY-MERGE-AUDIT.json.

2026-09-28: Goal run active toward Phase 0 completion or concrete blockers. PHASE-0-COMPLETION-TRACKER.json records lane requirements. The source-manifest clarification is pending; independent review continues. JOIN-AUTHORITY-AUDIT.json confirms the documented boundary between legacy transport auditing and logical entailment. Neutral-schema compliance of lifecycle event-shaped inputs is an explicit remaining task; no corpus expectations were changed.

Neutral lifecycle migration: GP-X142-163 now use a portable object/history vocabulary. All 22 reconstruct the original oracle inputs exactly, all 217 expected verdicts are unchanged, four adapter mutations pass, and the full replay retains the same outcomes. See NEUTRAL-LIFECYCLE-AUDIT.json. Earlier case bytes remain recoverable through Git and immutable replay digests; the current cases supersede their old input encoding.

Batch 10 adds ten conditional joint-premise/cover cases and passes 16 selected reporting, taint and mutation regressions. DESIGN.md and REVIEW.md are fully text-read with section dispositions; both remain semantically partial. Current source coverage is 36 partial / 332 unreviewed, not a completed 0a gate.

Lean documentation slice: lean/README.md (317 lines) and lean/THEORY.md (164 lines) fully text-read and dispositioned. Five source paths receive partial review credit; theorem premises remain distinct from runtime verification. See LEAN-AUTHORITY-BOUNDARIES.md. Corpus stays at 227 cases; no expected verdict or oracle code changed.

Batch 11 adds six provenance/review-policy controls, passes both source regressions and fully replays 233 cases. All earlier 227 case files remain byte-identical. SPEC (619 lines) is fully text-read with section dispositions; source review now 37 partial / 331 unreviewed. See PHASE-0A-BATCH-11.md for documentation overstatements and proposed corrections.
