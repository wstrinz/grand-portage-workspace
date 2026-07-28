/-
# Are the four gated conditions one condition?

`Identity.lean` ended with a conjecture: `ring_iso`, `identity_origin`,
`integral` and `coefficients_in_base` all *look* like instances of

    Carries φ I J := ∀ f, I f → J (φ f)

checked differently because the maps differ.

**They are not.**  Working through them turns up three distinct shapes, and
saying which is which explains why the eight gated cells resisted compression
while the point cells did not.
-/

import GrandPortage.Identity

namespace GrandPortage

universe u

/-- The converse of `Carries`: the map pulls the target ideal back INTO the
    source one.  Nothing in the earlier file needed this, which is why the
    conjecture looked plausible. -/
def Reflects {R S : Type u} (φ : R → S) (I : Ideal R) (J : Ideal S) : Prop :=
  ∀ f, J (φ f) → I f

/-! ## Shape 1 — `identity_origin : AMBIENT` is not about the map at all

An AMBIENT rewriting holds in the shared coordinate ring BEFORE any of the
model's equations are imposed.  So it is not a claim modulo `I` that happens to
survive: it is a claim modulo the ZERO ideal, and the zero ideal is inside
every ideal.

The condition therefore strengthens the HYPOTHESIS rather than constraining the
map, and the transport is the contravariance theorem applied from a smaller
ideal.  A corollary, not a new rule. -/

def zero {R : Type u} [OfNat R 0] : Ideal R := fun f => f = 0

/-- The zero ideal sits inside every ideal, provided the ideal contains 0. -/
theorem zero_grows {R : Type u} [OfNat R 0] {I : Ideal R} (h0 : I 0) :
    IdealGrows zero I := by
  intro f hf
  simp only [zero] at hf
  exact hf ▸ h0

/-- AMBIENT identities cross to ANY model in the same ring, in either
    direction, and this is `eqMod_against` from the zero ideal.  Nothing about
    `φ` appears. -/
theorem ambient_crosses_anywhere {R : Type u} [Sub R] [OfNat R 0]
    {I : Ideal R} (h0 : I 0) {f g : R} :
    EqMod zero f g → EqMod I f g :=
  eqMod_against (zero_grows h0)

/-! ## Shape 2 — descent needs `Reflects`, and `Carries` will not do

`coefficients_in_base` gates BASE_EXTENSION in the AGAINST direction: an
identity over the big field descends when both sides lie in the base.  That is
a statement about pulling BACK, and `Carries` is the wrong arrow.

The counterexample is the one from `Identity.lean` wearing a different hat.
Take `φ = id` on `ℤ`, source ideal `(0)`, target ideal `(2)`. -/

theorem carries_zero_to_evens : Carries id zeroI evens := by
  intro f hf
  simp only [zeroI] at hf
  simp only [evens, id_eq]
  exact ⟨0, by omega⟩

/-- `Carries` holds and descent still fails.  So a condition of `Carries` shape
    cannot be what licenses BASE_EXTENSION/AGAINST. -/
theorem carries_does_not_give_descent :
    ¬ (∀ {R S : Type} [Sub R] [Sub S] (φ : R → S) (I : Ideal R) (J : Ideal S),
        Carries φ I J → ∀ f g, EqMod J (φ f) (φ g) → EqMod I f g) := by
  intro h
  have h2 : EqMod evens (id 2) (id 0) := by
    simp only [EqMod, evens, id]
    exact ⟨1, by omega⟩
  have hz : EqMod zeroI 2 0 := h id zeroI evens carries_zero_to_evens 2 0 h2
  simp only [EqMod, zeroI] at hz
  omega

/-- What descent actually needs.  Not a condition on the claim's coefficients
    per se -- that is how you CHECK it -- but the reflection property those
    coefficients buy. -/
theorem reflects_gives_descent {R S : Type u} [Sub R] [Sub S]
    (φ : R → S) (hφ : ∀ a b : R, φ (a - b) = φ a - φ b)
    {I : Ideal R} {J : Ideal S} (h : Reflects φ I J) {f g : R} :
    EqMod J (φ f) (φ g) → EqMod I f g := by
  intro hfg
  apply h
  rw [hφ]
  exact hfg

/-! ## Shape 3 — `ring_iso` is both arrows at once

An EQUIVALENCE licenses IDENTITY in BOTH directions, and that is exactly
`Carries` together with `Reflects`.  The kernel's own warning is that a
bijection on POINTS does not give this: `V(x²)` and `V(x)` have the same single
solution and different coordinate rings.  Points give neither arrow. -/

structure RingIso {R S : Type u} (φ : R → S) (I : Ideal R) (J : Ideal S) where
  carries : Carries φ I J
  reflects : Reflects φ I J

theorem ringIso_both_ways {R S : Type u} [Sub R] [Sub S]
    (φ : R → S) (hφ : ∀ a b : R, φ (a - b) = φ a - φ b)
    {I : Ideal R} {J : Ideal S} (iso : RingIso φ I J) {f g : R} :
    EqMod I f g ↔ EqMod J (φ f) (φ g) :=
  ⟨eqMod_transports φ hφ iso.carries, reflects_gives_descent φ hφ iso.reflects⟩

/-! ## The answer

Three shapes, not one:

    identity_origin : AMBIENT    the claim lives at a SMALLER ideal
                                 (nothing about the map)
    coefficients_in_base         REFLECTS  (pull back)
    ring_iso                     CARRIES and REFLECTS
    integral                     CARRIES is even DEFINED -- reduction mod p
                                 is undefined on a coefficient with p in its
                                 denominator, so this gates the existence of
                                 φ rather than a property of it

So the conjecture is refuted, and the refutation is more useful than the
compression would have been.  The eight gated IDENTITY cells did not collapse
because they are answering four different questions:

  * does the claim hold in a smaller ideal than declared?
  * does the induced map push the ideal forward?
  * does it pull the ideal back?
  * is the induced map defined at all?

A single `Carries` gate would have licensed descent, which the counterexample
above refutes outright.  That is the concrete cost of the compression that did
not happen. -/

end GrandPortage
