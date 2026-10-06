#!/usr/bin/env python3
"""
S03.9 — P1 independence / seed-leakage audit.

Uses the frozen S03.8 priority queue and the explicit adjudication table encoded
below. Produces:
- strict P1 list
- P1 family/corpus/source-group coverage
- candidate dimension x family matrix
- seed-family vs P1-family leakage
- descriptive overlap summary

This is still exploratory. It does not establish independent discovery.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("/content/drive/MyMyDrive/Skill-Conscious")
ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
IN = ROOT / "results/s03/S03_PRIORITY_CLAIM_EXPORT_CPU_V1/priority_31_claims_complete.csv"
OUT = ROOT / "results/s03/S03_P1_INDEPENDENCE_AUDIT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

P1 = {
    "G31-S259-K02": "prereflexive_self_awareness",
    "G33-S283-K13": "embodied_experience",
    "G32-S268-K08": "self_reference_nonreduction",
    "G28-S233-K04": "altered_experiential_states",
    "G8-S060-TM04": "deidentification_conceptual_thought",
    "G9-S067-VB05": "attention_access_awareness",
    "G31-S265-K05": "intersubjective_experience",
    "G10-S070-HU10": "exceptional_experience_relational_disclosure",
    "G31-S265-K06": "embodied_prereflective_experience",
}

# The candidate table contains 31 rows; the adjudication document calls 8/31
# strict P1 but three of the above are closely related and all are retained.
# We keep the duplicate-dimension structure explicit rather than collapsing it.

SEED_FAMILIES = {
    "Ciencia/IA",
    "Filosofía/fenomenología",
    "Esoterismo occidental",
    "Suplementario",
}

def source_group(global_claim_id: str) -> str:
    # G31-S265-K05 -> G31
    return str(global_claim_id).split("-")[0]

def main():
    if not IN.exists():
        raise FileNotFoundError(IN)

    df = pd.read_csv(IN)
    if "global_claim_id" not in df.columns:
        raise RuntimeError("priority export missing global_claim_id")

    df = df[df["global_claim_id"].isin(P1)].copy()
    if df.empty:
        raise RuntimeError("No P1 claims matched the adjudication map.")

    df["p1_dimension"] = df["global_claim_id"].map(P1)
    df["source_group"] = df["global_claim_id"].map(source_group)
    df["candidate_family_is_seed_family"] = df["candidate_family"].isin(SEED_FAMILIES)

    # NOTE: candidate-level seed families are provided as a semicolon-delimited
    # field from S03.6; preserve exact values for leakage inspection.
    df["seed_family_list"] = df["seed_families"].fillna("").astype(str)

    df.to_csv(OUT / "strict_P1_priority_claims.csv", index=False)

    family = (
        df.groupby("candidate_family")
        .agg(
            p1_claims=("global_claim_id", "count"),
            corpus_units=("corpus_id", "nunique"),
            source_groups=("source_group", "nunique"),
            dimensions=("p1_dimension", "nunique"),
        )
        .reset_index()
        .sort_values("p1_claims", ascending=False)
    )
    family.to_csv(OUT / "p1_by_family.csv", index=False)

    source = (
        df.groupby(["source_group", "candidate_family"])
        .agg(
            p1_claims=("global_claim_id", "count"),
            corpus_units=("corpus_id", "nunique"),
        )
        .reset_index()
    )
    source.to_csv(OUT / "p1_by_source_group.csv", index=False)

    dim_family = pd.crosstab(df["p1_dimension"], df["candidate_family"])
    dim_family.to_csv(OUT / "p1_dimension_x_family.csv")

    seed_vs_family = (
        df.groupby(["candidate_family", "candidate_family_is_seed_family"])
        .size()
        .reset_index(name="p1_claims")
    )
    seed_vs_family.to_csv(OUT / "p1_seed_family_status.csv", index=False)

    # Exact pairwise family connections in the strict P1 set.
    rows = []
    for dim, sub in df.groupby("p1_dimension"):
        fams = sorted(sub["candidate_family"].unique())
        for i, a in enumerate(fams):
            for b in fams[i + 1:]:
                rows.append({
                    "dimension": dim,
                    "family_a": a,
                    "family_b": b,
                    "claims_a": int((sub["candidate_family"] == a).sum()),
                    "claims_b": int((sub["candidate_family"] == b).sum()),
                })
    pairs = pd.DataFrame(rows)
    pairs.to_csv(OUT / "p1_dimension_family_pairs.csv", index=False)

    manifest = {
        "study": "S03.9_P1_INDEPENDENCE_AUDIT_CPU_V1",
        "p1_claims": int(len(df)),
        "p1_families": int(df["candidate_family"].nunique()),
        "p1_corpus_units": int(df["corpus_id"].nunique()),
        "p1_source_groups": int(df["source_group"].nunique()),
        "seed_families": sorted(SEED_FAMILIES),
        "p1_claims_from_non_seed_families": int((~df["candidate_family_is_seed_family"]).sum()),
        "gpu_used": False,
        "new_embeddings": False,
        "guardrail": "Descriptive independence audit; not evidence of independent discovery.",
    }

    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=" * 80)
    print("S03.9 — P1 INDEPENDENCE AUDIT")
    print("=" * 80)
    print("P1 claims:", len(df))
    print("P1 families:", df["candidate_family"].nunique())
    print("P1 corpus units:", df["corpus_id"].nunique())
    print("P1 source groups:", df["source_group"].nunique())
    print("P1 claims from non-seed families:", int((~df["candidate_family_is_seed_family"]).sum()))
    print()
    print("P1 by family:")
    print(family.to_string(index=False))
    print("=" * 80)

if __name__ == "__main__":
    main()
