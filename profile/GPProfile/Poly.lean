import HexMvPoly

/-!
Canonical sparse polynomials (the 3a wire/AST form, post-G2 §3.1) and their conversion to
`HexMvPoly`. A `Sparse` polynomial is a list of (exponent vector, nonzero rational) terms,
strictly increasing in exponent order, so equality of `Sparse` values is equality of
polynomials. All arithmetic runs on `Hex.MvPoly n R Mono.lex` (Addendum A §3.1, §3.3).
-/

namespace GPProfile
open Hex

abbrev Sparse := List (List Nat × Rat)

/-! ## Primes (Mathlib-free; the binding package relates `isPrime` to `Nat.Prime`) -/

def isPrime (n : Nat) : Bool :=
  2 ≤ n && (List.range (n.sqrt + 1)).all fun d => d < 2 || n % d != 0

/-- Distinct prime factors, ascending, by trial division. -/
def primeFactors (n : Nat) : List Nat :=
  go n 2 n
where
  go (m d : Nat) : Nat → List Nat
    | 0 => []
    | fuel + 1 =>
      if m ≤ 1 then []
      else if d * d > m then [m]
      else if m % d == 0 then
        let rest := go (strip m d m) (d + 1) fuel
        d :: rest
      else go m (d + 1) fuel
  strip (m d : Nat) : Nat → Nat
    | 0 => m
    | fuel + 1 => if d ≥ 2 && m % d == 0 then strip (m / d) d fuel else m

def union (a b : List Nat) : List Nat := (a ++ b).eraseDups.mergeSort (· ≤ ·)

/-- Primes dividing some denominator. -/
def denominatorPrimes (cs : List Rat) : List Nat :=
  cs.foldl (fun acc c => union acc (primeFactors c.den)) []

def Sparse.coeffs (p : Sparse) : List Rat := p.map (·.2)

/-! ## Conversion to Hex polynomials -/

abbrev P (n : Nat) (R : Type) [Zero R] := MvPoly n R (Mono.lex (n := n))

def mono? (n : Nat) (e : List Nat) : Option (Mono n) :=
  if h : e.toArray.size = n then some ⟨e.toArray, h⟩ else none

def toHex (n : Nat) {R : Type} [Zero R] [Add R] [BEq R] [LawfulBEq R]
    (coeff : Rat → Option R) (p : Sparse) : Option (P n R) := do
  let terms ← p.mapM fun (e, c) => do pure (← mono? n e, ← coeff c)
  pure (MvPoly.ofTerms terms)

def ofHex {n : Nat} (p : P n Rat) : Sparse :=
  p.termsList.map fun (m, c) => (m.toList, c)

def canonical (n : Nat) (p : Sparse) : Option Sparse :=
  ofHex <$> toHex (R := Rat) n some p

/-! ## Residues modulo a prime -/

def modInv (a p : Nat) : Option Nat :=
  let rec go (r0 r1 : Int) (s0 s1 : Int) : Nat → Option Int
    | 0 => none
    | fuel + 1 => if r1 == 0 then (if r0 == 1 then some s0 else none)
      else let q := r0 / r1; go r1 (r0 - q * r1) s1 (s0 - q * s1) fuel
  (go (a % p) p 1 0 (2 * p + 2)).map fun s => (s % (p : Int)).toNat

/-- `c mod p` for a p-integral rational; `none` when `p` divides the denominator. -/
def ratMod (p : Nat) (c : Rat) : Option Nat := do
  let inv ← modInv (c.den % p) p
  pure (((c.num % p).toNat * inv) % p)

/-- `c` in `Fin (k+1)`, i.e. modulo `p = k + 1`; `none` when `p` divides the denominator.
Core `Fin` arithmetic is used instead of HexModArith (A3 deviation, DECISIONS 2026-10-02). -/
def ratFin (k : Nat) (c : Rat) : Option (Fin (k + 1)) :=
  (ratMod (k + 1) c).map fun r => ⟨r % (k + 1), Nat.mod_lt _ (Nat.succ_pos k)⟩

/-! ## Infix parser (untrusted adapter, §3.1): Singular/Macaulay2-style input to `Sparse` -/

inductive Tok where
  | num (n : Nat) | ident (s : String) | op (c : Char)
  deriving Repr, BEq

def tokenize (s : String) : Except String (List Tok) :=
  go s.toList [] (s.length + 1)
where
  go : List Char → List Tok → Nat → Except String (List Tok)
    | _, _, 0 => .error "tokenizer fuel exhausted"
    | [], acc, _ => .ok acc.reverse
    | c :: cs, acc, fuel + 1 =>
      if c.isWhitespace then go cs acc fuel
      else if c.isDigit then
        let digits := (c :: cs).takeWhile Char.isDigit
        go ((c :: cs).drop digits.length) (.num (String.ofList digits).toNat! :: acc) fuel
      else if c.isAlpha || c == '_' then
        let name := (c :: cs).takeWhile fun d => d.isAlphanum || d == '_'
        go ((c :: cs).drop name.length) (.ident (String.ofList name) :: acc) fuel
      else if "+-*/^()".toList.contains c then go cs (.op c :: acc) fuel
      else .error s!"unexpected character '{c}'"

section Parser
variable (n : Nat) (vars : List String)

def constant? (p : P n Rat) : Option Rat :=
  match p.termsList with
  | [] => some 0
  | [(m, c)] => if m.toList.all (· == 0) then some c else none
  | _ => none

-- Recursive descent with fuel bounded by the token count; returns the value and the rest.
mutual
def expr : Nat → List Tok → Except String (P n Rat × List Tok)
  | 0, _ => .error "parser fuel exhausted"
  | fuel + 1, ts => do
    let (first, rest) ← match ts with
      | .op '-' :: r => do let (t, r) ← term fuel r; pure (-t, r)
      | .op '+' :: r => term fuel r
      | r => term fuel r
    exprTail fuel first rest
def exprTail : Nat → P n Rat → List Tok → Except String (P n Rat × List Tok)
  | 0, _, _ => .error "parser fuel exhausted"
  | fuel + 1, acc, .op '+' :: r => do let (t, r) ← term fuel r; exprTail fuel (acc + t) r
  | fuel + 1, acc, .op '-' :: r => do let (t, r) ← term fuel r; exprTail fuel (acc - t) r
  | _, acc, r => .ok (acc, r)
def term : Nat → List Tok → Except String (P n Rat × List Tok)
  | 0, _ => .error "parser fuel exhausted"
  | fuel + 1, ts => do let (f, r) ← power fuel ts; termTail fuel f r
def termTail : Nat → P n Rat → List Tok → Except String (P n Rat × List Tok)
  | 0, _, _ => .error "parser fuel exhausted"
  | fuel + 1, acc, .op '*' :: r => do let (f, r) ← power fuel r; termTail fuel (acc * f) r
  | fuel + 1, acc, .op '/' :: r => do
    let (f, r) ← power fuel r
    match constant? n f with
    | some c => if c == 0 then .error "division by zero" else termTail fuel (acc * MvPoly.C c⁻¹) r
    | none => .error "division by a nonconstant polynomial"
  | _, acc, r => .ok (acc, r)
def power : Nat → List Tok → Except String (P n Rat × List Tok)
  | 0, _ => .error "parser fuel exhausted"
  | fuel + 1, ts => do
    let (b, r) ← atom fuel ts
    match r with
    | .op '^' :: .num k :: r => .ok (b ^ k, r)
    | .op '^' :: _ => .error "exponent must be a natural literal"
    | r => .ok (b, r)
def atom : Nat → List Tok → Except String (P n Rat × List Tok)
  | 0, _ => .error "parser fuel exhausted"
  | _, .num k :: r => .ok (MvPoly.C (k : Rat), r)
  | _, .ident s :: r =>
    match vars.idxOf? s with
    | some i => if h : i < n then .ok (MvPoly.X ⟨i, h⟩, r) else .error s!"variable out of range: {s}"
    | none => .error s!"undeclared variable: {s}"
  | fuel + 1, .op '(' :: r => do
    let (e, r) ← expr fuel r
    match r with
    | .op ')' :: r => .ok (e, r)
    | _ => .error "missing ')'"
  | fuel + 1, .op '-' :: r => do let (a, r) ← atom fuel r; .ok (-a, r)
  | _, t :: _ => .error s!"unexpected token {repr t}"
  | _, [] => .error "unexpected end of input"
end

end Parser

/-- Identifiers in an infix text, in order of first appearance. -/
def identifiers (text : String) : List String :=
  match tokenize text with
  | .ok toks => (toks.filterMap fun t => match t with | .ident s => some s | _ => none).eraseDups
  | .error _ => []

/-- Parse an infix polynomial over the declared variables into canonical sparse form.
Named parameters are substituted by natural literals before parsing. -/
def parse (vars : List String) (text : String) (params : List (String × Nat) := []) :
    Except String Sparse := do
  let toks := (← tokenize text).map fun t => match t with
    | .ident s => match params.lookup s with | some k => .num k | none => t
    | t => t
  let (p, rest) ← expr vars.length vars (2 * toks.length + 2) toks
  if !rest.isEmpty then throw s!"trailing input in '{text}'"
  pure (ofHex p)

end GPProfile
