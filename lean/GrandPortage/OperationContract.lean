/-
# Operation contracts: semantics are stronger than local validation

An operation contract must keep three things separate:

  * the mathematical relation the operation intends to construct;
  * the weaker guarantee established by the available local checkers;
  * the transport consequences licensed by that checked guarantee.

If those collapse into one predicate, a successful translation-validation
check can silently become a theorem that the backend computed the complete
mathematical object.  Saturation is the first executable instance because the
current runtime makes the distinction concrete:

    source containment       I ⊆ J
    generator certificates  recorded generators of J lie in I : f^∞
    exact saturation         J = I : f^∞

The first two are checked independently.  They do not imply the third.
-/

import GrandPortage.Localization

namespace GrandPortage

universe u v w

/-- A backend-neutral semantic contract for one model-changing operation.

    `semanticRelation` says what a mathematically exact implementation means.
    `checkedGuarantee` says only what the current translation validators earn.
    The required theorem points from exact semantics to the checked guarantee,
    deliberately not in the tempting and generally false reverse direction.

    Preconditions may mention both endpoints. A computed target has
    well-formedness obligations of its own; forcing those into source data would
    hide exactly the output boundary this record is meant to expose. -/
structure OperationContract (Params : Type u) (Source : Type v)
    (Target : Type w) where
  precondition : Params → Source → Target → Prop
  semanticRelation : Params → Source → Target → Prop
  checkedGuarantee : Params → Source → Target → Prop
  semantics_entails_checked :
    ∀ p source target,
      precondition p source target →
      semanticRelation p source target →
      checkedGuarantee p source target

/-- The semantic parameters of a saturation run include both the polynomial
    inverted and the generators actually recorded at the runtime boundary. -/
structure SaturationParams (R : Type u) where
  f : R
  recordedGenerator : R → Prop

/-- The exact meaning of a saturation result `J`: membership in `J` is
    precisely membership in `I : f^∞`. -/
def SaturationSemantics {R : Type u} [Mul R] [OfNat R 1]
    (p : SaturationParams R) (I J : Ideal R) : Prop :=
  ∀ g, J g ↔ SatMem I p.f g

/-- The endpoint facts needed to interpret the local checks: `1` is a left
    identity, and every recorded output generator denotes a member of `J`.

    The latter is definitional for the runtime model's generator list, but it
    must be explicit in this predicate-only Lean model. -/
def SaturationPrecondition {R : Type u} [Mul R] [OfNat R 1]
    (p : SaturationParams R) (_I J : Ideal R) : Prop :=
  (∀ g : R, 1 * g = g) ∧
  (∀ g, p.recordedGenerator g → J g)

/-- Exactly what Grand Portage's two independent checks currently establish.

    `containsSource` is the edge-containment check. `noInventedGenerator` is
    the operation-output certificate for each RECORDED GENERATOR. It does not
    quantify over every member of `J`: lifting generator certificates to the
    generated ideal requires algebraic closure facts absent from the current
    predicate-only `Ideal` model. -/
structure SaturationChecked {R : Type u} [Mul R] [OfNat R 1]
    (p : SaturationParams R) (I J : Ideal R) : Prop where
  containsSource : IdealGrows I J
  noInventedGenerator : ∀ g, p.recordedGenerator g → SatMem I p.f g

/-- Ordinary ideal membership gives saturation membership whenever `1` acts
    as a left identity.  This generalizes `mem_satMem` beyond `Int` without
    importing Mathlib's algebraic hierarchy. -/
theorem mem_satMem_of_one_mul {R : Type u} [Mul R] [OfNat R 1]
    (one_mul : ∀ g : R, 1 * g = g) {I : Ideal R} {f g : R}
    (h : I g) : SatMem I f g :=
  ⟨1, PowerOf.one, by rw [one_mul]; exact h⟩

/-- Exact saturation entails both checks for every well-formed recorded
    generator list. -/
theorem saturation_semantics_entails_checked
    {R : Type u} [Mul R] [OfNat R 1]
    (p : SaturationParams R) (I J : Ideal R)
    (pre : SaturationPrecondition p I J)
    (h : SaturationSemantics p I J) :
    SaturationChecked p I J := by
  constructor
  · intro g hg
    exact (h g).2 (mem_satMem_of_one_mul pre.1 hg)
  · intro g recorded
    exact (h g).1 (pre.2 g recorded)

/-- Saturation as an operation-contract instance. -/
def saturationContract {R : Type u} [Mul R] [OfNat R 1] :
    OperationContract (SaturationParams R) (Ideal R) (Ideal R) where
  precondition := SaturationPrecondition
  semanticRelation := SaturationSemantics
  checkedGuarantee := SaturationChecked
  semantics_entails_checked := saturation_semantics_entails_checked

/-! ## What the checked guarantee licenses -/

/-- Source identities remain valid on the checked saturation result.  This is
    the `NECESSARY_CONDITION / AGAINST / IDENTITY` theorem for saturation,
    derived from the independently checked `containsSource` field. -/
theorem saturation_checked_transports_identity_against
    {R : Type u} [Mul R] [OfNat R 1] [Sub R]
    {p : SaturationParams R} {I J : Ideal R}
    (checked : SaturationChecked p I J) {lhs rhs : R} :
    EqMod I lhs rhs → EqMod J lhs rhs :=
  eqMod_against checked.containsSource

/-! ## And what it does not license -/

/-- A single recorded generator for the ideal `(6)`. -/
def sixGenerator : Int → Prop := fun n => n = 6

/-- Saturation at `2`, with `(6)` recorded by its generator `6`. -/
def sixesSaturationParams : SaturationParams Int where
  f := 2
  recordedGenerator := sixGenerator

/-- The recorded generator really belongs to the declared output ideal. -/
theorem sixes_saturation_precondition :
    SaturationPrecondition sixesSaturationParams sixes sixes := by
  constructor
  · intro g
    exact Int.one_mul g
  · intro g recorded
    simp only [sixesSaturationParams, sixGenerator] at recorded
    subst g
    exact ⟨1, by omega⟩

/-- The unchanged ideal `(6)` passes both local checks: it contains the source
    and its recorded generator has a saturation witness. -/
theorem sixes_checked_as_output :
    SaturationChecked sixesSaturationParams sixes sixes := by
  constructor
  · intro g hg
    exact hg
  · intro g recorded
    simp only [sixesSaturationParams, sixGenerator] at recorded
    subst g
    exact mem_satMem ⟨1, by omega⟩

/-- But that checked output is not the exact saturation: `3` is in
    `(6) : 2^∞` and not in `(6)`. Thus local validation cannot be promoted to
    exact operation semantics. -/
theorem checked_does_not_imply_saturation_semantics :
    ¬ SaturationSemantics sixesSaturationParams sixes sixes := by
  intro h
  exact three_not_mem_sixes ((h 3).2 three_satMem_sixes)

/-- Even exact saturation does not let a derived identity travel back to the
    ambient ideal.  This pins the refused ALONG direction independently of the
    implementation or its local checker. -/
theorem exact_saturation_does_not_transport_identity_along :
    let saturated : Ideal Int := fun g => SatMem sixes 2 g
    SaturationSemantics sixesSaturationParams sixes saturated ∧
      EqMod saturated 3 0 ∧ ¬ EqMod sixes 3 0 := by
  dsimp [SaturationSemantics, sixesSaturationParams]
  constructor
  · intro g
    rfl
  constructor
  · simpa [EqMod] using three_satMem_sixes
  · simpa [EqMod] using three_not_mem_sixes

end GrandPortage