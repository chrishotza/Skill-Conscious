#!/usr/bin/env python3
"""
S03.4 — Exhaustive phenomenology inventory.

Scans all 4,315 frozen claims and inventories every claim carrying explicit
phenomenological metadata. This is an inventory, not a strict P1 judgment.

No GPU, no embeddings, no new model calls.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
import requests

REPO = "chrishotza/Skill-Conscious"
BRANCH = "corpus-v1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"

EXPECTED_CLAIMS = {
    "corpus/CLAIMS/claim_ledger_v1.json": "86a9a310c30f2937a206f09bd8d65e7d3097d90b",
    "corpus/CLAIMS/claim_ledger_v1_append_v24.json": "95af02d2af246a97d29dcc1b1266d28dbbaa6551",
    "corpus/CLAIMS/claim_ledger_v1_append_v25.json": "334dd00f724da4c8249e25895326e6892072f37c",
    "corpus/CLAIMS/claim_ledger_v1_append_v26.json": "7b1ac7528eb421a52d18a9fd615711381d624745",
    "corpus/CLAIMS/claim_ledger_v1_append_v27.json": "70b1f767c532acafaa761dda5a4e2d42df7e8228",
    "corpus/CLAIMS/claim_ledger_v1_append_v28.json": "6c96ac9c2aa041c7dcd8c6d76637d2e0730ae7ba",
    "corpus/CLAIMS/claim_ledger_v1_append_v29.json": "c5519ea542667dda6280e9c72116f7963ef6c20b",
    "corpus/CLAIMS/claim_ledger_v1_append_v30.json": "57fa05224c9e0c99157dd30a7ab98e222cc042c4",
    "corpus/CLAIMS/claim_ledger_v1_append_v31.json": "bda1909c0898713ae81497a63c84b0c753f5180a",
    "corpus/CLAIMS/claim_ledger_v1_append_v32.json": "06adec55d4ae1ea3c0b1b0d40ed06c4ff832af2c",
    "corpus/CLAIMS/claim_ledger_v1_append_v33.json": "7dca934f5ace9d0bbcc5c8e9ace7374c96bc4695",
    "corpus/CLAIMS/claim_ledger_v1_append_v34.json": "65ac747328c4e2345202190987cedb178ca4672c",
    "corpus/CLAIMS/claim_ledger_v1_append_v35.json": "3aa539f92efa7fb2526e4a2742105ad569281c9b",
    "corpus/CLAIMS/claim_ledger_v1_append_v36.json": "0e4805e1172afe2cc890209371ffadf822a25f5b",
    "corpus/CLAIMS/claim_ledger_v1_append_v37.json": "46acc9f2a0aaef9e86ffab3e519c330c4a7d7cf2",
}
SOURCE_REGISTER_PATH = "corpus/SOURCE_REGISTER_V1.md"
SOURCE_REGISTER_SHA = "a4184dc5c40dd9d3580ebf9cfd4302ac64686a8d"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def fetch_verified(relpath: str, expected_sha: str, cache: Path) -> bytes:
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / Path(relpath).name
    if target.exists():
        data = target.read_bytes()
        if git_blob_sha(data) == expected_sha:
            return data
    r = requests.get(f"{RAW_BASE}/{relpath}", timeout=120)
    r.raise_for_status()
    data = r.content
    actual = git_blob_sha(data)
    if actual != expected_sha:
        raise RuntimeError(f"SHA mismatch {relpath}: {actual} != {expected_sha}")
    target.write_bytes(data)
    return data

def parse_source_families(text: str) -> dict[str, str]:
    families = {}
    for line in text.splitlines():
        if not line.startswith("| C"):
            continue
        parts = line.split("|")
        if len(parts) < 4:
            continue
        cid = parts[1].strip()
        descriptor = parts[2].strip()
        if cid.startswith("C") and "—" in descriptor and ";" in descriptor:
            families[cid] = descriptor.split("—", 1)[1].split(";", 1)[0].strip()
    if len(families) != 325:
        raise RuntimeError(f"Expected 325 families, got {len(families)}")
    return families

EXCLUDED_KEYS = {
    "claim", "text", "source_text", "excerpt", "quote",
    "description", "notes", "comment", "citation",
}

def recursive_hits(value, prefix=""):
    hits = []
    if isinstance(value, dict):
        for k, v in value.items():
            lk = str(k).lower()
            if lk in EXCLUDED_KEYS:
                continue
            path = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                hits.extend(recursive_hits(v, path))
            elif isinstance(v, str) and "phenomen" in v.lower():
                hits.append(path)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            path = f"{prefix}[{i}]"
            if isinstance(item, (dict, list)):
                hits.extend(recursive_hits(item, path))
            elif isinstance(item, str) and "phenomen" in item.lower():
                hits.append(path)
    return hits

def load_claims(cache: Path):
    records = []
    for relpath, sha in EXPECTED_CLAIMS.items():
        data = fetch_verified(relpath, sha, cache)
        records.extend(json.loads(data.decode("utf-8"))["records"])
    if len(records) != 4315:
        raise RuntimeError(f"Expected 4315 claims, got {len(records)}")
    return records

def main():
    root = Path("/content/drive/MyDrive/Skill-Conscious")
    out = root / "results/s03/S03_EXHAUSTIVE_PHENOMENOLOGY_INVENTORY_CPU_V1"
    out.mkdir(parents=True, exist_ok=True)
    cache = out / "data_cache"

    print("=" * 80)
    print("S03.4 — EXHAUSTIVE PHENOMENOLOGY INVENTORY")
    print("=" * 80)
    print("4,315 claims scanned")
    print("No GPU / no embeddings")
    print()

    records = load_claims(cache)
    families = parse_source_families(
        fetch_verified(SOURCE_REGISTER_PATH, SOURCE_REGISTER_SHA, cache).decode("utf-8")
    )

    rows = []
    field_counts = Counter()

    for i, rec in enumerate(records):
        hits = recursive_hits(rec)
        if not hits:
            continue
        for h in hits:
            field_counts[h] += 1
        rows.append({
            "claim_index": i,
            "global_claim_id": rec.get("global_claim_id"),
            "corpus_id": rec.get("corpus_id"),
            "family": families[rec["corpus_id"]],
            "metadata_paths": ";".join(sorted(set(hits))),
            "claim": rec.get("claim", ""),
            "motifs": ";".join(map(str, rec.get("motifs") or [])),
        })

    raw = pd.DataFrame(rows)
    if raw.empty:
        raise RuntimeError("No explicit phenomenological metadata found.")

    claim_level = (
        raw.groupby(
            ["claim_index", "global_claim_id", "corpus_id", "family", "claim"],
            dropna=False,
            as_index=False,
        )
        .agg(
            metadata_paths=("metadata_paths", lambda s: ";".join(sorted(set(
                p for cell in s for p in str(cell).split(";") if p
            )))),
            motifs=("motifs", lambda s: ";".join(sorted(set(
                p for cell in s for p in str(cell).split(";") if p
            )))),
        )
    )

    by_family = (
        claim_level.groupby("family")
        .agg(
            tagged_claims=("global_claim_id", "count"),
            corpus_units=("corpus_id", "nunique"),
        )
        .reset_index()
        .sort_values("tagged_claims", ascending=False)
    )

    by_field = pd.DataFrame(
        [{"metadata_path": k, "hits": v} for k, v in field_counts.items()]
    ).sort_values("hits", ascending=False)

    motif_counts = Counter()
    motif_families = defaultdict(set)
    for _, row in claim_level.iterrows():
        for motif in [x for x in str(row["motifs"]).split(";") if x]:
            motif_counts[motif] += 1
            motif_families[motif].add(row["family"])

    motif_df = pd.DataFrame([
        {
            "motif": motif,
            "tagged_claim_support": support,
            "family_support": len(motif_families[motif]),
        }
        for motif, support in motif_counts.most_common()
    ])

    claim_level.to_csv(out / "all_tagged_phenomenological_claims.csv", index=False)
    by_family.to_csv(out / "tagged_claims_by_family.csv", index=False)
    by_field.to_csv(out / "phenomenological_metadata_fields.csv", index=False)
    motif_df.to_csv(out / "tagged_claim_motifs.csv", index=False)

    manifest = {
        "study": "S03.4_EXHAUSTIVE_PHENOMENOLOGY_INVENTORY_CPU_V1",
        "claims_scanned": 4315,
        "tagged_unique_claims": int(len(claim_level)),
        "families_with_tagged_claims": int(claim_level["family"].nunique()),
        "corpus_units_with_tagged_claims": int(claim_level["corpus_id"].nunique()),
        "metadata_paths_with_hits": int(len(by_field)),
        "gpu_used": False,
        "new_embeddings": False,
        "limit": "Metadata inventory only; tags are not equivalent to P1.",
    }

    (out / "run_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report = [
        "# S03.4 — Exhaustive Phenomenology Inventory",
        "",
        f"- Claims scanned: {len(records):,}",
        f"- Explicitly tagged unique claims: {len(claim_level):,}",
        f"- Families represented: {claim_level['family'].nunique()}",
        f"- Corpus units represented: {claim_level['corpus_id'].nunique()}",
        "",
        "## By family",
        "",
    ]

    for _, row in by_family.iterrows():
        report.append(
            f"- {row['family']}: {int(row['tagged_claims'])} claims / "
            f"{int(row['corpus_units'])} corpus units"
        )

    report += ["", "## Metadata fields / paths", ""]
    for _, row in by_field.iterrows():
        report.append(f"- {row['metadata_path']}: {int(row['hits'])}")

    report += ["", "## Top motifs among tagged claims", ""]
    for _, row in motif_df.head(30).iterrows():
        report.append(
            f"- {row['motif']}: {int(row['tagged_claim_support'])} claims / "
            f"{int(row['family_support'])} families"
        )

    report += [
        "",
        "## Guardrail",
        "",
        "An explicit phenomenological tag is annotation metadata, not proof that a claim directly describes experience.",
    ]

    (out / "S03_EXHAUSTIVE_PHENOMENOLOGY_INVENTORY_REPORT_V1.md").write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print("=" * 80)
    print("S03.4 COMPLETE")
    print("=" * 80)
    print("Claims scanned:", len(records))
    print("Tagged unique claims:", len(claim_level))
    print("Families represented:", claim_level["family"].nunique())
    print("Corpus units represented:", claim_level["corpus_id"].nunique())
    print("Output:", out)
    print()
    print("NOTE: inventory only; strict P1 adjudication comes next.")

if __name__ == "__main__":
    main()
