/-
# Determined affine fibers with one residual compatibility

The runtime checks concrete coefficient matrices, unit pivots, ranks, and
syzygies. This file states the small semantic contract earned after those
instance checks: two coordinates are uniquely determined and existence in the
fiber is equivalent to one remaining compatibility predicate.
-/

namespace GrandPortage

universe u v w z

/-- A semantic normal form for an affine fiber block. `Base` carries all
earlier coordinates and residual data. The checker must establish
`characterize`; this structure does not guess it from a rank integer. -/
structure DeterminedAffineFiber
    (Base : Type u) (First : Type v) (Second : Type w) where
  equations : Base -> First -> Second -> Prop
  solveFirst : Base -> First
  solveSecond : Base -> Second
  compatible : Base -> Prop
  characterize : forall base first second,
    equations base first second <->
      first = solveFirst base /\
      second = solveSecond base /\
      compatible base


/-- A checked determined block has a solution exactly on its compatibility
locus. -/
theorem determinedAffineFiber_nonempty_iff
    (block : DeterminedAffineFiber Base First Second)
    (base : Base) :
    (Exists fun first => Exists fun second =>
      block.equations base first second) <-> block.compatible base := by
  constructor
  · rintro ⟨first, second, equations⟩
    exact (block.characterize base first second).mp equations |>.2.2
  · intro compatible
    exact ⟨block.solveFirst base, block.solveSecond base,
      (block.characterize base _ _).mpr ⟨rfl, rfl, compatible⟩⟩


/-- Whenever the compatibility condition holds, the two fiber coordinates are
unique. This is the semantic content of "rank two determines the plane," not
a statement that the base residual is known or that a source lift exists. -/
theorem determinedAffineFiber_unique
    (block : DeterminedAffineFiber Base First Second)
    (base : Base)
    (first second : First)
    (left right : Second)
    (firstSolution : block.equations base first left)
    (secondSolution : block.equations base second right) :
    first = second /\ left = right := by
  have firstCharacter := (block.characterize base first left).mp firstSolution
  have secondCharacter :=
    (block.characterize base second right).mp secondSolution
  constructor
  · exact firstCharacter.1.trans secondCharacter.1.symm
  · exact firstCharacter.2.1.trans secondCharacter.2.1.symm

end GrandPortage
