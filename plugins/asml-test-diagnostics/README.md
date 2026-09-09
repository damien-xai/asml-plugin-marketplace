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
| Script | `scripts/mock_hil.py` | Run a canned SIL loop against a fake plant |
| Script | `scripts/cal_stage_x.py` | Off-cycle stage-X cal: measure → fit → sidecar JSON |

```bash
python3 scripts/mock_hil.py --module wafer-stage-x --inject missed-heartbeat
python3 scripts/cal_stage_x.py                  # measure + fit only
python3 scripts/cal_stage_x.py --apply          # also write the fake cal slot
```

## Related plugins

Control-path C++ stays in `asml-embedded-control`. This plugin owns **off-cycle** Python that measures, adjusts, and tests that C++.
