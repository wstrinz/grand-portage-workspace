# Phase 3a report

Authority: post-G2 handoff §3 and Addendum A §3. Will continued past G3a-0 on 2026-10-02. This report is for external review; several rulings are pending (see the last section).

## What exists

**Profile** (`profile/`, Mathlib-free, on HexMvPoly). It has:
- the canonical statement AST, with kinds EMPTY, NONEMPTY, IN_IDEAL, VANISHES_ON, NOT_IN_IDEAL, NONUNIT and COVER;
- characteristic-set scopes;
- the C1, C2 and C3 checkers, with computed reach, run as exact rational replay (an F_p replay is the rational residual vanishing mod p);
- the K3 rules R1–R4 with C4 relation certificates (carry kind 3);
- a plan engine, family adapters and an untrusted proposer behind the commit guard.

**Binding** (`binding/`, Mathlib `85e3a25e`):
- **soundness:** `check_sound`, rule soundness, and `fold_held_meaning_rules`, which says every claim the Kernel fold holds means its statement in every field of its scope;
- **binder:** the explicit statement form, `means_of_warranted`, the binder export, and generated theorem warrants.

Everything uses standard axioms only and is replayed by `leanchecker`. The Kernel pin is unchanged since G2.5.

## G3a conditions

| Condition | Status |
|---|---|
| 3a-owned cases through the shared frontend | **68 of 78** (provisional ownership): 69 rows agree, 0 losses among those run. 10 wait on rulings |
| Zero false ACCEPTs across all 239 profile cases | **Met.** Strict input keys turned 9 earlier false ACCEPTs into losses |
| Reach slice, including Fano and an earned widening | Met (reach slice, 19/19) |
| Checkers admitted | Met: soundness, adversarial controls, TCB entries, overlapping tool named (`linear_combination`) |
| K3 rules: carry kind and proved direction tables | Met (`r1_sound` … `r4_sound`) |
| Binder; A4 costs measured and policy applied | Binder exists. Theorem warrants are minted for C1 emptiness over ℚ, at 0.6–5.7 s each above imports, and support their claims; other shapes stay receipt-only |
| Oracle disagreements triaged | 25 inferences, **0 disagreements** |
| Kernel cases re-executed | 14, all schematic. Each is recorded with its proved profile analogue |

Receipts:
- [PHASE-3A-CORPUS.json](PHASE-3A-CORPUS.json)
- [PHASE-3A-SAFETY.json](PHASE-3A-SAFETY.json)
- [PHASE-3A-SLICE.json](PHASE-3A-SLICE.json)
- [PHASE-3A-BINDER.json](PHASE-3A-BINDER.json)
- [PHASE-3A-DIFFERENTIAL.json](PHASE-3A-DIFFERENTIAL.json)
- [PHASE-3A-KERNEL-REEXEC.json](PHASE-3A-KERNEL-REEXEC.json)
- [PHASE-3A-EXPRESSIVENESS.json](PHASE-3A-EXPRESSIVENESS.json)

## Findings

- **About half of the title-assigned 3a cases are not Nullstellensatz claims over fields.** Of 118:
  - 20 need 3b features: extension-field points, number-field fixtures and point universes;
  - 10 use ring contexts: ℤ, ℤ[i] and the zero algebra;
  - 10 test v0.37 operation contracts;
  - 7 are schematic, with no data;
  - 8 needed new statement kinds.
- **The frontend must never read past a key it doesn't understand.** The first safety run accepted 8 must-REFUSE cases, a ninth later, because adapters ignored keys such as `equations`, `question` or a nested `selected_real_interval`. Families now declare their exact keys at every level.
- **Characteristic scopes are absolute.** A char-0 claim in 3a covers every char-0 field. The ML8 base-extension errors the oracle retrodicts can't occur in 3a, but neither can the correct base-field-only claims be stated. They belong to 3b.
- **Kernel replay of the checker doesn't scale.** `decide +kernel` on X125 exceeded 24 GB. Warrants come from generated `linear_combination` proofs instead.

## Convergence (A5)

Over the 3a corpus run:
- **(a)** 34 cases ACCEPT, with 44 held requested claims. 3 of them also carry standard-axiom theorem warrants: the C1 shapes the generator covers. The rest are receipt-backed, though most could be warranted within budget once the generator covers C2, C3 and the new kinds.
- **(b)** The 44 held claims, by kind: 31 IN_IDEAL (mostly ambient identities and custody), 5 NONEMPTY, 3 EMPTY, 3 COVER, and 1 each of NOT_IN_IDEAL and NONUNIT. Widenings were filed in 40 cases (EARNED). The custody cases are CUSTODY by construction.
- **(c)** Theorem cost stays small, so the Lean-theorem share is limited by generator coverage, not by cost. GP's distinct contributions remain computed reach, refusal at elaboration and strict well-formedness, custody, and the earned surface.

## Decisions taken (provisional, for review)

- **Ownership moves:** 20 cases to 3b, 10 to campaign-op; ring-context cases pending.
- **AST extensions:** NOT_IN_IDEAL, NONUNIT and COVER.
- **IN_IDEAL** means some h·G^k lies in `Ideal.span` of the equations. Its R2 transport needs an ideal-level inclusion with identical guards.
- **Unnamed fields default to ℚ.** COVER certificates are built by literal branch inclusion.
- **Elaboration refusals** (undeclared variable, incomplete map) count as refusals.
- **The binder trusts its export** of the registry it was compiled against (see the TCB entry).

## Pending rulings

1. The 33 + 10 ambiguous gate owners, and the provisional moves.
2. Instantiation fixtures for the 7 schematic cases.
3. X120 (non-zerodivisor), X141 (completeness) and X138 (no saturating element).
4. Whether rings are in scope for any profile.
5. Fano corpus intake (`corpus/CHANGES.md`, proposed).

On pass, `v0.50.0-alpha` prep follows §1.12; publication needs your approval.
