import GP50.BoundReplayProofs
import GP50.AdmissionProofs
namespace GP50.Span
open PolyStub

@[simp] theorem except_bind_ok {α β : Type} (a : α) (f : α → Except String β) :
    (Except.ok a >>= f) = f a := rfl
@[simp] theorem except_bind_error {α β : Type} (e : String) (f : α → Except String β) :
    (Except.error e >>= f) = Except.error e := rfl
@[simp] theorem except_map_ok {α β : Type} (a : α) (f : α → β) :
    (f <$> (Except.ok a : Except String α)) = Except.ok (f a) := rfl
@[simp] theorem except_map_error {α β : Type} (e : String) (f : α → β) :
    (f <$> (Except.error e : Except String α)) = Except.error e := rfl

theorem eraseDups_nodup {α : Type} [BEq α] [LawfulBEq α] (values : List α) :
    values.eraseDups.Nodup := by
  cases valuesEq : values with
  | nil => simp
  | cons head tail =>
    rw [List.eraseDups_cons]
    apply List.nodup_cons.mpr
    constructor
    · intro present
      have filtered := List.mem_filter.mp (List.mem_eraseDups.mp present)
      simp at filtered
    · exact eraseDups_nodup (tail.filter fun value => !value == head)
termination_by values.length
decreasing_by
  have bound := List.length_filter_le (fun value => !value == head) tail
  simp_all only [List.length_cons]
  omega

theorem canonicalIds_nodup (values : List Nat) : (canonicalIds values).Nodup :=
  (List.mergeSort_perm values.eraseDups (fun a b => a ≤ b)).symm.nodup
    (eraseDups_nodup values)

theorem eraseDups_mem_source {α : Type} [BEq α] (values : List α) (x : α)
    (member : x ∈ values.eraseDups) : x ∈ values := by
  cases valuesEq : values with
  | nil => simp [valuesEq] at member
  | cons head tail =>
    rw [valuesEq, List.eraseDups_cons] at member
    rcases List.mem_cons.mp member with equal | present
    · exact List.mem_cons.mpr (Or.inl equal)
    · exact List.mem_cons.mpr (Or.inr
        (List.mem_filter.mp (eraseDups_mem_source _ x present)).1)
termination_by values.length
decreasing_by
  have bound := List.length_filter_le (fun value => !value == head) tail
  simp_all only [List.length_cons]
  omega

theorem warrantFor_id (values : List Warrant) (id : Nat) (w : Warrant)
    (found : warrantFor values id = .ok w) : w.id = id := by
  unfold warrantFor at found
  split at found <;> try contradiction
  rename_i value restEq
  have eqValue : value = w := Except.ok.inj found
  subst w
  have member : value ∈ (values.filter fun w => w.id == id).eraseDups := by rw [restEq]; simp
  exact eq_of_beq (List.mem_filter.mp (eraseDups_mem_source _ _ member)).2

theorem warrantFor_mapM_ids (values : List Warrant) (ids : List Nat)
    (warrants : List Warrant)
    (mapped : ids.mapM (warrantFor values) = .ok warrants) :
    warrants.map (·.id) = ids := by
  induction ids generalizing warrants with
  | nil => change Except.ok [] = Except.ok warrants at mapped; cases mapped; rfl
  | cons id rest ih =>
    cases headLookup : warrantFor values id with
    | error message => simp [List.mapM_cons, headLookup] at mapped
    | ok head =>
      cases tailLookup : rest.mapM (warrantFor values) with
      | error message => simp [List.mapM_cons, headLookup, tailLookup] at mapped
      | ok tail =>
        have listEq : head :: tail = warrants := by
          simpa [List.mapM_cons, headLookup, tailLookup] using mapped
        subst warrants
        simp [warrantFor_id values id head headLookup, ih tail tailLookup]

theorem except_return_constant {α β : Type} (action : Except String α)
    (expected actual : β)
    (success : (action >>= fun _ => Except.ok expected) = Except.ok actual) :
    expected = actual := by
  cases action with
  | error e => contradiction
  | ok a => exact Except.ok.inj success

theorem resolve_warrant_ids (events : List Event) (snapshot : Snapshot)
    (resolved : resolve events = .ok snapshot) :
    snapshot.warrants.map (·.id) = canonicalIds ((warrantsIn events).map (·.id)) := by
  unfold resolve at resolved
  cases currentMap : (canonicalIds ((currentsIn events).map (·.claim))).mapM
      (currentFor (currentsIn events)) with
  | error message => simp only [currentMap, except_bind_error] at resolved; contradiction
  | ok currents =>
    simp only [currentMap, except_bind_ok] at resolved
    cases warrantMap : (canonicalIds ((warrantsIn events).map (·.id))).mapM
        (warrantFor (warrantsIn events)) with
    | error message => simp only [warrantMap, except_bind_error] at resolved; contradiction
    | ok warrants =>
      simp only [warrantMap, except_bind_ok] at resolved
      have snapshotEq := except_return_constant _ _ _ resolved
      have warrantsEq := congrArg Snapshot.warrants snapshotEq
      rw [← warrantsEq]
      exact warrantFor_mapM_ids _ _ _ warrantMap


theorem resolve_warrant_ids_nodup (events : List Event) (snapshot : Snapshot)
    (resolved : resolve events = .ok snapshot) :
    (snapshot.warrants.map (·.id)).Nodup := by
  rw [resolve_warrant_ids events snapshot resolved]
  exact canonicalIds_nodup _

-- Meaning concerns decoded polynomial coefficients. Host byte/digest fidelity
-- remains a separate adapter trust boundary.
def ClaimMeaning (clauses : List Clause) (claim : Nat) : Prop :=
  (∃ clause ∈ clauses, clause.key = claim) ∧
  ∀ clause ∈ clauses, clause.key = claim → FormalSpan clause

def WarrantMeaning (snapshot : Snapshot) (clauses : List Clause) (id : Nat) : Prop :=
  ∃ w ∈ snapshot.warrants, w.id = id ∧ ClaimMeaning clauses w.claim

theorem admission_validator_sound (clauses : List Clause) (receipts : List Receipt)
    (snapshot : Snapshot) :
    ValidatorSound (admission clauses receipts) snapshot (WarrantMeaning snapshot clauses) := by
  constructor
  · intro w member name accepted
    refine ⟨w, member, rfl, ?_⟩
    constructor
    · rcases (accepts_exact_identity clauses receipts w name accepted).2 with
        ⟨clause, present, key, _⟩
      exact ⟨clause, present, key⟩
    · exact accepts_unique_clause_meaning clauses receipts w name accepted
  · intro w member name accepted
    contradiction
  · intro w member premises side accepted supported
    contradiction
  · intro w member source sourceMember accepted supported
    contradiction

theorem evaluate_held_formalSpan (clauses : List Clause) (receipts : List Receipt)
    (snapshot : Snapshot) (uniqueIds : (snapshot.warrants.map (·.id)).Nodup)
    (claim : Nat) (heldClaim : held (evaluate (admission clauses receipts) snapshot) claim = true) :
    ClaimMeaning clauses claim := by
  apply evaluate_held_truth_composition (admission clauses receipts) snapshot
    (WarrantMeaning snapshot clauses) (ClaimMeaning clauses)
    (admission_validator_sound clauses receipts snapshot) _ claim heldClaim
  intro w present meaning
  rcases meaning with ⟨other, otherPresent, sameId, meaning⟩
  have equal : other = w :=
    key_unique_of_nodup snapshot.warrants (fun w => w.id) uniqueIds
      other w otherPresent present sameId
  exact equal ▸ meaning

theorem resolve_held_formalSpan (clauses : List Clause) (receipts : List Receipt)
    (events : List Event) (snapshot : Snapshot) (claim : Nat)
    (resolved : resolve events = .ok snapshot)
    (heldClaim : held (evaluate (admission clauses receipts) snapshot) claim = true) :
    (∃ clause ∈ clauses, clause.key = claim) ∧
    (∀ clause ∈ clauses, clause.key = claim → FormalSpan clause) :=
  evaluate_held_formalSpan clauses receipts snapshot
    (resolve_warrant_ids_nodup events snapshot resolved) claim heldClaim

theorem fold_held_formalSpan (clauses : List Clause) (receipts : List Receipt)
    (events : List Event) (state : RuntimeState) (claim : Nat)
    (folded : fold (admission clauses receipts) events = .ok state)
    (heldClaim : held state claim = true) :
    (∃ clause ∈ clauses, clause.key = claim) ∧
    (∀ clause ∈ clauses, clause.key = claim → FormalSpan clause) := by
  unfold fold at folded
  cases resolved : resolve events with
  | error message => simp [resolved] at folded
  | ok snapshot =>
    rw [resolved] at folded
    have stateEq : evaluate (admission clauses receipts) snapshot = state := by
      exact Except.ok.inj folded
    subst state
    exact resolve_held_formalSpan clauses receipts events snapshot claim resolved heldClaim

#print axioms resolve_warrant_ids_nodup
#print axioms admission_validator_sound
#print axioms evaluate_held_formalSpan
#print axioms resolve_held_formalSpan
#print axioms fold_held_formalSpan

end GP50.Span
