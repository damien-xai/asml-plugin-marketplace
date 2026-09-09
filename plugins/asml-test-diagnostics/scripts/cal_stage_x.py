#!/usr/bin/env python3
"""Off-cycle wafer-stage X calibration against a fake device. No servo, no tool."""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from pathlib import Path

AXIS = "stage_x"
SPEC_3SIGMA_NM = 2.0
TRAVEL_LIMIT_NM = 150_000_000  # software stop; this script never changes it


class FakeStage:
    """Stand-in for the off-cycle diagnostics API. No actuate()."""

    def __init__(self, seed: int = 7) -> None:
        self._rng = random.Random(seed)
        self.true_offset_nm = 1.15
        self.true_gain = 0.997
        self.cal_slot = {"offset_nm": 0.0, "gain": 1.0}
        self.travel_limit_nm = TRAVEL_LIMIT_NM

    def sample_encoder_nm(self, commanded_nm: float) -> tuple[int, float]:
        t_ns = time.time_ns()
        noise = self._rng.gauss(0.0, 0.12)
        encoded = self.true_offset_nm + self.true_gain * commanded_nm + noise
        return t_ns, encoded

    def write_cal_slot(self, knobs: dict) -> None:
        self.cal_slot = {
            "offset_nm": float(knobs["offset_nm"]),
            "gain": float(knobs["gain"]),
        }


def measure(device: FakeStage, n: int = 32) -> list[dict]:
    """Take n off-cycle samples. May block; this is not the servo."""
    span_nm = 50_000.0
    samples = []
    for i in range(n):
        cmd = -span_nm + (2 * span_nm) * (i / max(n - 1, 1))
        t_ns, enc = device.sample_encoder_nm(cmd)
        samples.append(
            {
                "t_ns": t_ns,
                "commanded_nm": round(cmd, 3),
                "encoder_nm": round(enc, 4),
            }
        )
    return samples


def fit(samples: list[dict]) -> dict:
    """Least-squares encoder ≈ offset + gain * commanded."""
    n = len(samples)
    sx = sum(s["commanded_nm"] for s in samples)
    sy = sum(s["encoder_nm"] for s in samples)
    sxx = sum(s["commanded_nm"] ** 2 for s in samples)
    sxy = sum(s["commanded_nm"] * s["encoder_nm"] for s in samples)
    denom = n * sxx - sx * sx
    gain = (n * sxy - sx * sy) / denom
    offset = (sy - gain * sx) / n
    residuals = [
        s["encoder_nm"] - (offset + gain * s["commanded_nm"]) for s in samples
    ]
    mean = sum(residuals) / n
    var = sum((r - mean) ** 2 for r in residuals) / n
    residual_3sigma_nm = 3.0 * math.sqrt(var)
    return {
        "offset_nm": round(offset, 4),
        "gain": round(gain, 6),
        "residual_3sigma_nm": round(residual_3sigma_nm, 4),
        "n": n,
        "spec_3sigma_nm": SPEC_3SIGMA_NM,
        "travel_limit_nm": TRAVEL_LIMIT_NM,
    }


def apply(device: FakeStage, knobs: dict) -> None:
    """Write knobs to the device's calibration slot. Never to the servo loop."""
    device.write_cal_slot(knobs)


def write_sidecar(path: Path, samples: list[dict], knobs: dict) -> None:
    payload = {
        "axis": AXIS,
        "mock": True,
        "knobs": {
            "offset_nm": knobs["offset_nm"],
            "gain": knobs["gain"],
            "t_ns": samples[-1]["t_ns"] if samples else 0,
        },
        "fit": knobs,
        "samples": samples,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true", help="Write cal slot (opt-in)")
    p.add_argument("--n", type=int, default=32)
    p.add_argument("--out-dir", type=Path, default=Path("."))
    args = p.parse_args()

    device = FakeStage()
    samples = measure(device, n=args.n)
    knobs = fit(samples)

    ts = time.strftime("%Y%m%dT%H%M%S")
    sidecar = args.out_dir / f"cal_{AXIS}_{ts}.json"
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_sidecar(sidecar, samples, knobs)

    print(json.dumps({"sidecar": str(sidecar), "fit": knobs, "applied": False}, indent=2))

    if knobs["residual_3sigma_nm"] > SPEC_3SIGMA_NM:
        print(
            f"residual {knobs['residual_3sigma_nm']} nm 3σ exceeds spec "
            f"{SPEC_3SIGMA_NM} nm — not applying",
            file=sys.stderr,
        )
        return 1

    if not args.apply:
        return 0

    apply(device, knobs)
    print(
        json.dumps(
            {"applied": True, "cal_slot": device.cal_slot, "travel_limit_nm": device.travel_limit_nm},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
