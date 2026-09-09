"""In-memory fake — no TCP."""

from __future__ import annotations

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "gem_session",
    Path(__file__).resolve().parents[1] / "scripts" / "gem_session.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GemSession = mod.GemSession


def test_start_refused_without_recipe() -> None:
    s = GemSession()
    ack = s.s2f41("START")
    assert ack["hcack"] == 2
    assert ack["reason"] == "no recipe selected"
    assert s.gem_state == "Idle"


def test_pp_select_then_start() -> None:
    s = GemSession()
    sel = s.s2f41("PP-SELECT", "M1-PROD-014")
    assert sel["hcack"] == 0
    assert sel["sha16"] == "a1b2c3d4e5f67890"
    assert s.gem_state == "Setup"
    start = s.s2f41("START")
    assert start["hcack"] == 0
    assert start["gem_state"] == "Processing"


def test_unknown_ppid() -> None:
    s = GemSession()
    ack = s.s2f41("PP-SELECT", "NO-SUCH")
    assert ack["hcack"] == 3


if __name__ == "__main__":
    test_start_refused_without_recipe()
    test_pp_select_then_start()
    test_unknown_ppid()
    print("ok gem_session")
