# Legacy conservatisms identified during Phase 0

GP 0.50 has no kernel yet. These are observed v0.37 conditional-rule refusals.

| Cases | Missing sufficient condition | Evidence |
|---|---|---|
| GP-A08b / GP-A08c | p-integral certificate or witness with valid reduction | Exact controls and oracle table replay |
| GP-X03 | Exact image closure of an empty source | Frozen discharge register and oracle table replay |
| GP-X08 | Independent membership certificate in the target ideal | Exact target replay and oracle table replay |

Details and raw outcomes: reports/PHASE-0A-BATCH-1.md and reports/ORACLE-RESULTS.json.

# 3a profile conservatisms (G3a review §3, 3a.1)

Sound refusals where a weaker sufficient condition exists. Each entry names the condition not used.

| Where | Refused | Sufficient condition not used | Status |
|---|---|---|---|
| R2/R3 IN_IDEAL guard obligations | A loose guard without its own C1 certificate, even when it already occurs among the tight guards | A loose guard in `T.guards` is trivially a unit in `K[x][1/g_T]` | Costs one trivial certificate per shared guard |
| R2/R3 for NOT_IN_IDEAL, NONUNIT, COVER | Any inclusion or map transport | NOT_IN_IDEAL(1) moves tight→loose and S→T; COVER transport via the split tree | Review rulings 2, 4 and the COVER item: 3a.1 steps 4–5 |
| R1 | IN_IDEAL ⇒ VANISHES_ON across different systems | R1 composed with R2 on the tight system | Compose explicitly |
| `contra` | Contradictions between different presentations of one locus (EMPTY on S vs NONEMPTY on S′ with locus S′ ⊆ locus S) | A C4 inclusion certificate inside the conflict check | Only same-system pairs, plus VANISHES_ON(h) vs NONEMPTY with guard h |
| NONEMPTY witnesses | Points over extension fields | R3 maps from (a; {m}) into the system | Review ruling 2: 3a.1 step 4 |

Not conservatism. IN_IDEAL transport needs ideal-level equation obligations, because VANISHES_ON gives only radical membership. EMPTY does not move S→T along a map (GP-X360).

The runner's refutation report uses `Scope.overlaps`, which is executable and unproved. It only labels refusals and never admits anything.
