# Phase 2 Lean kernel

Mathlib-free package pinned to Lean 4.32.1. From F:/repos/grandportage-0.50:

```powershell
lake -d phase2/lean build
./phase2/lean/.lake/build/bin/gp_events_tests.exe
./phase2/lean/.lake/build/bin/gp_closure_tests.exe
./phase2/lean/.lake/build/bin/gp_completeness_tests.exe
./phase2/lean/.lake/build/bin/gp_order_tests.exe
./phase2/lean/.lake/build/bin/gp_decoder_tests.exe
./phase2/lean/.lake/build/bin/gp_runtime_tests.exe
./phase2/lean/.lake/build/bin/gp_poly_tests.exe
lake -d phase2/lean env leanchecker -v GP50.ClosureProofs
lake -d phase2/lean env leanchecker -v GP50.ClosureCompleteness
lake -d phase2/lean env leanchecker -v GP50.ClosureOrderProofs
lake -d phase2/lean env leanchecker -v GP50.RuntimeProofs
lake -d phase2/lean env leanchecker -v GP50.Decoder
lake -d phase2/lean env leanchecker -v GP50.PolyStubProofs
```

Events resolves complete event lists using explicit versions and targeted retraction/supersession. Decoder validates the typed wire envelope and rejects duplicate keys before typed admission. Installed Lean JSON still normalizes numeric syntax; raw-byte identity is an adapter contract.

Runtime converts current validated warrants into support nodes, computes finite closure and projects held claims. Entry connects raw decode to fold. Admission is a registry of validator functions; the default refuses all evidence. Runtime tests use explicit component seams, with theorem-name pointers refused.

ClosureProofs proves soundness under node semantic contracts. ClosureCompleteness proves exact finite reachability, including repeated IDs. ClosureOrderProofs proves support membership is invariant under equal complete declaration sets. RuntimeProofs proves held equals reachable warrant-backed claims for the actual fold. Whole-kernel semantic soundness and event-order proof remain in STATUS.md.

PolyStub supplies exact univariate rational cofactor replay. Its proof establishes all-exponent coefficient identity; binding and geometric interpretation remain separate.

The package has 375 passing component controls, including 13,122 finite graphs and 3,072 order transformations. These do not count as G2 corpus passes.
