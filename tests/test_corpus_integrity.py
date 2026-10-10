import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "corpus" / "CLAIMS"


def _load_records(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise AssertionError(f"unsupported ledger shape: {path}")


def test_effective_corpus_is_4315_atomic_claim_records():
    core = _load_records(CLAIMS_DIR / "claim_ledger_v1.json")
    appends = [_load_records(path) for path in sorted(CLAIMS_DIR.glob("claim_ledger_v1_append_v*.json"))]
    records = core + [record for batch in appends for record in batch]
    assert len(core) == 2482
    assert len(appends) == 14
    assert sum(len(batch) for batch in appends[:-1]) == 13 * 130
    assert len(appends[-1]) == 143
    assert len(records) == 4315
    assert len({record["global_claim_id"] for record in records}) == 4315
    assert all(record.get("global_claim_id") and record.get("source_id") for record in records)


def test_effective_corpus_has_328_source_ids_and_325_register_entries():
    core = _load_records(CLAIMS_DIR / "claim_ledger_v1.json")
    appends = [_load_records(path) for path in sorted(CLAIMS_DIR.glob("claim_ledger_v1_append_v*.json"))]
    records = core + [record for batch in appends for record in batch]
    source_ids = {record["source_id"] for record in records}
    register = (ROOT / "corpus" / "SOURCE_REGISTER_V1.md").read_text(encoding="utf-8")
    register_ids = re.findall(r"\| (C\d{3}) \|", register)
    assert len(source_ids) == 328
    assert len(set(register_ids)) == 325
    assert set(register_ids) == {f"C{i:03d}" for i in range(1, 326)}


def test_effective_corpus_closes_the_registered_claim_space_without_inventing_c326_c350():
    index = (CLAIMS_DIR / "CLAIM_EXTRACTION_INDEX_V1.md").read_text(encoding="utf-8")
    assert "4315" in index
    assert "325/325 represented" in index
    assert "No C326–C350 entries are inferred or invented." in index