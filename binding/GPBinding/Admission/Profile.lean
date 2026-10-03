import GPBinding.Admission.Sound
import GPBinding.ContextSpike
import GP50.NarrowingAdmissionProofs

/-!
The 3a algebraic profile's semantic half (post-G2 §3.9): contexts are fields (`FieldCtx`, the
§2.5c choice), membership is `ringChar K ∈ ⟦scope⟧`, and `Holds` is statement truth in `K`.
Receipt admission is sound, so the Kernel's generic fold theorem gives held claims their
meaning in every field their scope denotes.
-/

namespace GPBinding.Admission
open GPProfile GP50 GPBinding.Spike

/-- The semantic 3a profile over the executable `GPProfile.ops`. -/
noncomputable def profile : Semantic.Profile.{1} where
  toProfileOps := GPProfile.ops
  Ctx := FieldCtx
  mem K sc := Scope.mem K.carrier sc
  Holds s K := Holds K.carrier s
  le_sound a b K h hm := Scope.le_den h hm
  contra_sound a b K h ha hb := by
    obtain ⟨va, ea, ga, ka⟩ := a
    obtain ⟨vb, eb, gb, kb⟩ := b
    change GPProfile.contra _ _ = true at h
    simp only [GPProfile.contra, Bool.and_eq_true, beq_iff_eq, Bool.or_eq_true] at h
    obtain ⟨⟨⟨rfl, rfl⟩, rfl⟩, hk⟩ := h
    change Holds K.carrier _ at ha
    change Holds K.carrier _ at hb
    rcases hk with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
    · obtain ⟨x, hx⟩ := hb; exact ha x hx
    · obtain ⟨x, hx⟩ := ha; exact hb x hx

/-- The executable clauses are the semantic profile's clauses. -/
abbrev SClause := Semantic.Clause profile.toProfileOps

theorem accepts_claim_meaning (clauses : List GPProfile.Clause) (receipts : List Receipt)
    (w : Warrant) (name : String) (accepted : accepts clauses receipts w name = true) :
    Semantic.ClaimMeaning profile clauses w.claim := by
  unfold accepts at accepted
  simp only [Bool.and_eq_true, List.any_eq_true, beq_iff_eq, decide_eq_true_eq] at accepted
  obtain ⟨wf, c, hc, ⟨⟨hkey, -⟩, -⟩, r, -, hok⟩ := accepted
  have hcheck := hok.2
  have nodup : (clauses.map (·.key)).Nodup := by
    unfold wellFormed at wf
    simp only [Bool.and_eq_true, beq_iff_eq] at wf
    exact nodup_of_eraseDups_length_eq _ (by simpa only [List.length_map] using wf.1)
  have means : Semantic.Means profile c.stmt c.scope := by
    intro (K : FieldCtx) (hK : Scope.mem K.carrier c.scope)
    change Holds K.carrier c.stmt
    unfold Check.ok at hcheck
    split at hcheck
    · rename_i r' hr'
      exact check_sound hr' hK
    · contradiction
  refine ⟨⟨c, hc, hkey⟩, fun c' hc' hkey' => ?_⟩
  have := key_unique_of_nodup clauses (·.key) nodup c' c hc' hc (hkey'.trans hkey.symm)
  exact this ▸ means

theorem base_validator_sound (clauses : List GPProfile.Clause) (receipts : List Receipt)
    (snapshot : Snapshot) :
    Semantic.BaseValidatorSound profile clauses
      { Admission.refuseAll with receipt := accepts clauses receipts } snapshot := by
  constructor
  · intro w member name accepted
    exact ⟨w, member, rfl, accepts_claim_meaning clauses receipts w name accepted⟩
  · intros; contradiction
  · intros; contradiction

/-- Fold soundness for the 3a profile: a held claim means its registered statement in every
field whose characteristic its scope denotes. -/
theorem fold_held_meaning (clauses : List GPProfile.Clause) (receipts : List Receipt)
    (events : List Event) (state : RuntimeState) (claim : Nat)
    (folded : fold (GPProfile.admission clauses receipts) events = .ok state)
    (heldClaim : held state claim = true) :
    (∃ c ∈ clauses, c.key = claim) ∧
    ∀ c ∈ clauses, c.key = claim → ∀ K : FieldCtx, Scope.mem K.carrier c.scope →
      Holds K.carrier c.stmt :=
  Semantic.fold_held_meaning profile clauses _ events state claim
    (base_validator_sound clauses receipts state.snapshot) folded heldClaim

end GPBinding.Admission
