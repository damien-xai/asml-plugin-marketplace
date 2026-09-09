"""Lot-to-lot APC Control: gain, clamp, hold. Mock — no scanner client."""

from __future__ import annotations

GAIN = 0.7
MAX_STEP = {"Tx_nm": 2.0, "Ty_nm": 2.0, "R_urad": 5.0, "M_ppm": 1.0}
KNOBS = tuple(MAX_STEP)


def _clamp(name: str, delta: float) -> float:
    cap = MAX_STEP[name]
    return max(-cap, min(cap, delta))


def control(
    knobs_before: dict,
    measured: dict,
    *,
    quality_ok: bool,
    residual_3sigma_nm: dict,
) -> dict:
    if not quality_ok:
        return {
            "lot_id": measured.get("lot_id"),
            "knobs_before": dict(knobs_before),
            "knobs_after": dict(knobs_before),
            "residual_3sigma_nm": residual_3sigma_nm,
            "held": True,
        }
    after = {
        k: round(knobs_before[k] + _clamp(k, GAIN * (measured[k] - knobs_before[k])), 3)
        for k in KNOBS
    }
    return {
        "lot_id": measured.get("lot_id"),
        "knobs_before": dict(knobs_before),
        "knobs_after": after,
        "residual_3sigma_nm": residual_3sigma_nm,
        "held": False,
    }
