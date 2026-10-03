import GPBinding.Admission.Profile
import GPProfile.Rules
import GP50.CoverProofs

/-!
Soundness of the K3 rules R1–R4 and their C4 relation certificates (post-G2 §3.4): when a rule
instance is accepted, the premises' meanings give the conclusion's meaning in every field of the
conclusion scope. These proofs are the direction tables.
-/

noncomputable section

namespace GPBinding.Admission
open GPProfile MvPolynomial HexMvPolyMathlib

variable {K : Type*} [Field K]

/-! ## Scope meets and certificate obligations -/

theorem meet_den {a b : Scope} {c : ℕ} (h : c ∈ (a.meet b).den) : c ∈ a.den ∧ c ∈ b.den := by
  obtain ⟨ca, pa⟩ := a
  obtain ⟨cb, pb⟩ := b
  rcases h with ⟨rfl, h0⟩ | ⟨hp, hm⟩
  · simp only [Scope.meet, Bool.and_eq_true] at h0
    exact ⟨Or.inl ⟨rfl, h0.1⟩, Or.inl ⟨rfl, h0.2⟩⟩
  · cases pa <;> cases pb <;>
      simp_all [Scope.meet, Scope.den, List.mem_filter, mem_union]

theorem foldl_meet_den :
    ∀ (rs : List Scope) (a : Scope) {c : ℕ}, c ∈ (rs.foldl Scope.meet a).den →
      c ∈ a.den ∧ ∀ r ∈ rs, c ∈ r.den
  | [], _, _, h => ⟨h, by simp⟩
  | r :: rs, a, c, h => by
    obtain ⟨h1, h2⟩ := foldl_meet_den rs (a.meet r) h
    obtain ⟨ha, hr⟩ := meet_den h1
    exact ⟨ha, fun r' hr' => (List.mem_cons.mp hr').elim (fun e => e ▸ hr) (h2 r')⟩

theorem forall₂_exists_right {α β : Type} {R : α → β → Prop} :
    ∀ {l : List α} {l' : List β}, List.Forall₂ R l l' → ∀ a ∈ l, ∃ b ∈ l', R a b
  | [], [], .nil, _, ha => by simp at ha
  | _ :: _, b :: _, .cons hab rest, a, ha => by
    rcases List.mem_cons.mp ha with rfl | ha
    · exact ⟨b, List.mem_cons_self, hab⟩
    · obtain ⟨b', hb', h⟩ := forall₂_exists_right rest a ha
      exact ⟨b', List.mem_cons_of_mem _ hb', h⟩

theorem reachAll_sound {obs : List (Stmt × Cert)} {rr : Scope} (h : reachAll obs = some rr)
    (hK : rr.mem K) : ∀ o ∈ obs, Holds K o.1 := by
  unfold reachAll at h
  cases hm : obs.mapM (fun o => reach o.1 o.2) with
  | none => simp [hm] at h
  | some rs =>
    simp only [hm, Option.map_some, Option.some.injEq] at h
    subst h
    intro o ho
    obtain ⟨r, hr, hreach⟩ := forall₂_exists_right (mapM_forall₂ hm) o ho
    exact reach_sound hreach ((foldl_meet_den rs Scope.all hK).2 r hr)

/-! ## Scopes that avoid primes -/

theorem avoids_mem {sc : Scope} {bad : List ℕ} (h : sc.avoids bad = true) (hK : sc.mem K) :
    Avoids K bad := by
  rcases hK with ⟨h0, -⟩ | ⟨hp, hm⟩
  · exact Or.inl h0
  · right
    refine ⟨hp, fun hb => ?_⟩
    obtain ⟨c0, ps⟩ := sc
    cases ps with
    | finite ps =>
      simp only [Scope.avoids, List.all_eq_true, Bool.or_eq_true, Bool.not_eq_eq_eq_not,
        Bool.not_true, List.contains_iff_mem] at h
      rcases h _ hm with h' | h'
      · exact absurd ((isPrime_iff _).mpr hp) (by simp [h'])
      · simp_all
    | cofinite e =>
      simp only [Scope.avoids, List.all_eq_true, List.contains_iff_mem] at h
      exact hm (h _ hb)

/-! ## Evaluation kills the ideal of the equations -/

theorem eval_span_zero {n : ℕ} {x : Fin n → K} {l : List (MvPolynomial (Fin n) K)}
    {f : MvPolynomial (Fin n) K} (hf : f ∈ Ideal.span {g | g ∈ l}) (hl : ∀ g ∈ l, eval x g = 0) :
    eval x f = 0 := by
  have hle : Ideal.span {g | g ∈ l} ≤ RingHom.ker (eval x) :=
    Ideal.span_le.mpr fun g hg => (RingHom.mem_ker).mpr (hl g hg)
  exact (RingHom.mem_ker).mp (hle hf)

theorem eval_guards_ne_zero {s : Stmt} {x : Fin s.vars.length → K} (hx : Locus (K := K) s x) :
    eval x (s.guards.map fun g => toK (K := K) (meaning s.vars.length g)).prod ≠ 0 :=
  eval_prod_ne_zero x _ fun b hb => by
    obtain ⟨g, hg, rfl⟩ := List.mem_map.mp hb
    exact hx.2 g hg

theorem eval_eqs_zero {s : Stmt} {x : Fin s.vars.length → K} (hx : Locus (K := K) s x) :
    ∀ b ∈ s.eqs.map (fun e => toK (K := K) (meaning s.vars.length e)), eval x b = 0 := by
  intro b hb
  obtain ⟨e, he, rfl⟩ := List.mem_map.mp hb
  exact hx.1 e he

/-! ## R1: IN_IDEAL(h) ⇒ VANISHES_ON(h) -/

theorem r1_sound {P C : Stmt} {r : Scope} (h : ruleReach C [P] .r1 = some r) (hP : Holds K P) :
    Holds K C := by
  obtain ⟨vP, eP, gP, kP⟩ := P
  obtain ⟨vC, eC, gC, kC⟩ := C
  simp only [ruleReach] at h
  cases kP <;> cases kC <;> simp only at h <;> try contradiction
  rename_i hP' hC'
  split_ifs at h with hs
  simp only [sameSystem, Bool.and_eq_true, beq_iff_eq] at hs
  obtain ⟨⟨⟨rfl, rfl⟩, rfl⟩, rfl⟩ := hs
  obtain ⟨k, hk⟩ := hP
  intro x hx
  have h0 := eval_span_zero hk (eval_eqs_zero hx)
  rw [map_mul, map_pow] at h0
  rcases mul_eq_zero.mp h0 with hv | hv
  · exact hv
  · exact absurd (pow_eq_zero_iff'.mp hv).1 (eval_guards_ne_zero hx)

/-! ## R4: object cover by a structural split -/

theorem r4_sound {B₁ B₂ C : Stmt} {h : Sparse} {r : Scope}
    (hr : ruleReach C [B₁, B₂] (.split h) = some r) (h₁ : Holds K B₁) (h₂ : Holds K B₂) :
    Holds K C := by
  simp only [ruleReach] at hr
  split_ifs at hr with hc
  simp only [Bool.and_eq_true, beq_iff_eq] at hc
  obtain ⟨⟨hkind, rfl⟩, rfl⟩ := hc
  obtain ⟨v, e, g, k⟩ := C
  have split : ∀ x, Locus (K := K) ⟨v, e, g, k⟩ x →
      Locus (K := K) ⟨v, e ++ [h], g, k⟩ x ∨ Locus (K := K) ⟨v, e, g ++ [h], k⟩ x := by
    intro x ⟨he, hg⟩
    by_cases hv : value v.length h x = 0
    · left
      refine ⟨fun e' he' => ?_, hg⟩
      rcases List.mem_append.mp he' with he' | he'
      · exact he e' he'
      · rw [List.mem_singleton.mp he']; exact hv
    · right
      refine ⟨he, fun g' hg' => ?_⟩
      rcases List.mem_append.mp hg' with hg' | hg'
      · exact hg g' hg'
      · rw [List.mem_singleton.mp hg']; exact hv
  cases k with
  | empty =>
    intro x hx
    rcases split x hx with hx | hx
    · exact h₁ x hx
    · exact h₂ x hx
  | vanishesOn f =>
    intro x hx
    rcases split x hx with hx | hx
    · exact h₁ x hx
    · exact h₂ x hx
  | nonempty => simp at hkind
  | inIdeal _ => simp at hkind

/-! ## C4 inclusion: the tight locus lies in the loose locus -/

theorem mem_zip_of_mem {α β : Type} {l : List α} {l' : List β} (hlen : l.length = l'.length)
    {a : α} (ha : a ∈ l) : ∃ b, (a, b) ∈ l.zip l' := by
  obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp ha
  exact ⟨l'[i]'(hlen ▸ hi), List.mem_iff_getElem.mpr ⟨i, by simp [hi, hlen ▸ hi], by simp⟩⟩

theorem inclusion_locus {T L : Stmt} {eqCerts guardCerts : List Cert} {obs : List (Stmt × Cert)}
    (h : inclusionObligations T L eqCerts guardCerts = some obs)
    (hobs : ∀ o ∈ obs, Holds K o.1) :
    T.vars = L.vars ∧ ∀ x, Locus (K := K) T x →
      (∀ e ∈ L.eqs, value T.vars.length e x = 0) ∧ (∀ g ∈ L.guards, value T.vars.length g x ≠ 0) := by
  unfold inclusionObligations at h
  split_ifs at h with hc
  simp only [Bool.or_eq_true, bne_iff_ne, ne_eq, not_or, not_not] at hc
  obtain ⟨⟨hv, he⟩, hg⟩ := hc
  simp only [Option.some.injEq] at h
  subst h
  refine ⟨hv, fun x hx => ⟨fun e heq => ?_, fun g hgq => ?_⟩⟩
  · obtain ⟨c, hc⟩ := mem_zip_of_mem he.symm heq
    have := hobs _ (List.mem_append_left _ (List.mem_map.mpr ⟨(e, c), hc, rfl⟩))
    exact this x hx
  · obtain ⟨c, hc⟩ := mem_zip_of_mem hg.symm hgq
    have := hobs _ (List.mem_append_right _ (List.mem_map.mpr ⟨(g, c), hc, rfl⟩))
    intro hz
    apply this x
    refine ⟨fun e' he' => ?_, hx.2⟩
    rcases List.mem_append.mp he' with he' | he'
    · exact hx.1 e' he'
    · rw [List.mem_singleton.mp he']; exact hz

theorem idealInclusion_span {T L : Stmt} {eqCerts : List Cert} {obs : List (Stmt × Cert)}
    (h : idealInclusionObligations T L eqCerts = some obs) (hobs : ∀ o ∈ obs, Holds K o.1) :
    T.vars = L.vars ∧ T.guards = L.guards ∧
      ∀ e ∈ L.eqs, toK (K := K) (meaning T.vars.length e) ∈
        Ideal.span {f | f ∈ T.eqs.map fun e => toK (K := K) (meaning T.vars.length e)} := by
  unfold idealInclusionObligations at h
  split_ifs at h with hc
  simp only [Bool.or_eq_true, bne_iff_ne, ne_eq, not_or, not_not] at hc
  obtain ⟨⟨hv, hg⟩, he⟩ := hc
  simp only [Option.some.injEq] at h
  subst h
  refine ⟨hv, hg, fun e heq => ?_⟩
  obtain ⟨c, hc⟩ := mem_zip_of_mem he.symm heq
  obtain ⟨k, hk⟩ := hobs _ (List.mem_map.mpr ⟨(e, c), hc, rfl⟩)
  simpa using hk

/-! ## R2: inclusion, by the direction table -/

theorem r2_sound {P C : Stmt} {eqCerts guardCerts : List Cert} {r : Scope}
    (h : ruleReach C [P] (.inclusion eqCerts guardCerts) = some r) (hK : r.mem K)
    (hP : Holds K P) : Holds K C := by
  obtain ⟨vP, eP, gP, kP⟩ := P
  obtain ⟨vC, eC, gC, kC⟩ := C
  simp only [ruleReach] at h
  have hk : kP = kC := by
    by_contra hne
    simp [hne] at h
  subst hk
  simp only [bne_self_eq_false, Bool.false_eq_true, ite_false] at h
  cases kP with
  | empty =>
    cases ho : inclusionObligations ⟨vC, eC, gC, .empty⟩ ⟨vP, eP, gP, .empty⟩ eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      obtain ⟨hv, hloc⟩ := inclusion_locus ho (reachAll_sound h hK)
      simp only at hv
      subst hv
      intro x hx
      exact hP x (hloc x hx)
  | vanishesOn f =>
    cases ho : inclusionObligations ⟨vC, eC, gC, .vanishesOn f⟩ ⟨vP, eP, gP, .vanishesOn f⟩
        eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      obtain ⟨hv, hloc⟩ := inclusion_locus ho (reachAll_sound h hK)
      simp only at hv
      subst hv
      intro x hx
      exact hP x (hloc x hx)
  | nonempty =>
    cases ho : inclusionObligations ⟨vP, eP, gP, .nonempty⟩ ⟨vC, eC, gC, .nonempty⟩
        eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      obtain ⟨hv, hloc⟩ := inclusion_locus ho (reachAll_sound h hK)
      simp only at hv
      subst hv
      obtain ⟨x, hx⟩ := hP
      exact ⟨x, hloc x hx⟩
  | inIdeal f =>
    simp only at h
    split at h
    swap
    · simp at h
    cases ho : idealInclusionObligations ⟨vC, eC, gC, .inIdeal f⟩ ⟨vP, eP, gP, .inIdeal f⟩ eqCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      obtain ⟨hv, hgg, hspan⟩ := idealInclusion_span ho (reachAll_sound h hK)
      simp only at hv hgg
      subst hv hgg
      obtain ⟨k, hk⟩ := hP
      refine ⟨k, Ideal.span_le.mpr ?_ hk⟩
      intro g hg'
      obtain ⟨e, he, rfl⟩ := List.mem_map.mp hg'
      exact hspan e he

/-! ## Composition (R3) -/

theorem toK_bind₁ {σ τ : Type*} (f : σ → MvPolynomial τ Rat) (P : MvPolynomial σ Rat)
    (hf : ∀ i, f i ∈ GoodPoly K τ) (hP : P ∈ GoodPoly K σ) :
    toK (K := K) (bind₁ f P) = bind₁ (fun i => toK (K := K) (f i)) (toK P) := by
  choose f' hf' using hf
  obtain ⟨P', rfl, -⟩ := toK_lift hP
  have hfeq : f = fun i => MvPolynomial.map (Good K).subtype (f' i) := funext fun i => (hf' i).symm
  rw [hfeq, ← map_bind₁, toK_map, map_bind₁, toK_map]
  congr 2
  funext i
  exact (toK_map (f' i)).symm

theorem eval_bind₁ {σ τ : Type*} (x : τ → K) (g : σ → MvPolynomial τ K) (Q : MvPolynomial σ K) :
    eval x (bind₁ g Q) = eval (fun i => eval x (g i)) Q := by
  have := eval₂Hom_bind₁ (RingHom.id K) x g Q
  simpa [coe_eval₂Hom] using this

theorem compose_meaning {nS nT : ℕ} {phi : List Sparse} {p q : Sparse}
    (h : compose nS phi nT p = some q) :
    phi.length = nT ∧ meaning nS q =
      bind₁ (fun i : Fin nT => meaning nS (phi.getD i.val [])) (meaning nT p) := by
  unfold compose at h
  cases hg : phi.mapM (toHexQ nS) with
  | none => simp [hg] at h
  | some gs =>
    simp only [hg, Option.bind_eq_bind, Option.bind_some] at h
    split_ifs at h with hl
    simp only [bne_iff_ne, ne_eq, not_not] at hl
    cases hq : toHexQ nT p with
    | none => simp [hq] at h
    | some Q =>
      simp only [hq, Option.bind_some] at h
      split_ifs at h with hrt
      simp only [Option.some.injEq] at h
      subst h
      have F := mapM_forall₂ hg
      refine ⟨F.length_eq ▸ hl, ?_⟩
      rw [meaning_of (beq_iff_eq.mp hrt)]
      refine (toMvPolynomial_subst (R := Rat) (fun i => gs.getD i.val 0) Q).trans ?_
      rw [meaning_of hq]
      congr 2
      funext i
      have hi : i.val < phi.length := F.length_eq ▸ hl ▸ i.2
      have hig : i.val < gs.length := F.length_eq ▸ hi
      simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hig,
        List.getElem?_eq_getElem hi, Option.getD_some]
      have := F.get hi hig
      simp only [List.get_eq_getElem] at this
      exact (meaning_of this).symm

/-- Good coefficients for every listed sparse polynomial (in `K`). -/
def GoodAll (K : Type*) [Field K] (ps : List Sparse) : Prop := ∀ p ∈ ps, ∀ c ∈ p.coeffs, c ∈ Good K

theorem compose_value {nS nT : ℕ} {phi : List Sparse} {p q : Sparse}
    (h : compose nS phi nT p = some q) (hphi : GoodAll K phi) (hp : ∀ c ∈ p.coeffs, c ∈ Good K)
    (x : Fin nS → K) :
    value nS q x = value nT p (fun i => value nS (phi.getD i.val []) x) := by
  obtain ⟨hl, hm⟩ := compose_meaning h
  have hgood : ∀ i : Fin nT, meaning nS (phi.getD i.val []) ∈ GoodPoly K (Fin nS) := by
    intro i
    apply meaning_good
    have hi : i.val < phi.length := hl ▸ i.2
    rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi, Option.getD_some]
    exact hphi _ (List.getElem_mem hi)
  unfold value
  rw [hm, toK_bind₁ _ _ hgood (meaning_good hp), eval_bind₁]

theorem map_locus {S T : Stmt} {phi : List Sparse} {eqCerts guardCerts : List Cert}
    {obs : List (Stmt × Cert)} (h : mapObligations S T phi eqCerts guardCerts = some obs)
    (hobs : ∀ o ∈ obs, Holds K o.1) (hphi : GoodAll K phi) (hT : GoodAll K (T.eqs ++ T.guards)) :
    ∀ x, Locus (K := K) S x →
      Locus (K := K) T (fun i => value S.vars.length (phi.getD i.val []) x) := by
  unfold mapObligations at h
  split_ifs at h with hc
  simp only [Bool.or_eq_true, bne_iff_ne, ne_eq, not_or, not_not] at hc
  obtain ⟨⟨-, he⟩, hg⟩ := hc
  cases hE : T.eqs.mapM (compose S.vars.length phi T.vars.length) with
  | none => simp [hE] at h
  | some ceqs =>
    cases hG : T.guards.mapM (compose S.vars.length phi T.vars.length) with
    | none => simp [hE, hG] at h
    | some cgs =>
      simp only [hE, hG, Option.bind_eq_bind, Option.bind_some, Option.pure_def,
        Option.some.injEq] at h
      subst h
      have FE := mapM_forall₂ hE
      have FG := mapM_forall₂ hG
      intro x hx
      refine ⟨fun e heq => ?_, fun g hgq => ?_⟩
      · obtain ⟨ce, hce, hcomp⟩ := forall₂_exists_right FE e heq
        obtain ⟨c, hc⟩ := mem_zip_of_mem (FE.length_eq.symm.trans he.symm) hce
        have := hobs _ (List.mem_append_left _ (List.mem_map.mpr ⟨(ce, c), hc, rfl⟩))
        rw [← compose_value hcomp hphi (hT e (List.mem_append_left _ heq))]
        exact this x hx
      · obtain ⟨cg, hcg, hcomp⟩ := forall₂_exists_right FG g hgq
        obtain ⟨c, hc⟩ := mem_zip_of_mem (FG.length_eq.symm.trans hg.symm) hcg
        have := hobs _ (List.mem_append_right _ (List.mem_map.mpr ⟨(cg, c), hc, rfl⟩))
        rw [← compose_value hcomp hphi (hT g (List.mem_append_right _ hgq))]
        intro hz
        apply this x
        refine ⟨fun e' he' => ?_, hx.2⟩
        rcases List.mem_append.mp he' with he' | he'
        · exact hx.1 e' he'
        · rw [List.mem_singleton.mp he']; exact hz

theorem stmt_good {s : Stmt} (h : Avoids K s.primes) : GoodAll K s.polys :=
  fun p hp c hc => good_of_avoids h (List.mem_flatMap.mpr ⟨p, hp, hc⟩)

theorem polys_eqs_guards {s : Stmt} : ∀ p ∈ s.eqs ++ s.guards, p ∈ s.polys := by
  intro p hp
  simp only [Stmt.polys, List.mem_append] at hp ⊢
  tauto

/-! ## R3: polynomial maps, by the direction table -/

theorem r3_sound {P C : Stmt} {phi : List Sparse} {eqCerts guardCerts : List Cert} {r : Scope}
    (h : ruleReach C [P] (.map phi eqCerts guardCerts) = some r) (hK : r.mem K)
    (hP : Holds K P) (hphi : GoodAll K phi) (hPg : GoodAll K P.polys) (hCg : GoodAll K C.polys) :
    Holds K C := by
  have gP : GoodAll K (P.eqs ++ P.guards) := fun p hp => hPg p (polys_eqs_guards p hp)
  have gC : GoodAll K (C.eqs ++ C.guards) := fun p hp => hCg p (polys_eqs_guards p hp)
  simp only [ruleReach] at h
  split at h
  · -- NONEMPTY: source = premise, target = conclusion.
    rename_i hkP hkC
    cases ho : mapObligations P C phi eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      unfold Holds at hP ⊢
      rw [hkP] at hP; rw [hkC]
      obtain ⟨x, hx⟩ := hP
      exact ⟨_, map_locus ho (reachAll_sound h hK) hphi gC x hx⟩
  · -- EMPTY: target = premise, source = conclusion.
    rename_i hkP hkC
    cases ho : mapObligations C P phi eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      unfold Holds at hP ⊢
      rw [hkP] at hP; rw [hkC]
      intro x hx
      exact hP _ (map_locus ho (reachAll_sound h hK) hphi gP x hx)
  · -- VANISHES_ON(h) on the target gives VANISHES_ON(h ∘ φ) on the source.
    rename_i f f' hkP hkC
    split_ifs at h with hcomp
    cases ho : mapObligations C P phi eqCerts guardCerts with
    | none => simp [ho] at h
    | some obs =>
      simp only [ho, Option.bind_some] at h
      have hf : ∀ c ∈ f.coeffs, c ∈ Good K :=
        hPg f (by simp [Stmt.polys, hkP, Kind.target?])
      unfold Holds at hP ⊢
      rw [hkP] at hP; rw [hkC]
      intro x hx
      rw [compose_value (beq_iff_eq.mp hcomp) hphi hf]
      exact hP _ (map_locus ho (reachAll_sound h hK) hphi gP x hx)
  · simp at h

/-! ## Rule admission is sound -/

theorem reach_nil {C : Stmt} {d : RuleData} {rr : Scope} (h : ruleReach C [] d = some rr) : False := by
  cases d <;> simp [ruleReach] at h

theorem reach_many {C P Q R : Stmt} {Ps : List Stmt} {d : RuleData} {rr : Scope}
    (h : ruleReach C (P :: Q :: R :: Ps) d = some rr) : False := by
  cases d <;> simp [ruleReach] at h

theorem reach_one_split {C P : Stmt} {f : Sparse} {rr : Scope}
    (h : ruleReach C [P] (.split f) = some rr) : False := by
  simp [ruleReach] at h

theorem reach_two_r1 {C P Q : Stmt} {rr : Scope} (h : ruleReach C [P, Q] .r1 = some rr) : False := by
  simp [ruleReach] at h

theorem reach_two_inclusion {C P Q : Stmt} {a b : List Cert} {rr : Scope}
    (h : ruleReach C [P, Q] (.inclusion a b) = some rr) : False := by
  simp [ruleReach] at h

theorem reach_two_map {C P Q : Stmt} {phi : List Sparse} {a b : List Cert} {rr : Scope}
    (h : ruleReach C [P, Q] (.map phi a b) = some rr) : False := by
  simp [ruleReach] at h

open GP50 GPBinding.Spike in
theorem acceptsRule_claim_meaning (clauses : List GPProfile.Clause) (rules : List RuleInst)
    (w : Warrant) (premises : List Warrant) (name : String)
    (accepted : acceptsRule clauses rules w premises name = true)
    (truth : ∀ premise ∈ premises, Semantic.ClaimMeaning profile clauses premise.claim) :
    Semantic.ClaimMeaning profile clauses w.claim := by
  unfold acceptsRule at accepted
  simp only [Bool.and_eq_true, List.any_eq_true, beq_iff_eq] at accepted
  obtain ⟨-, r, -, hm⟩ := accepted
  obtain ⟨⟨⟨-, -⟩, -⟩, hmatch⟩ := hm
  cases hc : Semantic.boundClause ops clauses w with
  | none => simp [hc] at hmatch
  | some c =>
    cases hps : premises.mapM (Semantic.boundClause ops clauses) with
    | none => simp [hc, hps] at hmatch
    | some ps =>
      simp only [hc, hps, Bool.and_eq_true, List.all_eq_true] at hmatch
      obtain ⟨⟨⟨-, hle⟩, havoid⟩, hrr⟩ := hmatch
      cases hR : ruleReach c.stmt (ps.map (·.stmt)) r.data with
      | none => simp [hR] at hrr
      | some rr =>
        simp only [hR] at hrr
        have premiseMeans := Semantic.boundClauses_mapM_means profile clauses premises ps hps truth
        rcases Semantic.boundClause_registered profile clauses w c hc with ⟨unique, present, key⟩
        have means : Semantic.Means profile c.stmt c.scope := by
          intro (K : FieldCtx) (hK : Scope.mem K.carrier c.scope)
          change Holds K.carrier c.stmt
          have hrrK : rr.mem K.carrier := Scope.le_den hrr hK
          have hpK : ∀ p ∈ ps, Holds K.carrier p.stmt :=
            fun p hp => premiseMeans p hp K (Scope.le_den (hle p hp) hK)
          have hav := avoids_mem havoid hK
          have hCg : GoodAll K.carrier c.stmt.polys := stmt_good (hav.mono fun x hx => mem_union_left hx)
          have hPg : ∀ p ∈ ps, GoodAll K.carrier p.stmt.polys := fun p hp =>
            stmt_good (hav.mono fun x hx =>
              mem_union_right (mem_union_left (List.mem_flatMap.mpr ⟨p, hp, hx⟩)))
          have hDg : Avoids K.carrier r.data.primes :=
            hav.mono fun x hx => mem_union_right (mem_union_right hx)
          rcases ps with _ | ⟨p₁, _ | ⟨p₂, _ | ⟨p₃, ps⟩⟩⟩
          · exact (reach_nil hR).elim
          · have h₁ := hpK p₁ List.mem_cons_self
            cases hd : r.data with
            | r1 => rw [hd] at hR; exact r1_sound hR h₁
            | inclusion eqC gC => rw [hd] at hR; exact r2_sound hR hrrK h₁
            | map phi eqC gC =>
              rw [hd] at hR
              have hphi : GoodAll K.carrier phi := fun f hf c' hc' =>
                good_of_avoids (by simpa [RuleData.primes, hd] using hDg)
                  (List.mem_flatMap.mpr ⟨f, hf, hc'⟩)
              exact r3_sound hR hrrK h₁ hphi (hPg p₁ List.mem_cons_self) hCg
            | split h => rw [hd] at hR; exact (reach_one_split hR).elim
          · cases hd : r.data with
            | split h =>
              rw [hd] at hR
              exact r4_sound hR (hpK p₁ List.mem_cons_self)
                (hpK p₂ (List.mem_cons_of_mem _ List.mem_cons_self))
            | r1 => rw [hd] at hR; exact (reach_two_r1 hR).elim
            | inclusion _ _ => rw [hd] at hR; exact (reach_two_inclusion hR).elim
            | map _ _ _ => rw [hd] at hR; exact (reach_two_map hR).elim
          · exact (reach_many hR).elim
        refine ⟨⟨c, present, key⟩, fun c' hc' hkey' => ?_⟩
        have := key_unique_of_nodup clauses (·.key) unique c' c hc' present (hkey'.trans key.symm)
        exact this ▸ means

open GP50 in
theorem base_validator_sound_rules (clauses : List GPProfile.Clause) (receipts : List Receipt)
    (rules : List RuleInst) (snapshot : Snapshot) (unique : (snapshot.warrants.map (·.id)).Nodup) :
    Semantic.BaseValidatorSound profile clauses
      { Admission.refuseAll with receipt := accepts clauses receipts, rule := acceptsRule clauses rules }
      snapshot := by
  constructor
  · intro w member name accepted
    exact ⟨w, member, rfl, accepts_claim_meaning clauses receipts w name accepted⟩
  · intros; contradiction
  · intro w present premises name accepted members supported
    refine ⟨w, present, rfl, ?_⟩
    apply acceptsRule_claim_meaning clauses rules w premises name accepted
    intro premise hp
    exact Semantic.warrant_meaning_claim profile clauses snapshot unique premise (members premise hp)
      (supported premise hp)

open GP50 GPBinding.Spike in
/-- Fold soundness with K3 rules: every held claim means its registered statement in every
field its scope denotes, whether supported by receipts, rules, narrowing, or a mixture. -/
theorem fold_held_meaning_rules (clauses : List GPProfile.Clause) (receipts : List Receipt)
    (rules : List RuleInst) (events : List Event) (state : RuntimeState) (claim : Nat)
    (folded : fold (admissionWithRules clauses receipts rules) events = .ok state)
    (heldClaim : held state claim = true) :
    (∃ c ∈ clauses, c.key = claim) ∧
    ∀ c ∈ clauses, c.key = claim → ∀ K : FieldCtx, Scope.mem K.carrier c.scope →
      Holds K.carrier c.stmt := by
  have unique : (state.snapshot.warrants.map (·.id)).Nodup := by
    unfold fold at folded
    cases resolved : resolve events with
    | error message => simp [resolved] at folded
    | ok snapshot =>
      rw [resolved] at folded
      have stateEq : evaluate (admissionWithRules clauses receipts rules) snapshot = state :=
        Except.ok.inj folded
      subst state
      exact resolve_warrant_ids_nodup events snapshot resolved
  exact Semantic.fold_held_meaning profile clauses _ events state claim
    (base_validator_sound_rules clauses receipts rules state.snapshot unique) folded heldClaim

end GPBinding.Admission

end
