import GP50.Conflict
namespace GP50.Semantic
-- Detection cannot turn contradictory statements into sound claims.
theorem confirmed_conflict_excludes_joint_truth (p : Profile) (overlap : Overlap p)
    (a b : Clause p) (left right : Nat) (finding : ConflictFinding p) (ctx : p.Ctx)
    (found : assessConflict p overlap a b left right = some finding)
    (inhabited : finding.witness = some ctx) :
    ¬(Means p a.stmt a.scope ∧ Means p b.stmt b.scope) := by
  unfold assessConflict at found
  split at found
  next contra =>
    cases Option.some.inj found
    have both := overlap.sound a.scope b.scope ctx inhabited
    intro truths
    exact p.contra_sound a.stmt b.stmt ctx contra
      (truths.1 ctx both.1) (truths.2 ctx both.2)
  next => contradiction

theorem release_preserves_complete_state (p : Profile) (overlap : Overlap p)
    (clauses : List (Clause p)) (state : RuntimeState) :
    (reviewRelease p overlap clauses state).state = state := rfl
end GP50.Semantic
