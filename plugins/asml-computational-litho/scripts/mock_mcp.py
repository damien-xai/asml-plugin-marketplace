#!/usr/bin/env python3
"""Mock MCP server for asml-computational-litho. Canned data, no network."""
from __future__ import annotations

import json
import sys

PROTOCOL = "2024-11-05"
SERVER = {"name": "asml-computational-litho", "version": "0.1.0"}

JOBS = [
    {"id": "opc-m1-001", "layer": "M1", "method": "opc", "tool": "NXE:3800E", "status": "converged"},
    {"id": "ilt-via-014", "layer": "VIA1", "method": "ilt", "tool": "EXE:5000", "status": "running"},
    {"id": "smo-m2-003", "layer": "M2", "method": "smo", "tool": "NXE:3800E", "status": "queued"},
]

PROCESS_WINDOW = {
    "layer": "M1",
    "dose_pct": [-5, 0, 5],
    "focus_nm": [-40, 0, 40],
    "epe_nm": [
        [1.8, 1.2, 1.9],
        [1.3, 0.7, 1.4],
        [2.0, 1.4, 2.1],
    ],
    "mock": True,
}

ILT_PREVIEW = {
    "layer": "VIA1",
    "curvilinear": True,
    "iterations": 12,
    "pvband_nm": 1.1,
    "runtime_s": 42,
    "mock": True,
}

TOOLS = [
    {
        "name": "list_opc_jobs",
        "description": "List mocked OPC/ILT/SMO jobs. Optional layer filter (e.g. M1).",
        "inputSchema": {
            "type": "object",
            "properties": {"layer": {"type": "string"}},
        },
    },
    {
        "name": "get_process_window",
        "description": "Return a canned dose/focus EPE process window for a layer.",
        "inputSchema": {
            "type": "object",
            "properties": {"layer": {"type": "string"}},
        },
    },
    {
        "name": "preview_ilt",
        "description": "Return a canned ILT preview (iterations, PV band). Does not run ILT.",
        "inputSchema": {
            "type": "object",
            "properties": {"layer": {"type": "string"}},
        },
    },
]


def handle_tool(name: str, arguments: dict) -> dict:
    if name == "list_opc_jobs":
        layer = (arguments.get("layer") or "").upper()
        jobs = [j for j in JOBS if not layer or j["layer"] == layer]
        return {"jobs": jobs, "mock": True}
    if name == "get_process_window":
        out = dict(PROCESS_WINDOW)
        if arguments.get("layer"):
            out["layer"] = arguments["layer"]
        return out
    if name == "preview_ilt":
        out = dict(ILT_PREVIEW)
        if arguments.get("layer"):
            out["layer"] = arguments["layer"]
        return out
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
    if method == "notifications/initialized" or method == "notifications/cancelled":
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
