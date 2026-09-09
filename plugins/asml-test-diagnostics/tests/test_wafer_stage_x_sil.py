"""SIL: wafer-stage X against a fake plant. Simulated time only."""

from __future__ import annotations

import json
from pathlib import Path

CYCLE_NS = 1_000_000
SIDECAR = Path(__file__).resolve().parent / "traces" / "wafer_stage_x_sil.json"


def run_sil(*, cycles: int = 8, inject: str = "missed-heartbeat") -> dict:
    traces = []
    fault = None
    safe = False
    t_ns = 0
    for i in range(cycles):
        t_ns += CYCLE_NS  # no sleep
        cmd_nm = 100 * i
        beat = 1
        if inject == "missed-heartbeat" and i == cycles // 2:
            beat = 0
            fault = "missed_heartbeat"
            safe = True
        if inject == "driver-error" and i == cycles - 2:
            fault = "driver_error"
            safe = True
        traces.append(
            {
                "t_ns": t_ns,
                "cmd_nm": cmd_nm,
                "est_nm": cmd_nm - 2,
                "out_nm": 0 if safe else cmd_nm,
                "heartbeat": beat,
                "fault": fault,
            }
        )
    return {
        "module": "wafer-stage-x",
        "level": "SIL",
        "cycle_ns": CYCLE_NS,
        "inject": inject,
        "safe_state": safe,
        "fault": fault,
        "pass": safe if inject != "none" else fault is None,
        "traces": traces,
        "mock": True,
    }


def test_missed_heartbeat_goes_safe_and_stays_sticky(tmp_path: Path) -> None:
    result = run_sil(inject="missed-heartbeat")
    sidecar = tmp_path / "wafer_stage_x_sil.json"
    sidecar.write_text(json.dumps(result, indent=2) + "\n")
    SIDECAR.parent.mkdir(parents=True, exist_ok=True)
    SIDECAR.write_text(json.dumps(result, indent=2) + "\n")

    assert result["traces"][0]["t_ns"] == CYCLE_NS
    assert result["traces"][1]["t_ns"] == 2 * CYCLE_NS
    assert result["fault"] == "missed_heartbeat"
    assert result["safe_state"] is True
    inject_i = 8 // 2
    assert result["traces"][inject_i]["heartbeat"] == 0
    for row in result["traces"][inject_i:]:
        assert row["fault"] == "missed_heartbeat"
        assert row["out_nm"] == 0  # mock hold; not tracking cmd


def test_driver_error_abort() -> None:
    result = run_sil(inject="driver-error")
    assert result["fault"] == "driver_error"
    assert result["safe_state"] is True
    assert result["pass"] is True
