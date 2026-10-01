import GP50.Narrowing
namespace GP50.Semantic
-- A checker supplies an actual common context, never an overlap success flag.
structure Overlap (p : Profile) where
  witness : p.Scope → p.Scope → Option p.Ctx
  sound : ∀ a b c, witness a b = some c → p.mem c a ∧ p.mem c b
structure ConflictFinding (p : Profile) where
  leftSupport : Nat
  rightSupport : Nat
  leftClaim : Nat
  rightClaim : Nat
  witness : Option p.Ctx

def assessConflict (p : Profile) (overlap : Overlap p)
    (a b : Clause p) (left right : Nat) : Option (ConflictFinding p) :=
  if p.contra a.stmt b.stmt then
    some ⟨left, right, a.key, b.key, overlap.witness a.scope b.scope⟩
  else none

def conflictFindings (p : Profile) (overlap : Overlap p)
    (clauses : List (Clause p)) (state : RuntimeState) : List (ConflictFinding p) :=
  state.snapshot.warrants.flatMap fun a => state.snapshot.warrants.filterMap fun b =>
    if a.id < b.id && state.supports.contains a.id && state.supports.contains b.id then
      match boundClause p clauses a, boundClause p clauses b with
      | some ac, some bc => assessConflict p overlap ac bc a.id b.id
      | _, _ => none
    else none

structure ReleaseReview (p : Profile) where
  state : RuntimeState
  findings : List (ConflictFinding p)

def ReleaseReview.allowed (review : ReleaseReview p) : Bool :=
  !(review.findings.any fun finding => finding.witness.isSome)

def reviewRelease (p : Profile) (overlap : Overlap p)
    (clauses : List (Clause p)) (state : RuntimeState) : ReleaseReview p :=
  ⟨state, conflictFindings p overlap clauses state⟩
end GP50.Semantic
