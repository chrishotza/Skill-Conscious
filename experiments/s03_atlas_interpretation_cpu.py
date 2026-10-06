#!/usr/bin/env python3
"""
S03.1 — Atlas interpretation / content extraction.
CPU-only. Reads S03 outputs; does not regenerate embeddings.

Goal:
Turn 14 semantic communities into an interpretable content atlas:
- cluster/family composition
- phenomenological subset composition
- motif concentration
- representative claims
- candidate cross-family phenomenological clusters

This is descriptive/exploratory. No p-values, no confirmatory claim.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
S03 = ROOT / "results/s03/S03_PHENOMENOLOGICAL_ATLAS_CPU_V1"
OUT = ROOT / "results/s03/S03_ATLAS_INTERPRETATION_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

REQUIRED = [
    "cluster_assignments.csv",
    "cluster_summary.csv",
    "cluster_motifs.csv",
    "cluster_representatives.csv",
    "bridge_claims.csv",
    "lofo_transfer.csv",
    "lofo_fold_summary.csv",
    "S03_PHENOMENOLOGICAL_ATLAS_RESULTS_V1.json",
]

def require_files():
    missing = [x for x in REQUIRED if not (S03 / x).exists()]
    if missing:
        raise FileNotFoundError(f"Missing S03 artifacts: {missing}")

def entropy(counts):
    vals = np.asarray([x for x in counts if x > 0], dtype=float)
    if len(vals) <= 1:
        return 0.0
    p = vals / vals.sum()
    return float(-(p * np.log(p)).sum() / np.log(len(vals)))

def pct(x):
    return f"{100*x:.1f}%"

def main():
    require_files()

    assignments = pd.read_csv(S03 / "cluster_assignments.csv")
    summary = pd.read_csv(S03 / "cluster_summary.csv")
    motifs = pd.read_csv(S03 / "cluster_motifs.csv")
    reps = pd.read_csv(S03 / "cluster_representatives.csv")
    bridges = pd.read_csv(S03 / "bridge_claims.csv")
    lofo = pd.read_csv(S03 / "lofo_transfer.csv")
    lofo_fold = pd.read_csv(S03 / "lofo_fold_summary.csv")

    result_meta = json.loads((S03 / "S03_PHENOMENOLOGICAL_ATLAS_RESULTS_V1.json").read_text(encoding="utf-8"))

    phenom_path = S03 / "phenomenological_subset.csv"
    phenom = pd.read_csv(phenom_path) if phenom_path.exists() else pd.DataFrame()

    # Exact family x cluster matrix.
    family_cluster = pd.crosstab(assignments["family"], assignments["cluster"])
    family_cluster.to_csv(OUT / "family_x_cluster.csv")

    if not phenom.empty:
        phenom_family_cluster = pd.crosstab(phenom["family"], phenom["cluster"])
        phenom_family_cluster.to_csv(OUT / "phenomenological_family_x_cluster.csv")
    else:
        phenom_family_cluster = pd.DataFrame()

    # Cluster interpretation table.
    rows = []
    for cid in sorted(assignments["cluster"].unique()):
        cclaims = assignments[assignments["cluster"] == cid]
        fam_counts = cclaims["family"].value_counts()
        c_motifs = motifs[motifs["cluster"] == cid].copy()
        c_reps = reps[reps["cluster"] == cid].copy()

        if not phenom.empty:
            cp = phenom[phenom["cluster"] == cid]
            phenom_claims = len(cp)
            phenom_families = cp["family"].nunique()
            phenom_density = phenom_claims / len(cclaims)
            phenom_family_entropy = entropy(cp["family"].value_counts().tolist())
        else:
            phenom_claims = 0
            phenom_families = 0
            phenom_density = float("nan")
            phenom_family_entropy = float("nan")

        top_families = "; ".join(
            f"{fam} ({n})" for fam, n in fam_counts.head(8).items()
        )
        top_motifs = "; ".join(
            f"{m} ({int(n)})"
            for m, n in zip(c_motifs["motif"].head(8), c_motifs["claim_support"].head(8))
        )
        representative_texts = " || ".join(
            str(x).replace("\n", " ").strip()
            for x in c_reps["claim"].head(5).tolist()
        )

        rows.append({
            "cluster": int(cid),
            "claims": int(len(cclaims)),
            "family_coverage": int(cclaims["family"].nunique()),
            "family_entropy": entropy(fam_counts.tolist()),
            "max_family_share": float(fam_counts.iloc[0] / len(cclaims)),
            "phenomenological_claims": int(phenom_claims),
            "phenomenological_density": float(phenom_density),
            "phenomenological_family_coverage": int(phenom_families),
            "phenomenological_family_entropy": float(phenom_family_entropy),
            "top_families": top_families,
            "top_motifs": top_motifs,
            "representative_claims": representative_texts,
        })

    atlas = pd.DataFrame(rows)
    atlas = atlas.sort_values(
        ["phenomenological_family_coverage", "family_coverage", "phenomenological_density", "claims"],
        ascending=[False, False, False, False],
        na_position="last",
    )
    atlas.to_csv(OUT / "cluster_content_atlas.csv", index=False)

    # Candidate cross-family phenomenological clusters:
    # descriptive ranking only; thresholds are deliberately transparent.
    candidate = atlas[
        (atlas["phenomenological_family_coverage"] >= 3)
        & (atlas["family_coverage"] >= 5)
    ].copy()
    candidate["candidate_rank_score"] = (
        candidate["phenomenological_family_coverage"]
        * candidate["phenomenological_family_entropy"].fillna(0)
        * candidate["phenomenological_density"].fillna(0)
    )
    candidate = candidate.sort_values("candidate_rank_score", ascending=False)
    candidate.to_csv(OUT / "candidate_cross_family_phenomenological_clusters.csv", index=False)

    # Bridge-claim view: strongest cross-family semantic connectors inside the atlas.
    bridge_cols = [
        "global_claim_id",
        "corpus_id",
        "family",
        "cluster",
        "bridge_rank_score",
        "cross_family_neighbor_fraction",
        "cross_family_mean_cosine",
        "cluster_family_coverage",
        "claim",
    ]
    bridges[bridge_cols].head(100).to_csv(
        OUT / "top_100_bridge_claims.csv", index=False
    )

    # LOFO fold summary retained verbatim + compact summary.
    lofo_fold.to_csv(OUT / "lofo_fold_summary_copy.csv", index=False)
    lofo_cluster = (
        lofo.groupby("heldout_family", dropna=False)
        .agg(
            claims=("claim_index", "count"),
            mean_strength=("top_community_strength", "mean"),
            median_strength=("top_community_strength", "median"),
            mean_receiver_family_coverage=("top_community_family_coverage", "mean"),
            fraction_multifamily_receiver=("top_community_family_coverage", lambda x: float((x >= 2).mean())),
        )
        .reset_index()
    )
    lofo_cluster.to_csv(OUT / "lofo_transfer_compact.csv", index=False)

    # Human-readable markdown report.
    lines = []
    lines.append("# S03.1 — Atlas Content Interpretation")
    lines.append("")
    lines.append("Exploratory descriptive layer over the frozen S03 semantic atlas.")
    lines.append("")
    lines.append("## Global result")
    lines.append("")
    lines.append(f"- Claims: {len(assignments):,}")
    lines.append(f"- Clusters: {assignments['cluster'].nunique()}")
    lines.append(f"- Families: {assignments['family'].nunique()}")
    lines.append(
        f"- Phenomenological subset: {len(phenom):,} claims"
        if not phenom.empty
        else "- Explicit phenomenological subset: unavailable"
    )
    lines.append("")
    lines.append("## Cluster content")
    lines.append("")
    lines.append(
        "| Cluster | Claims | Family cov. | Phenom. claims | Phenom. family cov. | Top motifs |"
    )
    lines.append("|---:|---:|---:|---:|---:|---|")
    for _, r in atlas.iterrows():
        lines.append(
            f"| {int(r['cluster'])} | {int(r['claims'])} | "
            f"{int(r['family_coverage'])} | {int(r['phenomenological_claims'])} | "
            f"{int(r['phenomenological_family_coverage'])} | "
            f"{r['top_motifs']} |"
        )

    lines.append("")
    lines.append("## Candidate cross-family phenomenological clusters")
    lines.append("")
    if candidate.empty:
        lines.append("No cluster met the descriptive threshold (>=3 phenomenological families and >=5 total families).")
    else:
        for _, r in candidate.iterrows():
            lines.append(
                f"### Cluster {int(r['cluster'])}\n"
                f"- Claims: {int(r['claims'])}\n"
                f"- Family coverage: {int(r['family_coverage'])}\n"
                f"- Phenomenological claims: {int(r['phenomenological_claims'])}\n"
                f"- Phenomenological family coverage: {int(r['phenomenological_family_coverage'])}\n"
                f"- Top families: {r['top_families']}\n"
                f"- Top motifs: {r['top_motifs']}\n"
                f"- Representative claims: {r['representative_claims']}\n"
            )

    lines.append("## Guardrails")
    lines.append("")
    lines.append("- A semantic community is not itself a phenomenological invariant.")
    lines.append("- Cross-family coverage is descriptive, not evidence of independent discovery.")
    lines.append("- LOFO transfer measures structural portability through the frozen semantic graph; it is not causal evidence.")
    lines.append("- Candidate clusters must be read at the claim level before any ontology is assigned.")

    (OUT / "S03_ATLAS_INTERPRETATION_REPORT_V1.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    manifest = {
        "study": "S03.1_ATLAS_INTERPRETATION_CPU_V1",
        "input_dir": str(S03),
        "claims": int(len(assignments)),
        "clusters": int(assignments["cluster"].nunique()),
        "families": int(assignments["family"].nunique()),
        "phenomenological_subset_available": bool(not phenom.empty),
        "phenomenological_claims": int(len(phenom)),
        "candidate_clusters": int(len(candidate)),
        "source_s03_results": result_meta.get("study"),
        "gpu_used": False,
        "new_embeddings": False,
    }
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT / "S03_ATLAS_INTERPRETATION_RESULTS_V1.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print("=" * 70)
    print("S03.1 — ATLAS CONTENT INTERPRETATION")
    print("=" * 70)
    print(f"Clusters: {assignments['cluster'].nunique()}")
    print(f"Families: {assignments['family'].nunique()}")
    print(f"Phenomenological claims: {len(phenom)}")
    print(f"Candidate cross-family phenomenological clusters: {len(candidate)}")
    print(f"Output: {OUT}")
    print("=" * 70)
    print("Guardrail: descriptive/exploratory only.")

if __name__ == "__main__":
    main()
