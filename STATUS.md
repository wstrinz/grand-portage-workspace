# Grand Portage status
Updated 2026-10-01. Authority: [Phase 2 handoff](docs/GP-0.50-PHASE-2-HANDOFF.md) and [decisions](DECISIONS.md).

GPC now coordinates and builds directly; the separate builder chat is retired. Phase 0 is complete, G1 is ratified, and Phase 2 has 71 executed kernel corpus cases out of 79. The required early slice is complete. G2 remains open with eight cases remaining.

All supplied-premise-authority cases now execute. A14, X04 and X09 use one proved rule-closure contract: a held goal lies in the forward closure of supplied atoms under registered rules, and a closed set missing the goal yields a countermodel. A path not starting at the claim's object, an unwarranted partition branch and a kind change without a kind-changing rule therefore refuse. Earlier batches bind evidence, theorem premises, section certificates, context reach and frozen open-premise slots exactly.

The actual finite fold is proved sound and complete. Equal event sets give identical resolver/fold results. Sound validator contracts exclude confirmed contradictions at inhabited overlap. The ratified faulty-checker demonstration freezes release while preserving complete held closure.

Validation: 10 new tests/27 subtests and 229 prior regression tests/678 subtests pass. Unchanged retained suites cover 105/271, giving 344/976. Fresh compilation and independent kernel checking pass with only standard axioms. All 459 legacy bytes, expectations, outcomes and 67 protected artifacts remain unchanged. Earlier 68 execution records are reused verbatim. Production logic remains 636 lines against the 750 stop; budget checks pass.

Next: the eight native-event-lifecycle cases remain. Continue family batches. Work stays local; heartbeats remain paused.

- [Executed slice](reports/PHASE-2-SLICE.md)
- [Standing limits](LIMITS.md)
