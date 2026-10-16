# Current Research Checkpoint

**Updated:** 2026-10-16  
**Canonical repository:** chrishotza/Skill-Conscious  
**Canonical branch:** main

## Current state

The repository has a substantial experimental runtime and a structured research program. No paper is currently publication-ready. Canonical documentation/state consolidation is merged. The P008 / CF01 deterministic mechanism fixture passed its focused tests and two complete CI suites and PR #90 was merged into main. A diversified follow-up protocol remains an unfrozen draft. The pilot-only generator and matched A/B/C/D runner are implemented in review, with holdout 1000..1127 locked and the 32-scenario pilot has since executed and passed artifact audit on 2026-10-16; holdout 1000..1127 remains untouched. Its 12.5% paired divergence is exploratory, not confirmation. S01's raw-output gap remains documented and does not block that work.

## Corpus snapshot

- 4,315 effective claim records; 4,315 unique global claim IDs.
- 325 analytic corpus units.
- 328 effective source IDs.
- 19 source families in S01.
- The ledger is structurally covered; passage-level verification, edition/translation control, and independence/dependency review remain separate tasks.
- Frozen data manifest: research/S01_DATA_MANIFEST_V1.json; corpus branch: corpus-v1.

## S01 — current result state

**Status: primary and robustness outcomes recorded; original raw-output archival incomplete.**

Primary run S01_CONFIRMATORY_T4_V1 was recorded at 2026-10-09 02:59:42 UTC from preregistered commit 4fdea2f26ef2449e32ab74b67c2c19904bb3270c. Robustness run S01_ROBUSTNESS_T4_FAST_V1 was recorded at 04:23:54 UTC.

- Coded DeltaJ = -0.0870408416; mean cross-family Jaccard = 0.5222007632, mean within-family Jaccard = 0.6092416048; directional upper-tail p = 1.0.
- Semantic cross-family neighbor fraction = 0.7535341831 versus null mean 0.9400950452; upper-tail p = 1.0.
- Observed semantic cosine = 0.6607122186 versus null mean 0.6642799840; upper-tail p = 1.0.
- 23 robustness conditions were recorded; all had negative DeltaS and both reported upper-tail p-values equal to 1.0.
- The CPU/GPU reproducibility record reports absolute differences of 5.78e-10 for DeltaS and 5.28e-09 for observed cosine.

Interpretation: the tested analyses did not support the preregistered prediction of greater cross-family recurrence in the tested direction. This is not a universal disproof of recurrence or of a consciousness theory.

Canonical consolidated record: research/S01_RESULTS_STATUS_2026-10-09.md.

## S01 artifact integrity

The original primary and robustness run directories were not found in the disconnected Colab runtime, and repository searches did not locate the original output files in tracked GitHub paths. The Drive master backup at MyDrive/Skill-Conscious_PERSISTENT/S01_MASTER_BACKUP_20261009/ preserves the Git bundle, three branch archives, and a recovery snapshot. Its report verifies 11 inventoried files by SHA-256.

This is not a complete raw-run archive. In particular, do not describe the original JSON/NPZ run artifacts as recovered unless the actual files are found and their hashes/contents are inspected. Do not reconstruct originals from summary values.

## P008 — CF01 self-model causality

Hypothesis: intervention on a persistent self-model changes future trajectory selection under otherwise matched conditions.

- Evidence map: research/P008_EVIDENCE_MAP_V1.md and .json.
- Prediction contract: research/p008_prediction_registry.json.
- Target assay: experiments/p008_self_model_causal_runtime.py.
- Execution log: research/P008_EXECUTION_LOG.md.
- Recorded attempt on 2026-10-06 was blocked by inability to resolve github.com.
- Open PR #90 freezes A/B/C/D, one intervention (continuity weight 1.0 → 0.0), two integration cycles with restart/consequence/re-entry, and a JSON result contract with commit/runtime/input hashes.
- The PR's CPU workflow runs the complete pytest suite and uploads a result artifact with 90-day retention.
- Focused CF01 tests, assay execution, and artifact upload succeeded in workflow run 37898192199. The archived JSON is `research/results/p008/P008_CF01_37898192199.json`.
- The fixture produced A/B/D=`preserve` and C=`explore` in both cycles; C-vs-B and C-vs-D divergence were 1.0, B-vs-D disagreement was 0.0, and all restart state-contract checks passed.
- **This is accepted only as a deterministic mechanism-fixture result, not broad empirical validation.** On 2026-10-16, native-dynamic-core run 38977366222 passed 128 tests in 12.38 s and P008 run 38977365990 passed its focused job plus the full 128-test suite in 18.59 s. This establishes CI validated and PR #90 merged to main at commit e919057a9f07975242ea37bf2c30689e53e8c09c, not scientific generalization.

## P009 and P010

- P009 relational probes B2/B3 are implemented; broader multi-condition validation remains open.
- P010 has no specified physical model with an observable that discriminates it from plausible alternatives. B1 remains blocked; B4 follows only after candidate models exist.
- The three-scale bridge is a research framework, not an established hierarchy or empirical finding.

## Completed / recorded

- Research method north star and claim-family operating system.
- S01 protocol, manifest, frozen analysis snapshot, primary and robustness outcomes, and result-direction interpretation.
- Optimization of the secondary null implementation without changing the declared analysis definition.
- Drive master backup creation and SHA-256 verification for the 11 files in its manifest.
- P008 evidence map, prediction registry, runtime assay source, and blocked-execution log.

## Blockers

- S01 original run-output directories and complete raw artifacts remain unrecovered.
- P008 focused execution/artifact persistence and both full CI suites have passed; broader externally valid, preregistered P008 evidence has not been produced.
- P009 needs broader validation.
- P010 needs a concrete model-discrimination target.
- 52 non-canonical provenance labels in S069/S070/S071 still require source-level review.

## Immediate sequence

1. Preserve a durable copy of the verified P008 pilot artifact (GitHub Actions 38978718548; 90-day expiry 2027-01-14), then independently review scenario sampling and limitations.
2. Treat both the initial two-candidate fixture and the 32-scenario development pilot as functional synthetic software evidence, not evidence of phenomenal consciousness.
3. Independently review and freeze the generator, inference plan and exact runtime implementation before any holdout access.
4. Keep S01 raw-artifact recovery/inventory open without altering preregistered S01 results; continue P009/P010 only at their respective evidence gates.

## 2026-10-16 development-pilot result (exploratory)

P008 generalized runner succeeded with 32 seeded pilot scenarios, four arms and two cycles each. C-vs-B and C-vs-D divergence were both 0.125 (scenario bootstrap 95% interval 0.03125–0.25); B-vs-D and A-vs-B disagreements were zero. Focused tests 8/8 and complete suite 136/136. GitHub Actions run 38978718548 uploaded audited ZIP artifact 12079189698 (SHA-256 ef0d38acf1f1661298bd3472fe5747da59a5b087abf0c4e678ec20bf93a24ea5). Detailed limits and expiry: research/results/p008/P008_GENERALIZATION_PILOT_2026-10-16.md. This is **not** a confirmatory holdout result; IDs 1000–1127 remain untested.

## 2026-10-16 reserved-holdout engineering checkpoint

The 32-scenario pilot remains the latest verified generalized result. A separate 128-scenario runner and push-only workflow were implemented in a proposed PR. Their freeze/release contract requires a main-branch ancestor freeze SHA and rejects any changes under `src/`, relevant experiment code, the protocol and workflow. No holdout release marker exists yet; no 128-scenario execution is authorized or reported. Next steps: CI, freeze PR merge, and separately review/release the one-shot evaluation. Independent external scientific review is not yet recorded.

## P008 freeze decision — 2026-10-16

The guarded holdout executor passed a 140-test suite and a repeat of the 32-scenario exploratory pilot; PR #93 was merged at `524f10a8666510da5d1a3ab96ec0b5884130e237`. This follow-up freezes the internal P008 synthetic scenario protocol, controls, scenario-clustered bootstrap, failure gate and runtime source as a baseline before release. **Freeze baseline SHA is the main-branch squash merge of this freeze PR; no holdout IDs were accessed during the code/protocol validation.** A distinct release-marker PR must reference that SHA, and the first main push triggers the only authorized internal holdout. Independent external review has not occurred: do not call this a publication-grade preregistration or consciousness evidence.

## P008 sealed internal holdout release preparation (2026-10-16)

The internally frozen main baseline is **`c0278493e8ef31520beea29355f947a7ea3739a8`** (PR #94); prior implementation PR #93 was already green (140 tests). A *separate* release marker `research/p008_holdout_release.json` is proposed, referencing this SHA with IDs 1000–1127 and fixed outcome policy. The sealed workflow triggers on its first merge into main only. The holdout was NOT run when this release proposal was authored; verify GitHub Actions, manifest/raw records and controls before updating this claim. Independent external methodological review remains outstanding, so report any future evaluation as internal synthetic evidence only.

## P008 reserved-split execution — VERIFIED 2026-10-16

Internal freeze baseline `c0278493e8ef31520beea29355f947a7ea3739a8`; independent release commit `c9728d2552b184d4b37c8590279e8ea4e8a04337`. Main-branch Action 38980796822 verified freeze ancestry and source diff and passed **140/140** tests. It then executed **128/128** synthetic reserved scenarios × 4 controls × 2 cycles, recomputed outcomes from 640 SHA-256 audited raw records, and uploaded artifact **12081087004** (633705 bytes; ZIP SHA-256 `8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32`; expires 2027-01-14). C-B and C-D paired divergence **0.234375** (95% scenario-cluster bootstrap [0.164062, 0.3125]); A-B and B-D **0**. Predeclared internal software mechanism gate **PASS**. Full immutable outcome record: `research/results/p008/P008_CF01_INTERNAL_HOLDOUT_2026-10-16.md` and `research/p008_holdout_result_v1.json`. Frozen preregistration source is immutable and still describes pre-execution status by design; consult this checkpoint for latest evidence. Long-lived GitHub Release archive pending a separate checksum-verified archive workflow. Independent external review remains outstanding, and none of this establishes phenomenal consciousness.

## P008 durable evidence archival — VERIFIED 2026-10-16

The original 128-scenario internal holdout ZIP now has a checksum-verified persistent GitHub Release asset, not only an expiring Actions artifact. Archive workflow **38981166451** succeeded; Release `p008-cf01-internal-holdout-20261016`, ID 415457666, asset ID 648924054, bytes **633705**, SHA-256 `8903448199c676ec10cef090751dd73ed2087e263d75e472a29f0b908d189c32`. Release API verification matched the Actions original byte-for-byte by digest and size. Full provenance and artifact URL: `research/p008_holdout_result_v1.json` and `research/results/p008/P008_CF01_INTERNAL_HOLDOUT_2026-10-16.md`. Independent scientific review and alternative-implementation replication remain NEXT_STEP priorities.
