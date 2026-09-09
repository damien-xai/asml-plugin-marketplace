# asml-metrology

Mock Grok Build plugin for **scanner and YieldStar metrology**: overlay, critical dimension (CD), focus, and edge-placement error (EPE).

No live YieldStar or scanner connection. Wafer maps and correction recipes in the skills are examples.

## Use when

- Analyzing overlay, CD, focus, or EPE data
- Building a wafer-map plot or a scanner correction recipe
- Translating metrology residuals into stage or dose/focus offsets

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-metrology` | Overlay / CD / focus / EPE analysis and correction recipes |
| Skill | `asml-wafer-maps` | Wafer-map layout, sampling, and plotting conventions |
| Command | `/asml-overlay-report` | Build a mocked overlay/EPE report plus correction suggestion |
| Script | `scripts/mock_overlay.py` | Print a canned wafer + scanner-correctable recipe |

```bash
python3 scripts/mock_overlay.py --layer M1
```

## Languages

Python (NumPy / pandas) for analysis. C++ only if the repo already computes residuals on the scanner.
