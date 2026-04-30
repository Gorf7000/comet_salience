"""Map raw AERITH statuses to expected/seen/event_case fields (spec §6)."""

from __future__ import annotations

import pandas as pd

# Keys: raw AERITH status string (matches ICON_TO_STATUS values in source_aerith)
# Values: dict with expected, seen, event_case, confidence
AERITH_STATUS_MAP: dict[str, dict] = {
    "Discovered": {
        "expected": False, "seen": True,
        "event_case": "unexpected_seen", "confidence": "high",
    },
    "Appeared": {
        "expected": True, "seen": True,
        "event_case": "expected_seen", "confidence": "high",
    },
    "Not observed": {
        "expected": True, "seen": False,
        "event_case": "expected_not_seen", "confidence": "high",
    },
    "Appeared before discovery": {
        "expected": None, "seen": True,
        "event_case": "retrospective_pre_discovery", "confidence": "high",
    },
    "Not observed before discovery": {
        "expected": None, "seen": False,
        "event_case": "retrospective_not_observed", "confidence": "high",
    },
    "Returns in the future": {
        "expected": None, "seen": None,
        "event_case": "future_return", "confidence": "high",
    },
}


def code_status(raw_status: str) -> dict:
    """Look up the expected/seen/event_case mapping for a raw AERITH status.

    Unknown statuses get marked manual_review_status=True with confidence='low'.
    """
    entry = AERITH_STATUS_MAP.get(raw_status)
    if entry is None:
        return {
            "expected": None, "seen": None,
            "event_case": "unknown", "confidence": "low",
            "manual_review_status": True,
            "status_notes": f"Unrecognised raw status: {raw_status!r}",
        }
    return {
        "expected": entry["expected"],
        "seen": entry["seen"],
        "event_case": entry["event_case"],
        "confidence": entry["confidence"],
        "manual_review_status": False,
        "status_notes": "",
    }


def apply_status_mapping(df: pd.DataFrame, raw_col: str = "raw_aerith_status") -> pd.DataFrame:
    """Apply code_status() row-wise; return df with new columns merged in."""
    coded = df[raw_col].apply(code_status).apply(pd.Series)
    coded = coded.rename(columns={"confidence": "status_mapping_confidence"})
    out = df.copy()
    for col in ["expected", "seen", "event_case", "status_mapping_confidence",
                "manual_review_status", "status_notes"]:
        out[col] = coded[col]
    return out
