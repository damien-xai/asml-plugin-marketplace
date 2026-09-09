---
name: asml-opc-job
description: Scaffold a mocked OPC, ILT, or SMO job spec for an ASML computational lithography layer.
---

Load `asml-computational-litho` and `asml-mask-model`.

If the user did not name a layer, method, or tool, default to `M1` / `opc` / `NXE:3800E` and say so.

Write a job spec in the repo's existing config format, or YAML if none exists, using the fields from the computational-litho skill. Enable `mask3d` for EXE / High-NA.

Optionally call the mock MCP `preview_ilt` (ILT) or `get_process_window` (OPC/SMO) and attach the canned result next to the spec. Do not pretend the job ran on a cluster.
