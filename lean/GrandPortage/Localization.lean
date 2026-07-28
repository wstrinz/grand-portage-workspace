/-
# Does RESTRICTION mean the same ideal, or the localized algebra?

The kernel says one thing and `operations.localize` says another, written a day
apart:

  the ledger    "a restriction adds no equations, so both ends share a ring and
                 an ideal"        -- hence IDENTITY/ALONG unconditional
  localize      "the open locus D(f) has the same ideal WITH f INVERTED"

Both are coherent readings of "restrict to where f is nonzero".  They are not
the same reading, and this file shows they license different transport.

Mathlib-free, so `Monoid` and `pow` are unavailable; `PowerOf` below is the
inductive that stands in for "some power of f", which is all the argument needs.
-/

import GrandPortage.Identity

namespace GrandPortage

universe u

/-- `PowerOf f m` -- `m` is one of `1, f, f*f, ...`.

    Stated inductively rather than as `f ^ n` because this development has no
    Mathlib and therefore no `Monoid`.  Nothing below needs an exponent, only
    the existence of SOME power, so the weaker structure is enough. -/
inductive PowerOf {R : Type u} [Mul R] [OfNat R 1] (f : R) : R → Prop
  | one : PowerOf f 1
  | step {m : R} : PowerOf f m → PowerOf f (f * m)

/-- Membership in the localized algebra, pulled back along `R → R_f`.

    `g` becomes zero in `R_f` exactly when some power of `f` kills it into `I`;
    that set is the saturation `I : f^∞`.  This is the honest content of the
    phrase "f is inverted". -/
def SatMem {R : Type u} [Mul R] [OfNat R 1] (I : Ideal R) (f g : R) : Prop :=
  ∃ m, PowerOf f m ∧ I (m * g)

/-- READING (a) IMPLIES READING (b): anything already in the ideal is zero in
    the localization too, witnessed by the power `f^0 = 1`. -/
theorem mem_satMem {I : Ideal Int} {f g : Int} (h : I g) : SatMem I f g :=
  ⟨1, PowerOf.one, by rw [Int.one_mul]; exact h⟩

/-! ## And the converse fails, which is the whole question. -/

def sixes : Ideal Int := fun n => ∃ k, n = 6 * k

/-- `2 * 3 = 6`, so `3` dies in the localization at `2`. -/
theorem three_satMem_sixes : SatMem sixes 2 3 :=
  ⟨2 * 1, PowerOf.step PowerOf.one, ⟨1, by decide⟩⟩

/-- `3` is not in `(6)`. -/
theorem three_not_mem_sixes : ¬ sixes 3 := by
  intro h; obtain ⟨k, hk⟩ := h; omega

/-- THE POINT.  Zero in the localization does not mean zero in the ring.

    The polynomial version is the one the review supplied: in `k[x,y]/(xy)`
    localized at `x`, `y = 0` because `x` is invertible and `xy = 0`, while
    `y ≠ 0` in the ambient ring.  `(6)` at `2` is the same phenomenon with
    smaller numbers, and `PowerOf` makes it checkable without Mathlib. -/
theorem satMem_not_mem :
    ¬ (∀ (I : Ideal Int) (f g : Int), SatMem I f g → I g) :=
  fun h => three_not_mem_sixes (h sixes 2 3 three_satMem_sixes)

/-! ## What that settles

Under READING (a), an IDENTITY at the open model means `lhs - rhs ∈ I`.  Both
ends carry the same ideal, `EqMod` is literally the same proposition at each,
and transport in both directions is unconditional.  The kernel cell is CORRECT.

Under READING (b), it means `SatMem I f (lhs - rhs)`, and transporting back to
the ambient model needs plain membership -- which `satMem_not_mem` refutes.
The cell would need a gate, and the gate is exactly `∃ m, PowerOf f m ∧
I (m * (lhs - rhs))`.

THE PROJECT SHOULD TAKE (a), and not for convenience.  RESTRICTION was earned
by a semialgebraic positivity cone -- a condition on POINTS, in the same
coordinates, adding no equations.  Its six point-cells are identical to
NECESSARY_CONDITION's precisely because they follow from `Refines` and nothing
else, which `Points.lean` proves generically over any `Model`.  Reading (b)
changes the coordinate ring, so it is not a `Model α` refinement at all and
that whole column would have to be re-earned.

So the defect is not in the kernel.  It is that `localize` DESCRIBES itself as
(b) while EMITTING (a): it hands back a model whose `generators` are copied
across unchanged -- reading (a) -- under prose saying `f` is inverted.

And the object reading (b) wants already exists: `saturate_closure` emits
`I : f^∞`, whose members are exactly the `SatMem` ones.  Its identities are
DERIVED, and NECESSARY_CONDITION/ALONG/IDENTITY refuses a DERIVED rewriting, so
that path is already sound without a new gate.  The two constructors were
always the two readings; only the prose confused them. -/

end GrandPortage
