# Phase 2 Lean kernel

Mathlib-free package pinned to Lean 4.32.1. From F:/repos/grandportage-0.50:

```powershell
lake -d phase2/lean build
./phase2/lean/.lake/build/bin/gp_events_tests.exe
./phase2/lean/.lake/build/bin/gp_closure_tests.exe
./phase2/lean/.lake/build/bin/gp_completeness_tests.exe
./phase2/lean/.lake/build/bin/gp_order_tests.exe
lake -d phase2/lean env leanchecker -v GP50.ClosureProofs
lake -d phase2/lean env leanchecker -v GP50.ClosureCompleteness
lake -d phase2/lean env leanchecker -v GP50.ClosureOrderProofs
```

Events resolves complete typed event lists using explicit versions and targeted retraction/supersession. Liveness is custody eligibility; it does not validate evidence.

Closure computes support reachability with a bound derived from the declared support-node count. ClosureProofs proves soundness under node semantic contracts. ClosureCompleteness proves exact reachability equivalence for every finite list, including repeated IDs. ClosureOrderProofs proves supported membership is invariant under equal complete declaration sets, including reordered lists and changed duplicate counts. Independent kernel checks passed; axioms are propext, Quot.sound and Classical.choice.

The 22 event, 13 closure, 16 completeness and 14 graph-order controls include duplicate identity, conflicting current versions, stale binding, independent support, cycles, a 512-node reversed chain and event permutations. Completeness controls check 13,122 finite graphs; order controls check 3,072 transformations of 1,024 graphs. They are component tests; integration and G2 progress live in STATUS.md.
