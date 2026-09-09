---
name: asml-litho-insight
description: >
  Holistic lithography APC in the Litho InSight style — lot-to-lot and wafer-to-wafer
  control from metrology feedback into scanner setpoints. Use when designing process-control
  loops, control recipes, or Java/Python apps that consume YieldStar data. Triggers:
  /asml-apc-recipe, "asml litho insight", "asml apc", "holistic lithography",
  "lot to lot control", "process control".
---

# ASML Litho InSight (APC)

Mock skill. Recipes are never sent to a scanner.

## Loop types

| Loop | Cadence | Use |
|---|---|---|
| Lot-to-lot | After each lot's metrology | Overlay k-terms, dose, focus offsets |
| Wafer-to-wafer | After selected wafers | Fast drift (focus, translation) |
| Feed-forward | From previous layer's map | Overlay matching to a known fingerprint |

Default to **lot-to-lot**. Add wafer-to-wafer only if the user names drift within a lot. Feed-forward needs a previous-layer map; do not invent one.

## Knobs

Only these scanner-correctable knobs (names are mock):

- Overlay: `Tx_nm`, `Ty_nm`, `R_urad`, `M_ppm`
- Dose: `dose_offset_pct`
- Focus: `focus_offset_nm`

If the residual is not spannable by those knobs, say so and leave it as a wafer-map residual. Do not invent higher-order terms here — that is a metrology-model change (`asml-metrology`).

## Gain and guards

```yaml
loop: lot-to-lot
layer: M1
inputs: [overlay, epe]
knobs: [Tx_nm, Ty_nm, R_urad, M_ppm]
gain: 0.7                 # < 1 to avoid overshoot
max_step:
  Tx_nm: 2.0
  Ty_nm: 2.0
  R_urad: 5.0
  M_ppm: 1.0
hold_on_quality_fail: true
mock: true
```

- Gain 0.7 unless the user specifies.
- Clamp every step to `max_step`.
- If metrology quality flags fail (too few points, 3σ exploded), **hold last recipe**. Never update on a bad lot.

## Application structure

Customer-facing code is typically Java; prototypes may be Python.

- `Ingest` — metrology lot files (read-only)
- `Estimate` — call the overlay/CD fit; do not reimplement it
- `Control` — apply gain, clamps, hold policy
- `Publish` — write a recipe artifact + an audit log (lot id, knobs before/after, residual)

Persist the last-applied recipe next to the audit log so a hold is deterministic after restart.
