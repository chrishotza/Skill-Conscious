#!/usr/bin/env python3
"""
S03.3 — Phenomenological Purity Audit

Reads the 24 candidate-cluster phenomenological claims already extracted by
S03.2 and applies an explicit, frozen adjudication schema.

Important:
- These adjudications are researcher/model judgments from the claim text.
- They are not source-provided labels.
- This stage is descriptive and methodological, not confirmatory.
- No embeddings or GPU are used.

Strict invariant discovery uses only P1.
P2 is theoretical phenomenology and is reported separately.
M1/O1/H1/N1/U1 are excluded from strict phenomenological counts.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
INPUT = ROOT / "results/s03/S03_CANDIDATE_CLAIM_AUDIT_CPU_V1/candidate_phenomenological_claims.csv"
OUT = ROOT / "results/s03/S03_PHENOMENOLOGICAL_PURITY_AUDIT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

# Frozen adjudication map based on the S03.2 claim texts.
# P1 = direct/substantive phenomenological structure
# P2 = phenomenological theory/model
# M1 = meta-methodological/epistemic
# O1 = ontological/metaphysical
# H1 = historical/bibliographic
# N1 = normative/comparative methodology
# U1 = ambiguous/mixed
ADJ = {
    "G33-S286-K01": ("P2", "Phenomenal concepts and explanatory gap; conceptual account, not direct experience."),
    "G33-S286-K02": ("M1", "Epistemological distinction between experience concepts and functional concepts."),
    "G33-S286-K06": ("M1", "Classifies a philosophical response family; not phenomenological content itself."),
    "G33-S286-K09": ("M1", "About argumentative framing and physicalism, not experiential structure."),
    "G33-S286-K11": ("P2", "Addresses the structural difficulty of translating first-person perspective into objective vocabulary."),
    "G33-S286-K13": ("M1", "About how a philosophical strategy is evaluated."),
    "G27-S221-K02": ("O1", "Critique of materialist explanatory scope; ontological/epistemic framing."),
    "G27-S221-K07": ("N1", "Method for comparative identification of cross-tradition patterns."),
    "G27-S221-K09": ("N1", "Normative instruction about comparative interpretation."),
    "G27-S221-K12": ("P2", "Claims that some phenomena resist ordinary categories; theoretical phenomenology."),
    "G27-S221-K13": ("H1", "Publication/history and scientific-status qualification."),
    "G30-S257-K12": ("M1", "Positions a philosophical work relative to neuroscience; not the phenomenological claim itself."),
    "G31-S258-K06": ("P2", "Conceptual-development theory about contradiction/negation; not direct experience."),
    "G31-S258-K12": ("M1", "Historical/methodological status of a philosophical work."),
    "G33-S286-K08": ("M1", "Conceptual access to experience and explanatory limits; not direct phenomenology."),
    "G27-S221-K04": ("P1", "Explicit distinction among ordinary human states and unusual/occult experiences."),
    "G30-S257-K01": ("P1", "Lived-body organization of perception."),
    "G30-S257-K13": ("P1", "Embodied perception-action orientation toward the world."),
    "G31-S258-K01": ("P2", "Theory of changing forms of consciousness via subject-object relation."),
    "G31-S258-K02": ("P2", "Reflexive self-consciousness as becoming an object to itself."),
    "G31-S258-K03": ("P2", "Recognition by another self-consciousness in constitution of self-consciousness."),
    "G31-S258-K07": ("P2", "Relational constitution of self through desire, work, and recognition."),
    "G31-S258-K08": ("P2", "Attention/figure of consciousness determining what counts as object/knowledge."),
    "G31-S258-K13": ("P2", "Relational/social dimension of self-consciousness."),
}

def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    df = pd.read_csv(INPUT)
    required = {"global_claim_id", "family", "cluster", "claim"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns: {missing}")

    key_col = "global_claim_id"
    df["audit_key"] = df[key_col].astype(str).str.extract(r"(G\d+-S\d+-K\d+)", expand=False)

    labels = []
    rationales = []
    for key in df["audit_key"]:
        if key not in ADJ:
            raise RuntimeError(f"No frozen adjudication for {key}")
        label, rationale = ADJ[key]
        labels.append(label)
        rationales.append(rationale)

    df["purity_class"] = labels
    df["adjudication_rationale"] = rationales
    df["strict_phenomenology"] = df["purity_class"].eq("P1")
    df["phenomenology_or_theory"] = df["purity_class"].isin(["P1", "P2"])

    df.to_csv(OUT / "adjudicated_candidate_claims.csv", index=False)

    cluster = (
        df.groupby(["cluster", "purity_class"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    for c in ["P1", "P2", "M1", "O1", "H1", "N1", "U1"]:
        if c not in cluster:
            cluster[c] = 0

    cluster["total"] = cluster[["P1","P2","M1","O1","H1","N1","U1"]].sum(axis=1)
    cluster["strict_p1_fraction"] = cluster["P1"] / cluster["total"]
    cluster["p1_p2_fraction"] = (cluster["P1"] + cluster["P2"]) / cluster["total"]
    cluster.to_csv(OUT / "purity_by_cluster.csv", index=False)

    fam = (
        df.groupby(["cluster", "family", "purity_class"])
        .size()
        .reset_index(name="claims")
    )
    fam.to_csv(OUT / "purity_by_cluster_family.csv", index=False)

    p1 = df[df["purity_class"] == "P1"].copy()
    p2 = df[df["purity_class"] == "P2"].copy()

    p1.to_csv(OUT / "strict_P1_claims.csv", index=False)
    p2.to_csv(OUT / "P2_theoretical_phenomenology_claims.csv", index=False)

    report = []
    report.append("# S03.3 — Phenomenological Purity Audit")
    report.append("")
    report.append("## Classification rule")
    report.append("")
    report.append("Only P1 is counted as direct/substantive phenomenological content.")
    report.append("P2 is theoretical phenomenology and is reported separately.")
    report.append("M1/O1/H1/N1/U1 are excluded from strict invariant discovery.")
    report.append("")
    report.append("## Overall")
    report.append("")
    report.append(f"- Candidate claims audited: {len(df)}")
    report.append(f"- P1 direct phenomenological: {int((df.purity_class == 'P1').sum())}")
    report.append(f"- P2 theoretical phenomenology: {int((df.purity_class == 'P2').sum())}")
    report.append(f"- M1 meta-methodological/epistemic: {int((df.purity_class == 'M1').sum())}")
    report.append(f"- O1 ontological/metaphysical: {int((df.purity_class == 'O1').sum())}")
    report.append(f"- H1 historical/bibliographic: {int((df.purity_class == 'H1').sum())}")
    report.append(f"- N1 normative/comparative: {int((df.purity_class == 'N1').sum())}")
    report.append(f"- U1 ambiguous/mixed: {int((df.purity_class == 'U1').sum())}")
    report.append("")
    report.append("## Strict P1 family coverage")
    p1_fams = sorted(p1["family"].unique().tolist())
    report.append(f"- Families represented: {len(p1_fams)}")
    for f in p1_fams:
        n = int((p1["family"] == f).sum())
        report.append(f"  - {f}: {n}")
    report.append("")
    report.append("## Strict P1 claims")
    for _, r in p1.sort_values(["cluster","family","global_claim_id"]).iterrows():
        report.append(
            f"- [Cluster {int(r.cluster)}] [{r.family}] {r.global_claim_id}: {r.claim}"
        )
    report.append("")
    report.append("## Interpretation")
    report.append("")
    report.append(
        "The audit is intended to prevent metadata contamination from being "
        "mistaken for phenomenological convergence."
    )

    (OUT / "S03_PHENOMENOLOGICAL_PURITY_AUDIT_REPORT_V1.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    manifest = {
        "study": "S03.3_PHENOMENOLOGICAL_PURITY_AUDIT_CPU_V1",
        "input": str(INPUT),
        "claims_audited": int(len(df)),
        "P1_count": int((df.purity_class == "P1").sum()),
        "P2_count": int((df.purity_class == "P2").sum()),
        "families_with_P1": int(p1["family"].nunique()),
        "gpu_used": False,
        "new_embeddings": False,
    }
    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=" * 80)
    print("S03.3 — PHENOMENOLOGICAL PURITY AUDIT")
    print("=" * 80)
    print("Claims audited:", len(df))
    print("P1 direct:", int((df.purity_class == "P1").sum()))
    print("P2 theoretical:", int((df.purity_class == "P2").sum()))
    print("M1 meta/epistemic:", int((df.purity_class == "M1").sum()))
    print("O1 ontological:", int((df.purity_class == "O1").sum()))
    print("H1 historical:", int((df.purity_class == "H1").sum()))
    print("N1 comparative:", int((df.purity_class == "N1").sum()))
    print("P1 family coverage:", int(p1["family"].nunique()))
    print("Output:", OUT)

if __name__ == "__main__":
    main()
