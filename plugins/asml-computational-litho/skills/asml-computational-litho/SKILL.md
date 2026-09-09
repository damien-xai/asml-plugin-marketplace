---
name: asml-computational-litho
description: >
  OPC, inverse lithography (ILT), and source-mask optimization (SMO) job setup for ASML
  computational lithography. Use when correcting a mask, running ILT, optimizing the
  illuminator, or estimating a process window. Triggers: /asml-opc-job, "asml opc",
  "asml ilt", "asml smo", "computational lithography", "tachyon", "process window".
---

# ASML computational lithography

Mock skill. Job specs and `scripts/mock_litho.py` return canned data. Do not claim a real mask was corrected.

## Pick a method

| Method | Use when | Cost |
|---|---|---|
| Rule / model-based OPC | Mature node, Manhattan-ish metal, fast turnaround | Low |
| ILT | Tight pitches, curvilinear masks, High-NA EXE layers | High |
| SMO | Illuminator + mask must move together (new source, new NA) | High |

Default: model-based OPC. Switch to ILT only if the user names curvilinear, High-NA, or a process window that OPC already failed.

## Job spec

Write a YAML (or the repo's existing format) with these fields and no others on first scaffold:

```yaml
# mock OPC job — not submitted anywhere
layer: M1
tool: NXE:3800E          # or EXE:5000 for High-NA
na: 0.33                 # 0.55 for EXE
method: opc              # opc | ilt | smo
pixel_nm: 1.0
mask3d: true
resist: compact          # compact | calibrated
pw:
  dose_pct: [-5, 0, 5]
  focus_nm: [-40, 0, 40]
```

Load `asml-mask-model` before changing `mask3d` or `resist`.

## Coding rules

- Kernels stay in C++/CUDA. Python only orchestrates jobs, I/O, and plots.
- Tile the mask. Never hold a full-reticle aerial image in one process if a tiled API exists.
- Seed RNG and record `tool`, `na`, `method`, and model hashes in the result sidecar.
- Treat dose as percent from nominal and focus in nm. Overlay belongs in the process-window consumer, not inside the OPC kernel.

## Canned data

From this plugin's root (parent of `skills/`), run:

```bash
python3 scripts/mock_litho.py list-jobs --layer M1
python3 scripts/mock_litho.py process-window --layer M1
python3 scripts/mock_litho.py preview-ilt --layer VIA1
```

Use that JSON. Do not invent live cluster output.
