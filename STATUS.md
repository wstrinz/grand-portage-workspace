# Grand Portage status
Updated 2026-09-30. Current authority: [Phase 2 handoff](docs/GP-0.50-PHASE-2-HANDOFF.md) and [decisions](DECISIONS.md).

Phase 0 is complete and G1 is now closed by Will's explicit coverage exception and design decisions. The paper score remains 52 of 67; we did not turn the seven unknowns into successes.

Phase 2 is authorized. We will build the actual Lean kernel and prove that every held claim is sound and every reachable claim in the declared finite domain is held. Receipts are the default; durable Lean proofs share the same scope/binding interface. No production kernel proof or executed Phase 2 slice exists yet.

Event arrival order will not choose current authority. Explicit versions and targeted retractions determine the final snapshot. Will confirmed that conflicts freeze release separately from the complete checked held closure.

The local layer draft accounts for all 459 cases: 84 kernel, 193 profile, 53 adapter, 7 surface, 11 host and 111 unresolved. All ten metadata tests pass; case bytes are unchanged. Parent semantic review and grouped boundary decisions remain before final G2 selection. The next implementation is the small kernel slice.

The three-file public freeze is published as [6f38e96](https://github.com/wstrinz/grandportage/commit/6f38e96b8e18a726ff97cdde20daeaa34a6e15b5); checks passed and the tag is unchanged. Will confirmed that the shadow stays public. The reviewed integration is pushed; the worker draft remains separate pending semantic review. Heartbeats remain paused.

The main implementation risks are support/retraction semantics, parser-to-record binding, proving finite saturation, and keeping the kernel small. The next checkpoint must show actual code/tests, an ambiguity list and measured budget use.

- [Execution plan](docs/PHASE-2-PLAN.md)
- [Core contract](SPEC-CORE.md)
- [Standing limits](LIMITS.md)
- [Phase 1 review](reports/PHASE-1-PAPER-PARENT-REVIEW.md)
- [Freeze publication receipt](reports/FREEZE-PUBLICATION.json)
- [Review shadow](https://github.com/wstrinz/grand-portage-workspace/tree/codex/phase-0)
