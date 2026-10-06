import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _claim_ids(path: Path):
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^###\s+(SC-[A-Z0-9-]+)\s*$", text, re.MULTILINE)


def test_canonical_corpus_has_360_unique_claims_across_36_families():
    paths = [ROOT / "sources" / "CLAIM_ATLAS.md"] + sorted(
        (ROOT / "sources" / "claim_addendum").glob("*.md")
    )
    ids = [claim_id for path in paths for claim_id in _claim_ids(path)]
    assert len(ids) == 360
    assert len(set(ids)) == 360

    counts = {}
    for claim_id in ids:
        family = claim_id.split("-")[1]
        counts[family] = counts.get(family, 0) + 1
    assert len(counts) == 36
    assert set(counts.values()) == {10}


def test_canonical_corpus_keeps_hume_and_interoception_nonduplicated():
    ids = _claim_ids(ROOT / "sources" / "CLAIM_ATLAS.md")
    assert sum(item.startswith("SC-HUME-") for item in ids) == 10
    assert sum(item.startswith("SC-INTERO-") for item in ids) == 10
    addendum_ids = [
        claim_id
        for path in (ROOT / "sources" / "claim_addendum").glob("*.md")
        for claim_id in _claim_ids(path)
    ]
    assert not any(item.startswith("SC-HUME-") for item in addendum_ids)
    assert not any(item.startswith("SC-INTERO-") for item in addendum_ids)