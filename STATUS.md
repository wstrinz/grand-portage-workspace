# Grand Portage status
Updated 2026-10-01. Authority: [Phase 2 handoff](docs/GP-0.50-PHASE-2-HANDOFF.md) and [decisions](DECISIONS.md).

GPC coordinates; GPB builds. Phase 0 is complete, G1 is ratified, and Phase 2 now has 23 executed kernel corpus cases out of 79. G2 remains open.

The latest additions are X183/X184/X186. The actual Lean fold requires every named branch-emptiness premise and an explicit exhaustive-cover dependency. X183 has no right-premise record. X186 has held coverage but omits it from its argument; parent remains unheld. X184 accepts conditionally. Lean proves validator/fold soundness for every point type and parent/branch interpretation satisfying precisely the named hypotheses. No underlying algebraic truth or production profile is certified.

Other passes cover unfinished/stale/wrong-object receipts, current exact rational replay, complete supersession records and stale/current receipt arrival orders.

GPB's full event-set theorem is independently checked: equal event membership gives identical resolver and fold results, including duplicates and malformed diagnostics. GPC proved release review inherits that equality. Soundness and finite reachability completeness are also proved. Confirmed inhabited-overlap conflicts freeze release separately; held closure remains complete.

There are 553 passing native component controls, 80 compiled proof controls and 133 passing host tests. These counts stay separate from corpus passes. Fresh replay preserved all 459 legacy cases, expectations, outcomes and 67 historical artifacts.

Production logic is 636 lines against the 750 stop. Budget checks pass; conditional harness code is explicitly test-only.

Next: GPB owns conditional two-premise route fixtures X177/X178. GPC reviews their scope/object contracts and selects the next lifecycle batch. Required real fixtures for independent support/retraction, failed retry, narrowing, earned consequence and proved-overlap conflict remain open. Implementation stays local; heartbeats remain paused.

- [Executed slice](reports/PHASE-2-SLICE.md)
- [Standing limits](LIMITS.md)
