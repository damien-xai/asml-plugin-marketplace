# SIL plan — wafer-stage X (mock plant)

- **Level:** SIL (no hardware rig named)
- **Module:** wafer-stage X
- **Cycle:** 1 ms (1_000_000 ns). Advance `t_ns += cycle_ns`. No `sleep`.
- **Safe state:** hold last-good position, force 0 (horizontal axis). Sticky fault; supervisory `reset()` only.

## Stimulus

| Cycle | `t_ns` | `cmd_nm` | Inject |
|---|---|---|---|
| 1–4 | 1–4 ms | 0, 100, 200, 300 | none |
| 5 | 5 ms | 400 | missed heartbeat |
| 6–8 | 6–8 ms | 500, 600, 700 | none (fault stays sticky) |

Also run as abort cases (separate executions): `travel-limit` (cmd beyond ±150 mm), `driver-error`.

## Expect

| Case | Expect |
|---|---|
| healthy 1–4 | `out_nm` tracks `cmd_nm` ± 0 nm in this mock; `fault` null |
| missed heartbeat at 5 ms | `heartbeat=0`, `fault=missed_heartbeat`, `safe_state=true` |
| cycles 6–8 | `out_nm` frozen (not tracking cmd); fault still `missed_heartbeat` |
| driver-error | sticky `driver_error`, safe-state write |
| travel-limit | sticky `travel_limit`, clamp/hold, do not raise the limit |

## Collect

Trace fields: `t_ns`, `cmd_nm`, `est_nm`, `out_nm`, `heartbeat`, `fault`.

Sidecar: `tests/traces/wafer_stage_x_sil.json` (written by the pytest).

Last step: `pytest` against the fake plant. No “run on tool”.
