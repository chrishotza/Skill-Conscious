#!/usr/bin/env python3
"""
S03.11 — Remaining 36 multifamily candidate readout.

Reads the authoritative S03.10 export. No calculations beyond descriptive
sorting; no embeddings; no GPU; no adjudication.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
IN = ROOT / "results/s03/S03_MULTIFAMILY_FULL_EXPORT_CPU_V1/remaining_36_candidates.csv"
OUT = ROOT / "results/s03/S03_REMAINING36_READOUT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    if not IN.exists():
        raise FileNotFoundError(IN)

    df = pd.read_csv(IN)

    required = {
        "global_claim_id","corpus_id","candidate_family","candidate_cluster",
        "seed_family_coverage","seed_families","best_seed_global_claim_id",
        "best_seed_family","best_seed_similarity","seed_connection_count",
        "candidate_claim","best_seed_claim"
    }
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing columns: {sorted(missing)}")

    df = df.sort_values(
        ["seed_family_coverage","best_seed_similarity","seed_connection_count"],
        ascending=[False,False,False]
    ).reset_index(drop=True)
    df["remaining36_order"] = range(1, len(df)+1)

    cols = [
        "remaining36_order","global_claim_id","corpus_id","candidate_family",
        "candidate_cluster","seed_family_coverage","seed_families",
        "best_seed_global_claim_id","best_seed_family","best_seed_similarity",
        "seed_connection_count","candidate_claim","best_seed_claim"
    ]
    df[cols].to_csv(OUT / "remaining_36_claims_complete.csv", index=False)

    pair_rows = []
    for _, r in df.iterrows():
        fams = sorted(set(
            x.strip() for x in str(r["seed_families"]).split(";") if x.strip()
        ))
        for i,a in enumerate(fams):
            for b in fams[i+1:]:
                pair_rows.append({
                    "global_claim_id": r["global_claim_id"],
                    "candidate_family": r["candidate_family"],
                    "family_a": a,
                    "family_b": b,
                    "seed_family_coverage": int(r["seed_family_coverage"]),
                    "best_seed_similarity": float(r["best_seed_similarity"]),
                    "claim": r["candidate_claim"],
                })

    pairs = pd.DataFrame(pair_rows)
    if not pairs.empty:
        pair_summary = (
            pairs.groupby(["family_a","family_b"])
            .agg(
                candidate_claims=("global_claim_id","nunique"),
                mean_similarity=("best_seed_similarity","mean"),
            )
            .reset_index()
            .sort_values("candidate_claims", ascending=False)
        )
    else:
        pair_summary = pd.DataFrame()

    pairs.to_csv(OUT / "remaining36_family_pairs.csv", index=False)
    pair_summary.to_csv(OUT / "remaining36_family_pair_summary.csv", index=False)

    lines = []
    lines.append("="*100)
    lines.append("S03.11 — REMAINING 36 MULTIFAMILY CANDIDATES")
    lines.append("="*100)
    lines.append("")
    lines.append("No automatic classification. Read claims before adjudication.")
    lines.append("")

    for _,r in df.iterrows():
        lines.append(
            f"#{int(r['remaining36_order'])} | {r['global_claim_id']} | "
            f"{r['corpus_id']} | FAMILY={r['candidate_family']}"
        )
        lines.append(
            f"SEED-FAMILIES ({int(r['seed_family_coverage'])}): {r['seed_families']}"
        )
        lines.append(
            f"BEST-SEED: {r['best_seed_global_claim_id']} | "
            f"{r['best_seed_family']} | sim={float(r['best_seed_similarity']):.6f} | "
            f"connections={int(r['seed_connection_count'])}"
        )
        lines.append("CLAIM:")
        lines.append(str(r["candidate_claim"]))
        lines.append("SEED CLAIM:")
        lines.append(str(r["best_seed_claim"]))
        lines.append("-"*100)

    (OUT / "S03.11_REMAINING36_CLAIMS.txt").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    manifest = {
        "study":"S03.11_REMAINING36_READOUT_CPU_V1",
        "claims":int(len(df)),
        "gpu_used":False,
        "new_embeddings":False,
        "automatic_adjudication":False
    }
    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )

    print("="*100)
    print("S03.11 COMPLETE")
    print("="*100)
    print("Remaining claims:",len(df))
    print("Output:",OUT)
    print()
    print("Family pairs:")
    if pair_summary.empty:
        print("none")
    else:
        print(pair_summary.to_string(index=False))
    print("="*100)

if __name__ == "__main__":
    main()
