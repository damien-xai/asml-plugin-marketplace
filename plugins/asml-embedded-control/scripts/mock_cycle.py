#!/usr/bin/env python3
"""One mocked 1 ms wafer-stage X cycle. No hardware."""
from __future__ import annotations

import argparse
import json

TRAVEL_NM = 150_000_000  # ±150 mm


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cmd-nm", type=int, default=1200)
    p.add_argument("--inject-fault", choices=["none", "limit", "missed-heartbeat"], default="none")
    args = p.parse_args()

    sample = {"t_ns": 1_000_000, "pos_nm": 800, "vel_nm_s": 400_000}
    setpoint = {"pos_nm": args.cmd_nm, "force_mN": 12}
    fault = None
    safe = False

    if abs(setpoint["pos_nm"]) > TRAVEL_NM:
        fault = "travel_limit"
        setpoint = {"pos_nm": sample["pos_nm"], "force_mN": 0}
        safe = True
    if args.inject_fault == "limit":
        fault = "travel_limit"
        setpoint = {"pos_nm": sample["pos_nm"], "force_mN": 0}
        safe = True
    if args.inject_fault == "missed-heartbeat":
        fault = "missed_heartbeat"
        setpoint = {"pos_nm": sample["pos_nm"], "force_mN": 0}
        safe = True

    print(
        json.dumps(
            {
                "axis": "wafer-stage-x",
                "cycle_ns": 1_000_000,
                "sample": sample,
                "setpoint": setpoint,
                "heartbeat": 1 if args.inject_fault != "missed-heartbeat" else 0,
                "fault": fault,
                "safe_state": safe,
                "mock": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
