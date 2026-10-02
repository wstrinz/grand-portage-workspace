# Grand Portage 0.50 — WIP for review

This is a separate rework of Grand Portage. Its review shadow is [wstrinz/grand-portage-workspace](https://github.com/wstrinz/grand-portage-workspace); work lands on codex/phase-0 and is merged into master, which also keeps the v0.37 package and history (its README is in [HISTORY/README-v0.37.md](HISTORY/README-v0.37.md)). **It is not a production release.** Phases 0–2 are complete: Will ratified G2 on 2026-10-02 after all 79 kernel-tagged corpus cases executed through the native Lean kernel. Phase 3 is next.

The intended guarantee is that accurately specified claims are held only through current, bound evidence and sound admitted rules, throughout their stated scope. GP also aims to expose consequences reachable within a declared finite closure domain. It cannot establish the intended meaning of a wrongly specified problem.

## Start here

Read [STATUS.md](STATUS.md) for the current checkpoint, [Phase 2 plan](docs/PHASE-2-PLAN.md) for execution order and [LIMITS.md](LIMITS.md) for standing limits.

1. [Review guide](REVIEW.md): reading order, questions and reproduction limits.
2. [Core specification](SPEC-CORE.md): the ratified core contract.
3. [Phase 1 parent review](reports/PHASE-1-PAPER-PARENT-REVIEW.md): coverage and the exact decision boundary.
4. [Adoption proposals](reports/PHASE-1-ADOPTION-PROPOSAL.md) and [contract checklist](reports/PHASE-1-CONTRACT-CHECKLIST.md).
5. [Trust observations](TCB.md), [prior-art review](PRIOR-ART.md) and [Phase 0c completion](reports/PHASE-0C-COMPLETION.md).

Read [BACKBRIEF-REV3.md](BACKBRIEF-REV3.md), [DECISIONS.md](DECISIONS.md) and the retained [revision 3 packet](docs/GP-0.50-REWORK-PACKET-rev3.md) for authority and context. Approved decisions amend the verbatim packet; older reports retain the state at their creation.

## Current checkpoint

- **Phase 0:** bounded predecessor/campaign intake, regression corpus, prior-art review, private freeze preparation and Lean feasibility spike complete. G0 continuation was explicitly ratified with limits.
- **Corpus:** 459 source-linked cases with fixed expectations, pinned oracle identity and immutable replay history. See [corpus/README.md](corpus/README.md) and [oracle/PIN.json](oracle/PIN.json).
- **Inventory:** 115 descriptive incident/correction/diagnostic/design owners, not 115 independent incidents. Costs and shipping remain mostly unknown; the cost-based pivot percentages remain indeterminate. See [INCIDENT-INVENTORY.md](INCIDENT-INVENTORY.md).
- **Lean feasibility:** 41 bounded controls passed; actual A08b/A05 Mathlib proofs were checked. The spike is illustrative code, not an admitted checker or production kernel. Native LRAT has explicit runtime/compiler trust.
- **Phase 1:** ratified core spec and a 64-line Mathlib-free soundness obligation that elaborates. Its production implementation slot remains unimplemented; no global runtime soundness proof is claimed.
- **Paper coverage:** 52/67 primary non-MEANING owners expressible, 8 outside the core guarantee, 7 unresolved. This is architectural paper representation, not an executed prevention rate. 77.6% is below a strict 80% minimum; no numerical pass is asserted.
- **G1 is closed:** Will ratified the design directions and 52/67 coverage exception.
- **Phase 2 (G2 ratified):** a Mathlib-free Lean kernel under [phase2/lean](phase2/lean) with proved soundness, completeness, order independence, lifecycle properties and totality; all 79 kernel cases execute natively. See the [executed slice](reports/PHASE-2-SLICE.md), [TCB](TCB.md) and [closeout](reports/PHASE-2-CLOSEOUT.md). Package/checker admission remains separate.

[STATUS.md](STATUS.md) is the current human status. Phase reports retain their historical evidence.

## Working data and reproduction

Local work lives at F:/repos/grandportage-0.50; predecessor/campaign repositories are read-only sources. Private verbatim harvests, oracle checkout, dependency caches, generated builds, virtual environment and scratch data are excluded from Git. Tracked reports preserve pointers and hashes, not all source bytes needed for independent replay.

Existing local checks, from that workspace:

```powershell
./.venv/Scripts/python.exe -B tools/check-corpus.py
./.venv/Scripts/python.exe -B tools/check-incidents.py
```

These require the pinned local sources/private custody files and the dependencies in requirements-dev.txt. A fresh clone alone does not reproduce the complete historical validation. The corpus runner's --run-oracle option creates a new replay; it is not needed for documentation review.

Will separately authorized the exact [freeze patch](reports/freeze-v0.37.1/README-REVIEW.md). Its publication state is recorded in STATUS.md.
