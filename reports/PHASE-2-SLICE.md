# Phase 2 executed slice — checkpoint 1

Three unchanged kernel fixtures execute through the compiled Lean runner: strict registry/event decoding, exact rational receipt replay, event resolution, support closure and held projection.

| Case | Executed result | Accepting contrast |
|---|---|---|
| GP-A17 | REFUSE: unfinished attempt supplies no authority | Same current claim with an actual replayed receipt |
| GP-A18 | REFUSE: old receipt after ideal inputs change from (x) to (x²) | Original x = 1·x receipt before mutation |
| GP-A25b | REFUSE: B asks for A's bound receipt without alias evidence | Independently bound and replayed B receipt |

The adapter preserves fixture contracts and original expectations. A18 tests receipt freshness, not geometric emptiness. A25b preserves both selected identities. The contrasts are component controls, not additional corpus cases.

The runner reads actual polynomial generators, targets and cofactors. Accepted receipts imply exact all-exponent rational coefficient identities for the registered clause, with exact claim/version/binding equality. Host mapping and digest fidelity are specified in TCB.md.

The ten-case slice is incomplete. Remaining required behaviors: non-exhaustive cover; independent checked support surviving targeted retraction; failed retry; the real branch-order fixture; K2 narrowing; earned consequence; proved-overlap conflict; and a corpus positive control. Existing component controls for lifecycle behaviors do not replace those corpus runs.

Full legacy replay preserved all 459 case bytes and outcomes: 403 AGREES, 14 KNOWN_DIFFERENCE, nine UNSUPPORTED, four DIAGNOSTIC_OBSERVED and 29 RETAINED_DIAGNOSTIC. Source pins and the prior latest replay artifact remain unchanged.

Machine receipts: [native slice](PHASE-2-SLICE.json), [integration and preservation](PHASE-2-ADMISSION.json). G2 remains open.
