---
name: asml-hil-plan
description: Scaffold a SIL/HIL test plan and a pytest fake-plant test for an ASML scanner module.
---

Load `asml-test-diagnostics`. If the module is a control axis, also load `asml-embedded-control` and `asml-motion-safety`. If the work is a calibration script, load `asml-calibration` instead of inventing servo tests.

Default to SIL with a fake plant. Name the module (ask if missing).

Emit:

1. A test-plan markdown section: stimulus, expect, abort cases, traces.
2. A `pytest` file that advances simulated `t_ns` (no `sleep`) and asserts safe state on injected faults.
3. A JSON sidecar path for traces.

Mark the plant as mock. Do not add a network or vendor-tool client.
