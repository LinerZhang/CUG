from pydantic import BaseModel
from typing import List, Optional, Dict


class ProcItem(BaseModel):
    pid: int
    name: str
    cpu_percent: float
    rss_mb: float
    status: Optional[str] = None
    cmdline: Optional[str] = None


class LinuxExtras(BaseModel):
    load1: float
    load5: float
    load15: float

    mem_cached_mb: float
    mem_buffers_mb: float
    mem_available_mb: float

    proc_state_counts: Dict[str, int]


class Metrics(BaseModel):
    ts: float

    cpu_percent: float

    mem_percent: float
    mem_used_mb: float
    mem_total_mb: float

    disk_percent: float

    net_sent_bps: float
    net_recv_bps: float

    top_cpu: List[ProcItem]
    top_mem: List[ProcItem]

    linux: LinuxExtras


class AlarmEvent(BaseModel):
    ts: float
    level: str   # INFO/WARN/CRIT
    key: str     # CPU_HIGH / MEM_HIGH / LOAD1_HIGH...
    value: float
    message: str