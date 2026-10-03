import GPBinding.Admission.Semantics

/-!
Reach soundness for C1/C2/C3 (post-G2 §3.3): when `reach s c = some r`, the statement holds
in every field whose characteristic `r` denotes. Q replays and F_p replays (a rational residual
vanishing mod p) share one proof.
-/

noncomputable section

namespace GPBinding.Admission
open GPProfile MvPolynomial HexMvPolyMathlib

variable {K : Type*} [Field K]

/-! ## List helpers -/

theorem toK_zipWith_mul {σ : Type*} :
    ∀ (A B : List (MvPolynomial σ Rat)), (∀ P ∈ A, P ∈ GoodPoly K σ) → (∀ P ∈ B, P ∈ GoodPoly K σ) →
      (List.zipWith (· * ·) A B).map (toK (K := K)) =
        List.zipWith (· * ·) (A.map (toK (K := K))) (B.map (toK (K := K)))
  | [], _, _, _ => by simp
  | _ :: _, [], _, _ => by simp
  | a :: A, b :: B, hA, hB => by
    simp only [List.zipWith_cons_cons, List.map_cons]
    rw [toK_mul (hA a List.mem_cons_self) (hB b List.mem_cons_self),
      toK_zipWith_mul A B (fun P h => hA P (List.mem_cons_of_mem _ h))
        (fun P h => hB P (List.mem_cons_of_mem _ h))]

theorem zipWith_mul_good {σ : Type*} :
    ∀ (A B : List (MvPolynomial σ Rat)), (∀ P ∈ A, P ∈ GoodPoly K σ) → (∀ P ∈ B, P ∈ GoodPoly K σ) →
      ∀ P ∈ List.zipWith (· * ·) A B, P ∈ GoodPoly K σ
  | [], _, _, _ => by simp
  | _ :: _, [], _, _ => by simp
  | a :: A, b :: B, hA, hB => by
    intro P hP
    simp only [List.zipWith_cons_cons, List.mem_cons] at hP
    rcases hP with rfl | hP
    · exact (GoodPoly K σ).mul_mem (hA a List.mem_cons_self) (hB b List.mem_cons_self)
    · exact zipWith_mul_good A B (fun P h => hA P (List.mem_cons_of_mem _ h))
        (fun P h => hB P (List.mem_cons_of_mem _ h)) P hP

theorem eval_zipWith_sum_zero {n : ℕ} (x : Fin n → K) :
    ∀ (A B : List (MvPolynomial (Fin n) K)), (∀ b ∈ B, eval x b = 0) →
      eval x (List.zipWith (· * ·) A B).sum = 0
  | [], _, _ => by simp
  | _ :: _, [], _ => by simp
  | a :: A, b :: B, hB => by
    simp only [List.zipWith_cons_cons, List.sum_cons, map_add, map_mul]
    rw [hB b List.mem_cons_self, mul_zero, zero_add,
      eval_zipWith_sum_zero x A B fun c h => hB c (List.mem_cons_of_mem _ h)]

theorem eval_prod_ne_zero {n : ℕ} (x : Fin n → K) :
    ∀ (l : List (MvPolynomial (Fin n) K)), (∀ g ∈ l, eval x g ≠ 0) → eval x l.prod ≠ 0
  | [], _ => by simp
  | g :: l, h => by
    rw [List.prod_cons, map_mul]
    exact mul_ne_zero (h g List.mem_cons_self)
      (eval_prod_ne_zero x l fun c hc => h c (List.mem_cons_of_mem _ hc))

theorem zipWith_sum_mem_span {R : Type*} [CommRing R] :
    ∀ (A B : List R), (List.zipWith (· * ·) A B).sum ∈ Ideal.span {f | f ∈ B}
  | [], _ => by simp
  | _ :: _, [] => by simp
  | a :: A, b :: B => by
    simp only [List.zipWith_cons_cons, List.sum_cons]
    refine Ideal.add_mem _ (Ideal.mul_mem_left _ _ (Ideal.subset_span List.mem_cons_self)) ?_
    exact Ideal.span_mono (fun f hf => List.mem_cons_of_mem _ hf) (zipWith_sum_mem_span A B)

/-! ## The identity in `K[x]` -/

/-- Every coefficient of every listed sparse polynomial is good in `K`. -/
def AllGood (K : Type*) [Field K] (ps : List Sparse) : Prop := ∀ p ∈ ps, ∀ c ∈ p.coeffs, c ∈ Good K

theorem identity_in_K {n : ℕ} {s : Stmt} {qs : List Sparse} {h : Sparse} {m k : ℕ}
    {R : GPProfile.P n Rat} (hR : residual n s qs h m k = some R)
    (hgood : AllGood K (s.eqs ++ s.guards ++ qs ++ [h]))
    (hzero : toK (K := K) (toMvPolynomial R) = 0) :
    qs.length = s.eqs.length ∧
      (List.zipWith (· * ·) (qs.map fun q => toK (K := K) (meaning n q))
        (s.eqs.map fun e => toK (K := K) (meaning n e))).sum =
        toK (meaning n h) ^ m * (s.guards.map fun g => toK (K := K) (meaning n g)).prod ^ k := by
  obtain ⟨hlen, hR'⟩ := residual_meaning hR
  refine ⟨hlen, ?_⟩
  have good : ∀ p ∈ s.eqs ++ s.guards ++ qs ++ [h], meaning n p ∈ GoodPoly K (Fin n) :=
    fun p hp => meaning_good (hgood p hp)
  have gE : ∀ P ∈ s.eqs.map (meaning n), P ∈ GoodPoly K (Fin n) := by
    intro P hP; obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hP; exact good p (by simp [hp])
  have gG : ∀ P ∈ s.guards.map (meaning n), P ∈ GoodPoly K (Fin n) := by
    intro P hP; obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hP; exact good p (by simp [hp])
  have gQ : ∀ P ∈ qs.map (meaning n), P ∈ GoodPoly K (Fin n) := by
    intro P hP; obtain ⟨p, hp, rfl⟩ := List.mem_map.mp hP; exact good p (by simp [hp])
  have gH : meaning n h ∈ GoodPoly K (Fin n) := good h (by simp)
  have gS := (GoodPoly K (Fin n)).list_sum_mem (zipWith_mul_good _ _ gQ gE)
  have gP := (GoodPoly K (Fin n)).mul_mem ((GoodPoly K (Fin n)).pow_mem gH m)
    ((GoodPoly K (Fin n)).pow_mem ((GoodPoly K (Fin n)).list_prod_mem gG) k)
  rw [hR', toK_sub gS gP, sub_eq_zero, toK_list_sum _ (zipWith_mul_good _ _ gQ gE),
    toK_zipWith_mul _ _ gQ gE, toK_mul ((GoodPoly K (Fin n)).pow_mem gH m)
      ((GoodPoly K (Fin n)).pow_mem ((GoodPoly K (Fin n)).list_prod_mem gG) k),
    toK_pow gH, toK_pow ((GoodPoly K (Fin n)).list_prod_mem gG), toK_list_prod _ gG,
    List.map_map, List.map_map, List.map_map] at hzero
  exact hzero

/-- A rational residual that vanishes mod `ringChar K` maps to zero. -/
theorem toK_residual_zero_mod {n : ℕ} {R : GPProfile.P n Rat} {p : ℕ} (hK : ringChar K = p)
    (h : R.termsList.all (fun t => zeroMod p t.2) = true) : toK (K := K) (toMvPolynomial R) = 0 := by
  ext d
  obtain ⟨m, rfl⟩ := (monoEquiv (n := n)).surjective d
  rw [coeff_toK, coeff_toMvPolynomial, coeff_zero]
  by_cases hc : Hex.MvPoly.coeff m R = 0
  · rw [hc, Rat.cast_zero]
  · have hz := List.all_eq_true.mp h _ (mem_terms_of_coeff_ne R m hc)
    simp only [zeroMod, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hz
    apply cast_eq_zero_of_dvd_num
    rw [hK]
    exact Int.dvd_of_emod_eq_zero hz.2

/-! ## Goodness from avoided primes -/

theorem allGood_of_avoids {ps : List Sparse} {bad : List ℕ} (h : Avoids K bad)
    (hsub : ∀ x ∈ denominatorPrimes (ps.flatMap Sparse.coeffs), x ∈ bad) : AllGood K ps :=
  fun p hp c hc => good_of_avoids (h.mono hsub) (List.mem_flatMap.mpr ⟨p, hp, hc⟩)

theorem mem_denominatorPrimes_flatMap {ps qs : List Sparse} (hsub : ∀ p ∈ ps, p ∈ qs) {x : ℕ}
    (hx : x ∈ denominatorPrimes (ps.flatMap Sparse.coeffs)) :
    x ∈ denominatorPrimes (qs.flatMap Sparse.coeffs) := by
  obtain ⟨c, hc, h⟩ := mem_denominatorPrimes_iff.mp hx
  obtain ⟨p, hp, hc⟩ := List.mem_flatMap.mp hc
  exact mem_denominatorPrimes_iff.mpr ⟨c, List.mem_flatMap.mpr ⟨p, hsub p hp, hc⟩, h⟩

/-! ## Reach soundness -/

theorem reach_ideal_spec {s : Stmt} {field : Field} {qs : List Sparse}
    {m k : ℕ} {r : Scope} (hr : reach s (.ideal field qs m k) = some r) (hK : r.mem K) :
    ∃ h R, idealTarget s m = some h ∧ residual s.vars.length s qs h m k = some R ∧
      Avoids K (union s.primes (denominatorPrimes (qs.flatMap Sparse.coeffs))) ∧
      toK (K := K) (toMvPolynomial R) = 0 := by
  simp only [reach, Cert.primes] at hr
  split_ifs at hr with h1
  cases ht : idealTarget s m with
  | none => simp [ht] at hr
  | some h =>
    simp only [ht, Option.bind_eq_bind, Option.bind_some] at hr
    split_ifs at hr with h2
    cases hres : residual s.vars.length s qs h m k with
    | none => simp [hres] at hr
    | some R =>
      simp only [hres, Option.bind_some] at hr
      cases field with
      | rat =>
        dsimp only at hr
        split_ifs at hr with h3
        simp only [Option.some.injEq] at hr
        subst hr
        refine ⟨h, R, rfl, hres, mem_outside hK, ?_⟩
        rw [beq_iff_eq.mp h3]
        simp [toK_zero]
      | prime p =>
        simp at hr
        obtain ⟨⟨hpr, hnb⟩, hz, rfl⟩ := hr
        have hc := mem_only hK
        refine ⟨h, R, rfl, hres, Or.inr ⟨hc ▸ (isPrime_iff p).mp hpr, hc ▸ hnb⟩, ?_⟩
        exact toK_residual_zero_mod hc (List.all_eq_true.mpr fun t ht => hz t.1 t.2 ht)

theorem stmt_poly_primes {s : Stmt} {bad : List ℕ}
    (hsub : ∀ x ∈ s.primes, x ∈ bad) {p : Sparse} (hp : p ∈ s.polys) {c : Rat}
    (hc : c ∈ p.coeffs) {x : ℕ} (hx : x ∈ primeFactors c.den) : x ∈ bad :=
  hsub x (mem_denominatorPrimes_iff.mpr ⟨c, List.mem_flatMap.mpr ⟨p, hp, hc⟩, hx⟩)

theorem reach_ideal_sound {s : Stmt} {field : Field} {qs : List Sparse}
    {m k : ℕ} {r : Scope} (hr : reach s (.ideal field qs m k) = some r) (hK : r.mem K) :
    Holds K s := by
  obtain ⟨h, R, ht, hres, havoid, hzero⟩ := reach_ideal_spec hr hK
  have hS : ∀ x ∈ s.primes, x ∈ union s.primes (denominatorPrimes (qs.flatMap Sparse.coeffs)) :=
    fun x hx => mem_union_left hx
  have hgood : AllGood K (s.eqs ++ s.guards ++ qs ++ [h]) := by
    apply allGood_of_avoids havoid
    intro x hx
    obtain ⟨c, hc, hxc⟩ := mem_denominatorPrimes_iff.mp hx
    obtain ⟨p, hp, hcp⟩ := List.mem_flatMap.mp hc
    simp only [List.mem_append, List.mem_singleton] at hp
    rcases hp with ((hp | hp) | hp) | rfl
    · exact stmt_poly_primes hS (by simp [Stmt.polys, hp]) hcp hxc
    · exact stmt_poly_primes hS (by simp [Stmt.polys, hp]) hcp hxc
    · exact mem_union_right (mem_denominatorPrimes_iff.mpr ⟨c, List.mem_flatMap.mpr ⟨p, hp, hcp⟩, hxc⟩)
    · unfold idealTarget at ht
      cases hk : s.kind with
      | empty =>
        simp only [hk] at ht
        split_ifs at ht
        simp only [Option.some.injEq] at ht
        subst ht
        simp only [Sparse.coeffs, List.map_cons, List.map_nil, List.mem_singleton] at hcp
        subst hcp
        simp [primeFactors_one] at hxc
      | nonempty => simp [hk] at ht
      | inIdeal h0 =>
        simp only [hk] at ht; split_ifs at ht; simp only [Option.some.injEq] at ht; subst ht
        exact stmt_poly_primes hS (by simp [Stmt.polys, hk, Kind.target?]) hcp hxc
      | vanishesOn h0 =>
        simp only [hk] at ht; split_ifs at ht; simp only [Option.some.injEq] at ht; subst ht
        exact stmt_poly_primes hS (by simp [Stmt.polys, hk, Kind.target?]) hcp hxc
  obtain ⟨hlen, I⟩ := identity_in_K hres hgood hzero
  have locusEval : ∀ x, Locus (K := K) s x →
      eval x (List.zipWith (· * ·) (qs.map fun q => toK (K := K) (meaning _ q))
        (s.eqs.map fun e => toK (K := K) (meaning _ e))).sum = 0 ∧
      eval x (s.guards.map fun g => toK (K := K) (meaning _ g)).prod ≠ 0 := by
    intro x ⟨he, hg⟩
    refine ⟨eval_zipWith_sum_zero x _ _ ?_, eval_prod_ne_zero x _ ?_⟩
    · intro b hb; obtain ⟨e, heq, rfl⟩ := List.mem_map.mp hb; exact he e heq
    · intro b hb; obtain ⟨g, hgq, rfl⟩ := List.mem_map.mp hb; exact hg g hgq
  unfold idealTarget at ht
  unfold Holds
  cases hk : s.kind with
  | empty =>
    simp only [hk] at ht; split_ifs at ht with hm
    simp only [beq_iff_eq] at hm; subst hm
    intro x hx
    obtain ⟨h0, hG⟩ := locusEval x hx
    rw [I, map_mul, map_pow, map_pow, pow_zero, one_mul] at h0
    exact hG (pow_eq_zero_iff'.mp h0).1
  | nonempty => simp [hk] at ht
  | inIdeal h0 =>
    simp only [hk] at ht; split_ifs at ht with hm
    simp only [beq_iff_eq] at hm; subst hm
    simp only [Option.some.injEq] at ht; subst ht
    refine ⟨k, ?_⟩
    rw [← pow_one (toK (meaning _ h0)), ← I]
    exact zipWith_sum_mem_span _ _
  | vanishesOn h0 =>
    simp only [hk] at ht; split_ifs at ht with hm
    simp only [Option.some.injEq] at ht; subst ht
    intro x hx
    obtain ⟨h0, hG⟩ := locusEval x hx
    rw [I, map_mul, map_pow, map_pow] at h0
    rcases mul_eq_zero.mp h0 with hv | hv
    · exact pow_eq_zero_iff (by omega) |>.mp hv
    · exact absurd (pow_eq_zero_iff'.mp hv).1 hG

theorem eval_toK_cast {n : ℕ} {P : MvPolynomial (Fin n) Rat}
    (hP : P ∈ GoodPoly K (Fin n)) {a : Fin n → Rat} (ha : ∀ i, a i ∈ Good K) :
    eval (fun i => ((a i : Rat) : K)) (toK P) = ((eval a P : Rat) : K) ∧ eval a P ∈ Good K := by
  obtain ⟨P', rfl, hPK⟩ := toK_lift hP
  let a' : Fin n → Good K := fun i => ⟨a i, ha i⟩
  have hx : (fun i => ((a i : Rat) : K)) = castGood K ∘ a' := rfl
  have hq : a = (Good K).subtype ∘ a' := rfl
  have hv : eval a (MvPolynomial.map (Good K).subtype P') = ((eval a' P' : Good K) : Rat) := by
    rw [eval_map, hq, ← eval₂_comp]; rfl
  rw [hPK, hx, eval_map, ← eval₂_comp, hv]
  exact ⟨rfl, (eval a' P').2⟩

theorem reach_point_spec {s : Stmt} {field : Field} {vs : List Rat}
    {r : Scope} (hr : reach s (.point field vs) = some r) (hK : r.mem K) :
    s.kind = .nonempty ∧ ∃ ev gv, pointValues s.vars.length s vs = some (ev, gv) ∧
      Avoids K (union s.primes (denominatorPrimes vs)) ∧
      (∀ v ∈ ev, (v : K) = 0) ∧ (∀ v ∈ gv, v ∈ Good K → (v : K) ≠ 0) := by
  simp only [reach, Cert.primes] at hr
  split_ifs at hr with h1
  simp only [Bool.or_eq_true, bne_iff_ne, ne_eq, not_or, not_not] at h1
  cases hv : pointValues s.vars.length s vs with
  | none => simp [hv] at hr
  | some evgv =>
    obtain ⟨ev, gv⟩ := evgv
    simp only [hv, Option.bind_eq_bind, Option.bind_some] at hr
    refine ⟨h1.1, ev, gv, rfl, ?_⟩
    cases field with
    | rat =>
      simp at hr
      obtain ⟨⟨hev, hgv⟩, rfl⟩ := hr
      have hL := mem_outside hK
      have hbad : Avoids K (union s.primes (denominatorPrimes vs)) :=
        hL.mono fun x hx => (mem_foldl_union_iff _ _).mpr (Or.inl hx)
      refine ⟨hbad, fun v h => by rw [hev v h, Rat.cast_zero], fun v h hg => ?_⟩
      rw [Rat.cast_def]
      refine div_ne_zero (intCast_ne_zero_of_primes (Rat.num_ne_zero.mpr (hgv v h)) ?_) hg
      intro q hq hd
      exact hL.ne hq ((mem_foldl_union_iff _ _).mpr
        (Or.inr ⟨v, h, mem_primeFactors hq (Int.natAbs_pos.mpr (Rat.num_ne_zero.mpr (hgv v h))) hd⟩))
    | prime p =>
      simp at hr
      obtain ⟨⟨hpr, hnb⟩, ⟨hev, hgv⟩, rfl⟩ := hr
      have hc := mem_only hK
      refine ⟨Or.inr ⟨hc ▸ (isPrime_iff p).mp hpr, hc ▸ hnb⟩, fun v h => ?_, fun v h _ => ?_⟩
      · have hz := hev v h
        simp only [zeroMod, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hz
        apply cast_eq_zero_of_dvd_num
        rw [hc]; exact Int.dvd_of_emod_eq_zero hz.2
      · have hu := hgv v h
        simp only [unitMod, Bool.and_eq_true, bne_iff_ne, ne_eq] at hu
        rw [Rat.cast_def]
        refine div_ne_zero ?_ ?_
        · intro hn
          have := (CharP.intCast_eq_zero_iff K (ringChar K) v.num).mp hn
          rw [hc] at this
          exact hu.2 (Int.emod_eq_zero_of_dvd this)
        · intro hd
          have := (ringChar.spec K v.den).mp hd
          rw [hc] at this
          exact hu.1 (Nat.mod_eq_zero_of_dvd this)

theorem reach_point_sound {s : Stmt} {field : Field} {vs : List Rat}
    {r : Scope} (hr : reach s (.point field vs) = some r) (hK : r.mem K) : Holds K s := by
  obtain ⟨hk, ev, gv, hv, havoid, hev, hgv⟩ := reach_point_spec hr hK
  obtain ⟨hev', hgv'⟩ := pointValues_meaning hv
  have ha : ∀ i, pointFn vs s.vars.length i ∈ Good K := by
    intro i
    unfold pointFn
    by_cases hi : i.val < vs.length
    · rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some]
      exact good_of_avoids (havoid.mono fun x hx => mem_union_right hx) (List.getElem_mem hi)
    · rw [List.getD_eq_getElem?_getD, List.getElem?_eq_none (by omega), Option.getD_none]
      exact (Good K).zero_mem
  have hS : Avoids K (denominatorPrimes (s.polys.flatMap Sparse.coeffs)) :=
    havoid.mono fun x hx => mem_union_left hx
  have meaningGood : ∀ p ∈ s.polys, meaning s.vars.length p ∈ GoodPoly K (Fin s.vars.length) :=
    fun p hp => meaning_good fun c hc => good_of_avoids hS (List.mem_flatMap.mpr ⟨p, hp, hc⟩)
  unfold Holds
  rw [hk]
  refine ⟨fun i => ((pointFn vs _ i : Rat) : K), ?_, ?_⟩
  · intro e he
    obtain ⟨h1, -⟩ := eval_toK_cast (meaningGood e (by simp [Stmt.polys, he])) ha
    unfold value
    rw [h1]
    apply hev
    rw [hev']
    exact List.mem_map.mpr ⟨e, he, rfl⟩
  · intro g hg
    obtain ⟨h1, h2⟩ := eval_toK_cast (meaningGood g (by simp [Stmt.polys, hg])) ha
    unfold value
    rw [h1]
    apply hgv _ _ h2
    rw [hgv']
    exact List.mem_map.mpr ⟨g, hg, rfl⟩

/-- Reach soundness: a certificate's computed reach holds in every field it denotes. -/
theorem reach_sound {s : Stmt} {c : Cert} {r : Scope}
    (hr : reach s c = some r) (hK : r.mem K) : Holds K s := by
  cases c with
  | ideal field qs m k => exact reach_ideal_sound hr hK
  | point field vs => exact reach_point_sound hr hK

/-- An accepted receipt check: the statement holds throughout the requested scope. -/
theorem check_sound {s : Stmt} {scope : Scope} {c : Cert} {r : Scope}
    (h : check s scope c = .accepted r) (hK : scope.mem K) : Holds K s := by
  unfold check at h
  split_ifs at h
  cases hr : reach s c with
  | none =>
    simp only [hr] at h
    split at h <;> (try split_ifs at h) <;> (try split at h) <;> simp_all
  | some r' =>
    simp only [hr] at h
    split_ifs at h with hle
    exact reach_sound hr (Scope.le_den hle hK)

end GPBinding.Admission

end
