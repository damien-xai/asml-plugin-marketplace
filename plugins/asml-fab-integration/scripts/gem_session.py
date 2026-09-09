"""In-memory GEM host adapter. Mock — no TCP, no recipe bodies."""

from __future__ import annotations

KNOWN_PPID = {
    "M1-PROD-014": "a1b2c3d4e5f67890",
    "VIA1-ENG-002": "1111222233334444",
    "M2-PROD-009": "abcdabcdabcdabcd",
}

T3_S = 45


class GemSession:
    def __init__(self) -> None:
        self.tool_id = "NXE3800E-MOCK-01"
        self.ec_wafer_size_mm = 300
        self.ec_control_state = "REMOTE"  # OFFLINE | LOCAL | REMOTE
        self.gem_state = "Idle"  # Idle | Setup | Processing | Completing
        self.selected_ppid: str | None = None
        self.outstanding_primary = False
        self.mock = True

    def _s2f42(self, hcack: int, **extra) -> dict:
        self.outstanding_primary = False
        out = {"hcack": hcack, "mock": True, **extra}
        if hcack != 0 and "reason" not in out:
            out["reason"] = "rejected"
        return out

    def s2f41(self, rcmd: str, ppid: str | None = None) -> dict:
        if self.outstanding_primary:
            return {"hcack": 1, "reason": "outstanding primary", "mock": True}
        self.outstanding_primary = True
        rcmd = rcmd.upper()

        if rcmd == "PP-SELECT":
            if ppid not in KNOWN_PPID:
                return self._s2f42(3, reason="PPID not found")
            self.selected_ppid = ppid
            self.gem_state = "Setup"
            return self._s2f42(0, selected_ppid=ppid, sha16=KNOWN_PPID[ppid])

        if rcmd == "START":
            if self.ec_control_state != "REMOTE":
                return self._s2f42(2, reason="not REMOTE")
            if self.gem_state not in {"Idle", "Setup"}:
                return self._s2f42(2, reason=f"bad state {self.gem_state}")
            if not self.selected_ppid:
                return self._s2f42(2, reason="no recipe selected")
            self.gem_state = "Processing"
            return self._s2f42(0, rcmd="START", gem_state=self.gem_state)

        if rcmd == "ABORT":
            self.gem_state = "Idle"
            return self._s2f42(0, rcmd="ABORT", gem_state="Idle")

        return self._s2f42(1, reason=f"unknown RCMD {rcmd}")
