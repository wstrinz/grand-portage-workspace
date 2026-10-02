import GP50.Events
namespace GP50.Semantic
structure Profile where
  Stmt : Type
  Scope : Type
  Ctx : Type
  same : Stmt → Stmt → Bool
  same_sound : ∀ a b, same a b = true → a = b
  mem : Ctx → Scope → Prop
  le : Scope → Scope → Bool
  le_sound : ∀ a b c, le a b = true → mem c a → mem c b
  Holds : Stmt → Ctx → Prop
  contra : Stmt → Stmt → Bool
  contra_sound : ∀ a b c, contra a b = true → Holds a c → Holds b c → False

def Means (p : Profile) (stmt : p.Stmt) (scope : p.Scope) : Prop :=
  ∀ c, p.mem c scope → p.Holds stmt c

-- Statement data includes selected objects; scope restriction cannot alter it.
structure Clause (p : Profile) where
  key : Nat
  version : Nat
  binding : Binding
  stmt : p.Stmt
  scope : p.Scope
end GP50.Semantic
