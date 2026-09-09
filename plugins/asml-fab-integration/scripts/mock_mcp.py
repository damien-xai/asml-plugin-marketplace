#!/usr/bin/env python3
"""Mock MCP server for asml-fab-integration. Canned GEM traffic, no network."""
from __future__ import annotations

import json
import sys

PROTOCOL = "2024-11-05"
SERVER = {"name": "asml-fab-host", "version": "0.1.0"}

STATUS = {
    "tool_id": "NXE3800E-MOCK-01",
    "gem_state": "Idle",
    "control_state": "REMOTE",
    "selected_ppid": "M1-PROD-014",
    "alarms": [],
    "mock": True,
}

RECIPES = [
    {"ppid": "M1-PROD-014", "layer": "M1", "sha16": "a1b2c3d4e5f67890"},
    {"ppid": "VIA1-ENG-002", "layer": "VIA1", "sha16": "1111222233334444"},
    {"ppid": "M2-PROD-009", "layer": "M2", "sha16": "abcdabcdabcdabcd"},
]

ALLOWED_RCMD = {"START", "PAUSE", "RESUME", "ABORT", "PP-SELECT"}

TOOLS = [
    {
        "name": "get_equipment_status",
        "description": "Return mocked GEM state, control state, selected recipe, and alarms.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_recipes",
        "description": "List mocked process programs (PPID + layer + hash). No recipe bodies.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "send_s2f41",
        "description": "Pretend to send S2F41. Returns a canned S2F42 HCACK. Does not talk to a tool.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rcmd": {"type": "string", "description": "START, PAUSE, RESUME, ABORT, PP-SELECT"},
                "ppid": {"type": "string", "description": "Required for PP-SELECT"},
            },
            "required": ["rcmd"],
        },
    },
]


def send_s2f41(arguments: dict) -> dict:
    rcmd = str(arguments.get("rcmd") or "").upper()
    if rcmd not in ALLOWED_RCMD:
        return {"hcack": 1, "reason": f"unknown RCMD {rcmd}", "mock": True}
    if rcmd == "PP-SELECT":
        ppid = arguments.get("ppid")
        known = {r["ppid"] for r in RECIPES}
        if ppid not in known:
            return {"hcack": 3, "reason": "PPID not found", "mock": True}
        return {"hcack": 0, "selected_ppid": ppid, "mock": True}
    if rcmd == "START" and not STATUS.get("selected_ppid"):
        return {"hcack": 2, "reason": "no recipe selected", "mock": True}
    return {
        "hcack": 0,
        "rcmd": rcmd,
        "gem_state": "Processing" if rcmd == "START" else STATUS["gem_state"],
        "mock": True,
    }


def handle_tool(name: str, arguments: dict) -> dict:
    if name == "get_equipment_status":
        return dict(STATUS)
    if name == "list_recipes":
        return {"recipes": RECIPES, "mock": True}
    if name == "send_s2f41":
        return send_s2f41(arguments)
    raise ValueError(f"unknown tool: {name}")


def read_message():
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("utf-8").partition(":")
        headers[key.strip().lower()] = value.strip()
    n = int(headers.get("content-length", "0"))
    if n <= 0:
        return None
    return json.loads(sys.stdin.buffer.read(n))


def write_message(msg: dict) -> None:
    body = json.dumps(msg).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def ok(id_, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def err(id_, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def dispatch(msg: dict) -> dict | None:
    method = msg.get("method")
    id_ = msg.get("id")
    params = msg.get("params") or {}
    if method == "initialize":
        return ok(
            id_,
            {
                "protocolVersion": PROTOCOL,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER,
            },
        )
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return ok(id_, {})
    if method == "tools/list":
        return ok(id_, {"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            result = handle_tool(name, arguments)
        except ValueError as e:
            return err(id_, -32601, str(e))
        return ok(
            id_,
            {"content": [{"type": "text", "text": json.dumps(result)}], "isError": False},
        )
    if id_ is None:
        return None
    return err(id_, -32601, f"unknown method: {method}")


def main() -> None:
    while True:
        msg = read_message()
        if msg is None:
            return
        reply = dispatch(msg)
        if reply is not None:
            write_message(reply)


if __name__ == "__main__":
    main()
