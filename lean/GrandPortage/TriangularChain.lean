/-
# Ordered solve chains compose semantically

The runtime `localized_triangular_solve_chain_v1` checker validates exact
ordered polynomial substitutions and state fingerprints. It does not mint
this semantic premise. Once every checked solve step has been bound to a
`MappedEquivalence`, however, the entire chain is one mapped equivalence and
emptiness moves in both directions.
-/

import GrandPortage.MappedEquivalence
import GrandPortage.FactorPower

namespace GrandPortage

universe u

/-- Runtime v2 checks `equation = unit * affine + contextDebt`. If the
normalization equations make `contextDebt` zero and the checked coefficient is
interpreted as a unit, equation vanishing forces the normalized affine form to
vanish. -/
theorem normalizedAffine_zero_of_equation_zero
    {R : Type u} [Mul R] [Add R] [OfNat R 0] [OfNat R 1]
    (zeroMul : forall r : R, 0 * r = 0)
    (addZero : forall r : R, r + 0 = r)
    (zeroNeOne : Not ((0 : R) = 1))
    (noZeroDivisors : HasNoZeroDivisors (R := R))
    {equation unit affine contextDebt : R}
    (unitWitness : HasRightInverse unit)
    (receipt : equation = unit * affine + contextDebt)
    (equationZero : equation = 0)
    (contextZero : contextDebt = 0) :
    affine = 0 := by
  have productZero : unit * affine = 0 := by
    calc
      unit * affine = unit * affine + 0 := (addZero _).symm
      _ = unit * affine + contextDebt := by rw [contextZero]
      _ = equation := receipt.symm
      _ = 0 := equationZero
  have unitNonzero := rightInverse_nonzero zeroMul zeroNeOne unitWitness
  exact (noZeroDivisors unit affine productZero).resolve_left unitNonzero

/-- The reverse implication uses only the checked receipt and ordinary zero
laws: a solved affine form plus vanishing normalization debt satisfies the
original equation. -/
theorem normalizedEquation_zero_of_affine_zero
    {R : Type u} [Mul R] [Add R] [OfNat R 0]
    (mulZero : forall r : R, r * 0 = 0)
    (zeroAdd : forall r : R, 0 + r = r)
    {equation unit affine contextDebt : R}
    (receipt : equation = unit * affine + contextDebt)
    (affineZero : affine = 0)
    (contextZero : contextDebt = 0) :
    equation = 0 := by
  calc
    equation = unit * affine + contextDebt := receipt
    _ = unit * 0 + 0 := by rw [affineZero, contextZero]
    _ = 0 := by rw [mulZero, zeroAdd]

/-- Together these are the semantic normalization law a v2 solve step still
must bind at its interpreted model. -/
theorem normalizedEquation_zero_iff_affine_zero
    {R : Type u} [Mul R] [Add R] [OfNat R 0] [OfNat R 1]
    (zeroMul : forall r : R, 0 * r = 0)
    (mulZero : forall r : R, r * 0 = 0)
    (addZero : forall r : R, r + 0 = r)
    (zeroAdd : forall r : R, 0 + r = r)
    (zeroNeOne : Not ((0 : R) = 1))
    (noZeroDivisors : HasNoZeroDivisors (R := R))
    {equation unit affine contextDebt : R}
    (unitWitness : HasRightInverse unit)
    (receipt : equation = unit * affine + contextDebt)
    (contextZero : contextDebt = 0) :
    equation = 0 <-> affine = 0 :=
  Iff.intro
    (fun equationZero => normalizedAffine_zero_of_equation_zero
      zeroMul addZero zeroNeOne noZeroDivisors unitWitness receipt
      equationZero contextZero)
    (fun affineZero => normalizedEquation_zero_of_affine_zero
      mulZero zeroAdd receipt affineZero contextZero)

/-- Identity is a mapped equivalence. -/
def MappedEquivalence.refl {A : Type u} (model : Model A) :
    MappedEquivalence model model where
  forward := id
  backward := id
  left_inv := by intro x; rfl
  right_inv := by intro x; rfl
  forward_maps := by intro _ hx; exact hx
  backward_maps := by intro _ hx; exact hx

/-- An explicitly ordered sequence of mapped-equivalent model states. The
intermediate point types may differ, which accommodates actual coordinate
elimination rather than pretending every step is literal containment. -/
inductive MappedEquivalenceChain :
    {A B : Type u} -> Model A -> Model B -> Type (u + 1) where
  | nil {A : Type u} (model : Model A) :
      MappedEquivalenceChain model model
  | cons {A B C : Type u}
      {src : Model A} {mid : Model B} {dst : Model C}
      (head : MappedEquivalence src mid)
      (tail : MappedEquivalenceChain mid dst) :
      MappedEquivalenceChain src dst

/-- A checked sequence composes to one endpoint equivalence. -/
def MappedEquivalenceChain.toMappedEquivalence
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    MappedEquivalence src dst :=
  match chain with
  | .nil model => MappedEquivalence.refl model
  | .cons head tail => head.trans tail.toMappedEquivalence

/-- A chain transports witnesses from its initial state to its final state. -/
theorem MappedEquivalenceChain.hasPoint_forward
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    HasPoint src -> HasPoint dst :=
  chain.toMappedEquivalence.hasPoint_forward

/-- A chain reconstructs initial witnesses from final witnesses. -/
theorem MappedEquivalenceChain.hasPoint_backward
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    HasPoint dst -> HasPoint src :=
  chain.toMappedEquivalence.hasPoint_backward

/-- Final-state emptiness licenses initial-state emptiness. -/
theorem MappedEquivalenceChain.isEmpty_backward
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    IsEmpty dst -> IsEmpty src :=
  fun emptyDst x hx =>
    Exists.elim (chain.hasPoint_forward (Exists.intro x hx))
      (fun y hy => emptyDst y hy)

/-- Initial-state emptiness also licenses final-state emptiness. -/
theorem MappedEquivalenceChain.isEmpty_forward
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    IsEmpty src -> IsEmpty dst :=
  fun emptySrc y hy =>
    Exists.elim (chain.hasPoint_backward (Exists.intro y hy))
      (fun x hx => emptySrc x hx)

/-- A semantically bound ordered solve chain preserves emptiness exactly. -/
theorem MappedEquivalenceChain.isEmpty_iff
    {A B : Type u} {src : Model A} {dst : Model B}
    (chain : MappedEquivalenceChain src dst) :
    IsEmpty src <-> IsEmpty dst :=
  Iff.intro chain.isEmpty_forward chain.isEmpty_backward

end GrandPortage
