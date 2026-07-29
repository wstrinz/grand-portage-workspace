/-
# Mapped equivalence is not literal containment

An isomorphism can identify two models after a change of coordinates without
making either solution set a literal subset of the other. This separates the
meaning of `verify.ring_iso` from `verify.containment`: the former may apply a
declared map, while the latter asks about the coordinates as written.
-/

import GrandPortage.Points

namespace GrandPortage

universe u v

/-- Every source point is sent to a target point by the declared map. -/
def MapsTo {A : Type u} {B : Type v}
    (f : A -> B) (src : Model A) (dst : Model B) : Prop :=
  forall x, src x -> dst (f x)

/-- Two models agree after an invertible change of coordinates. -/
structure MappedEquivalence {A : Type u} {B : Type v}
    (src : Model A) (dst : Model B) where
  forward : A -> B
  backward : B -> A
  left_inv : forall x, backward (forward x) = x
  right_inv : forall y, forward (backward y) = y
  forward_maps : MapsTo forward src dst
  backward_maps : MapsTo backward dst src

/-- A declared mapped equivalence transports witnesses forward. -/
theorem MappedEquivalence.hasPoint_forward
    {A : Type u} {B : Type v} {src : Model A} {dst : Model B}
    (e : MappedEquivalence src dst) : HasPoint src -> HasPoint dst
  | Exists.intro x hx => Exists.intro (e.forward x) (e.forward_maps x hx)

/-- A declared mapped equivalence transports witnesses backward. -/
theorem MappedEquivalence.hasPoint_backward
    {A : Type u} {B : Type v} {src : Model A} {dst : Model B}
    (e : MappedEquivalence src dst) : HasPoint dst -> HasPoint src
  | Exists.intro y hy => Exists.intro (e.backward y) (e.backward_maps y hy)

def onlyB : Model Two := fun x => x = Two.b

def swapTwo : Two -> Two
  | Two.a => Two.b

  | Two.b => Two.a
/-- A non-involutive example pins the word `forward`: source point 0 is sent
    to target point 1 by adding one. Polynomial pullback is contravariant, but
    the user-facing map is the point map formalised here. -/
def onlyZeroInt : Model Int := fun x => x = 0
def onlyOneInt : Model Int := fun x => x = 1
def shiftUp (x : Int) : Int := x + 1
def shiftDown (x : Int) : Int := x - 1

def zero_one_translation : MappedEquivalence onlyZeroInt onlyOneInt where
  forward := shiftUp
  backward := shiftDown
  left_inv := by intro x; simp [shiftUp, shiftDown]
  right_inv := by intro x; simp [shiftUp, shiftDown]
  forward_maps := by
    intro x hx
    subst x
    simp [onlyOneInt, shiftUp]
  backward_maps := by
    intro x hx
    subst x
    simp [onlyZeroInt, shiftDown]

theorem shiftDown_is_not_point_forward :
    Not (MapsTo shiftDown onlyZeroInt onlyOneInt) := by
  simp [MapsTo, onlyZeroInt, onlyOneInt, shiftDown]

/-- The one-point models are equivalent after swapping their point names. -/
def onlyA_onlyB_equiv : MappedEquivalence onlyA onlyB where
  forward := swapTwo
  backward := swapTwo
  left_inv := by intro x; cases x <;> rfl
  right_inv := by intro x; cases x <;> rfl
  forward_maps := by
    intro x hx
    cases x <;> simp [onlyA, onlyB, swapTwo] at *
  backward_maps := by
    intro x hx
    cases x <;> simp [onlyA, onlyB, swapTwo] at *

theorem onlyA_not_refines_onlyB : Not (Refines onlyA onlyB) := by
  intro h
  have ha := h Two.a rfl
  simp [onlyB] at ha

theorem onlyB_not_refines_onlyA : Not (Refines onlyB onlyA) := by
  intro h
  have hb := h Two.b rfl
  simp [onlyA] at hb

/-- Mapped equivalence does not imply literal containment in the forward
    direction. -/
theorem mappedEquivalence_not_refines :
    Not (forall (src dst : Model Two),
      MappedEquivalence src dst -> Refines src dst) := by
  intro h
  exact onlyA_not_refines_onlyB (h onlyA onlyB onlyA_onlyB_equiv)

/-- Nor does mapped equivalence imply literal containment in reverse. -/
theorem mappedEquivalence_not_refines_reverse :
    Not (forall (src dst : Model Two),
      MappedEquivalence src dst -> Refines dst src) := by
  intro h
  exact onlyB_not_refines_onlyA (h onlyA onlyB onlyA_onlyB_equiv)

end GrandPortage
