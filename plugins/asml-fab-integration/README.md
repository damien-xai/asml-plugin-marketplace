# asml-fab-integration

Mock Grok Build plugin for **fab host integration** of ASML scanners: SECS/GEM (SEMI E5/E30), GEM300 (E40/E87/E90/E94), and HSMS (E37).

The MCP server is a local stdio stub. It does not open a TCP session to a tool or fab host.

## Use when

- Implementing recipe download, equipment constants, or remote commands
- Modelling GEM300 carrier / control-job / substrate tracking
- Encoding or decoding a SECS-II message for a mocked scanner

## Components

| Kind | Name | Purpose |
|---|---|---|
| Skill | `asml-fab-integration` | SECS/GEM + GEM300 coding conventions |
| Command | `/asml-gem-session` | Scaffold a mocked GEM session + S2F41 remote command |
| MCP | `asml-fab-host` | Canned `get_equipment_status`, `list_recipes`, `send_s2f41` |

## Languages

Java or C# for the host adapter (match the repo). Python is acceptable for message-level tests.
