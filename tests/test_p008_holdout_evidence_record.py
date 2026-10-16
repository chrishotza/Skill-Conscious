"""Integrity of the post-run P008 record without accessing any holdout scenario."""
import json
from pathlib import Path


def test_holdout_postrun_archive_record_is_consistent_with_release_request():
    root = Path(__file__).resolve().parents[1]
    result = json.loads((root / "research/p008_holdout_result_v1.json").read_text())
    release = json.loads((root / "research/p008_holdout_archive_request.json").read_text())
    assert result["status"] == "COMPLETED_VERIFIED_INTERNAL_RESERVED_SPLIT"
    assert result["archive_status"] == "GITHUB_RELEASE_VERIFIED_SHA256_AND_SIZE"
    assert result["workflow_run_id"] == release["source_run_id"] == 38980796822
    assert result["artifact_id"] == release["source_artifact_id"] == 12081087004
    assert result["archive_asset_sha256"] == result["artifact_zip_sha256"] == release["source_zip_sha256"]
    assert result["archive_asset_size_bytes"] == result["artifact_size_bytes"] == release["source_size_bytes"] == 633705
    assert len(result["archive_asset_sha256"]) == 64
    assert result["scenario_count"] == 128 and result["expected_raw_rows"] == 640
    assert result["all_tests_passed"] is True
    assert result["predeclared_software_mechanism_gate_passed"] is True
    assert result["comparisons"]["B_vs_D"]["mean"] == 0
    assert result["comparisons"]["A_vs_B"]["mean"] == 0
    assert result["comparisons"]["C_vs_B"]["bootstrap_95"][0] > 0
    assert result["comparisons"]["C_vs_D"]["bootstrap_95"][0] > 0
    assert result["review_limit"].lower().find("no independent") >= 0
