---
name: asml-apc-recipe
description: Scaffold a lot-to-lot holistic lithography APC recipe (knobs, gain, hold policy).
---

Load `asml-litho-insight`. If overlay fitting is required, also load `asml-metrology`.

Ask for layer and loop type only if missing; default `M1` / lot-to-lot.

Emit:

1. The YAML control recipe from the skill (gain 0.7, max steps, hold-on-quality-fail).
2. A small `Control` function (Java if the repo is Java, else Python) that applies gain + clamps + hold.
3. An audit-log record shape: `lot_id`, `knobs_before`, `knobs_after`, `residual_3sigma_nm`, `held`.

Run `python3 scripts/mock_apc.py --lot LOT-7781` from this plugin's root and attach the canned before/after knobs. Mark everything mock. Do not add a network client to a scanner or Litho InSight service.
