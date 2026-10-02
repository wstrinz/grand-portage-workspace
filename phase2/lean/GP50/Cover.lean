import GP50.Narrowing
namespace GP50.Semantic

-- A coverage checker certifies membership coverage, never branch truth or existence.
structure Coverage (p : Profile) where
  covers : p.Scope → List p.Scope → Bool
  sound : ∀ destination branches ctx, covers destination branches = true →
    p.mem ctx destination → ∃ branch ∈ branches, p.mem ctx branch

def checkCover (p : Profile) (coverage : Coverage p)
    (destination : Clause p) (branches : List (Clause p)) : Bool :=
  branches.all (fun branch => p.same destination.stmt branch.stmt &&
    (destination.binding.statementHash == branch.binding.statementHash &&
     destination.binding.modelHash == branch.binding.modelHash &&
     destination.binding.inputHashes == branch.binding.inputHashes &&
     destination.binding.kernelVersion == branch.binding.kernelVersion)) &&
  coverage.covers destination.scope (branches.map (·.scope))

-- All premises are bound here; support for their IDs remains Runtime's obligation.
def acceptsCover (p : Profile) (coverage : Coverage p) (clauses : List (Clause p))
    (destination : Warrant) (premises : List Warrant) : Bool :=
  match boundClause p clauses destination, premises.mapM (boundClause p clauses) with
  | some dest, some branches => checkCover p coverage dest branches
  | _, _ => false

end GP50.Semantic
