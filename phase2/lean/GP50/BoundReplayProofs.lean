import GP50.BoundReplay
import GP50.PolyStubProofs
namespace GP50.Span
open PolyStub

-- Native formal Rat coefficient identities; byte/digest binding is an adapter contract.
def ReceiptIdentity (clause : Clause) (receipt : Receipt) : Prop :=
  clause.generators.length = receipt.cofactors.length ∧
    ∀ exponent, ((clause.generators.zip receipt.cofactors).map fun (generator,cofactor) =>
      coefficient (multiply generator cofactor) exponent).sum = coefficient clause.target exponent

def FormalSpan (clause : Clause) : Prop :=
  ∃ cofactors : List Polynomial, clause.generators.length = cofactors.length ∧
    ∀ exponent, ((clause.generators.zip cofactors).map fun (generator,cofactor) =>
      coefficient (multiply generator cofactor) exponent).sum = coefficient clause.target exponent

theorem eraseDups_length_le {α : Type} [BEq α] (values : List α) :
    values.eraseDups.length ≤ values.length := by
  cases values with
  | nil => simp
  | cons head tail =>
    rw [List.eraseDups_cons]
    have smaller := eraseDups_length_le (tail.filter fun value => !value == head)
    have bound := List.length_filter_le (fun value => !value == head) tail
    simp only [List.length_cons]
    omega
termination_by values.length
decreasing_by
  have bound := List.length_filter_le (fun value => !value == head) tail
  simp only [List.length_cons]
  omega

theorem nodup_of_eraseDups_length_eq {α : Type} [BEq α] [LawfulBEq α]
    (values : List α) (sameLength : values.eraseDups.length = values.length) :
    values.Nodup := by
  induction values with
  | nil => simp
  | cons head tail ih =>
    have dedupLength : (tail.filter fun value => !value == head).eraseDups.length = tail.length := by
      simpa only [List.eraseDups_cons, List.length_cons, Nat.add_right_cancel_iff] using sameLength
    have dedupBound := eraseDups_length_le (tail.filter fun value => !value == head)
    have filterBound := List.length_filter_le (fun value => !value == head) tail
    have filterLength : (tail.filter fun value => !value == head).length = tail.length := by omega
    have filterSame : (tail.filter fun value => !value == head) = tail :=
      List.filter_sublist.eq_of_length filterLength
    have absent : head ∉ tail := by
      intro present
      have rejected := (List.filter_eq_self.mp filterSame) head present
      simp at rejected
    have tailLength : tail.eraseDups.length = tail.length := by
      simpa only [filterSame] using dedupLength
    exact List.nodup_cons.mpr ⟨absent, ih tailLength⟩

theorem wellFormed_nodup (clauses : List Clause) (receipts : List Receipt)
    (valid : wellFormed clauses receipts = true) :
    (clauses.map (·.key)).Nodup ∧ (receipts.map (·.name)).Nodup := by
  have lengths : (clauses.map (·.key)).eraseDups.length = clauses.length ∧
      (receipts.map (·.name)).eraseDups.length = receipts.length := by
    simpa only [wellFormed, Bool.and_eq_true, beq_iff_eq] using valid
  constructor
  · apply nodup_of_eraseDups_length_eq
    simpa only [List.length_map] using lengths.1
  · apply nodup_of_eraseDups_length_eq
    simpa only [List.length_map] using lengths.2

theorem key_unique_of_nodup {α β : Type} (values : List α) (key : α → β)
    (distinct : (values.map key).Nodup) (left right : α)
    (leftPresent : left ∈ values) (rightPresent : right ∈ values)
    (sameKey : key left = key right) : left = right := by
  induction values generalizing left right with
  | nil => simp at leftPresent
  | cons head tail ih =>
    have parts : key head ∉ tail.map key ∧ (tail.map key).Nodup := by
      simpa only [List.map_cons, List.nodup_cons] using distinct
    simp only [List.mem_cons] at leftPresent rightPresent
    rcases leftPresent with rfl | leftTail
    · rcases rightPresent with rfl | rightTail
      · rfl
      · apply False.elim
        apply parts.1
        rw [sameKey]
        exact List.mem_map.mpr ⟨right, rightTail, rfl⟩
    · rcases rightPresent with rfl | rightTail
      · apply False.elim
        apply parts.1
        rw [← sameKey]
        exact List.mem_map.mpr ⟨left, leftTail, rfl⟩
      · exact ih parts.2 left right leftTail rightTail sameKey

theorem accepts_exact_identity (clauses : List Clause) (receipts : List Receipt)
    (warrant : Warrant) (name : String)
    (accepted : accepts clauses receipts warrant name = true) :
    wellFormed clauses receipts = true ∧
      ∃ clause ∈ clauses, clause.key = warrant.claim ∧ clause.version = warrant.version ∧
        clause.binding = warrant.binding ∧
        ∃ receipt ∈ receipts, receipt.name = name ∧ receipt.claim = clause.key ∧
          receipt.version = clause.version ∧ receipt.binding = clause.binding ∧
          ReceiptIdentity clause receipt := by
  have checks : wellFormed clauses receipts = true ∧
      ∃ clause ∈ clauses, clause.key = warrant.claim ∧ clause.version = warrant.version ∧
        clause.binding = warrant.binding ∧
        ∃ receipt ∈ receipts, receipt.name = name ∧ receipt.claim = clause.key ∧
          receipt.version = clause.version ∧ receipt.binding = clause.binding ∧
          replay clause.generators receipt.cofactors clause.target = true := by
    simpa only [accepts, Bool.and_eq_true, List.any_eq_true, beq_iff_eq,
      decide_eq_true_eq, and_assoc] using accepted
  rcases checks with ⟨valid, clause, clausePresent, claimEq, versionEq, bindingEq,
    receipt, receiptPresent, nameEq, receiptClaim, receiptVersion, receiptBinding, replayed⟩
  exact ⟨valid, clause, clausePresent, claimEq, versionEq, bindingEq,
    receipt, receiptPresent, nameEq, receiptClaim, receiptVersion, receiptBinding,
    replay_coefficient_sum clause.generators receipt.cofactors clause.target replayed⟩

theorem accepts_unique_clause_meaning (clauses : List Clause) (receipts : List Receipt)
    (warrant : Warrant) (name : String)
    (accepted : accepts clauses receipts warrant name = true) :
    ∀ clause ∈ clauses, clause.key = warrant.claim → FormalSpan clause := by
  rcases accepts_exact_identity clauses receipts warrant name accepted with
    ⟨valid, chosen, chosenPresent, claimEq, versionEq, bindingEq,
      receipt, receiptPresent, nameEq, receiptClaim, receiptVersion, receiptBinding, identity⟩
  intro clause present sameKey
  have sameClause := key_unique_of_nodup clauses (·.key)
    (wellFormed_nodup clauses receipts valid).1 clause chosen present chosenPresent
    (sameKey.trans claimEq.symm)
  subst clause
  exact ⟨receipt.cofactors, identity⟩

#print axioms wellFormed_nodup
#print axioms key_unique_of_nodup
#print axioms accepts_exact_identity
#print axioms accepts_unique_clause_meaning
end GP50.Span
