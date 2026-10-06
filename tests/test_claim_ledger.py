import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claim_ledger_is_complete_and_explicitly_unresolved_before_testing():
    payload = json.loads((ROOT / "sources" / "CLAIM_LEDGER_V1.json").read_text(encoding="utf-8"))
    claims = payload["claims"]
    assert payload["corpus"]["claims"] == 360
    assert payload["corpus"]["families"] == 36
    assert len(claims) == 360
    assert len({claim["id"] for claim in claims}) == 360
    assert {claim["status"] for claim in claims} == {"UNRESOLVED"}
    required = {
        "id", "family", "source_class", "canonical_source", "source_claim",
        "engineering_extraction", "epistemic_class", "motif", "system_component",
        "mechanism", "prediction", "intervention", "result", "status",
    }
    assert all(required <= claim.keys() for claim in claims)


def test_claim_ledger_preserves_hume_and_interoception_once_each():
    payload = json.loads((ROOT / "sources" / "CLAIM_LEDGER_V1.json").read_text(encoding="utf-8"))
    ids = [claim["id"] for claim in payload["claims"]]
    assert sum(x.startswith("SC-HUME-") for x in ids) == 10
    assert sum(x.startswith("SC-INTERO-") for x in ids) == 10