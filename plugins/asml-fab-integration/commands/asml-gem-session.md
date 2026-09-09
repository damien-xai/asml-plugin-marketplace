---
name: asml-gem-session
description: Scaffold a mocked SECS/GEM session with equipment status, recipe select, and S2F41 START.
---

Load `asml-fab-integration`.

Scaffold a small host-side adapter (match repo language; Python if none):

1. Session object with GEM state + `EC_CONTROL_STATE`.
2. `PP-SELECT` then `START` remote commands, refusing START without a recipe.
3. A unit test that uses an in-memory fake — no TCP.

Run `python3 scripts/mock_fab.py status`, `recipes`, and `s2f41 START` from this plugin's root and show the HCACK. Mark all of it mock.
