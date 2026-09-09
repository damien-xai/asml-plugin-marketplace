#!/usr/bin/env python3
"""Canned SECS/GEM fab-host traffic. No TCP, no tool."""
from __future__ import annotations

import argparse
import json

STATUS = {
    "tool_id": "NXE3800E-MOCK-01",
    "gem_state": "Idle",
    "control_state": "REMOTE",
    "selected_ppid": "M1-PROD-014",
    "wafer_size_mm": 300,
    "alarms": [],
    "mock": True,
}

RECIPES = [
    {"ppid": "M1-PROD-014", "layer": "M1", "sha16": "a1b2c3d4e5f67890"},
    {"ppid": "VIA1-ENG-002", "layer": "VIA1", "sha16": "1111222233334444"},
    {"ppid": "M2-PROD-009", "layer": "M2", "sha16": "abcdabcdabcdabcd"},
]

ALLOWED = {"START", "PAUSE", "RESUME", "ABORT", "PP-SELECT"}


def dump(obj: dict) -> None:
    print(json.dumps(obj, indent=2))


def s2f41(rcmd: str, ppid: str | None) -> dict:
    rcmd = rcmd.upper()
    if rcmd not in ALLOWED:
        return {"hcack": 1, "reason": f"unknown RCMD {rcmd}", "mock": True}
    if rcmd == "PP-SELECT":
        known = {r["ppid"] for r in RECIPES}
        if ppid not in known:
            return {"hcack": 3, "reason": "PPID not found", "mock": True}
        return {"hcack": 0, "selected_ppid": ppid, "mock": True}
    if rcmd == "START" and not STATUS.get("selected_ppid"):
        return {"hcack": 2, "reason": "no recipe selected", "mock": True}
    gem = "Processing" if rcmd == "START" else STATUS["gem_state"]
    if rcmd in {"ABORT"}:
        gem = "Idle"
    return {"hcack": 0, "rcmd": rcmd, "gem_state": gem, "mock": True}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("recipes")
    s2 = sub.add_parser("s2f41")
    s2.add_argument("rcmd")
    s2.add_argument("--ppid")
    args = p.parse_args()
    if args.cmd == "status":
        dump(STATUS)
    elif args.cmd == "recipes":
        dump({"recipes": RECIPES, "mock": True})
    else:
        dump(s2f41(args.rcmd, args.ppid))


if __name__ == "__main__":
    main()
