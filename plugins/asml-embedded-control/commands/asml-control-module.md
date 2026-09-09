---
name: asml-control-module
description: Scaffold a TWINSCAN mechatronic control module (sense, estimate, control, actuate) in C++.
---

Load the `asml-embedded-control` and `asml-motion-safety` skills.

Ask for the axis/module name if missing (e.g. wafer-stage X, reticle-stage Y, wafer-handler). Then scaffold:

1. A header with `asml::mc` POD `Sample` / `Setpoint` and a `Stage`-like device interface.
2. Four functions: `sense`, `estimate`, `control`, `actuate`, plus `init` / `heartbeat`.
3. Travel-limit clamp and sticky-fault handling in `actuate`.
4. A unit test that runs one 1 ms cycle with a fake device (no hardware).

Match the surrounding repo's build system. If none exists, emit a single `.hpp` / `.cpp` / `_test.cpp` trio. Mark types as mock.
