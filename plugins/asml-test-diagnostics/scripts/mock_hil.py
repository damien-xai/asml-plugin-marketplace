#!/usr/bin/env python3
"""Mock SIL run of a scanner module against a fake plant. No hardware."""
from __future__ import annotations

import argparse
import json


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--module", default="wafer-stage-x")
    p.add_argument("--cycles", type=int, default=8)
    p.add_argument("--inject", choices=["none", "missed-heartbeat", "driver-error"], default="none")
    args = p.parse_args()

    traces = []
    fault = None
    safe = False
    for i in range(args.cycles):
        t_ns = (i + 1) * 1_000_000
        beat = 1
        if args.inject == "missed-heartbeat" and i == args.cycles // 2:
            beat = 0
            fault = "missed_heartbeat"
            safe = True
        if args.inject == "driver-error" and i == args.cycles - 2:
            fault = "driver_error"
            safe = True
        traces.append(
            {
                "t_ns": t_ns,
                "cmd_nm": 100 * i,
                "est_nm": 100 * i - 2,
                "out_nm": 0 if safe else 100 * i,
                "heartbeat": beat,
                "fault": fault,
            }
        )

    print(
        json.dumps(
            {
                "module": args.module,
                "level": "SIL",
                "cycle_ns": 1_000_000,
                "inject": args.inject,
                "safe_state": safe,
                "fault": fault,
                "pass": safe if args.inject != "none" else fault is None,
                "traces": traces,
                "mock": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
