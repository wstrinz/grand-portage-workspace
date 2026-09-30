# Phase 2 Lean kernel

Mathlib-free package pinned to Lean 4.32.1. From F:/repos/grandportage-0.50:

```powershell
lake -d phase2/lean build
./phase2/lean/.lake/build/bin/gp_events_tests.exe
./phase2/lean/.lake/build/bin/gp_closure_tests.exe
lake -d phase2/lean env leanchecker -v GP50.ClosureProofs
```

Events resolves complete typed event lists using explicit versions and targeted retraction/supersession. Liveness is custody eligibility; it does not validate evidence.

Closure computes support reachability with a bound derived from the declared support-node count. ClosureProofs proves that every computed support is reachable, and semantic soundness follows from each node's admitted contract. The independent kernel check passed; theorem axioms are propext and Quot.sound.

The 22 event and 13 closure controls include duplicate identity, conflicting current versions, stale binding, independent support, cyclic support, a 128-node reversed chain and event permutations. They are component tests. The real corpus slice, full kernel soundness, unconditional completeness, order theorem, decoder and queries remain in STATUS.md.
