# Grand Portage status
Updated 2026-09-30. Authority: [Phase 2 handoff](docs/GP-0.50-PHASE-2-HANDOFF.md) and [decisions](DECISIONS.md).

GPC coordinates; GPB builds. Phase 0 is complete, G1 is ratified, and Phase 2 now has 17 executed kernel corpus cases out of 79. G2 remains open.

The latest additions are A16-missing and A16-covered. The actual Lean fold refuses parent emptiness without exhaustive coverage and accepts it under both explicitly named premises. The approved test-only harness proves validator/fold soundness for every point type and parent/branch interpretation satisfying those premises. It certifies the conditional conclusion, with no underlying algebraic truth claim or production profile adoption.

Other passes cover unfinished/stale/wrong-object receipts, current exact rational replay, complete supersession records and stale/current receipt arrival orders.

GPB's full event-set theorem is independently checked: equal event membership gives identical resolver and fold results, including duplicates and malformed diagnostics. GPC proved release review inherits that equality. Soundness and finite reachability completeness are also proved. Confirmed inhabited-overlap conflicts freeze release separately; held closure remains complete.

There are 553 passing native component controls, 78 compiled proof controls and 102 passing host tests. These counts stay separate from corpus passes. Fresh replay preserved all 459 legacy cases, expectations, outcomes and 67 historical artifacts.

Production logic is 636 lines against the 750 stop. Budget checks pass; conditional harness code is explicitly test-only.

Next: GPB owns three declaration collision/idempotence fixtures. GPC owns integration and extensions of the approved conditional harness. Required real fixtures for independent support/retraction, failed retry, narrowing, earned consequence and proved-overlap conflict remain open. Implementation stays local; heartbeats remain paused.

- [Executed slice](reports/PHASE-2-SLICE.md)
- [Standing limits](LIMITS.md)
