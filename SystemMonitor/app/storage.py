from pathlib import Path
from .models import Metrics, AlarmEvent


class JsonlStore:
    """
    JSON Lines：每行一个 JSON
    好处：追加写简单、易于后处理、支持结构化数据（top进程列表）
    """
    def __init__(self, metrics_path: str, alarms_path: str):
        self.metrics_path = Path(metrics_path)
        self.alarms_path = Path(alarms_path)
        self.metrics_path.parent.mkdir(parents=True, exist_ok=True)
        self.alarms_path.parent.mkdir(parents=True, exist_ok=True)

    def append_metrics(self, m: Metrics):
        with self.metrics_path.open("a", encoding="utf-8") as f:
            f.write(m.model_dump_json() + "\n")

    def append_alarm(self, a: AlarmEvent):
        with self.alarms_path.open("a", encoding="utf-8") as f:
            f.write(a.model_dump_json() + "\n")