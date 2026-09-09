#!/usr/bin/env python3
"""Canned computational-lithography data. No network."""
from __future__ import annotations

import argparse
import json

JOBS = [
    {
        "id": "opc-m1-001",
        "layer": "M1",
        "method": "opc",
        "tool": "NXE:3800E",
        "na": 0.33,
        "status": "converged",
        "epe_nm": 0.7,
        "runtime_s": 18,
    },
    {
        "id": "ilt-via-014",
        "layer": "VIA1",
        "method": "ilt",
        "tool": "EXE:5000",
        "na": 0.55,
        "status": "running",
        "epe_nm": None,
        "runtime_s": 42,
    },
    {
        "id": "smo-m2-003",
        "layer": "M2",
        "method": "smo",
        "tool": "NXE:3800E",
        "na": 0.33,
        "status": "queued",
        "epe_nm": None,
        "runtime_s": 0,
    },
]

WINDOWS = {
    "M1": {
        "dose_pct": [-5, 0, 5],
        "focus_nm": [-40, 0, 40],
        "epe_nm": [[1.8, 1.2, 1.9], [1.3, 0.7, 1.4], [2.0, 1.4, 2.1]],
        "pw_area_nm_pct": 320,
    },
    "VIA1": {
        "dose_pct": [-4, 0, 4],
        "focus_nm": [-30, 0, 30],
        "epe_nm": [[1.6, 1.1, 1.7], [1.2, 0.9, 1.3], [1.8, 1.2, 1.9]],
        "pw_area_nm_pct": 210,
    },
}


def dump(obj: dict) -> None:
    print(json.dumps(obj, indent=2))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    lj = sub.add_parser("list-jobs")
    lj.add_argument("--layer")
    pw = sub.add_parser("process-window")
    pw.add_argument("--layer", default="M1")
    ilt = sub.add_parser("preview-ilt")
    ilt.add_argument("--layer", default="VIA1")
    args = p.parse_args()

    if args.cmd == "list-jobs":
        layer = (args.layer or "").upper()
        jobs = [j for j in JOBS if not layer or j["layer"] == layer]
        dump({"jobs": jobs, "mock": True})
        return
    if args.cmd == "process-window":
        layer = args.layer.upper()
        win = dict(WINDOWS.get(layer, WINDOWS["M1"]))
        dump({"layer": layer, **win, "mock": True})
        return
    dump(
        {
            "layer": args.layer.upper(),
            "curvilinear": True,
            "iterations": 12,
            "pvband_nm": 1.1,
            "runtime_s": 42,
            "mock": True,
        }
    )


if __name__ == "__main__":
    main()
