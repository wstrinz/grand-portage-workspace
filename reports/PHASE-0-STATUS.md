# Phase 0 status - 2026-09-27

G0 is not yet evaluated; Phase 0 is in progress.

## Verified here

- Approved backbrief and F: workspace; local repository has no remote.
- Separate oracle copy on F:, pinned at ac4155787207e2847d248cffed7be871d5dcd577; original source checkout unchanged.
- 348 source-pointed neutral cases (106 acceptance controls, 242 refusals), schema validator and reproducible layer-specific oracle adapter.
- Latest replay: 334 agreements, eleven known differences (five conservative refusals, four producer-trust/replay-policy mismatches and two partition context omissions), one diagnostic observation, one pending projection, one unsupported dimension-credit case.
- First-batch focused runs passed 95 tests with one live-CAS case excluded; the second batch passed 54 focused tests; the third passed 75 plus three adapter controls; the fourth passed 19 with two companion checks deselected; the fifth passed 12 with two companion checks deselected and two diagnostic controls; the sixth passed all 15 p-axis tests. The seventh milestone passed 271 selected historical instances (including 24 corrected-harness retries). The eighth slice passed 30 offline current-tree tests with three live tests deselected, plus four constructor-emission controls. The ninth slice passed 93 lifecycle, merge and provenance regressions plus four retry/section order controls. These runs overlap and are not the full release suite.
- Source and history indexes plus a partial-review ledger generated. All 29 deleted test files have been read and all 226 functions dispositioned. Of 197 selected functions, all 271 parametrized instances pass; 29 original functions remain unrun (27 companion-dependent, two live CAS). Semantic coverage remains incomplete.
- Freeze documentation preparation fully audited: exact banner, 17 repairs, current status constants, three doc-only paths, isolated patch application and pinned existing release tag verified; not applied or published.
- Existing Lean 4.32.1/Lake executables inspected successfully; no kernel spike code.

## Next work and dependencies

- 0a: resolve pending projections, review the remaining sources/history, split compound incidents into minimal cases and replay the additional routes. See PHASE-0A-BATCH-25.md and NEXT-REVIEW-PRIORITIES.md and corpus/REVIEW-COVERAGE.json.
- 0b: concrete JC/GP paths approved; other campaign directories discovered but not yet confirmed. Await remaining manifest paths, optional campaign scope and exclusions. No campaign harvesting has started.
- 0c: corpus-first restriction remains; agree a measurable effort cap before the deferred spike. See ENVIRONMENT.md.
- 0d: authorized private preparation verified under freeze-v0.37.1/AUDIT.json and RELEASE-HANDOFF.md. Public application and tag/release actions remain unperformed under the approved prepare-only scope.

The chat's default directory still points to C:. Continue explicitly in F:\repos\grandportage-0.50 and keep practical outputs there.

Current lifecycle finding: two current identity receipts can produce different active fields under reversed branch merge order, although both receipts remain retained. The proposed 0.50 policy is not settled; see LIFECYCLE-DESIGN-FINDINGS.md and RETRY-MERGE-AUDIT.json.

2026-09-28: Goal run active toward Phase 0 completion or concrete blockers. PHASE-0-COMPLETION-TRACKER.json records lane requirements. The source-manifest clarification is pending; independent review continues. JOIN-AUTHORITY-AUDIT.json confirms the documented boundary between legacy transport auditing and logical entailment. Neutral-schema compliance of lifecycle event-shaped inputs is an explicit remaining task; no corpus expectations were changed.

Neutral lifecycle migration: GP-X142-163 now use a portable object/history vocabulary. All 22 reconstruct the original oracle inputs exactly, all 217 expected verdicts are unchanged, four adapter mutations pass, and the full replay retains the same outcomes. See NEUTRAL-LIFECYCLE-AUDIT.json. Earlier case bytes remain recoverable through Git and immutable replay digests; the current cases supersede their old input encoding.

Batch 10 adds ten conditional joint-premise/cover cases and passes 16 selected reporting, taint and mutation regressions. DESIGN.md and REVIEW.md are fully text-read with section dispositions; both remain semantically partial. Current source coverage is 36 partial / 332 unreviewed, not a completed 0a gate.

Lean documentation slice: lean/README.md (317 lines) and lean/THEORY.md (164 lines) fully text-read and dispositioned. Five source paths receive partial review credit; theorem premises remain distinct from runtime verification. See LEAN-AUTHORITY-BOUNDARIES.md. Corpus stays at 227 cases; no expected verdict or oracle code changed.

Batch 11 adds six provenance/review-policy controls, passes both source regressions and fully replays 233 cases. All earlier 227 case files remain byte-identical. SPEC (619 lines) is fully text-read with section dispositions; source review now 37 partial / 331 unreviewed. See PHASE-0A-BATCH-11.md for documentation overstatements and proposed corrections.

Batch 12 adds eight coverage/refinement cases, eight passing source regressions and three coverage deletion diagnostics. KILL-CRITERIA and EXPERIMENT-B are fully text-read; their historical metric caveats are preserved. Current coverage: 41 partial / 327 unreviewed. Prior 233 cases are byte-identical.

Freeze audit checkpoint: the existing v0.37.0 annotated tag targets the oracle commit but has no freeze wording. Its object remains unchanged. The exact freeze banner is prepared in the audited patch; no claim of a published freeze is made. Phase 0a/0b/0c and G0 remain open.

Batch 13 adds ten offline backend identity/completion cases. Seventeen selected envelope regressions and all thirteen artifact tests pass. Three unsupported-input adapter controls refuse. Source coverage is 44 partial / 324 unreviewed; earlier 241 cases remain byte-identical. No live backend or graph authority is claimed from fabricated transcripts.

Batch 14 adds eleven durable-artifact controls and three manifest-composition diagnostics; full replay agrees on all new cases. Current source coverage: 45 partial / 323 unreviewed. Earlier 251 cases remain byte-identical.

Batch 15 adds eight exact-replay/availability cases, three structural conformance diagnostics and four passing adapter harness tests. Current source coverage: 48 partial / 320 unreviewed. All earlier 262 case files are unchanged.

Batch 16 adds ten launch/recording controls and passes 17 source regression instances. Missing source references are rejected after execution and raw artifact persistence, while graph bytes remain unchanged; proposed preflight improvement recorded separately. Current source coverage: 48 partial / 320 unreviewed.

Batch 17 adds fifteen compiler-slot cases and passes fifteen source test instances, including three process controls. GP-X241 retains expected ACCEPT but the frozen scalar-division guard rejects harmless comments; COMMENT-DIVISION-AUDIT.json isolates the defect. Current coverage: 48 partial / 320 unreviewed. No expected verdict changed.

Batch 18 fully text-reads SCOPE and ARCHITECTURE, passes all 16 architecture tests, and calibrates relative-import-only checking. The private freeze README was corrected from 161 to the tested 160-line limit; patch reapplication and the actual frozen test now pass. Corpus/replay unchanged; source coverage 51 partial / 317 unreviewed.

Batch 19 fully text-reads COMPATIBILITY.md and separates historical semantics, evidence extensions, migration custody and current replay-only requirements. Source coverage 52 partial / 316 unreviewed. No corpus or runtime edits, and no new test execution claimed. OPERATION-CONTRACTS reading is incomplete and receives no new full-read credit.

Batch 20 completes OPERATION-CONTRACTS text reading, reads runtime contract metadata and correspondence tests, and passes 30 tests. Direct effective-verdict mutation tests do not verify persisted authority binding. Header version drift documented; 54 partial / 314 unreviewed.

Batch 21 reads authority binder/registry and both test files: 31 tests pass. Four direct API controls document caller-owned target binding and shallow proof payloads without claiming a persisted bypass. Continue store subject-specific replay and real provenance controls. Coverage 57 partial / 311 unreviewed.

Batch 22 completes _apply_verdict reading and diagnoses section proof custody with actual freshness: stale tampering refuses, but invalid cofactors with reissued producer metadata project VERIFIED_SECTION. Independent arithmetic rejects the altered row. Offline fabricated provenance only; no live backend failure or external attack claimed. Extract neutral controls next.

Batch 23 adds GP-X255-257 section receipt controls. All 295 prior case files remain byte-identical. Fresh producer metadata can activate invalid section cofactors in the predecessor; expected REFUSE remains fixed under replay-only policy. Full replay has no ERROR or REVIEW_REQUIRED.

Batch 24 verifies five operation-output custody controls: valid producer, stale proof edit, invalid reissued producer, invalid nonempty native and valid empty native. Nonempty cofactor arithmetic remains trusted to producer in the legacy fold; empty native output earns no completeness. See OPERATION-REPLAY-BOUNDARY.json; corpus unchanged.

Batch 25 extracts GP-X258-262 operation-output evidence controls. All 298 previous case files are byte-identical. Expected REFUSE for false fresh-bound membership is preserved; full replay has no errors or untriaged differences.

Batch 26 compares the exact mapped-ring verifier with native fold admission. Both invalid controls are refused by the real verifier but admitted when a positive native verdict is deliberately synthesized with current metadata. This diagnoses producer trust, not a real verifier false positive. Corpus unchanged.

Batch 27 adds paired mapped-ring checks GP-X263-268. Real verifier refusals remain distinct from synthetic positive receipt admission. All 303 prior cases unchanged.

Batch 28 reproduces omitted open branch guards: two D(x) branches miss zero in A1 but ideal-only partition verification returns VERIFIED. Exact zero-ideal backend stub, no CAS. Four point-universe tests pass; portable extraction remains next.

Batch 29 extracts GP-X269-272. Two punctured branches miss the origin, while three positive controls preserve valid closed/open covers. All 309 prior case files unchanged.

Batch 30 reproduces a selected-embedding partition omission: negative-root branches of x^2-2 are reported as covering a positive-root parent. point_scope excludes embedding; exact identical-ideal backend answers cannot establish selected-locus coverage. Corpus extraction remains next.

Batch 31 extracts GP-X273-274 selected-root cover controls. All 313 prior case files unchanged; no replay errors or untriaged differences.

Batch 32 fully reads the eight-path point-universe fix 93770c6 and passes its broader 15-instance retained regression selection. Historical review remains semantically partial pending all relation/omission corpus controls. No campaign or historical executable run claimed.

Batch 33 extracts GP-X275-283: other typed universe mismatches, same/both-omitted readability and untyped debt versus transport. All nine agree; 315 prior cases unchanged.

Batch 34 fully reads the eight-path characteristic fix f2b7c49. Eight isolated historical predicate controls expose intermediate 1/composite acceptance corrected in the pinned validator. Existing corpus and constructor-emission evidence reused; live historical tests remain unrun.

Batch 35: reference-checker release slice and six exact sparse-input controls recorded. Four standalone reference validation gaps are blocked by production validation; no new production false licence. Corpus and latest replay unchanged; Phase 0 active.

Batch 36: eight more release path diffs reviewed; twelve of thirty-six now dispositioned. Actual projection CLI output exceeds its 1 MB compact-size check; three retained tests pass and proposed repair recorded. No publication or authority change.

Batch 37: 22 additional release diffs dispositioned; 34/36 complete path diffs read. Registry consistency and conditional Lean scope proof limits recorded; no new runtime authority or Lean execution.

Batch 38 completes full v0.27 diff reading: all 36 changed paths and hashes verified. Semantic extraction remains partial. Historical private HISTORY/ link bypasses root-md link check; fix candidate documented.

Batch 39: product checker/constructor review, 28 offline tests passed and neutral premise controls verified. Coverage now 62 partial / 306 unreviewed; corpus unchanged, portable extraction next.

Batch 40: GP-X284Ã¢â‚¬â€œ291 extract eight product identity/construction controls, all agree. All 324 prior case bytes and outcome classifications preserved. Full replay 20260928T141329008590Z; 332 total cases, 318 agreements and unchanged exceptions.

Batch 41: factor-power and affine-composition review complete at text/selected-control level; 26 tests and ten neutral controls pass. Coverage 68 partial / 300 unreviewed; fixed-expectation extraction remains next.

Batch 42: ten factor/composition cases agree; 342 total, 328 agreements and unchanged exceptions. Earlier 332 case bytes and outcome classifications preserved. Replay 20260928T141913475576Z.

Batch 43: full Laurent/pipeline source and combined-test reading; 15 tests plus six neutral composition controls pass. Coverage 70 partial / 298 unreviewed; corpus unchanged.

Batch 44: six pipeline controls agree after each pair of individual passes verifies. Full replay 20260928T142458952693Z has 348 cases, 334 agreements and unchanged exceptions; all earlier 342 case bytes/outcome classifications preserved.

Batch 45: coefficient source/tests reviewed and four direct/CLI controls verified. Malformed coverage list escapes CLI as TypeError; no false acceptance. Coverage 71 partial / 297 unreviewed; corpus unchanged.

Batch 46: exact polynomial parser/arithmetic/encoding slice read; five controls verify a generated-exponent sparse roundtrip mismatch and internal API assumptions. No serialized false proof admission reproduced; corpus unchanged.

Batch 47 completes polynomial checker and test text reading: 43 offline tests pass, one live test deselected; seven inclusion/preflight controls verified. Completeness-only acceptance remains distinct from exact contraction; shared native lists are conservatively rejected as cycles. Corpus unchanged. Source coverage 72 partial / 296 unreviewed; semantic review remains incomplete. See PHASE-0A-BATCH-47.md.

Batch 48 reviews localization callers: 29 source tests and six representation controls pass. Sparse guards crash default CLI rendering after verification; mixed infix/sparse duplicates bypass the stated uniqueness contract without falsifying the identity. Fix proposals and narrow soundness arguments recorded. Corpus unchanged; 74 partial / 294 unreviewed sources. See PHASE-0A-BATCH-48.md.

Batch 49 reviews ordered SOS recording and typed routes: 31 tests pass; two native controls reproduce noncanonical model text verifying but failing receipt replay. Canonical input records successfully. Corpus unchanged; 78 partial / 290 unreviewed sources. See PHASE-0A-BATCH-49.md.
