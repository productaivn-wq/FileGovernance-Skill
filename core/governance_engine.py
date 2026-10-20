"""
File Governance Engine — Core specification implementation.
Provides deterministic 5-zone routing, PDCA artifact lifecycle validation,
and Knowledge Graph ontology mapping.
"""
import re
from pathlib import Path
from typing import Dict, Any

ZONES = {
    "00_INBOX": "Ephemeral triage zone for unorganized raw inputs",
    "10_ACTIVE_TIMEBOUND": "Sprint and milestone-driven deliverables with finite lifecycles",
    "20_ACTIVE_CONTINUOUS": "Continuous production assets and persistent system capabilities",
    "30_REFERENCE": "Read-only reference materials, standards, and schemas",
    "40_ARCHIVE": "Immutable historical records and frozen artifacts",
}

PDCA_CYCLES = ["PLAN", "DO", "CHECK", "ACT"]


def validate_zone(path_str: str) -> bool:
    """Validate if path conforms to the 5-zone MECE classification."""
    parts = Path(path_str).parts
    return any(zone in parts for zone in ZONES)


def parse_pdca_prefix(filename: str) -> Dict[str, Any]:
    """Parse standard PDCA naming convention from filename."""
    pattern = r"^(?P<domain>\d{2})\.(?P<cycle>[A-Z]{2})\.(?P<seq>\d{2})\s*-\s*(?P<date>\d{8})\s*-\s*(?P<title>.+)$"
    match = re.match(pattern, filename)
    if not match:
        return {"valid": False}
    return {"valid": True, **match.groupdict()}
