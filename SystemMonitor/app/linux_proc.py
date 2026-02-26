from pathlib import Path

def read_loadavg():
    """
    /proc/loadavg: 1min 5min 15min runnable/total last_pid
    """
    s = Path("/proc/loadavg").read_text().strip().split()
    return float(s[0]), float(s[1]), float(s[2])

def read_meminfo_mb():
    """
    /proc/meminfo 以 kB 为单位
    我们取 Cached / Buffers / MemAvailable 来解释 Linux 的缓存机制。
    """
    kv = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        if ":" not in line:
            continue
        k, rest = line.split(":", 1)
        parts = rest.strip().split()
        if not parts:
            continue
        kv[k] = int(parts[0])  # kB

    cached = kv.get("Cached", 0) / 1024
    buffers = kv.get("Buffers", 0) / 1024
    available = kv.get("MemAvailable", 0) / 1024
    return cached, buffers, available

def count_proc_states():
    """
    统计进程状态：R/S/D/Z/...（Linux 特有）
    /proc/[pid]/stat 第三列是 state
    """
    counts = {}
    proc = Path("/proc")

    for p in proc.iterdir():
        if not p.name.isdigit():
            continue
        stat_path = p / "stat"
        try:
            content = stat_path.read_text()
            # 格式：pid (comm) state ...
            # comm 里可能有空格，但被括号包围，所以找最后一个 ')'
            rparen = content.rfind(")")
            after = content[rparen + 2 :]  # 跳过 ") "
            state = after.split()[0]
            counts[state] = counts.get(state, 0) + 1
        except Exception:
            # 某些 pid 可能瞬间结束/无权限，忽略即可
            continue
    return counts