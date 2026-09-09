#!/usr/bin/env python3
"""Canned overlay wafer + scanner-correctable recipe. No YieldStar."""
from __future__ import annotations

import argparse
import json
import math

R_MM = 147.0


def fields() -> list[dict]:
    rows = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            x = i * 26.0
            y = j * 33.0
            if x * x + y * y > R_MM * R_MM:
                continue
            # translation + rotation + mild edge fingerprint
            ovx = 0.4 + (-0.8e-3) * y + 0.004 * (x / 150.0) ** 2 * x
            ovy = -0.2 + (0.8e-3) * x + 0.003 * (y / 150.0) ** 2 * y
            rows.append(
                {
                    "field_i": i,
                    "field_j": j,
                    "x_mm": round(x, 2),
                    "y_mm": round(y, 2),
                    "ov_x_nm": round(ovx, 3),
                    "ov_y_nm": round(ovy, 3),
                    "epe_nm": round(math.hypot(ovx, ovy), 3),
                }
            )
    return rows


def fit(rows: list[dict]) -> dict:
    n = len(rows)
    tx = sum(r["ov_x_nm"] for r in rows) / n
    ty = sum(r["ov_y_nm"] for r in rows) / n
    r_urad = 0.8
    m_ppm = -0.1
    rx = [r["ov_x_nm"] - tx for r in rows]
    ry = [r["ov_y_nm"] - ty for r in rows]

    def sigma3(vals: list[float]) -> float:
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        return 3.0 * math.sqrt(var)

    return {
        "tool": "NXE:3800E",
        "layer": "M1",
        "n_fields": n,
        "corrections": {
            "Tx_nm": round(tx, 3),
            "Ty_nm": round(ty, 3),
            "R_urad": r_urad,
            "M_ppm": m_ppm,
        },
        "residual_3sigma_nm": {"x": round(sigma3(rx), 3), "y": round(sigma3(ry), 3)},
        "mock": True,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--layer", default="M1")
    args = p.parse_args()
    rows = fields()
    recipe = fit(rows)
    recipe["layer"] = args.layer
    print(json.dumps({"wafer_id": "MOCK-W-014", "fields": rows, "recipe": recipe}, indent=2))


if __name__ == "__main__":
    main()
