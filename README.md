# Grand Portage 0.50 — WIP for review

This is a separate rework of Grand Portage, currently at the boundary between specification and kernel implementation. **It is not a production release.** Phase 0 is complete under its recorded source, observation and trust limits; Phase 1 has a reviewed design and paper scoring, with G1 decisions still open.

The intended guarantee is that accurately specified claims are held only through current, bound evidence and sound admitted rules, throughout their stated scope. GP also aims to expose consequences reachable within a declared finite closure domain. It cannot establish the intended meaning of a wrongly specified problem.

## Start here

1. [Review guide](REVIEW.md): reading order, questions and reproduction limits.
2. [Core specification](SPEC-CORE.md): the one-page G1 proposal.
3. [Phase 1 parent review](reports/PHASE-1-PAPER-PARENT-REVIEW.md): coverage and the exact decision boundary.
4. [Adoption proposals](reports/PHASE-1-ADOPTION-PROPOSAL.md) and [contract checklist](reports/PHASE-1-CONTRACT-CHECKLIST.md).
5. [Trust observations](TCB.md), [prior-art review](PRIOR-ART.md) and [Phase 0c completion](reports/PHASE-0C-COMPLETION.md).

Read [BACKBRIEF-REV3.md](BACKBRIEF-REV3.md), [DECISIONS.md](DECISIONS.md) and the retained [revision 3 packet](docs/GP-0.50-REWORK-PACKET-rev3.md) for authority and context. Approved decisions amend the verbatim packet; older reports retain the state at their creation.

## Current checkpoint

- **Phase 0:** bounded predecessor/campaign intake, regression corpus, prior-art review, private freeze preparation and Lean feasibility spike complete. G0 continuation was explicitly ratified with limits.
- **Corpus:** 459 source-linked cases with fixed expectations, pinned oracle identity and immutable replay history. See [corpus/README.md](corpus/README.md) and [oracle/PIN.json](oracle/PIN.json).
- **Inventory:** 115 descriptive incident/correction/diagnostic/design owners, not 115 independent incidents. Costs and shipping remain mostly unknown; the cost-based pivot percentages remain indeterminate. See [INCIDENT-INVENTORY.md](INCIDENT-INVENTORY.md).
- **Lean feasibility:** 41 bounded controls passed; actual A08b/A05 Mathlib proofs were checked. The spike is illustrative code, not an admitted checker or production kernel. Native LRAT has explicit runtime/compiler trust.
- **Phase 1:** 457-word core spec and a 64-line Mathlib-free soundness obligation that elaborates. Its production implementation slot remains unimplemented; no global runtime soundness proof is claimed.
- **Paper coverage:** 52/67 primary non-MEANING owners expressible, 8 outside the core guarantee, 7 unresolved. This is architectural paper representation, not an executed prevention rate. 77.6% is below a strict 80% minimum; no numerical pass is asserted.
- **G1 remains open:** three design sign-offs and a proposed explicit coverage exception/Phase 2 authorization. No package/checker adoption or Phase 2 implementation has begun.

The latest [Phase 1 status](reports/PHASE-1-STATUS.json) and [Phase 0 tracker](reports/PHASE-0-COMPLETION-TRACKER.json) supersede stale historical status text.

## Working data and reproduction

Local work lives at F:/repos/grandportage-0.50; predecessor/campaign repositories are read-only sources. Private verbatim harvests, oracle checkout, dependency caches, generated builds, virtual environment and scratch data are excluded from Git. Tracked reports preserve pointers and hashes, not all source bytes needed for independent replay.

Existing local checks, from that workspace:

```powershell
./.venv/Scripts/python.exe -B tools/check-corpus.py
./.venv/Scripts/python.exe -B tools/check-incidents.py
```

These require the pinned local sources/private custody files and the dependencies in requirements-dev.txt. A fresh clone alone does not reproduce the complete historical validation. The corpus runner's --run-oracle option creates a new replay; it is not needed for documentation review.

The [freeze patch](reports/freeze-v0.37.1/README-REVIEW.md) is prepared only; publishing this WIP rework does not apply it to the predecessor.
