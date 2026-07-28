# Experiment B: are hand-declared relation types mislabelled often enough to justify building constructors?

**Run 2026-07-28 against all 57 edges in five live campaigns.**

## Why this shape

The planned form was: run identical tasks twice, once with the caller naming
the relation type and once with a structured operation emitting the program and
the relation together. That needs constructors to exist — and the whole point
of the experiment is deciding whether to build them. Circular.

The cheaper form uses data we already have. Every edge carries a `why` field
stating what the step did. **The type is determined by the `why`**, so auditing
declared-type against why-text measures the same thing without building
anything, on real campaign data rather than synthetic tasks.

**Bias, stated up front:** I am the judge, and I wrote some of these edges. The
mitigation is that the `why` is usually mechanical — "drops the equation
s13 = 0" determines `NECESSARY_CONDITION` and nothing else — and that every
call requiring judgement is listed separately below rather than folded into the
headline number.

## Result

| | count | rate |
|---|---|---|
| edges audited | 57 | |
| **clear mislabels** | **7** | **12%** |
| judgement calls, arguably mislabelled | 6 | 11% |
| clearly correct | 44 | 77% |

### The seven clear mislabels

| edge | declared | should be | why |
|---|---|---|---|
| `e.checkres` | `UNTYPED` | a **doubt** | "Nothing relates the two" |
| `GE4` | `UNTYPED` | a **doubt** | "Nothing established relates the (50,75) replay to (75,125)" |
| `GE5` | `UNTYPED` | a **doubt** | "share NOT ONE VARIABLE" |
| `GE6` | `UNTYPED` | a **doubt** | "Two distinct layers that share a NAME and nothing else" |
| `GE10` | `UNTYPED` | a **doubt** | "Nothing derived here fixes the gamma=4 degree cap" |
| `e.sh3` | `SPECIALIZATION` | no type fits | restricts an *index*, 0..526 down to three values |
| `E-IV-PD` | `UNTYPED` | `RESTRICTION` | "Forgets that Omega is positive definite" |

### The six judgement calls

- `E_LAUR` — `NECESSARY_CONDITION` for a **localisation** (`K[x,y] → K[x,y,y⁻¹]`).
  Dropping `y ≠ 0` is dropping an inequality, which is `RESTRICTION`.
- `E-G3_ELIM_NO_A5` — `NECESSARY_CONDITION` for dropping a **saturation**
  generator `1 − w·a`, whose content is `a ≠ 0`. Same shape as `E_LAUR`, hidden
  behind the Rabinowitsch trick that turns an inequality into an equation.
- `GE7`, `GE8` — `NECESSARY_CONDITION` for finite covers (determinant −2, −3).
  A morphism with image contained in the target; arguably `IMAGE_CLOSURE`.
- `GE9` — `NECESSARY_CONDITION` for a map explicitly described as "a genuine
  automorphism, so the covering loss of GE7/GE8 is ABSENT here".
- `e.chain14` — an entire chain "composed into one step". Flattening several
  operations of possibly different types into one edge.

## What this actually says about constructors

The headline number is not the useful part. **The mislabels split into
populations, and constructors only reach one of them.**

| population | count | would a constructor fix it? |
|---|---|---|
| no operation happened at all | 5 | **No** — nothing to construct |
| an operation with no vocabulary | 2 | **No** — `e.sh3` restricts an index; `E-IV-PD` needed a type that did not exist |
| localisation / saturation mis-typed | 2 | **Yes** — `Localize(f)` emits the right relation by construction |
| morphism vs relaxation | 3 | **Probably** — an operation object knows it applied a map |
| composite flattened into one edge | 1 | **Yes** — a constructor emits one edge per operation |

So structured operations address roughly **6 of 13** observed mislabels, and
**0 of the 5 largest single category**, which is the one where the author
correctly determined that no relation exists and had no way to say so.

That category is now fixed, and not by constructors: `doubt` landed today.

### The decision rule, applied

The rule set in advance was:

> If hand declarations are nearly as accurate and much cheaper, the frontend
> investment does not pay. If operation-derived contracts sharply cut
> mislabelling, that validates the compiler direction.

Neither branch fires cleanly. Hand declarations are **88% accurate** on clear
calls, which is better than I expected and not good enough to leave alone. But
constructors do not "sharply cut" the observed mislabelling, because most of it
is not about operations.

**Verdict: narrow #27 rather than cancel or fund it in full.** Build
constructors for the operations where mis-typing actually happened and where
the operation determines the answer:

1. `Localize(f)` / `SaturateClosure(I, f)` — kept distinct, because they are
   the two that got confused with `NECESSARY_CONDITION` and with each other.
2. `Eliminate(vars)` — zero observed mislabels (all four `IMAGE_CLOSURE` edges
   are correct), but it is the operation where the *consequence* of a mislabel
   is worst, and the hyperbola example makes the failure demonstrable.

Do **not** build the full sixteen-constructor set until something has needed
it. `AddEquations` / `DropEquations` have 27 instances and zero mislabels —
the caller gets that right every time, so a constructor buys nothing there.

## Correction: an earlier measurement was wrong

`KILL-CRITERIA.md` D1 reported "**zero** ever refined away from `UNTYPED`". That
figure is a **measurement artifact**, not a fact.

The script looked for the *same edge id* changing type between records.
Supersession never does that — it mints a new id and points back. Checking for
back-pointers instead:

```
E-IV-PD  --supersedes--> E-IV-PD-R  --supersedes--> E-IV-PD-RESTRICT
UNTYPED                  RESTRICTION                 RESTRICTION
```

A two-step refinement chain, plus `GE11` added as a typed successor to `GE10`.
So `UNTYPED` **is** refined, in exactly the campaign whose `discharge_hint`
asked for the type that was later built.

The finding underneath D1 survives — five of six `UNTYPED` edges assert that
nothing relates the models, independently confirmed by reading the `why` fields
here. But the number that made it look alarming was measuring the wrong thing.
