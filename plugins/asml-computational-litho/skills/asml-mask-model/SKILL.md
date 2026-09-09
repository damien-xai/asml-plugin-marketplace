---
name: asml-mask-model
description: >
  Choose mask-3D and resist-model fidelity for ASML computational lithography jobs.
  Use when setting mask3d, resist compact vs calibrated, or trading runtime against
  EPE accuracy. Triggers: "mask 3d", "resist model", "mask3d", "aerial image model".
---

# Mask and resist models

Mock skill. Model names are stand-ins.

## Fidelity ladder

| Knob | Fast (setup / screening) | Production-ish |
|---|---|---|
| Mask | Thin-mask Kirchhoff | Mask-3D (enable `mask3d: true`) |
| Resist | Compact (threshold + blur) | Calibrated compact or full resist |
| Source | Top-hat / measured pupil | Measured pupil + polarization |

High-NA EXE (`na: 0.55`) always enables mask-3D. NXE Low-NA may skip it for a first OPC screening if the user asks for speed.

## What to change together

- Turning on mask-3D without a measured pupil is wasted cost — flag it.
- Calibrated resist without a focus-exposure matrix in the job spec is incomplete — require `pw.focus_nm` and `pw.dose_pct`.
- Do not retune resist parameters to hide an OPC failure. Fix the mask correction first.

## Output

When asked to pick models, answer with the YAML knobs (`mask3d`, `resist`, `na`) and one sentence on why. Do not paste a simulator derivation.
