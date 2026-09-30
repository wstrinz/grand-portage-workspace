# Grand Portage status
Updated 2026-09-30. Authority: [Phase 2 handoff](docs/GP-0.50-PHASE-2-HANDOFF.md) and [decisions](DECISIONS.md).

Phase 0 is complete; G1 is closed by Will's documented 52/67 coverage exception. Phase 2 now has a raw JSON decoder and executable warrant-to-held pipeline.

The decoder rejects unknown constructors/statuses, wrong types, missing/extra fields and duplicate object keys, including escaped equivalents. The pipeline resolves explicit versions and targeted retractions, validates evidence through supplied capabilities, computes support closure, and projects held claims. Default admission refuses everything; theorem pointers remain inert.

Lean proves finite support reachability equivalence, support-graph order/duplicate invariance, and exact held/reachable-warrant equivalence for the actual fold. Independent kernel checks passed using only the three allowed standard axioms. Whole-kernel semantic soundness and general event-order independence remain open.

There are 335 passing component controls: 247 decoder, 23 runtime and 65 earlier foundation controls. Runtime controls include raw JSON through held, stale bindings, independent support, failed retries, missing premises, cycles and narrowing. Test capabilities are explicit seams; no corpus slice or mathematical checker admission is claimed.

All 459 case bytes and expectations remain unchanged. The registry is complete: 79 kernel, 239 profile, 94 adapter, 17 surface and 30 host.

Sol owns exact rational cofactor replay, its soundness proof and adversarial tests. Next: integrate that stub with exact statement/input binding, execute the real ten-case slice, then finish semantic soundness, conflict/release handling and queries.

Implementation checkpoints are local; the reviewed handoff and predecessor freeze are published. Heartbeats remain paused.

- [Lean package](phase2/lean/README.md)
- [Execution plan](docs/PHASE-2-PLAN.md)
- [Core contract](SPEC-CORE.md)
- [Standing limits](LIMITS.md)
