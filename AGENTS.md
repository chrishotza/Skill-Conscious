# Agent operating instructions

## First pass

Before editing or running experiments, read:

1. RESEARCH_MAP.md
2. research/CURRENT_CHECKPOINT.md
3. REPO_MEMORY.md
4. The active study registry and protocol.
5. Only then, the implementation and tests required for the assigned task.

The checkpoint is the live scientific state. If another document conflicts with it, verify the repository and update the state files together; do not silently choose the more convenient version.

## Evidence discipline

Use these labels precisely: SOURCE CLAIM, PROJECT HYPOTHESIS, OPERATIONAL DEFINITION, EMPIRICAL PREDICTION, PROTOCOL, EMPIRICAL RESULT, INFERENCE, OPEN QUESTION.

- A file's existence does not show that an experiment ran.
- A test passing does not validate a scientific hypothesis.
- A README metric is a reported claim until its underlying artifact and procedure are inspectable.
- Behavioral change, persistence, self-modeling, or causal control is not proof of phenomenal consciousness.
- Preserve negative results, null results, contradictions, preregistered definitions, and provenance.
- Never revise a preregistration retrospectively. Put post-result changes in a separately versioned analysis.

## Safe repository changes

- Work on a task-specific branch; do not commit directly to main.
- Prefer focused, reviewable changes. Do not delete branches, experiments, data, workflows, or historical records as a cleanup shortcut.
- Before replacing long documentation, preserve information that is not duplicated elsewhere and clearly mark any historical archive as non-canonical.
- Never claim a test or benchmark was run unless its command completed and its output was observed.
- Do not launch expensive or GPU-bound experiments until the output destination, provenance manifest, and persistence/recovery path have been tested.
- Never reconstruct a missing raw artifact and then label it as an original run output.

## Required state synchronization

Any meaningful change under research/, papers/, experiments/, docs/, sources/, or to README.md must update these files in the same change set:

- research/CURRENT_CHECKPOINT.md
- REPO_MEMORY.md
- RESEARCH_MAP.md

Also update the relevant registry or index if study/paper status changes. Preserve the exact commit, branch, seed, configuration, model revision, and artifact locations whenever available.

## Minimal completion checklist

Before reporting a task complete:

1. Identify files changed and the exact scope.
2. Validate JSON/YAML syntax for changed machine-readable files.
3. Check internal links and paths introduced by the change.
4. Run relevant lightweight tests where an execution environment is available; otherwise state explicitly what could not be run.
5. Verify that the three canonical state files agree.
6. Report unresolved blockers and avoid claiming more than the evidence supports.
