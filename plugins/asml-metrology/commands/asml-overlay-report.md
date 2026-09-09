---
name: asml-overlay-report
description: Build a mocked overlay/EPE wafer-map report and a scanner-correctable recipe.
---

Load `asml-metrology` and `asml-wafer-maps`.

1. Use the user's overlay table if they provided one. Otherwise run `python3 scripts/mock_overlay.py` from this plugin's root and use that wafer.
2. Fit translation, rotation, magnification. Report residual 3σ.
3. Emit the fictional recipe payload from the metrology skill.
4. Plot OvX, OvY, and EPE (if CD is available; else skip EPE) as wafer maps.

Do not claim the recipe was sent to a scanner.
