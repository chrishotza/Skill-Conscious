# P008 generalized synthetic development PILOT — 2026-10-16

**Evidence class:** exploratory software-mechanism pilot; NOT a preregistered holdout result, NOT independent replication, NOT evidence of phenomenal consciousness.

## Execution and provenance

- GitHub Actions run: https://github.com/chrishotza/Skill-Conscious/actions/runs/38978718548
- Pilot workflow: `.github/workflows/p008-generalization-pilot.yml`
- Source PR branch at execution: `research/p008-generalization-pilot-harness-20261016`; head `016ec1ed4aa29787a7da1cbb4203cc9834ec8043`. The raw JSON stores the workflow-provided tested commit, runtime version, Python version, protocol and generator hashes.
- Exploratory sample: 32 seeded scenarios (IDs 0–31), two candidates/scenario, four arms (A/B/C/D), two cycles/arm (32 × 4 × 2 = 256 arm cycles). Holdout IDs 1000–1127 were not accessed.
- Focused pilot tests: **8 passed** in 0.29 seconds in the pilot workflow.
- Full repository tests: **136 passed** in 16.13 seconds, workflow run https://github.com/chrishotza/Skill-Conscious/actions/runs/38978718586.
- Raw files: 32 scenario input JSON + 128 arm JSON + one manifest, verified by the pilot's independent manifest audit before ZIP upload.
- GitHub artifact ID `12079189698`; name `p008-generalization-pilot`; archive SHA-256 `ef0d38acf1f1661298bd3472fe5747da59a5b087abf0c4e678ec20bf93a24ea5`; size 146840 bytes; expires 2027-01-14 22:57 UTC (90-day retention). Preserve a durable copy before expiry if this study is promoted.

## Observed exploratory outcomes

| Paired contrast | Mean divergence | Scenario bootstrap 95% interval |
|---|---:|---:|
| C vs B, active self-model vs disconnected self-model | 0.125 | 0.03125–0.25 |
| C vs D, active self-model vs generic-state control | 0.125 | 0.03125–0.25 |
| B vs D, disconnected vs generic-state control | 0 | 0–0 |
| A vs B, no supplied model vs disconnected self-model | 0 | 0–0 |

Bootstrap: 2000 resamples of 32 **scenario** clusters; seed 20261016. Two cycles from a scenario are correlated and are not treated as independent samples. All observations are confined to synthetic candidates and a purpose-built fixed-weight scorer.

## Interpretation and limitations

The result is consistent with the expected functional dependence of this implementation's trajectory selector on the intervention parameter across a wider synthetic sample than the original hand-picked two candidates. The intervention effect occurs in **12.5%** of the seeded scenarios/cycles by this metric; it is not universal. The null controls agree in this pilot. This is a **development sample**, so bootstrap intervals are descriptive, not confirmatory evidence of out-of-sample generalization. A/B/D use explicitly disconnected scorer weights; information and memory budgets are only matched at the experiment-contract level, not proven information-theoretically equivalent.

No 128-scenario holdout was executed. Before a future confirmatory run, independently review the pilot's generated candidate distribution, exact generator/harness/runtime code, archive the raw evidence durably, finalize blind analysis/thresholds and freeze a versioned protocol on main. Never silently tune the protocol after seeing holdout results.
