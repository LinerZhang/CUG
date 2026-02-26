import json
from pathlib import Path
from statistics import mean
from datetime import datetime
from jinja2 import Template


TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>SysMon Report</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1,h2 { margin-bottom: 6px; }
    .small { color:#666; font-size: 12px; margin-bottom: 12px; }
    table { border-collapse: collapse; width: 100%; margin: 12px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background: #f3f3f3; text-align: left; }
  </style>
</head>
<body>
  <h1>System Monitor Report</h1>
  <div class="small">Range: {{ start }} ~ {{ end }} | Samples: {{ n }}</div>

  <h2>Summary</h2>
  <table>
    <tr><th>Metric</th><th>Average</th><th>Peak</th></tr>
    <tr><td>CPU %</td><td>{{ cpu_avg }}</td><td>{{ cpu_peak }}</td></tr>
    <tr><td>Memory %</td><td>{{ mem_avg }}</td><td>{{ mem_peak }}</td></tr>
    <tr><td>Disk %</td><td>{{ disk_avg }}</td><td>{{ disk_peak }}</td></tr>
    <tr><td>Load1</td><td>{{ load_avg }}</td><td>{{ load_peak }}</td></tr>
    <tr><td>Net Sent (KB/s)</td><td>{{ sent_avg }}</td><td>{{ sent_peak }}</td></tr>
    <tr><td>Net Recv (KB/s)</td><td>{{ recv_avg }}</td><td>{{ recv_peak }}</td></tr>
  </table>

  <h2>Alarm Events</h2>
  {% if alarms|length == 0 %}
    <div>No alarms.</div>
  {% else %}
  <table>
    <tr><th>Time</th><th>Level</th><th>Key</th><th>Value</th><th>Message</th></tr>
    {% for a in alarms %}
      <tr>
        <td>{{ a.time }}</td><td>{{ a.level }}</td><td>{{ a.key }}</td><td>{{ a.value }}</td><td>{{ a.message }}</td>
      </tr>
    {% endfor %}
  </table>
  {% endif %}
</body>
</html>
"""


def _read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def generate_report(metrics_path: str, alarms_path: str, out_html: str):
    mp = Path(metrics_path)
    ap = Path(alarms_path)

    metrics = _read_jsonl(mp)
    alarms = _read_jsonl(ap)

    if not metrics:
        Path(out_html).write_text("No data.", encoding="utf-8")
        return

    cpu = [m["cpu_percent"] for m in metrics]
    mem = [m["mem_percent"] for m in metrics]
    disk = [m["disk_percent"] for m in metrics]
    load1 = [m["linux"]["load1"] for m in metrics]
    sent = [m["net_sent_bps"] / 1024 for m in metrics]
    recv = [m["net_recv_bps"] / 1024 for m in metrics]

    alarm_rows = [
        {
            "time": _fmt_ts(a["ts"]),
            "level": a["level"],
            "key": a["key"],
            "value": f'{a["value"]:.2f}',
            "message": a["message"],
        }
        for a in alarms
    ]

    ctx = dict(
        start=_fmt_ts(metrics[0]["ts"]),
        end=_fmt_ts(metrics[-1]["ts"]),
        n=len(metrics),

        cpu_avg=f"{mean(cpu):.1f}", cpu_peak=f"{max(cpu):.1f}",
        mem_avg=f"{mean(mem):.1f}", mem_peak=f"{max(mem):.1f}",
        disk_avg=f"{mean(disk):.1f}", disk_peak=f"{max(disk):.1f}",
        load_avg=f"{mean(load1):.2f}", load_peak=f"{max(load1):.2f}",
        sent_avg=f"{mean(sent):.1f}", sent_peak=f"{max(sent):.1f}",
        recv_avg=f"{mean(recv):.1f}", recv_peak=f"{max(recv):.1f}",

        alarms=alarm_rows
    )

    html = Template(TEMPLATE).render(**ctx)
    Path(out_html).write_text(html, encoding="utf-8")