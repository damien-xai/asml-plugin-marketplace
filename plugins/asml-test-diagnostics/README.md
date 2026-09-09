# asml-test-diagnostics

Mock Grok Build plugin for **calibration, diagnostics, and hardware-in-the-loop (HIL) / software-in-the-loop (SIL)** testing of ASML scanners.

Python is the usual language for this work (calibration scripts, functional test automation). The plugin never drives real hardware; HIL plans target a local fake plant.

## Use when

- Writing a calibration or diagnostic script
- Planning a HIL/SIL test for a mechatronic module
- Turning a field symptom (overlay drift, focus excursion, abort) into a diagnostic playbook

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-test-diagnostics` | HIL/SIL plans and diagnostic playbooks |
| Skill | `asml-calibration` | Python calibration script conventions |
| Command | `/asml-hil-plan` | Scaffold a HIL/SIL test plan for a named module |

## Related plugins

Control-path C++ stays in `asml-embedded-control`. This plugin owns **off-cycle** Python that measures, adjusts, and tests that C++.
