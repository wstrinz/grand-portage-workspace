/-
# When may a cover be REFUTED?

`verify.partition_exhaustiveness` decides

    V(parent) ⊆ ⋃ V(B_i)   by   ⋂ I(B_i) ⊆ radical(I(parent))

and the equivalence of those two is the Nullstellensatz, which needs an
ALGEBRAICALLY CLOSED FIELD.  The tool works over ℚ.

Only one direction survives that, and it is the one that matters for soundness:

  ideal test PASSES  →  the cover really does hold.  Every generator common to
                        the branches vanishes on the parent, over ANY field.
                        VERIFIED is safe.

  ideal test FAILS   →  says nothing over ℚ.  The parent may have no rational
                        points at all, in which case the branches cover it
                        VACUOUSLY and the tool has just called a sound case
                        analysis broken.

That second line is a FALSE REFUTATION, and NOT_EXHAUSTIVE is UNSOUND_PREMISE:
it exits 1 on a partition that is fine.
-/

import GrandPortage.Points

namespace GrandPortage

universe u v

/-- A family of branches covers the parent when every point of the parent lies
    on one of them.  Stated on POINTS, which is what a cover means; the ideal
    criterion is a way of deciding it, not its definition. -/
def Covers {α : Type u} {ι : Type v} (parent : Model α) (branch : ι → Model α) :
    Prop :=
  ∀ x, parent x → ∃ i, branch i x

/-- AN EMPTY PARENT IS COVERED BY ANYTHING, including nothing.

    This is the whole engine of the counterexample, and it is two lines.  A
    criterion that REFUTES a cover has to rule this out first, and the ideal
    test cannot: over ℚ, `(x² + 1)` has no points while its ideal is nowhere
    near the unit ideal. -/
theorem empty_parent_covered {α : Type u} {ι : Type v}
    {parent : Model α} (h : IsEmpty parent) (branch : ι → Model α) :
    Covers parent branch :=
  fun x hx => absurd hx (h x)

/-- So COVERING IS NOT DECIDED BY THE BRANCHES ALONE.  Two parents with the
    same branches can disagree, which means any test that ignores whether the
    parent has points is testing something else. -/
theorem covers_depends_on_the_parent :
    ∃ (p q : Model Two) (b : Empty → Model Two), Covers p b ∧ ¬ Covers q b :=
  ⟨nowhere, both, fun e => e.elim,
   fun x hx => absurd hx (fun h => h),
   fun h => (h Two.a trivial).elim (fun e => e.elim)⟩

/-! ## What this settles

The verifier keeps VERIFIED exactly as it is -- that direction is sound over
any field, because `⋂ I(B_i) ⊆ radical(I(parent))` says every common generator
vanishes wherever the parent does, and vanishing is field-independent.

NOT_EXHAUSTIVE must stop being an unqualified refutation.  What the failing
ideal test establishes is a statement about the ALGEBRAIC CLOSURE: there is a
point of `V(parent)` over `k̄` that no branch reaches.  Over the base field
that point may not exist.

Two honest repairs, and the tool should do both:

  * if the parent's ideal is the UNIT IDEAL it has no points over any field,
    so the cover is vacuous and the answer is VERIFIED.  Cheap, and it catches
    the case a reader will hit first.
  * otherwise NOT_EXHAUSTIVE must SAY that it is a statement over the closure,
    and that a parent with no points over the base field is covered vacuously.
    The tool cannot decide that in general -- it is exactly the emptiness
    question the certificate machinery exists for -- so it must not pretend to.

SAME SHAPE AS THE `IMAGE_CLOSURE` DENSITY ARGUMENT (`ImageClosure.lean`): a
justification that is correct over an algebraically closed field, applied by a
tool that works over ℚ.  That is now twice, which makes it a class worth
naming rather than two accidents. -/

end GrandPortage
