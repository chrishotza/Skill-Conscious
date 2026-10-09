# S01 — Results and artifact status

**Status as of 2026-10-09: analyses reported complete; archival of the original run outputs remains incomplete.**  
This document is a consolidated result/status record. It is not a substitute for the missing raw run directories.

## Frozen study identity

- Study: S01 — Cross-Cultural Consciousness Claim Recurrence Analysis.
- Preregistered code/data snapshot: branch s01-preregistered-v1, commit 4fdea2f26ef2449e32ab74b67c2c19904bb3270c.
- Effective corpus: 4,315 claims, 325 analytic corpus units, 328 effective source IDs, 19 source families.
- Seed: 20261006.
- Primary execution: S01_CONFIRMATORY_T4_V1, recorded at 2026-10-09 02:59:42 UTC, Tesla T4.
- Robustness execution: S01_ROBUSTNESS_T4_FAST_V1, recorded at 2026-10-09 04:23:54 UTC, Tesla T4.
- Semantic model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2, revision ef15aed8b328d308d7237b9bf15269f2cd19e268.

The preregistration itself remains frozen. This status file records outcomes; it does not alter the preregistered hypotheses or analysis definitions.

## Primary coded outcome

| Metric | Recorded result |
|---|---:|
| Mean cross-family Jaccard | 0.5222007632 |
| Mean within-family Jaccard | 0.6092416048 |
| DeltaJ = cross minus within | -0.0870408416 |
| Cross-family pairs | 49,496 |
| Within-family pairs | 3,154 |
| Family-label permutation null mean | 0.0000285656 |
| Family-label null 95% interval | [-0.0079603970, 0.0074177399] |
| Upper-tail p-value P(null DeltaJ >= observed DeltaJ) | 1.0 |

The observed coded effect is negative: the tested corpus showed stronger within-family motif clustering than cross-family clustering. This does not establish that cross-cultural recurrence is absent in every possible corpus, representation, or definition.

## Secondary degree-preserving rewiring null

- Recorded null mean: -0.0052016957.
- Recorded 95% interval: [-0.0096825659, -0.0006686911].
- Recorded upper-tail p-value: 1.0.

## Primary semantic outcome

| Metric | Recorded result |
|---|---:|
| Observed cross-family neighbor fraction | 0.7535341831 |
| Permutation-null mean fraction | 0.9400950452 |
| Null 95% interval for fraction | [0.9346228273, 0.9450984936] |
| Upper-tail p-value for fraction | 1.0 |
| Observed mean cosine | 0.6607122186 |
| Permutation-null mean cosine | 0.6642799840 |
| Null 95% interval for cosine | [0.6641420549, 0.6644048014] |
| Upper-tail p-value for cosine | 1.0 |

The observed semantic neighbors were less cross-family and had slightly lower mean cosine than the corresponding null expectations, in the preregistered upper-tail direction. A p-value of 1.0 is a result for that directional test; it is not the probability that the null hypothesis is true.

## Robustness and numerical reproducibility

- 23 preregistered robustness conditions were recorded.
- Every listed condition had negative DeltaS, ranging from -0.004034858 to -0.003412666.
- The reported cross-family-fraction and cosine upper-tail p-values were 1.0 in all 23 conditions.
- The CPU/GPU artifact reported absolute differences of 5.781229939e-10 for DeltaS and 5.284592874e-09 for observed mean cosine.

These findings support the same directional interpretation within the tested conditions. They do not validate every scientific assumption or show that any universal theory of consciousness is true or false.

## Audit caveats

The V10 audit reported 11 PASS and 3 FAIL. The three failures were missing claim/unit/source counts inside the primary execution metadata; those counts were present in the consolidated primary summary and corpus manifest. This is a provenance-schema defect that must remain visible, not be silently converted to a PASS.

The V8 independent artifact audit reported 113 PASS, 0 WARN, and 0 FAIL, but explicitly did not establish full equivalence of all runners. Separate V6/V7 equivalence runs were reported as PASS in the execution record; their full raw logs are not listed in the recovered master-backup inventory and must not be assumed archived until verified.

## Artifact recovery status

At the end of the Colab runtime, the original directories were reported missing from the active filesystem. Subsequent GitHub searches did not find the original run-output files in the tracked repository. The persistent Drive master backup is at:

~~~text
MyDrive/Skill-Conscious_PERSISTENT/S01_MASTER_BACKUP_20261009/
~~~

The recovery snapshot contains summaries and the recovery record, and the master backup contains a verified Git bundle and three branch archives. The backup report records 11 inventoried files with all 11 hashes verified. **That verifies those backup files; it does not mean the original primary/robustness output directories or all raw analysis artifacts were recovered.**

Known summary paths include:

~~~text
recovery_snapshot/S01_VERIFIED_RESULTS_SNAPSHOT.json
recovery_snapshot/S01_ROBUSTNESS_23_CONDITIONS.json
recovery_snapshot/S01_RECOVERY_REPORT.md
recovery_snapshot/ORIGINAL_ARTIFACTS_STATUS.json
recovery_snapshot/S01_MASTER_RECOVERY_RECORD.json
~~~

Do not fabricate missing JSON/NPZ outputs from these summaries. Keep the original preregistration and data/code history intact. If raw outputs cannot be recovered, document the exact missing files and apply the publication gate explicitly before writing a paper.

## Decision

- Directional hypothesis of cross-family recurrence: **not supported by these recorded analyses**.
- S01 raw-artifact archive and exit condition: **not yet satisfied**.
- Paper status: **not promoted**.
- Next work: stabilize and verify archival/provenance, then audit P008's executable intervention design and prepare an output-persistence path before any expensive execution.
