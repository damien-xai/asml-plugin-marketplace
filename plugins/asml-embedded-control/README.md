# asml-embedded-control

Mock Grok Build plugin for **real-time C++ machine control** on ASML TWINSCAN NXE (Low-NA EUV) and EXE (High-NA EUV) scanners.

This plugin does **not** talk to a scanner. Types, cycle budgets, and module names are fictional stand-ins for the kinds of work ASML embedded teams do: motion control, mechatronics coordination, and safety interlocks.

## Use when

- Writing or reviewing C++ that runs on a 1 ms (or tighter) control cycle
- Scaffolding a sensor → estimator → controller → actuator module
- Checking a change for heap, locks, logging, or blocking I/O on the hot path

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-embedded-control` | Real-time C++ conventions for scanner control |
| Skill | `asml-motion-safety` | Watchdogs, interlocks, and fail-safe actuator commands |
| Command | `/asml-control-module` | Scaffold a mechatronic control module |
| Agent | `asml-rt-reviewer` | Review a diff for real-time violations |
| Script | `scripts/mock_cycle.py` | Print one mocked 1 ms cycle (optional injected fault) |

```bash
python3 scripts/mock_cycle.py
python3 scripts/mock_cycle.py --inject-fault missed-heartbeat
clang++ -std=c++17 -o /tmp/wafer_stage_x_test src/wafer_stage_x.cpp src/wafer_stage_x_test.cpp && /tmp/wafer_stage_x_test
```

## Languages

C++17 (hot path), C for drivers, Python only in off-cycle diagnostics — use `asml-test-diagnostics` for that.
