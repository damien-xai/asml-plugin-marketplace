---
name: asml-wafer-maps
description: >
  Wafer-map layout, sampling, and plotting conventions for ASML metrology.
  Use when drawing an overlay/CD/focus/EPE map, choosing sample targets, or
  converting field indices to wafer coordinates. Triggers: "wafer map",
  "field map", "asml sampling", "shot map".
---

# Wafer maps

Mock skill.

## Coordinates

- Origin at wafer center. +X to the right, +Y up, millimetres on the wafer, nanometres on the error.
- Fields are a regular grid (`field_i`, `field_j`) plus intra-field `(dx_mm, dy_mm)`.
- Do not rotate the map to "look like the notch" unless the user asks; put the notch at −Y and label it.

## Sampling

If the user does not specify a scheme:

- 5-point intra-field (center + four corners) on a sparse field grid (every other field) for a first overlay look.
- Full-wafer dense (all fields, 1-point) for a fingerprint / process-control map.

Never interpolate across the wafer edge. Mask points with `x^2 + y^2 > (R - margin)^2`. Default `R = 150` mm (300 mm wafer), `margin = 3` mm.

## Plot

One figure, one signal. Diverging colormap centered at 0 for overlay/EPE, sequential for CD. Colorbar in nm. Title: `{signal} · {layer} · {wafer_id}`. If data is mocked, the title includes `(mock)`.
