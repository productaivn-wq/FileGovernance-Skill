"""
Adversarial tests for file governance engine.
Tests edge cases, malicious path traversal, invalid characters, and hallucinated payloads.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from core.governance_engine import validate_zone, parse_pdca_prefix


def test_path_traversal_rejection():
    assert not validate_zone("../../../etc/passwd")
    assert not validate_zone("arbitrary_folder/file.txt")


def test_valid_zone_acceptance():
    assert validate_zone("10_ACTIVE_TIMEBOUND/sprint_1/spec.md")
    assert validate_zone("30_REFERENCE/iso_19650.md")


def test_pdca_parsing_adversarial():
    assert not parse_pdca_prefix("random_file.py")["valid"]
    assert not parse_pdca_prefix("99.XX.99 - invalid - title")["valid"]
    valid_res = parse_pdca_prefix("12.PL.01 - 20260907 - Project_Plan.md")
    assert valid_res["valid"]
    assert valid_res["domain"] == "12"
    assert valid_res["cycle"] == "PL"
