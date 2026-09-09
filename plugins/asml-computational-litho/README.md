# asml-computational-litho

Mock Grok Build plugin for **computational lithography**: optical proximity correction (OPC), inverse lithography technology (ILT), and source-mask optimization (SMO).

Canned job, process-window, and ILT data come from `scripts/mock_litho.py`. Nothing is submitted to a compute cluster.

## Use when

- Setting up or reviewing an OPC / ILT / SMO job
- Choosing a resist or mask-3D model fidelity vs. runtime tradeoff
- Interpreting a mocked process window (dose, focus, overlay)

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-computational-litho` | OPC / ILT / SMO job setup and HPC patterns |
| Skill | `asml-mask-model` | Mask-3D and resist-model fidelity choices |
| Command | `/asml-opc-job` | Scaffold a mocked OPC/ILT job spec |
| Script | `scripts/mock_litho.py` | Print canned jobs, process windows, ILT previews |

```bash
python3 scripts/mock_litho.py list-jobs --layer M1
python3 scripts/mock_litho.py process-window --layer M1
python3 scripts/mock_litho.py preview-ilt --layer VIA1
```

## Languages

Python for job orchestration, C++/CUDA for kernels. Prefer the existing solver entrypoints in the repo; do not rewrite a lithography simulator from scratch.
