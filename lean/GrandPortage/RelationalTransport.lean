/-
# Relational transport and predicate transformers

Model-changing operations need not be functions and need not preserve every
point. A binary relation is their common point-level semantic core.
-/

import GrandPortage.Points

namespace GrandPortage

universe u v w

def PointRelation (α : Type u) (β : Type v) := α → β → Prop

def PredicateLe {α : Type u} (P Q : α → Prop) : Prop :=
  ∀ x, P x → Q x

def ExistsImage {α : Type u} {β : Type v}
    (R : PointRelation α β) (P : α → Prop) : β → Prop :=
  fun y => ∃ x, P x ∧ R x y

def ForallPre {α : Type u} {β : Type v}
    (R : PointRelation α β) (Q : β → Prop) : α → Prop :=
  fun x => ∀ y, R x y → Q y

theorem existsImage_le_iff_le_forallPre
    {α : Type u} {β : Type v}
    (R : PointRelation α β) (P : α → Prop) (Q : β → Prop) :
    PredicateLe (ExistsImage R P) Q ↔ PredicateLe P (ForallPre R Q) := by
  constructor
  · intro imageLe x hx y hxy
    exact imageLe y ⟨x, hx, hxy⟩
  · intro preLe y
    rintro ⟨x, hx, hxy⟩
    exact preLe x hx y hxy

def IdentityRelation (α : Type u) : PointRelation α α :=
  fun x y => x = y

def RelationComp {α : Type u} {β : Type v} {γ : Type w}
    (R : PointRelation α β) (S : PointRelation β γ) :
    PointRelation α γ :=
  fun x z => ∃ y, R x y ∧ S y z

theorem existsImage_identity
    {α : Type u} (P : α → Prop) (x : α) :
    ExistsImage (IdentityRelation α) P x ↔ P x := by
  constructor
  · rintro ⟨y, hy, rfl⟩
    exact hy
  · intro hx
    exact ⟨x, hx, rfl⟩

theorem forallPre_identity
    {α : Type u} (P : α → Prop) (x : α) :
    ForallPre (IdentityRelation α) P x ↔ P x := by
  constructor
  · intro h
    exact h x rfl
  · intro hx y hxy
    cases hxy
    exact hx

theorem existsImage_comp
    {α : Type u} {β : Type v} {γ : Type w}
    (R : PointRelation α β) (S : PointRelation β γ)
    (P : α → Prop) (z : γ) :
    ExistsImage (RelationComp R S) P z ↔
      ExistsImage S (ExistsImage R P) z := by
  constructor
  · rintro ⟨x, hx, y, hxy, hyz⟩
    exact ⟨y, ⟨x, hx, hxy⟩, hyz⟩
  · rintro ⟨y, ⟨x, hx, hxy⟩, hyz⟩
    exact ⟨x, hx, y, hxy, hyz⟩

theorem forallPre_comp
    {α : Type u} {β : Type v} {γ : Type w}
    (R : PointRelation α β) (S : PointRelation β γ)
    (Q : γ → Prop) (x : α) :
    ForallPre (RelationComp R S) Q x ↔
      ForallPre R (ForallPre S Q) x := by
  constructor
  · intro h y hxy z hyz
    exact h z ⟨y, hxy, hyz⟩
  · intro h z
    rintro ⟨y, hxy, hyz⟩
    exact h y hxy z hyz

def RelationTotalOn {α : Type u} {β : Type v}
    (R : PointRelation α β) (src : Model α) (dst : Model β) : Prop :=
  ∀ x, src x → ∃ y, dst y ∧ R x y

def RelationSurjectiveOn {α : Type u} {β : Type v}
    (R : PointRelation α β) (src : Model α) (dst : Model β) : Prop :=
  ∀ y, dst y → ∃ x, src x ∧ R x y

theorem relationTotal_hasPoint_along
    {α : Type u} {β : Type v}
    {R : PointRelation α β} {src : Model α} {dst : Model β}
    (total : RelationTotalOn R src dst)
    (sourcePoint : HasPoint src) :
    HasPoint dst := by
  obtain ⟨x, hx⟩ := sourcePoint
  obtain ⟨y, hy, _⟩ := total x hx
  exact ⟨y, hy⟩

theorem relationTotal_isEmpty_against
    {α : Type u} {β : Type v}
    {R : PointRelation α β} {src : Model α} {dst : Model β}
    (total : RelationTotalOn R src dst)
    (targetEmpty : IsEmpty dst) :
    IsEmpty src := by
  intro x hx
  obtain ⟨y, hy, _⟩ := total x hx
  exact targetEmpty y hy

theorem relationSurjective_hasPoint_against
    {α : Type u} {β : Type v}
    {R : PointRelation α β} {src : Model α} {dst : Model β}
    (surjective : RelationSurjectiveOn R src dst)
    (targetPoint : HasPoint dst) :
    HasPoint src := by
  obtain ⟨y, hy⟩ := targetPoint
  obtain ⟨x, hx, _⟩ := surjective y hy
  exact ⟨x, hx⟩

theorem relationSurjective_isEmpty_along
    {α : Type u} {β : Type v}
    {R : PointRelation α β} {src : Model α} {dst : Model β}
    (surjective : RelationSurjectiveOn R src dst)
    (sourceEmpty : IsEmpty src) :
    IsEmpty dst := by
  intro y hy
  obtain ⟨x, hx, _⟩ := surjective y hy
  exact sourceEmpty x hx

theorem relationTotal_comp
    {α : Type u} {β : Type v} {γ : Type w}
    {R : PointRelation α β} {S : PointRelation β γ}
    {src : Model α} {mid : Model β} {dst : Model γ}
    (first : RelationTotalOn R src mid)
    (second : RelationTotalOn S mid dst) :
    RelationTotalOn (RelationComp R S) src dst := by
  intro x hx
  obtain ⟨y, hy, hxy⟩ := first x hx
  obtain ⟨z, hz, hyz⟩ := second y hy
  exact ⟨z, hz, y, hxy, hyz⟩

theorem relationSurjective_comp
    {α : Type u} {β : Type v} {γ : Type w}
    {R : PointRelation α β} {S : PointRelation β γ}
    {src : Model α} {mid : Model β} {dst : Model γ}
    (first : RelationSurjectiveOn R src mid)
    (second : RelationSurjectiveOn S mid dst) :
    RelationSurjectiveOn (RelationComp R S) src dst := by
  intro z hz
  obtain ⟨y, hy, hyz⟩ := second z hz
  obtain ⟨x, hx, hxy⟩ := first y hy
  exact ⟨x, hx, y, hxy, hyz⟩

theorem refines_iff_identityRelation_total
    {α : Type u} (src dst : Model α) :
    Refines src dst ↔
      RelationTotalOn (IdentityRelation α) src dst := by
  constructor
  · intro refines x hx
    exact ⟨x, refines x hx, rfl⟩
  · intro total x hx
    obtain ⟨y, hy, hxy⟩ := total x hx
    cases hxy
    exact hy

end GrandPortage
