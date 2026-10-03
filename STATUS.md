# Grand Portage status
Updated 2026-10-03. Authority: [post-G2 handoff](docs/GP-0.50-POST-G2-HANDOFF.md), [Addendum A](docs/GP-0.50-POST-G2-ADDENDUM-A.md) and [decisions](DECISIONS.md).

**Where things stand.** Phases 0–2 are complete (G2 ratified 2026-10-02). Phase 2.5 is complete (G2.5 ratified 2026-10-02): the Lean package is split into a pinned 22-module `Kernel`, `Stub` and `Run`; profiles are split into executable `ProfileOps` and a universe-polymorphic `Profile`; all packages use Lean `v4.34.0-rc2`, Hex v0.6.0 and Mathlib `85e3a25e`.

**What is proved.** The finite fold is sound, complete, order independent, total and deterministic, using only standard axioms. Retraction removes exactly the claims whose every derivation used it; failed retries never revoke support; circular support never bootstraps. Sound validator contracts exclude confirmed conflicts; the ratified faulty-checker demonstration freezes release while keeping held closure. Each case family has its own kernel-checked harness: held claims mean only their stated, often conditional, statements, and every refusal family has an explicit Lean countermodel.

**What the families check.** Exact theorem premises and section certificates; context reach; frozen open-premise slots; evidence versus labels (with real cofactor replay); a proved rule-closure contract; and native lifecycle concerns, where withdrawal never hides live traffic, supersession never repoints, and AMEND is computed from pinned licensing fields.

**Not claimed.** No production profile, checker admission, census, field or class-group mathematics is certified. Conditional harnesses assume named premises; OPEN premises stay open.

**Validation.** A full run on 2026-10-03 at rc2 passed 408 of 410 tests (1,674 subtests). The two failures were layer-tag corpus counts made stale by the Fano intake; they were fixed and re-run green. Every Kernel module passes `leanchecker`, and all 1,054 Kernel constants use only standard axioms; the Kernel pin is unchanged. The corpus has 462 cases (the 459 legacy cases unchanged, plus the Fano intake GP-X413–X415). Kernel logic is 382 lines against 500.

**Next.** Phase 3a is built and the 3a.1 patch is in ([report](reports/PHASE-3A-REPORT.md)). All 105 3a-owned cases agree, on 106 rows with no losses, 19 of them through signed instantiation fixtures. There are zero false ACCEPTs across all 242 profile cases. Nine generated theorem warrants are bound at their computed reach. G3a awaits Will's ratification; on pass come the merge to master, `v0.50.0-alpha` prep (publication needs approval) and Phase 4. Heartbeats paused.

- [Phase 2.5 report](reports/PHASE-2.5-REPORT.md)
- [Executed slice](reports/PHASE-2-SLICE.md)
- [Standing limits](LIMITS.md)
