#!/usr/bin/env python3
"""
S03.8 — Priority claim export for human inspection.

Reads the frozen S03.7 priority queue and emits the 31 claims in a compact,
copy/paste-friendly form. No calculations, no embeddings, no classification.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path("/content/drive/MyDrive/Skill-Conscious")
IN = ROOT / "results/s03/S03_CANDIDATE_CLAIM_READOUT_CPU_V1/priority_31_claims.csv"
OUT = ROOT / "results/s03/S03_PRIORITY_CLAIM_EXPORT_CPU_V1"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    if not IN.exists():
        raise FileNotFoundError(IN)

    df = pd.read_csv(IN)
    cols = [
        "review_batch_order",
        "global_claim_id",
        "corpus_id",
        "candidate_family",
        "candidate_cluster",
        "seed_family_coverage",
        "seed_families",
        "best_seed_global_claim_id",
        "best_seed_family",
        "best_seed_similarity",
        "seed_connection_count",
        "candidate_claim",
        "best_seed_claim",
    ]

    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing columns: {missing}")

    df = df.sort_values("review_batch_order").reset_index(drop=True)
    df[cols].to_csv(OUT / "priority_31_claims_complete.csv", index=False)

    lines = []
    lines.append("=" * 100)
    lines.append("S03.8 — PRIORITY 31 CLAIMS")
    lines.append("=" * 100)

    for _, r in df.iterrows():
        lines.append("")
        lines.append(
            f"#{int(r['review_batch_order'])} | {r['global_claim_id']} | "
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
        lines.append("-" * 100)

    report = "\n".join(lines)
    (OUT / "S03.8_PRIORITY_31_CLAIMS.txt").write_text(report, encoding="utf-8")

    manifest = {
        "study": "S03.8_PRIORITY_CLAIM_EXPORT_CPU_V1",
        "claims_exported": int(len(df)),
        "gpu_used": False,
        "new_embeddings": False,
        "purpose": "Human inspection only; no classification or inference.",
    }
    (OUT / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(report)
    print("")
    print("=" * 100)
    print("S03.8 COMPLETE")
    print("=" * 100)
    print("Output:", OUT)

if __name__ == "__main__":
    main()
