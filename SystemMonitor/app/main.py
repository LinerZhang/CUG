import threading
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

from .collector import Collector
from .alarms import AlarmEngine
from .storage import JsonlStore
from .report import generate_report

ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT / "web"
DATA_DIR = ROOT / "data"

app = FastAPI(title="System Monitor (Lin'er Zhang)")#创建 Web 服务实例

collector = Collector(interval=1.0, window=300)
alarms = AlarmEngine(cpu_high=80.0, mem_high=85.0, load1_high=4.0, hold_sec=10.0)
store = JsonlStore(str(DATA_DIR / "metrics.jsonl"), str(DATA_DIR / "alarms.jsonl"))


def background_loop():
    while True:
        m = collector.sample_once()
        collector.buffer.append(m)
        store.append_metrics(m)

        for ev in alarms.evaluate(m):
            store.append_alarm(ev)

        time.sleep(collector.interval)


@app.on_event("startup")
def startup():
    t = threading.Thread(target=background_loop, daemon=True)
    t.start()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (WEB_DIR / "dashboard.html").read_text(encoding="utf-8")


@app.get("/api/latest")
def api_latest():
    if not collector.buffer:
        return {"ok": False, "error": "no data yet"}
    return {"ok": True, "data": collector.buffer[-1].model_dump()}


@app.get("/api/history")
def api_history(limit: int = 60):
    buf = list(collector.buffer)[-max(1, min(limit, 300)):]
    return {"ok": True, "data": [m.model_dump() for m in buf]}


@app.get("/api/alarms")
def api_alarms(limit: int = 50):
    path = DATA_DIR / "alarms.jsonl"
    if not path.exists():
        return {"ok": True, "data": []}
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [ln for ln in lines if ln.strip()]
    data = lines[-max(1, min(limit, 500)):]
    return {"ok": True, "data": [__import__("json").loads(x) for x in data]}


@app.post("/api/report")
def api_report():
    out = str(DATA_DIR / "report.html")
    generate_report(str(DATA_DIR / "metrics.jsonl"), str(DATA_DIR / "alarms.jsonl"), out)
    return {"ok": True, "path": out}


@app.get("/report")
def report_page():
    out = DATA_DIR / "report.html"
    if not out.exists():
        return HTMLResponse("Report not generated yet. Click 'Generate Report' on dashboard.", status_code=404)
    return FileResponse(str(out))