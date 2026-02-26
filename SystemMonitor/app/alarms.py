from dataclasses import dataclass
from typing import Optional, List

from .models import Metrics, AlarmEvent


@dataclass
class RuleState:
    active_since: Optional[float] = None


class AlarmEngine:
    """
    告警策略：阈值 + 持续时间（hold_sec）
    目的：避免瞬时峰值误报（jitter）
    """
    def __init__(self, cpu_high=80.0, mem_high=85.0, load1_high=4.0, hold_sec=10.0):
        self.cpu_high = cpu_high
        self.mem_high = mem_high
        self.load1_high = load1_high
        self.hold_sec = hold_sec

        self._cpu = RuleState()
        self._mem = RuleState()
        self._load = RuleState()

    def _check(self, ts: float, key: str, value: float, threshold: float, st: RuleState) -> Optional[AlarmEvent]:
        if value >= threshold:
            if st.active_since is None:
                st.active_since = ts
                return None

            if ts - st.active_since >= self.hold_sec:
                st.active_since = None  # 触发后重置（防止每秒刷屏）
                return AlarmEvent(
                    ts=ts,
                    level="WARN",
                    key=key,
                    value=float(value),
                    message=f"{key} >= {threshold} for {self.hold_sec:.0f}s (value={value:.2f})"
                )
        else:
            st.active_since = None

        return None

    def evaluate(self, m: Metrics) -> List[AlarmEvent]:
        ts = m.ts
        events: List[AlarmEvent] = []

        checks = [
            ("CPU_HIGH", m.cpu_percent, self.cpu_high, self._cpu),
            ("MEM_HIGH", m.mem_percent, self.mem_high, self._mem),
            ("LOAD1_HIGH", m.linux.load1, self.load1_high, self._load),
        ]

        for key, val, thr, st in checks:
            ev = self._check(ts, key, float(val), float(thr), st)
            if ev:
                events.append(ev)

        return events