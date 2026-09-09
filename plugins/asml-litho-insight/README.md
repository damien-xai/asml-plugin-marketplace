# asml-litho-insight

Mock Grok Build plugin for **holistic lithography application software** — Litho InSight-style advanced process control (APC). Turns YieldStar / scanner metrology into lot-to-lot and wafer-to-wafer setpoint updates.

Java is the usual customer-facing stack for this class of app at ASML; Python is fine for prototypes. Nothing here talks to a live Litho InSight deployment.

## Use when

- Designing an APC feedback or feed-forward loop
- Mapping metrology residuals onto scanner knobs (overlay k-terms, dose, focus)
- Building a lot-level control recipe from mocked data

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-litho-insight` | APC loop design, knobs, and application structure |
| Command | `/asml-apc-recipe` | Scaffold a lot-to-lot control recipe |
| Agent | `asml-apc-designer` | Propose a control loop from a stated patterning problem |

## Related plugins

Metrology math lives in `asml-metrology`. This plugin owns the **control application** (when to update, which knobs, how to persist a recipe).
