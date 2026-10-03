import GPProfile.Frontend
import GPProfile.Plan

/-!
Family adapters of the shared case-to-profile frontend (post-G2 §1.8). Each adapter reads one
input family of the v0.37-derived corpus and builds a `Plan` of profile inputs only. Families
are recognized by their input keys; none is keyed to a case id. A case no family recognizes is
an expressiveness loss.
-/

namespace GPProfile.Families
open Lean GPProfile

/-! ## JSON helpers -/

def obj? (j : Json) (k : String) : Option Json := (j.getObjVal? k).toOption
def has (j : Json) (k : String) : Bool := (obj? j k).isSome
def str? (j : Json) (k : String) : Option String := (obj? j k).bind (·.getStr?.toOption)
def strList (j : Json) : Except String (List String) := do (← j.getArr?).toList.mapM Json.getStr?
def strs (j : Json) (k : String) : Except String (List String) :=
  match obj? j k with | some v => strList v | none => pure []
def nats (j : Json) (k : String) : Except String (List Nat) :=
  match obj? j k with | some v => do (← v.getArr?).toList.mapM Json.getNat? | none => pure []
def text (j : Json) : Except String String :=
  match j with
  | .str s => pure s
  | .num n => pure (toString n)
  | _ => throw "expected a polynomial string or number"

/-- The requested scope and replay field from the case's characteristic fields. -/
def scopeField (inputs : Json) : Except String (Scope × Field) := do
  let p ← characteristic inputs []
  pure (if p == 0 then (.char0Only, .rat) else (.only p, .prime p))

def P (vars : List String) (t : String) : Except String Sparse := parse vars t

def one (n : Nat) : Sparse := [(List.replicate n 0, 1)]

def mkItem (key : Nat) (stmt : Stmt) (scope : Scope) (support : Support) (extra : List String := []) : Item :=
  { key, stmt, scope, extra, support }

def single (stmt : Stmt) (scope : Scope) (support : Support) : Plan :=
  { items := [{ key := 1, stmt, scope, support }], requested := [1] }

def splitEq (t : String) : Except String (String × String) :=
  match t.splitOn "=" with
  | [l, r] => pure (l, r)
  | [l] => pure (l, "0")
  | _ => throw "identity must have at most one '='"

/-- `p * q` in canonical sparse form. -/
def mulS (n : Nat) (p q : Sparse) : Option Sparse := do
  let a ← toHexQ n p
  let b ← toHexQ n q
  pure (ofHex (a * b))

def subS (n : Nat) (p q : Sparse) : Option Sparse := do
  let a ← toHexQ n p
  let b ← toHexQ n q
  pure (ofHex (a - b))

def powS (n : Nat) (p : Sparse) (k : Nat) : Option Sparse := do
  let a ← toHexQ n p
  pure (ofHex (a ^ k))

def need {α : Type} (o : Option α) (msg : String) : Except String α :=
  match o with | some a => pure a | none => throw msg

/-- A total map on `vars`, as source polynomials in the given order. -/
def totalMap (images : Json) (domain codomain : List String) : Except String (List Sparse) :=
  domain.mapM fun v => match obj? images v with
    | some t => do P codomain (← text t)
    | none => throw s!"incomplete map: no image for {v}"

/-! ## Families -/

/-- Localized membership: `numerator / ∏ guards^d = 0` in the declared localization, certified by
cofactors for `membership_target = numerator · ∏ guardᵢ^{locᵢ}`. The per-guard powers are
brought to a common exponent by scaling the cofactors (exact arithmetic on certificate data). -/
def localized (inputs : Json) : Except String (Stmt × Cert × Scope) := do
  let vars ← strs inputs "variables"
  let n := vars.length
  let gens ← (← strs inputs "generators").mapM (P vars)
  let guards ← (← strs inputs "guards").mapM (P vars)
  let num ← P vars (← need (str? inputs "numerator") "no numerator")
  let qs ← (← strs inputs "cofactors").mapM (P vars)
  let loc ← nats inputs "localization_powers"
  if loc.length != guards.length then throw "localization powers do not match the guards"
  let k := loc.foldl max 0
  let scale ← need ((guards.zip loc).foldlM (fun acc (g, l) => do mulS n acc (← powS n g (k - l)))
    (one n)) "scaling failed"
  let qs' ← need (qs.mapM (mulS n scale)) "scaling failed"
  let (scope, field) ← scopeField inputs
  pure (⟨vars, gens, guards, .inIdeal num⟩, .ideal field qs' 1 k, scope)

/-- Binding inputs of a receipt beyond its statement. -/
def extrasOf (inputs : Json) : List String :=
  [s!"chart:{(str? inputs "chart").getD ""}", s!"cite:{(str? inputs "cite").getD ""}",
    s!"universe:{(str? inputs "point_universe").getD ""}"]

def localizedFamily (inputs : Json) : Except String Plan := do
  let (stmt, cert, scope) ← localized inputs
  let extra := extrasOf inputs
  let base : Item := { key := 1, stmt, scope, extra, support := .receipt cert }
  match obj? inputs "parent_generators", obj? inputs "proposed_change" with
  | some pg, _ =>
    -- Promote local emptiness to a looser parent: an R2 inclusion with no certificate.
    let parent : Stmt := { stmt with eqs := ← (← strList pg).mapM (P stmt.vars), kind := .empty }
    let local' : Stmt := { stmt with kind := .empty }
    -- EMPTY uses the same identity with m = 0 (the target is 1).
    let localCert := match cert with | .ideal f qs _ k => Cert.ideal f qs 0 k | c => c
    let items := [mkItem 1 local' scope (.receipt localCert) extra, mkItem 2 parent scope (.rule (.inclusion [] []) [1])]
    pure { items, requested := [2] }
  | _, some (.obj change) =>
    -- Custody: the receipt stays bound to the original statement and binding inputs.
    let ch := Json.obj change
    let eqs ← match obj? ch "generators" with
      | some v => (← strList v).mapM (P stmt.vars) | none => pure stmt.eqs
    let guards ← match obj? ch "open_conditions" with
      | some v => (← strList v).mapM (P stmt.vars) | none => pure stmt.guards
    let merged := Json.mergeObj inputs ch
    let changed := mkItem 2 { stmt with eqs, guards } scope (.receipt cert (some (stmt, extra))) (extrasOf merged)
    pure { items := [base, changed], requested := [2] }
  | _, _ => pure { items := [base], requested := [1] }

/-- An identity checked against a model's ideal: `left - right` in the ideal of the equations. -/
def modelIdentity (inputs : Json) : Except String Plan := do
  let model ← need (obj? inputs "model") "no model"
  let vars ← strs model "variables"
  let eqs ← (← strs model "equations").mapM (P vars)
  let idn ← need (obj? inputs "identity") "no identity"
  let lhs ← text (← need (obj? idn "left") "no left")
  let rhs ← text (← need (obj? idn "right") "no right")
  let h ← P vars s!"({lhs})-({rhs})"
  let qs ← (← strs inputs "cofactors").mapM (P vars)
  let (scope, field) ← scopeField model
  pure (single ⟨vars, eqs, [], .inIdeal h⟩ scope (.receipt (.ideal field qs 1 0)))

/-- An ambient identity `lhs = rhs`: membership of the difference in the zero ideal. -/
def ambient (vars : List String) (lhs rhs : String) (scope : Scope) (field : Field) : Except String Plan := do
  let h ← P vars s!"({lhs})-({rhs})"
  pure (single ⟨vars, [], [], .inIdeal h⟩ scope (.receipt (.ideal field [] 1 0)))

def ambientFamily (inputs : Json) : Except String Plan := do
  let (scope, field) ← scopeField inputs
  let vars ← strs inputs "variables"
  if let (some l, some r) := (str? inputs "lhs", str? inputs "rhs") then
    return ← ambient vars l r scope field
  if let some pi := obj? inputs "power_identity" then
    let eq ← text (← need (obj? pi "equation") "no equation")
    let sc ← text (← need (obj? pi "scalar") "no scalar")
    let b ← text (← need (obj? pi "base") "no base")
    let e ← need ((obj? pi "exponent").bind (·.getNat?.toOption)) "no exponent"
    return ← ambient vars eq s!"({sc})*({b})^{e}" scope field
  let idn ← need (obj? inputs "identity") "no identity"
  let eq ← text (← need (obj? idn "equation") "no equation")
  let sc ← text (← need (obj? idn "scalar") "no scalar")
  let l ← text (← need (obj? idn "left") "no left")
  let r ← text (← need (obj? idn "right") "no right")
  ambient vars eq s!"({sc})*({l})*({r})" scope field

/-- A proposed result of a simultaneous substitution: GP composes and checks the identity. -/
def substitution (inputs : Json) : Except String Plan := do
  let vars ← strs inputs "variables"
  let images ← need (obj? inputs "images") "no images"
  let phi ← totalMap images vars vars
  let e ← P vars (← need (str? inputs "expression") "no expression")
  let composed ← need (compose vars.length phi vars.length e) "composition failed"
  let proposed ← P vars (← need (str? inputs "proposed") "no proposed result")
  let h ← need (subS vars.length proposed composed) "difference failed"
  pure (single ⟨vars, [], [], .inIdeal h⟩ .char0Only (.receipt (.ideal .rat [] 1 0)))

/-- A ring-isomorphism certificate between quotient rings, as the bundle of its obligations:
pullback memberships in both directions and both inverse laws. Every one must be held. -/
def isoBundle (vS : List String) (eS : List Sparse) (vT : List String) (eT : List Sparse)
    (fwd : List Sparse) (inv : List Sparse) (fwdRows invRows : List (List Sparse)) : Except String Plan := do
  let nS := vS.length
  let nT := vT.length
  -- forward: target variable images in source coordinates; inverse: source images in target.
  let pullT ← need (eT.mapM (compose nS fwd nT)) "forward pullback failed"
  let pullS ← need (eS.mapM (compose nT inv nS)) "inverse pullback failed"
  let backS ← need (inv.mapM (compose nS fwd nT)) "inverse law failed"
  let backT ← need (fwd.mapM (compose nT inv nS)) "inverse law failed"
  let xS := (List.range nS).map fun i => [((List.range nS).map fun j => if i == j then 1 else 0, (1 : Rat))]
  let xT := (List.range nT).map fun i => [((List.range nT).map fun j => if i == j then 1 else 0, (1 : Rat))]
  let lawS ← need ((backS.zip xS).mapM fun (b, x) => subS nS b x) "inverse law failed"
  let lawT ← need ((backT.zip xT).mapM fun (b, x) => subS nT b x) "inverse law failed"
  let mk (vars : List String) (eqs : List Sparse) (h : Sparse) (qs : List Sparse) : Stmt × Cert :=
    (⟨vars, eqs, [], .inIdeal h⟩, .ideal .rat qs 1 0)
  let rows (rs : List (List Sparse)) (i : Nat) (len : Nat) : List Sparse :=
    (rs.getD i []) ++ List.replicate (len - (rs.getD i []).length) []
  let obligations :=
    (pullT.zipIdx.map fun (h, i) => mk vS eS h (rows fwdRows i eS.length)) ++
    (pullS.zipIdx.map fun (h, i) => mk vT eT h (rows invRows i eT.length)) ++
    (lawS.map fun h => mk vS eS h (List.replicate eS.length [])) ++
    (lawT.map fun h => mk vT eT h (List.replicate eT.length []))
  let items := obligations.zipIdx.map fun ((s, c), i) => mkItem (i + 1) s .char0Only (.receipt c)
  pure { items, requested := items.map (·.key) }

def ringMapFamily (inputs : Json) : Except String Plan := do
  if let (some src, some tgt) := (obj? inputs "source", obj? inputs "target") then
    let vS ← strs src "variables"; let vT ← strs tgt "variables"
    let eS ← (← strs src "equations").mapM (P vS)
    let eT ← (← strs tgt "equations").mapM (P vT)
    let fwd ← totalMap (← need (obj? inputs "point_forward") "no forward map") vT vS
    let inv ← totalMap (← need (obj? inputs "point_inverse") "no inverse map") vS vT
    let rowsOf (k : String) (vars : List String) : Except String (List (List Sparse)) := do
      match obj? inputs k with
      | some (.arr rs) => rs.toList.mapM fun r => do (← strList r).mapM (P vars)
      | _ => pure []
    return ← isoBundle vS eS vT eT fwd inv (← rowsOf "target_pullback_rows" vS) (← rowsOf "source_pullback_rows" vT)
  let vars ← strs inputs "variables"
  let eqs ← (← strs inputs "generators").mapM (P vars)
  let fwd ← totalMap (← need (obj? inputs "forward") "no forward map") vars vars
  let inv ← totalMap (← need (obj? inputs "inverse") "no inverse map") vars vars
  let rowsOf (k : String) : Except String (List (List Sparse)) := do
    match obj? inputs k with
    | some (.arr rs) => rs.toList.mapM fun r => do (← strList r).mapM (P vars)
    | _ => pure []
  isoBundle vars eqs vars eqs fwd inv (← rowsOf "forward_cofactors") (← rowsOf "inverse_cofactors")

/-- Transport of an identity between ideals (relaxation, quotient pullback, witnesses). -/
def idealsFamily (inputs : Json) : Except String Plan := do
  let srcT ← strs inputs "source_ideal"
  let tgtT ← strs inputs "target_ideal"
  let texts := srcT ++ tgtT ++ ((str? inputs "identity").toList) ++ ((str? inputs "identity_difference").toList)
  let vars ← match obj? inputs "variables" with
    | some v => strList v
    | none => pure (texts.flatMap identifiers).eraseDups
  let src ← srcT.mapM (P vars)
  let tgt ← tgtT.mapM (P vars)
  if let some pt := obj? inputs "point" then
    let values ← vars.mapM fun v => do
      match ← parse [] (← text (← need (obj? pt v) s!"point lacks {v}")) with
      | [] => pure (0 : Rat)
      | [([], c)] => pure c
      | _ => throw "point coordinate is not a constant"
    return single ⟨vars, tgt, [], .nonempty⟩ .char0Only (.receipt (.point .rat values))
  if let some d := str? inputs "identity_difference" then
    let qs ← (← strs inputs "target_cofactors").mapM (P vars)
    return single ⟨vars, tgt, [], .inIdeal (← P vars d)⟩ .char0Only (.receipt (.ideal .rat qs 1 0))
  let (l, r) ← splitEq (← need (str? inputs "identity") "no identity")
  let h ← P vars s!"({l})-({r})"
  if has inputs "point_containment_proof" then
    -- Only point-level evidence is offered: VANISHES_ON(h) on the source cannot become ideal
    -- membership there (R1 runs the other way). The attempted step is an R1 instance in reverse.
    let items := [mkItem 1 ⟨vars, src, [], .vanishesOn h⟩ .char0Only .none,
      mkItem 2 ⟨vars, src, [], .inIdeal h⟩ .char0Only (.rule .r1 [1])]
    return { items, requested := [2] }
  -- Carry the identity to the target ideal, replayed there with no cofactors.
  pure (single ⟨vars, tgt, [], .inIdeal h⟩ .char0Only (.receipt (.ideal .rat (tgt.map fun _ => []) 1 0)))

/-- An offered point at an exact open model. -/
def pointFamily (inputs : Json) : Except String Plan := do
  let vars ← strs inputs "variables"
  let eqs ← (← strs inputs "equations").mapM (P vars)
  let guards ← (← strs inputs "nonzero_guards").mapM (P vars)
  let pt ← need (obj? inputs "point") "no point"
  let values ← vars.mapM fun v => do
    match ← parse [] (← text (← need (obj? pt v) s!"point lacks {v}")) with
    | [] => pure (0 : Rat)
    | [([], c)] => pure c
    | _ => throw "point coordinate is not a constant"
  let (scope, field) ← scopeField inputs
  pure (single ⟨vars, eqs, guards, .nonempty⟩ scope (.receipt (.point field values)))

/-- Elimination targets: statements over the retained coordinates only (signature check). -/
def eliminationFamily (inputs : Json) : Except String Plan := do
  if let (some tv, some idn) := (obj? inputs "target_variables", str? inputs "identity") then
    let vars ← strList tv
    let (l, r) ← splitEq idn
    let h ← P vars s!"({l})-({r})"
    return single ⟨vars, [], [], .inIdeal h⟩ .char0Only .none
  let built ← strs inputs "built_generators"
  let elim ← strs inputs "eliminated"
  let vars := ((built.flatMap identifiers).eraseDups).filter fun v => !elim.contains v
  let gens ← built.mapM (P vars)
  pure (single ⟨vars, gens, [], .nonempty⟩ .char0Only .none)

/-- Excluding one fiber does not exclude the parent: R4 needs both branches. -/
def fiberFamily (inputs : Json) : Except String Plan := do
  let vars ← strs inputs "variables"
  let parentEqs ← (← strs inputs "parent_equations").mapM (P vars)
  let base ← need (obj? inputs "excluded_base") "no excluded base"
  let fiberEqs ← vars.filterMapM fun v => match obj? base v with
    | some t => do pure (some (← P vars s!"{v}-({← text t})"))
    | none => pure none
  let parent : Stmt := ⟨vars, parentEqs, [], .empty⟩
  let h ← need fiberEqs.head? "empty excluded base"
  let items := [mkItem 1 { parent with eqs := parentEqs ++ [h] } .char0Only .none,
    mkItem 2 parent .char0Only (.rule (.split h) [1])]
  pure { items, requested := [2] }

/-- A rational point given as `{variable: constant}`, in variable order. -/
def ratPoint (vars : List String) (pt : Json) : Except String (List Rat) :=
  vars.mapM fun v => do
    match ← parse [] (← text (← need (obj? pt v) s!"point lacks {v}")) with
    | [] => pure (0 : Rat)
    | [([], c)] => pure c
    | _ => throw "point coordinate is not a constant"

/-- Cancelling a factor that is not proved invertible: VANISHES_ON(x) on `{z·x = 0}`. A supplied
point is filed as the counterexample (NONEMPTY with the conclusion as a guard), so the refusal is
`contra`'s, not mere lack of support (G3a review §4). -/
def cancelFamily (inputs : Json) : Except String Plan := do
  let vars ← strs inputs "variables"
  let prod ← P vars (← need (str? inputs "product") "no product")
  let conc ← P vars (← need (str? inputs "cancelled_conclusion") "no conclusion")
  let claim := mkItem 1 ⟨vars, [prod], [], .vanishesOn conc⟩ .char0Only .none
  match obj? inputs "point" with
  | none => pure { items := [claim], requested := [1] }
  | some pt =>
    let witness := mkItem 2 ⟨vars, [prod], [conc], .nonempty⟩ .char0Only
      (.receipt (.point .rat (← ratPoint vars pt)))
    pure { items := [claim, witness], requested := [1] }

/-- Rewriting a point predicate through a translation: the case's control names the map used. -/
def translationFamily (inputs : Json) : Except String Plan := do
  let ctrl ← need (str? inputs "control") "no control"
  let pred ← need (str? inputs "source_predicate") "no predicate"
  let (l, r) ← splitEq pred
  let p ← P ["x"] s!"({l})-({r})"
  let mapText ← need (if ctrl == "backward_rewrite" then str? inputs "backward" else str? inputs "forward")
    "no map"
  let map ← P ["y"] (if ctrl == "backward_rewrite" then mapText else mapText.replace "x" "y")
  let rewritten ← need (compose 1 [map] 1 p) "composition failed"
  let tp ← need ((obj? inputs "target_point").bind (·.getNat?.toOption)) "no target point"
  pure (single ⟨["y"], [rewritten], [], .nonempty⟩ .char0Only (.receipt (.point .rat [(tp : Rat)])))

/-- A false emptiness claim next to a witness point: the witness supports NONEMPTY only. -/
def attemptFamily (inputs : Json) (case : Json) : Except String Plan := do
  let attempt ← need (str? inputs "attempt") "no attempt"
  let i ← frontend case []
  if attempt == "empty" then
    let items := [mkItem 1 i.stmt i.scope (.receipt i.cert), mkItem 2 { i.stmt with kind := .empty } i.scope .none]
    pure { items, requested := [2] }
  else pure (single i.stmt i.scope (.receipt i.cert))

/-- Ring-element properties refuted by witness points: NOT_IN_IDEAL (a locus point where the
element is nonzero) and NONUNIT (a locus point where it vanishes). Non-zerodivisor claims have no
3a kind and stay expressiveness losses. -/
def elementFamily (case inputs : Json) : Except String Plan := do
  let claim := (str? case "attempted_conclusion").getD ""
  if (claim.splitOn "nonzerodivisor").length > 1 then throw "non-zerodivisor claims have no 3a statement kind"
  let vars ← strs inputs "variables"
  let eqs ← (← strs inputs "generators").mapM (P vars)
  let el ← P vars (← need (str? inputs "element") "no element")
  let ptOf (k : String) : Except String (List Rat) := do ratPoint vars (← need (obj? inputs k) s!"no {k}")
  let items := [mkItem 1 ⟨vars, eqs, [], .notInIdeal el⟩ .char0Only (.receipt (.point .rat (← ptOf "nonzero_point"))),
    mkItem 2 ⟨vars, eqs, [], .nonunit el⟩ .char0Only (.receipt (.point .rat (← ptOf "zero_point")))]
  pure { items, requested := [1, 2] }

/-- An object cover. The proposer looks for a branch whose equations and guards occur literally
in the parent's and supplies the canonical inclusion certificates (no search); with no such
branch the cover claim is unsupported. -/
def coverFamily (inputs : Json) : Except String Plan := do
  let parent ← need (obj? inputs "parent") "no parent"
  let vars ← strs parent "variables"
  let n := vars.length
  let eqs ← (← strs parent "equations").mapM (P vars)
  let guards ← (← strs parent "nonzero").mapM (P vars)
  let branches ← match obj? inputs "branches" with
    | some (.arr bs) => bs.toList.mapM fun b => do
        pure ((← (← strs b "equations").mapM (P vars)), (← (← strs b "nonzero").mapM (P vars)))
    | _ => throw "no branches"
  let stmt : Stmt := ⟨vars, eqs, guards, .cover branches⟩
  let zero : Sparse := []
  -- Loose equation `e` equal to parent equation `j`: VANISHES_ON e with cofactor 1 at `j`.
  let eqCert (e : Sparse) : Option IdealCert := do
    let j ← eqs.idxOf? e
    pure ⟨.rat, eqs.mapIdx fun i _ => if i == j then one n else zero, 1, 0⟩
  -- Loose guard `g` equal to parent guard `j`: {eqs, g = 0, guards} is empty, since
  -- ∏ guards = (∏ other guards) · g; cofactor ∏ other guards at the new equation.
  let guardCert (g : Sparse) : Option IdealCert := do
    let j ← guards.idxOf? g
    let others ← (guards.eraseIdx j).foldlM (fun acc h => mulS n acc h) (one n)
    pure ⟨.rat, eqs.map (fun _ => zero) ++ [others], 0, 1⟩
  let found := branches.zipIdx.findSome? fun ((be, bg), i) => do
    let ec ← be.mapM eqCert
    let gc ← bg.mapM guardCert
    pure (Cert.cover i ec gc)
  pure (single stmt .char0Only (match found with | some c => .receipt c | none => .none))

/-- A family applies only when every input key is one it reads (or ignores as provenance) and
the fixed fields it requires have the stated values. Anything else is an expressiveness loss:
the frontend never guesses past a key it does not understand. -/
def onlyKeys (inputs : Json) (allowed : List String) : Bool :=
  match inputs with
  | .obj kvs => kvs.toList.all fun (k, _) => allowed.contains k
  | _ => false

/-- A nested model object: only these keys, and a rational field when one is named. -/
def modelOk (j : Json) : Bool :=
  onlyKeys j ["field", "variables", "equations", "nonzero"] &&
    (str? j "field").all fun f => (fieldChar? f).isSome && f != "R" && f != "RR"

def nestedOk (inputs : Json) (key : String) (allowed : List String) : Bool :=
  (obj? inputs key).all fun j => onlyKeys j allowed

def questionIs (inputs : Json) (qs : List String) : Bool :=
  match str? inputs "question" with
  | some q => qs.contains q
  | none => true

/-- A scalar factor is a constant or a declared unit. -/
def scalarOk (inputs : Json) (scalar : Option String) : Except String Bool := do
  let some sc := scalar | return true
  let units ← strs inputs "declared_units"
  let ids := identifiers sc
  pure (ids.all units.contains)

def legacyKeys : List String :=
  ["variables", "generators", "cofactors", "target", "characteristic", "target_characteristic",
    "guards", "exponent", "point", "reduced_point", "identity", "source_ideal", "cofactor",
    "source_context", "target_context"]

/-- Dispatch on input keys. -/
def plan (case : Json) (params : List (String × Nat)) : Except String Plan := do
  let inputs ← case.getObjVal? "inputs"
  let elabOr (r : Except String Plan) : Except String Plan :=
    match r with
    | .ok p => .ok p
    | .error e =>
      if e.startsWith "undeclared variable" || e.startsWith "incomplete map" then
        .ok { items := [], requested := [], elaboration := some e }
      else .error e
  let k := onlyKeys inputs
  if has inputs "membership_target" && k ["variables", "generators", "guards", "numerator",
      "denominator_powers", "localization_powers", "membership_target", "cofactors", "coefficient_field",
      "point_universe", "chart", "cite", "proposed_change", "parent_generators", "characteristic"] &&
      (str? inputs "point_universe" |>.all (· == "ALGEBRAIC_CLOSURE")) &&
      ((obj? inputs "proposed_change").all fun c => onlyKeys c ["generators", "open_conditions", "chart", "cite"] || c == .null) then
    return ← localizedFamily inputs
  if has inputs "model" && k ["model", "identity", "cofactors", "local_backend", "historical_identity",
      "raw_artifact", "question"] && questionIs inputs ["exact_identity_current"] &&
      (obj? inputs "model").all modelOk && nestedOk inputs "identity" ["left", "right"] then
    return ← modelIdentity inputs
  if k ["lhs", "rhs", "variables", "characteristic"] && has inputs "lhs" then
    return ← ambientFamily inputs
  if has inputs "power_identity" && k ["variables", "characteristic", "declared_units", "exponent_limit",
      "power_identity", "question"] && questionIs inputs ["check_power_identity"] &&
      nestedOk inputs "power_identity" ["equation", "scalar", "base", "exponent"] &&
      (← scalarOk inputs ((obj? inputs "power_identity").bind (str? · "scalar"))) then
    return ← ambientFamily inputs
  if (obj? inputs "identity").any (fun j => has j "equation") && k ["variables", "characteristic",
      "declared_units", "identity", "parent_equations", "open_guards", "question"] &&
      questionIs inputs ["check_identity"] && has inputs "question" &&
      nestedOk inputs "identity" ["equation", "scalar", "left", "right"] &&
      (← scalarOk inputs ((obj? inputs "identity").bind (str? · "scalar"))) then
    return ← ambientFamily inputs
  if has inputs "images" && k ["variables", "expression", "images", "proposed"] then
    return ← elabOr (substitution inputs)
  if has inputs "point_forward" && k ["source", "target", "point_forward", "point_inverse",
      "target_pullback_rows", "source_pullback_rows", "question"] &&
      (obj? inputs "source").all modelOk && (obj? inputs "target").all modelOk then
    return ← ringMapFamily inputs
  if has inputs "forward_cofactors" && k ["variables", "generators", "forward", "inverse",
      "forward_cofactors", "inverse_cofactors"] then
    return ← ringMapFamily inputs
  if has inputs "target_ideal" && k ["variables", "source_ideal", "target_ideal", "identity", "origin",
      "point", "point_containment_proof", "identity_difference", "target_cofactors"] then
    return ← elabOr (idealsFamily inputs)
  if has inputs "nonzero_guards" && k ["coefficient_domain", "point_universe", "variables", "equations",
      "nonzero_guards", "point"] && (str? inputs "point_universe").all (· == "rational points") then
    return ← pointFamily inputs
  if (has inputs "target_variables" && k ["source_variables", "target_variables", "identity"]) ||
      (has inputs "eliminated" && k ["built_generators", "eliminated"]) then
    return ← elabOr (eliminationFamily inputs)
  if has inputs "excluded_fiber_generators" && k ["variables", "parent_equations", "excluded_base",
      "excluded_fiber_generators", "parent_point"] then
    return ← fiberFamily inputs
  if has inputs "cancelled_conclusion" && k ["variables", "product", "cancelled_conclusion", "point",
      "unit_witness"] then
    return ← cancelFamily inputs
  if has inputs "source_predicate" && k ["control", "source_point", "target_point", "forward", "backward",
      "source_predicate"] && (str? inputs "control").any (["backward_rewrite", "wrong_forward_rewrite"].contains ·) then
    return ← translationFamily inputs
  if has inputs "element" && k ["variables", "generators", "element", "annihilator", "cofactors",
      "nonzero_point", "zero_point"] then
    return ← elementFamily case inputs
  if has inputs "branches" && k ["parent", "branches"] && (obj? inputs "parent").all modelOk &&
      (match obj? inputs "branches" with | some (.arr bs) => bs.all modelOk | _ => false) then
    return ← coverFamily inputs
  if has inputs "attempt" && k ["variables", "generators", "characteristic", "point", "attempt"] then
    return ← attemptFamily inputs case
  if let some (.arr ids) := obj? inputs "identity" then
    if k ["identity", "source_context", "target_context"] then
      -- An identity written in one context and copied into another context's signature.
      let sides ← ids.toList.mapM text
      let vars := (sides.flatMap identifiers).eraseDups
      let (scope, field) ← scopeField inputs
      return ← ambient vars (sides.getD 0 "0") (sides.getD 1 "0") scope field
  if k legacyKeys then
    return ← elabOr (do let i ← frontend case params; pure (single i.stmt i.scope (.receipt i.cert)))
  throw "inputs fit no 3a frontend family"

end GPProfile.Families
