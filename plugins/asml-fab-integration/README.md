# asml-fab-integration

Mock Grok Build plugin for **fab host integration** of ASML scanners: SECS/GEM (SEMI E5/E30), GEM300 (E40/E87/E90/E94), and HSMS (E37).

Canned equipment status, recipes, and S2F41 acks come from `scripts/mock_fab.py`. No TCP session is opened.

## Use when

- Implementing recipe download, equipment constants, or remote commands
- Modelling GEM300 carrier / control-job / substrate tracking
- Encoding or decoding a SECS-II message for a mocked scanner

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-fab-integration` | SECS/GEM + GEM300 coding conventions |
| Command | `/asml-gem-session` | Scaffold a mocked GEM session + S2F41 remote command |
| Script | `scripts/mock_fab.py` | Print canned status, recipes, and S2F41 HCACK |

```bash
python3 scripts/mock_fab.py status
python3 scripts/mock_fab.py recipes
python3 scripts/mock_fab.py s2f41 START
python3 scripts/mock_fab.py s2f41 PP-SELECT --ppid VIA1-ENG-002
```

## Languages

Java or C# for the host adapter (match the repo). Python is acceptable for message-level tests.
