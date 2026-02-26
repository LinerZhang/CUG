import time
import psutil
from collections import deque
from typing import Deque, Tuple, List

from .models import Metrics, ProcItem, LinuxExtras
from .linux_proc import read_loadavg, read_meminfo_mb, count_proc_states

_MB = 1024 * 1024


class Collector:
    """
    采集器：
    - 每 interval 秒采样一次
    - 使用 ring buffer 保存最近 window 条（例如 300 秒）
    """
    def __init__(self, interval: float = 1.0, window: int = 300):
        self.interval = interval
        self.buffer: Deque[Metrics] = deque(maxlen=window)

        # 网络速率需要用差分计算
        self._prev_net: Tuple[float, psutil._common.snetio] | None = None

        # 初始化 cpu_percent 计数基准
        psutil.cpu_percent(interval=None)

        # 初始化进程 cpu_percent 基准
        for p in psutil.process_iter():
            try:
                p.cpu_percent(interval=None)
            except Exception:
                pass

    def _net_bps(self) -> tuple[float, float]:
        now = time.time()
        net = psutil.net_io_counters()

        if self._prev_net is None:
            self._prev_net = (now, net)
            return 0.0, 0.0

        prev_t, prev_net = self._prev_net
        dt = max(1e-6, now - prev_t)

        sent_bps = (net.bytes_sent - prev_net.bytes_sent) / dt
        recv_bps = (net.bytes_recv - prev_net.bytes_recv) / dt

        self._prev_net = (now, net)
        return float(sent_bps), float(recv_bps)

    def _top_processes(self) -> tuple[List[ProcItem], List[ProcItem]]:
        """
        进程 CPU% 需要“先采样后对比”，这里给一个短窗口。
        """
        time.sleep(0.05)

        items: List[ProcItem] = []
        for p in psutil.process_iter(attrs=["pid", "name"]):
            try:
                cpu = p.cpu_percent(interval=None)
                rss_mb = p.memory_info().rss / _MB

                status = None
                try:
                    status = p.status()
                except Exception:
                    pass

                cmdline = None
                try:
                    cmdline = " ".join(p.cmdline())
                except Exception:
                    pass

                items.append(
                    ProcItem(
                        pid=p.info["pid"],
                        name=p.info.get("name") or "",
                        cpu_percent=float(cpu),
                        rss_mb=float(rss_mb),
                        status=status,
                        cmdline=cmdline,
                    )
                )
            except Exception:
                continue

        top_cpu = sorted(items, key=lambda x: x.cpu_percent, reverse=True)[:10]
        top_mem = sorted(items, key=lambda x: x.rss_mb, reverse=True)[:10]
        return top_cpu, top_mem

    def sample_once(self) -> Metrics:
        ts = time.time()

        cpu_percent = float(psutil.cpu_percent(interval=None))

        vm = psutil.virtual_memory()
        mem_percent = float(vm.percent)
        mem_used_mb = float((vm.total - vm.available) / _MB)
        mem_total_mb = float(vm.total / _MB)

        du = psutil.disk_usage("/")
        disk_percent = float(du.percent)

        sent_bps, recv_bps = self._net_bps()
        top_cpu, top_mem = self._top_processes()

        # Linux extras from /proc
        l1, l5, l15 = read_loadavg()
        cached_mb, buffers_mb, available_mb = read_meminfo_mb()
        states = count_proc_states()

        linux = LinuxExtras(
            load1=l1, load5=l5, load15=l15,
            mem_cached_mb=float(cached_mb),
            mem_buffers_mb=float(buffers_mb),
            mem_available_mb=float(available_mb),
            proc_state_counts=states,
        )

        return Metrics(
            ts=ts,
            cpu_percent=cpu_percent,
            mem_percent=mem_percent,
            mem_used_mb=mem_used_mb,
            mem_total_mb=mem_total_mb,
            disk_percent=disk_percent,
            net_sent_bps=sent_bps,
            net_recv_bps=recv_bps,
            top_cpu=top_cpu,
            top_mem=top_mem,
            linux=linux,
        )