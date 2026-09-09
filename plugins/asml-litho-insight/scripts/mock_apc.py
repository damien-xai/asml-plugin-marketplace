#!/usr/bin/env python3
"""Apply a mocked lot-to-lot APC step to canned overlay residuals."""
from __future__ import annotations

import argparse
import json

GAIN = 0.7
MAX_STEP = {"Tx_nm": 2.0, "Ty_nm": 2.0, "R_urad": 5.0, "M_ppm": 1.0}
LAST = {"Tx_nm": 0.1, "Ty_nm": -0.05, "R_urad": 0.2, "M_ppm": 0.0}


def clamp(name: str, value: float) -> float:
    cap = MAX_STEP[name]
    return max(-cap, min(cap, value))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lot", default="LOT-7781")
    p.add_argument("--tx", type=float, default=0.41)
    p.add_argument("--ty", type=float, default=-0.19)
    p.add_argument("--quality-fail", action="store_true")
    args = p.parse_args()

    measured = {"Tx_nm": args.tx, "Ty_nm": args.ty, "R_urad": 0.8, "M_ppm": -0.1}
    if args.quality_fail:
        out = {
            "lot_id": args.lot,
            "held": True,
            "reason": "metrology quality fail",
            "knobs_before": LAST,
            "knobs_after": LAST,
            "mock": True,
        }
        print(json.dumps(out, indent=2))
        return

    after = {
        k: round(LAST[k] + clamp(k, GAIN * (measured[k] - LAST[k])), 3) for k in LAST
    }
    print(
        json.dumps(
            {
                "lot_id": args.lot,
                "held": False,
                "gain": GAIN,
                "measured": measured,
                "knobs_before": LAST,
                "knobs_after": after,
                "mock": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
