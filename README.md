# grand-portage-lean

A shadow formalisation of Grand Portage's transport calculus. **Not
authoritative.** Its job is to try to break the ontology, not to bless it.

## Why it exists

A measurement against the Python kernel found the transport table splits into
two halves with very different characters:

|                    | agree with the generic rule | disagree | conditional |
|--------------------|------|------|------|
| point cells (36)   | **27** | 3 | 6 |
| IDENTITY cells (12)| 1 | 3 | **8** |

The point half looks like one subset argument repeated. The identity half is
where every hand-entered boolean lives — `ring_iso`, `identity_origin`,
`integral`, `coefficients_in_base` — and none of it follows from points.

That measurement shows the cells are *consistent with* being derived. It does
not show they *are*. Closing that gap is what this is for.

## What is here

`GrandPortage/Points.lean` — models as predicates, `Refines` as inclusion.
The three cells inclusion licenses, proved; the three it refuses, with
countermodels. Plus `Cover` and the partition recombination law, which is why
a partition is a distinct inference form rather than another edge type.

`GrandPortage/Identity.lean` — `EqMod I f g := I (f - g)`, the one identity
cell that derives from ideal containment, and the ℤ counterexample refusing the
other direction. Then `Carries`, the shape the remaining eight gated cells
appear to share: an identity crosses when the induced map sends the source
ideal into the target ideal. **Whether they really are one condition is open.**

## Trust

No `sorry`. Mathlib-free — core Lean only, so a fresh `lake build` is seconds
rather than an afternoon. Axiom audit:

```
hasPoint_along, isEmpty_against, everywhere_against   no axioms
isEmpty_not_along, hasPoint_not_against               no axioms
cover_empty, eqMod_against, eqMod_both_ways           no axioms
eqMod_transports                                      no axioms
everywhere_not_along                                  propext
eqMod_not_along                                       propext, Quot.sound
```

Both non-empty entries come from `simp`/`omega` on concrete decidable goals,
not from anything load-bearing.

## Build

```bash
lake build
```
