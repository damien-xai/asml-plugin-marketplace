---
name: asml-gem-session
description: Scaffold a mocked SECS/GEM session with equipment status, recipe select, and S2F41 START.
---

Load `asml-fab-integration`.

Scaffold a small host-side adapter (match repo language; Python if none):

1. Session object with GEM state + `EC_CONTROL_STATE`.
2. `PP-SELECT` then `START` remote commands, refusing START without a recipe.
3. A unit test that uses canned MCP responses *or* an in-memory fake — no TCP.

If MCP is available, call `get_equipment_status`, `list_recipes`, and `send_s2f41` with `START` and show the ack. Mark all of it mock.
