# Grand Portage status
Updated 2026-10-02. Authority: [post-G2 handoff](docs/GP-0.50-POST-G2-HANDOFF.md), [Addendum A](docs/GP-0.50-POST-G2-ADDENDUM-A.md) and [decisions](DECISIONS.md).

**Where things stand.** Phases 0–2 are complete (G2 ratified 2026-10-02). Phase 2.5 is complete (G2.5 ratified 2026-10-02): the Lean package is split into a pinned 22-module `Kernel`, `Stub` and `Run`; profiles are split into executable `ProfileOps` and a universe-polymorphic `Profile`; all packages use Lean `v4.34.0-rc2`, Hex v0.6.0 and Mathlib `85e3a25e`.

**What is proved.** The finite fold is sound, complete, order independent, total and deterministic, using only standard axioms. Retraction removes exactly the claims whose every derivation used it; failed retries never revoke support; circular support never bootstraps. Sound validator contracts exclude confirmed conflicts; the ratified faulty-checker demonstration freezes release while keeping held closure. Each case family has its own kernel-checked harness: held claims mean only their stated, often conditional, statements, and every refusal family has an explicit Lean countermodel.

**What the families check.** Exact theorem premises and section certificates; context reach; frozen open-premise slots; evidence versus labels (with real cofactor replay); a proved rule-closure contract; and native lifecycle concerns, where withdrawal never hides live traffic, supersession never repoints, and AMEND is computed from pinned licensing fields.

**Not claimed.** No production profile, checker admission, census, field or class-group mathematics is certified. Conditional harnesses assume named premises; OPEN premises stay open.

**Validation.** A fresh full run at rc2 passes all 386 tests/1,130 subtests. Every Kernel module passes `leanchecker`, and all 1,054 Kernel constants use only standard axioms. All 79 and 459 legacy cases are unchanged. Kernel logic is 382 lines against 500.

**Next.** Will chose to continue at G3a-0 ([checkpoint](reports/G3A-0-CHECKPOINT.md)). In progress: C1–C3 admission (Mathlib soundness theorems), then the binder, `GATE-OWNERS.json` and broad corpus runs. Heartbeats remain paused.

- [Phase 2.5 report](reports/PHASE-2.5-REPORT.md)
- [Executed slice](reports/PHASE-2-SLICE.md)
- [Standing limits](LIMITS.md)
