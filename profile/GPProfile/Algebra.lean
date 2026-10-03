import GP50.Narrowing
import GPProfile.Poly

/-!
The 3a algebraic profile, Nullstellensatz regime (post-G2 §3.1–3.3), executable half.
Statements are canonical sparse ASTs; scopes are characteristic sets; checkers replay
certificates with Hex arithmetic and compute reach. The Mathlib soundness theorems live
in the binding package.
-/

namespace GPProfile
open Hex GP50

/-! ## Statements (§3.1) -/

inductive Kind where
  | empty | nonempty
  | inIdeal (h : Sparse)
  | vanishesOn (h : Sparse)
  deriving Repr, DecidableEq

structure Stmt where
  vars : List String
  eqs : List Sparse
  guards : List Sparse
  kind : Kind
  deriving Repr, DecidableEq

def Kind.target? : Kind → Option Sparse
  | .inIdeal h | .vanishesOn h => some h
  | _ => none

def Stmt.polys (s : Stmt) : List Sparse := s.eqs ++ s.guards ++ s.kind.target?.toList

/-- Every polynomial is canonical and has the declared arity. -/
def Stmt.canonical (s : Stmt) : Bool :=
  s.vars.eraseDups.length == s.vars.length &&
    s.polys.all fun p => GPProfile.canonical s.vars.length p == some p

/-- `S_stmt`: primes dividing any coefficient denominator, including the target's. -/
def Stmt.primes (s : Stmt) : List Nat := denominatorPrimes (s.polys.flatMap Sparse.coeffs)

/-! ## Scopes: characteristic sets (§3.2) -/

inductive PrimeSet where
  | finite (primes : List Nat)
  | cofinite (excluded : List Nat)
  deriving Repr, DecidableEq

structure Scope where
  char0 : Bool
  primes : PrimeSet
  deriving Repr, DecidableEq

/-- Exact inclusion of denotations: `char0` plus the selected primes. -/
def Scope.le (a b : Scope) : Bool :=
  (!a.char0 || b.char0) &&
  match a.primes, b.primes with
  | .finite xs, .finite ys => xs.all fun x => !isPrime x || ys.contains x
  | .finite xs, .cofinite e => xs.all fun x => !isPrime x || !e.contains x
  | .cofinite _, .finite _ => false
  | .cofinite ea, .cofinite eb => eb.all fun x => !isPrime x || ea.contains x

/-- Well-formedness (§3.2): the scope's characteristics avoid `S_stmt`. -/
def Scope.avoids (s : Scope) (bad : List Nat) : Bool :=
  match s.primes with
  | .finite ps => ps.all fun p => !isPrime p || !bad.contains p
  | .cofinite e => bad.all fun p => e.contains p

def Scope.only (p : Nat) : Scope := ⟨false, .finite [p]⟩
def Scope.char0Only : Scope := ⟨true, .finite []⟩
def Scope.outside (bad : List Nat) : Scope := ⟨true, .cofinite bad⟩

/-! ## Certificates and checkers (§3.3) -/

inductive Field where
  | rat
  | prime (p : Nat)
  deriving Repr, DecidableEq

inductive Cert where
  /-- C1/C3: `h^m · (∏ guards)^k = Σ qᵢ·eqᵢ` (C1 has `h = 1`). -/
  | ideal (field : Field) (cofactors : List Sparse) (m k : Nat)
  /-- C2: a point of the locus. -/
  | point (field : Field) (values : List Rat)
  deriving Repr, DecidableEq

def Cert.field : Cert → Field
  | .ideal f .. | .point f _ => f

def Cert.primes : Cert → List Nat
  | .ideal _ qs .. => denominatorPrimes (qs.flatMap Sparse.coeffs)
  | .point _ vs => denominatorPrimes vs

/-- Exponents beyond this bound are refused rather than expanded. -/
def maxExponent : Nat := 64

section Replay
variable {R : Type} [Zero R] [One R] [Add R] [Neg R] [Mul R] [DecidableEq R]

/-- `Σ qᵢ·eqᵢ − h^m·(∏ guards)^k = 0`, computed with HexMvPoly arithmetic. -/
def identityHolds (n : Nat) (coeff : Rat → Option R) (s : Stmt) (qs : List Sparse)
    (h : Sparse) (m k : Nat) : Bool :=
  match s.eqs.mapM (toHex n coeff), s.guards.mapM (toHex n coeff), qs.mapM (toHex n coeff),
      toHex n coeff h with
  | some eqs, some guards, some qs, some h =>
    eqs.length == qs.length &&
      ((qs.zip eqs).foldl (fun acc (q, e) => acc + q * e) 0 -
        h ^ m * (if k == 0 then 1 else guards.foldl (· * ·) 1 ^ k)) == 0
  | _, _, _, _ => false
end Replay

/-- The polynomial whose multiple must lie in the ideal, and the exponent `m` it needs. -/
def idealTarget (s : Stmt) (m : Nat) : Option Sparse :=
  match s.kind with
  | .empty => if m == 0 then some [(List.replicate s.vars.length 0, 1)] else none
  | .inIdeal h => if m == 1 then some h else none
  | .vanishesOn h => if 1 ≤ m then some h else none
  | .nonempty => none

/-- C2 over a coefficient ring: equations vanish and guards do not. -/
def pointHolds {R : Type} [Lean.Grind.Semiring R] [DecidableEq R]
    (n : Nat) (coeff : Rat → Option R) (s : Stmt) (x : Fin n → R) : Bool :=
  match s.eqs.mapM (toHex n coeff), s.guards.mapM (toHex n coeff) with
  | some eqs, some guards =>
    eqs.all (fun e => MvPoly.eval x e == 0) && guards.all (fun g => !(MvPoly.eval x g == 0))
  | _, _ => false

def pointFn {R : Type} [Zero R] (values : List R) (n : Nat) : Fin n → R :=
  fun i => values.getD i.val 0

/-- Primes dividing the numerator of some guard value at a rational point (GP-X410). -/
def guardPrimes (n : Nat) (s : Stmt) (values : List Rat) : List Nat :=
  match s.guards.mapM (toHex n some) with
  | some guards => guards.foldl (fun acc g =>
      union acc (primeFactors (MvPoly.eval (pointFn values n) g).num.natAbs)) []
  | none => []

/-- The computed reach of a certificate for a statement, or `none` when replay fails. -/
def reach (s : Stmt) (c : Cert) : Option Scope :=
  let n := s.vars.length
  let bad := union s.primes c.primes
  match c with
  | .ideal field qs m k =>
    if m > maxExponent || k > maxExponent then none else do
    let h ← idealTarget s m
    match field with
    | .rat => if identityHolds n some s qs h m k then some (.outside bad) else none
    | .prime (p + 1) =>
      if !isPrime (p + 1) || bad.contains (p + 1) then none
      else if identityHolds n (ratFin p) s qs h m k then some (.only (p + 1)) else none
    | .prime 0 => none
  | .point field values =>
    if s.kind != .nonempty || values.length != n then none else
    match field with
    | .rat =>
      if pointHolds n some s (pointFn values n)
      then some (.outside (union bad (guardPrimes n s values))) else none
    | .prime (p + 1) =>
      if !isPrime (p + 1) || bad.contains (p + 1) then none else
      match values.mapM (ratFin p) with
      | some xs => if pointHolds n (ratFin p) s (pointFn xs n) then some (.only (p + 1)) else none
      | none => none
    | .prime 0 => none

/-! ## Profile operations and receipt admission -/

def contra (a b : Stmt) : Bool :=
  a.vars == b.vars && a.eqs == b.eqs && a.guards == b.guards &&
    ((a.kind == .empty && b.kind == .nonempty) || (a.kind == .nonempty && b.kind == .empty))

def ops : Semantic.ProfileOps where
  Stmt := Stmt
  Scope := Scope
  same a b := decide (a = b)
  same_sound := by intro a b h; exact of_decide_eq_true h
  le := Scope.le
  contra := contra

abbrev Clause := Semantic.Clause ops

structure Receipt where
  name : String
  claim : Nat
  version : Nat
  binding : Binding
  cert : Cert
  deriving Repr, DecidableEq

/-- Why a bound receipt does or does not support its clause (diagnostics only). -/
inductive Check where
  | accepted (reach : Scope)
  | notCanonical
  | illFormed (sStmt : List Nat)
  | replayFailed
  | outsideReach (reach : Scope)
  deriving Repr, DecidableEq

def check (stmt : Stmt) (scope : Scope) (cert : Cert) : Check :=
  if !stmt.canonical then .notCanonical
  else if !scope.avoids stmt.primes then .illFormed stmt.primes
  else match reach stmt cert with
    | some r => if scope.le r then .accepted r else .outsideReach r
    | none =>
      -- A prime-field certificate that is not p-integral is refused on reach: report the
      -- reach the same cofactors compute over ℚ (diagnostic only; `ok` stays false).
      match cert with
      | .ideal (.prime p) qs m k =>
        if (union stmt.primes cert.primes).contains p then
          match reach stmt (.ideal .rat qs m k) with
          | some r => .outsideReach r
          | none => .replayFailed
        else .replayFailed
      | _ => .replayFailed

def Check.ok : Check → Bool
  | .accepted _ => true
  | _ => false

def wellFormed (clauses : List Clause) (receipts : List Receipt) : Bool :=
  (clauses.map (·.key)).eraseDups.length == clauses.length &&
    (receipts.map (·.name)).eraseDups.length == receipts.length

def accepts (clauses : List Clause) (receipts : List Receipt) (w : Warrant) (name : String) : Bool :=
  wellFormed clauses receipts &&
    clauses.any fun c => c.key == w.claim && c.version == w.version && decide (c.binding = w.binding) &&
      receipts.any fun r => r.name == name && r.claim == c.key && r.version == c.version &&
        decide (r.binding = c.binding) && (check c.stmt c.scope r.cert).ok

def admission (clauses : List Clause) (receipts : List Receipt) : Admission :=
  Semantic.withNarrowing ops clauses { Admission.refuseAll with receipt := accepts clauses receipts }

end GPProfile
