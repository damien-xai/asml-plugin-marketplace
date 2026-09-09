---
name: asml-metrology
description: >
  Overlay, CD, focus, and edge-placement-error (EPE) analysis for ASML scanners and YieldStar.
  Use when computing residuals, fitting correction models, or turning metrology into scanner
  setpoints. Triggers: /asml-overlay-report, "asml overlay", "asml epe", "asml yieldstar",
  "cd metrology", "focus exposure".
---

# ASML metrology

Mock skill. Use the user's data if present; otherwise the sample wafer in `asml-wafer-maps`.

## Signals

| Signal | Unit | Typical question |
|---|---|---|
| Overlay (OvX, OvY) | nm | How much did layer N miss layer N-1? |
| CD | nm | Is the printed width on target? |
| Focus | nm | Is the wafer in the process window? |
| EPE | nm | Combined overlay + CD/2 placement error |

EPE is the consumer metric for holistic lithography. If the user asks for "patterning error" or "on-product overlay", report overlay and EPE, not CD alone.

## Correction models (overlay)

Fit in this order, stop when residuals meet the user's spec (default 1.0 nm 3σ):

1. Translation (Tx, Ty)
2. Rotation + magnification (R, M)
3. Higher-order scanner-correctable (k-terms the tool can apply)

Do not fit terms the scanner cannot apply. Put leftover systematic as a wafer-map residual, not as an invented k-term.

Fictional recipe payload:

```python
recipe = {
    "tool": "NXE:3800E",
    "layer": "M1",
    "corrections": {"Tx_nm": 0.4, "Ty_nm": -0.2, "R_urad": 0.8, "M_ppm": -0.1},
    "residual_3sigma_nm": {"x": 0.9, "y": 1.1},
    "mock": True,
}
```

## CD / focus

- CD: report mean, 3σ, and a simple dose-to-target if a dose sensitivity (nm/%) is known; otherwise skip the dose suggestion.
- Focus: report mean and a recommended offset only when a focus-exposure matrix exists.

## Coding rules

- Keep field names `ov_x_nm`, `ov_y_nm`, `cd_nm`, `focus_nm`, `epe_nm`. Convert at I/O.
- One wafer = one dataframe (or equivalent) keyed by `field_i`, `field_j`, `target_id`.
- Never drop fields silently; mark them `excluded_reason` if a sample is invalid.
- Load `asml-wafer-maps` before plotting.
