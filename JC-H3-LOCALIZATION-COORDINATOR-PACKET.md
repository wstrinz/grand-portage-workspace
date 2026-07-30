# JC H3 localization rendezvous packet

**Update after dispatch:** GP 0.15 now accepts canonical bounded
`sparse_polynomial_v1` evidence without raising the infix parser limits. The
isolated batch replay has verified all twelve frozen q pivots independently
against model digest `a17f0a4fa0ab0b10de3c4e84310ad51ed84d95c0becb93e3dce156cf5c513999`.
This supersedes the packet's request for a first real q pivot. The p-chart
request and every whole-chain/source-membership/H3 refusal remain open. The
0.14 SHA below remains the historical dispatch pin; use the eventual 0.15
release SHA for sparse replay.

**Audience:** lead JC coordinator. **Date:** 2026-07-30.

## Decision

Keep q/p graded elimination in the main JC workstream. Run GP translation and
replay as an isolated side lane. Research agents continue to emit the frozen
native certificate; they do not edit the canonical GP campaign or learn GP's
internal schema.

```text
q/p native calculation
    -> frozen JC certificate
    -> isolated GP adapter and mutation replay
    -> lead review
    -> optional canonical campaign promotion
```

The lead remains the sole owner of truth/status files, the canonical campaign,
and promotion. The adapter lane owns no H3 or source-membership conclusion.

## Why this is on the critical path

The frozen contract declares only `q,t` as units on the q chart and `p,t` on
the p chart. It forbids pivots on `I4`, arbitrary coefficients, residual
polynomials, or merely generic nonzero expressions. This is exactly the
semantic premise needed by every triangular solve, not optional provenance.

GP 0.14's standalone `localization_membership_v1` checker records guards,
denominator powers, an exact guard-monomial multiplier, and membership
cofactors. Its licence is deliberately only an identity in the declared
localized coordinate algebra. It grants neither ambient identity nor point
transport.

## Minimal native replay envelope

Retain the existing pivot fields, and ensure the serialized output also makes
the following available for every pivot after all earlier substitutions:

```json
{
  "chart": "q",
  "model_digest": "a17f0a4fa0ab0b10de3c4e84310ad51ed84d95c0becb93e3dce156cf5c513999",
  "equation_id": "E[2,17]",
  "equation_polynomial": "3*q^2*t*x+p+I4",
  "ring_vars": ["p", "q", "t", "I4", "x"],
  "current_generators": ["15*t^3+1", "3*q^2*t*x+p+I4"],
  "pivot": "x",
  "coefficient": "3*q^2*t",
  "unit_witness": {
    "coefficient": "3",
    "powers": {"q": 2, "t": 1},
    "inverse": "1/(3*q^2*t)"
  },
  "substitution": "-(p+I4)/(3*q^2*t)"
}
```

The present frozen schema names `equation`, but an identifier alone is not
enough for independent replay. GP needs the exact post-restriction,
post-substitution polynomial and the generator list against which the step is
claimed. For the local solve identity, the singleton list containing that exact
pivot equation is already a sufficient ideal-membership basis; GP does not need
the entire 115-equation state. These fields may be placed in a separate replay
envelope rather than changing the research certificate if that preserves the
frozen interface more cleanly.

The p producer's `normalize` function also returns receipts for a cleared
declared-unit denominator, a stripped `p^a*t^b` unit, and stripped rational
content. The current elimination loop discards that receipt object. This is
sound inside the JC lane because its independent replay reconstructs and checks
the normalized state from the original equations. For the first GP pilot,
therefore, the boundary is:

```text
JC independent replay  owns extraction, substitution chain, and normalization
GP adapter             owns the local solve from the replay-accepted polynomial
```

Do not describe the normalized polynomial as ambient-identical to the original
generator. If GP later owns normalization replay too, serialize those receipts
and add a separate localization-equivalence certificate.

## Coordinator instructions

1. Do not block q/p discovery on GP 0.14 integration.
2. Ask each lane to preserve exact post-substitution pivot polynomials and the
   chart/model digest; do not ask it to emit GP JSON.
3. Give the adapter lane one q control, one p control, then the first real pivot
   certificate from each chart.
   The current p producer already has the exact expression as `state[key]`
   immediately before appending `pivot_records`; serializing that value as
   `equation_polynomial` is sufficient. Its independent replay reconstructs
   the same state but does not currently retain the expression or normalization
   receipts in JSON.
4. Treat adapter refusal as an interface or evidence obligation, not as a
   mathematical refutation.
5. Promote only after changed chart, undeclared unit, altered denominator,
   changed equation, wrong cofactor, and cross-chart replay mutations refuse.
6. Keep rows 7--8 coefficient lowering independent. Localization certificates
   must not acquire source-membership authority.

## Version gate

The canonical campaign remains pinned to GP 0.13, graph format 2, epoch 8.
GP 0.14 is committed and pushed on `origin/master` at `8114195` (graph format
3, kernel epoch 9). The coordinator may now pin that exact SHA, but should first
replay and migrate a disposable campaign copy. Do not replace the canonical
graph until the migration and new scope declarations have been reviewed.

## Stop rule

The isolated lane stops after it can translate and mutation-check one q and one
p real pivot, or after it identifies the smallest exact missing field. It does
not expand into general localization, primary decomposition, source membership,
or linearization semantics.
