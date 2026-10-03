import GPProfile.Rules

/-!
Executable checks of the K3 IN_IDEAL rows (G3a review §3), evaluated at build time. Each instance
runs the real `ruleReach`, so its obligations are replayed by the certificate checkers.
-/

namespace GPProfile.RuleChecks
open GPProfile

private def p (vars : List String) (t : String) : Sparse :=
  match parse vars t with
  | .ok q => (canonical vars.length q).getD q
  | .error _ => []

private def xy := ["x", "y"]

/-! ### R2: an identity survives restriction to a chart

The loose system `{x²y − x = 0, x ≠ 0}` and the hyperbola `{xy = 1}` have the same locus but
different presentations. Before the sound condition, R2 refused because the guards differ. -/

private def looseC : Stmt := ⟨xy, [p xy "x^2*y - x"], [p xy "x"], .inIdeal (p xy "y - x*y^2")⟩
private def tightC : Stmt := ⟨xy, [p xy "x*y - 1"], [], .inIdeal (p xy "y - x*y^2")⟩

-- x²y − x = x·(xy − 1); and x is a unit on the hyperbola: 1 = −(xy − 1) + y·x.
private def chart : RuleData :=
  .inclusion [.ideal .rat [p xy "x"] 1 0] [.ideal .rat [p xy "-1", p xy "y"] 0 0]

#guard ruleReach tightC [looseC] chart == some Scope.all

-- Without the guard obligation the loose guard is not known to be a unit: refused.
#guard ruleReach tightC [looseC] (.inclusion [.ideal .rat [p xy "x"] 1 0] []) == none

-- A wrong guard certificate fails replay: refused.
#guard ruleReach tightC [looseC] (.inclusion [.ideal .rat [p xy "x"] 1 0]
  [.ideal .rat [p xy "1", p xy "y"] 0 0]) == none

/-! ### R3: IN_IDEAL along a polynomial map

`φ : t ↦ −t` maps `{t² = 1}` into `{x² = 1, x ≠ 2}`; IN_IDEAL(x³ − x) on the target gives
IN_IDEAL(−t³ + t) on the source. The guard certificate divides by 3, so the computed reach
excludes characteristic 3, where `x = 2` and `x = −1` coincide and the guard vanishes. -/

private def target : Stmt := ⟨["x"], [p ["x"] "x^2 - 1"], [p ["x"] "x - 2"], .inIdeal (p ["x"] "x^3 - x")⟩
private def phi : List Sparse := [p ["t"] "-t"]
private def source : Stmt :=
  ⟨["t"], [p ["t"] "t^2 - 1"], [], .inIdeal ((compose 1 phi 1 (p ["x"] "x^3 - x")).getD [])⟩

-- (−t)² − 1 = 1·(t² − 1); 1 = (t² − 1)/3 + (t − 2)(−t − 2)/3.
private def along : RuleData :=
  .map phi [.ideal .rat [p ["t"] "1"] 1 0] [.ideal .rat [p ["t"] "1/3", p ["t"] "1/3*t - 2/3"] 0 0]

#guard ruleReach source [target] along == some (Scope.outside [3])

-- The conclusion must be the composed target: IN_IDEAL(t³ − t) with the wrong sign is refused.
#guard ruleReach { source with kind := .inIdeal (p ["t"] "t^3 - t") } [target] along == none

end GPProfile.RuleChecks
