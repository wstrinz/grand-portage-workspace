import GP50.CoveredSpan
import GP50.CoverProofs
import GP50.ScopedSpanProofs
namespace GP50.CoveredSpan

theorem boundClauses_mapM_means (p : Semantic.Profile) (clauses : List (Semantic.Clause p))
    (premises : List Warrant) (branches : List (Semantic.Clause p))
    (mapped : premises.mapM (Semantic.boundClause p clauses) = some branches)
    (truth : ∀ premise ∈ premises, Semantic.ClaimMeaning p clauses premise.claim) :
    ∀ branch ∈ branches, Semantic.Means p branch.stmt branch.scope := by
  induction premises generalizing branches with
  | nil =>
    simp at mapped
    subst branches
    simp
  | cons premise rest ih =>
    cases found : Semantic.boundClause p clauses premise with
    | none => simp [List.mapM_cons, found] at mapped
    | some chosen =>
      cases tailMapped : rest.mapM (Semantic.boundClause p clauses) with
      | none => simp [List.mapM_cons, found, tailMapped] at mapped
      | some tail =>
        have branchesEq : chosen :: tail = branches := by
          simpa [List.mapM_cons, found, tailMapped] using mapped
        subst branches
        intro branch present
        rcases List.mem_cons.mp present with equal | tailPresent
        · subst branch
          have info := Semantic.boundClause_registered p clauses premise chosen found
          exact (truth premise (List.mem_cons_self)).2 chosen info.2.1 info.2.2
        · exact ih tail tailMapped (fun w member => truth w (List.mem_cons_of_mem _ member))
            branch tailPresent

theorem accepts_claim_meaning (rows : List ScopedSpan.Row) (rules : List Rule)
    (dest : Warrant) (premises : List Warrant) (name : String)
    (accepted : accepts rows rules dest premises name = true)
    (truth : ∀ premise ∈ premises,
      Semantic.ClaimMeaning ScopedSpan.profile (rows.map ScopedSpan.semantic) premise.claim) :
    Semantic.ClaimMeaning ScopedSpan.profile (rows.map ScopedSpan.semantic) dest.claim := by
  have coverAccepted : Semantic.acceptsCover ScopedSpan.profile coverage
      (rows.map ScopedSpan.semantic) dest premises = true := by
    simp only [accepts, Bool.and_eq_true] at accepted
    exact accepted.2
  unfold Semantic.acceptsCover at coverAccepted
  cases found : Semantic.boundClause ScopedSpan.profile (rows.map ScopedSpan.semantic) dest with
  | none => simp [found] at coverAccepted
  | some destination =>
    cases mapped : premises.mapM (Semantic.boundClause ScopedSpan.profile
        (rows.map ScopedSpan.semantic)) with
    | none => simp [found, mapped] at coverAccepted
    | some branches =>
      have checked : Semantic.checkCover ScopedSpan.profile coverage destination branches = true := by
        simpa only [found, mapped] using coverAccepted
      rcases Semantic.boundClause_registered ScopedSpan.profile
        (rows.map ScopedSpan.semantic) dest destination found with ⟨unique, present, key⟩
      have meaning := Semantic.checked_cover_sound ScopedSpan.profile coverage destination branches
        checked (boundClauses_mapM_means _ _ _ _ mapped truth)
      refine ⟨⟨destination, present, key⟩, ?_⟩
      intro other otherPresent otherKey
      have equal := Span.key_unique_of_nodup (rows.map ScopedSpan.semantic) (fun c => c.key)
        unique other destination otherPresent present (otherKey.trans key.symm)
      exact equal ▸ meaning

theorem base_validator_sound (rows : List ScopedSpan.Row) (receipts : List Span.Receipt)
    (rules : List Rule) (snapshot : Snapshot)
    (unique : (snapshot.warrants.map (·.id)).Nodup) :
    Semantic.BaseValidatorSound ScopedSpan.profile (rows.map ScopedSpan.semantic)
      (baseAdmission rows receipts rules) snapshot := by
  constructor
  · exact (ScopedSpan.base_validator_sound rows receipts snapshot).receipt
  · intros; contradiction
  · intro w present premises name accepted members supported
    refine ⟨w, present, rfl, ?_⟩
    apply accepts_claim_meaning rows rules w premises name accepted
    intro premise premisePresent
    exact Semantic.warrant_meaning_claim ScopedSpan.profile (rows.map ScopedSpan.semantic)
      snapshot unique premise (members premise premisePresent) (supported premise premisePresent)

theorem fold_warrant_ids_nodup (rows : List ScopedSpan.Row) (receipts : List Span.Receipt)
    (rules : List Rule) (events : List Event) (state : RuntimeState)
    (folded : fold (admission rows receipts rules) events = .ok state) :
    (state.snapshot.warrants.map (·.id)).Nodup := by
  unfold fold at folded
  cases resolved : resolve events with
  | error message => simp [resolved] at folded
  | ok snapshot =>
    rw [resolved] at folded
    have stateEq : evaluate (admission rows receipts rules) snapshot = state := Except.ok.inj folded
    subst state
    exact Span.resolve_warrant_ids_nodup events snapshot resolved

theorem fold_held_meaning (rows : List ScopedSpan.Row) (receipts : List Span.Receipt)
    (rules : List Rule) (events : List Event) (state : RuntimeState) (claim : Nat)
    (folded : fold (admission rows receipts rules) events = .ok state)
    (heldClaim : held state claim = true) :
    Semantic.ClaimMeaning ScopedSpan.profile (rows.map ScopedSpan.semantic) claim := by
  have result := Semantic.fold_held_meaning ScopedSpan.profile (rows.map ScopedSpan.semantic)
    (baseAdmission rows receipts rules) events state claim
    (base_validator_sound rows receipts rules state.snapshot
      (fold_warrant_ids_nodup rows receipts rules events state folded))
  apply result
  · exact folded
  · exact heldClaim

#print axioms boundClauses_mapM_means
#print axioms accepts_claim_meaning
#print axioms base_validator_sound
#print axioms fold_warrant_ids_nodup
#print axioms fold_held_meaning
end GP50.CoveredSpan
