---
name: asml-fab-integration
description: >
  SECS/GEM, GEM300, and HSMS integration for ASML scanners talking to a fab host.
  Use when building recipe download, equipment-constant, alarm, or carrier/control-job
  flows. Triggers: /asml-gem-session, "asml secs gem", "asml gem300", "asml hsms",
  "s2f41", "recipe download", "fab host".
---

# ASML fab integration (SECS/GEM)

Mock skill. Message examples are legal SECS-II shapes with fictional bodies. No TCP.

## Stack

| Layer | SEMI | Role |
|---|---|---|
| HSMS | E37 | Session over TCP (mocked; do not open a real port unless the user runs a local simulator) |
| SECS-II | E5 | Messages (`S*F*`) |
| GEM | E30 | Equipment model: state, recipes, alarms, events |
| GEM300 | E40/E87/E90/E94 | Process jobs, carriers, substrate tracking, control jobs |

Talk GEM300 for 300 mm. Do not invent a custom XML job API if a GEM300 object already covers it.

## Scanner GEM state

Idle → Setup → Processing → Completing → Idle.

Remote commands (S2F41) that this mock understands:

| RCMD | Meaning |
|---|---|
| `START` | Start the loaded recipe / process job |
| `PAUSE` | Pause processing |
| `RESUME` | Resume |
| `ABORT` | Abort to idle (safe) |
| `PP-SELECT` | Select a process program (recipe) by name |

Refuse `START` unless state is Idle or Setup and a recipe is selected. Return a mocked S2F42 with `HCACK != 0` and a reason string.

## Recipes

Recipes are named process programs (`PPID`). Download is S7F1/F3-style (or the repo's existing wrapper). Treat recipe bodies as opaque bytes. Never log a full recipe body; log `PPID` + hash.

Equipment constants (ECs) that code may read:

- `EC_WAFER_SIZE_MM` (200/300)
- `EC_TOOL_ID`
- `EC_CONTROL_STATE` (`OFFLINE` / `LOCAL` / `REMOTE`)

Do not add new ECs without naming them in the equipment model first.

## Coding rules

- One outstanding primary message at a time per session. No pipelining unless the existing stack already supports it.
- Timeouts are explicit (default 45 s T3). Never block a UI thread on HSMS.
- Alarms are events + a sticky list. Clearing an alarm is a separate operator/host action.
- Use the mock MCP (`get_equipment_status`, `list_recipes`, `send_s2f41`) for canned traffic.

## Sample S2F41

```
S2F41 W
  <L
    <A 'START'>
    <L>
  >
```

Expected mock ack: `HCACK=0` when status is `REMOTE` + recipe selected, else `HCACK=2`.
