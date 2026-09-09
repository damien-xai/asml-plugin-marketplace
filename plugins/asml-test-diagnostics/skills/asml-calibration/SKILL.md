---
name: asml-calibration
description: >
  Python calibration-script conventions for ASML scanners (stage, overlay, focus, dose).
  Use when writing or reviewing off-cycle calibration, gain tuning, or diagnostic
  measurement scripts. Triggers: "asml calibration", "cal script", "gain tune",
  "encoder cal", "dose cal".
---

# ASML calibration scripts

Mock skill. Scripts read/write files and a fake device API, not a live tool.

## Script shape

```python
# cal_stage_x.py — mock
def measure(device, n: int = 32) -> list[float]:
    """Take n off-cycle samples. May block; this is not the servo."""

def fit(samples: list[float]) -> dict:
    """Return JSON-serializable knobs, e.g. {'offset_nm': 1.2, 'gain': 0.998}."""

def apply(device, knobs: dict) -> None:
    """Write knobs to the device's calibration slot. Never to the servo loop directly."""

def main() -> None:
    # measure → fit → write sidecar JSON → apply only with --apply
    ...
```

`--apply` is opt-in. Default is measure + fit + write `cal_<axis>_<timestamp>.json`.

The plugin ships `scripts/cal_stage_x.py` as the wafer-stage X mock. Run it from this plugin's root:

```bash
python3 scripts/cal_stage_x.py
python3 scripts/cal_stage_x.py --apply
```

## Rules

- Off-cycle only. Do not call `actuate()` on the inner servo from a cal script.
- Persist raw samples next to the knobs so a fit can be replayed.
- Units in the JSON: `offset_nm`, `gain` (dimensionless), `t_ns`.
- If a fit residual exceeds the module's cal spec (ask; default 2 nm 3σ for stage), **do not apply**. Exit non-zero.
- Load `asml-motion-safety` mentally: a calibration must not widen travel limits.
