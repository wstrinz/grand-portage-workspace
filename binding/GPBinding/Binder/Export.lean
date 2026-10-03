import GPBinding.Warrants.Generated

/-!
The binder (G1 decision 2, Addendum A4). For every registry entry it checks
* the declaration type: `Bound.proof : Warranted stmt scope`, enforced by Lean's typechecker;
* the imported axioms of the named theorem: standard ones only;
* well-formedness: arity, and the scope avoids the statement's primes, so that
  `means_of_warranted` gives the Kernel's meaning;
and writes binding records keyed on the exact canonical statement and scope. Run with
`lake env lean GPBinding/Binder/Export.lean`; the profile's proof validator reads the records.
-/

open Lean Elab Command GPProfile GPBinding.Binder

def standardAxioms : List Name := [``propext, ``Quot.sound, ``Classical.choice]

#eval show CommandElabM Unit from do
  let mut rows : Array Json := #[]
  for b in GPBinding.Warrants.registry do
    let decl := `GPBinding.Warrants ++ b.name.toName
    let axs ← liftCoreM (Lean.collectAxioms decl)
    let axiomsOk := axs.all standardAxioms.contains
    let wf := stmtArityOk b.stmt && b.scope.avoids b.stmt.primes
    rows := rows.push (Json.mkObj [
      ("declaration", toJson decl.toString), ("statementHash", toJson (reprStr b.stmt)),
      ("scopeHash", toJson (reprStr b.scope)), ("axioms", toJson (axs.map toString)),
      ("axiomsOk", toJson axiomsOk), ("wellFormed", toJson wf), ("bound", toJson (axiomsOk && wf))])
  IO.println (Json.mkObj [("schema", "gp-binder/v1"), ("records", toJson rows)]).pretty
