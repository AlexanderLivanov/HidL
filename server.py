from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

stats = {}

class Activity(BaseModel):
    app: str | None
    title: str | None
    session_start: int
    timestamp: int

@app.post("/api/activity")
def receive_activity(data: Activity):
    if not data.app:
        return {"status": "ignored"}

    app_name = data.app
    now = data.timestamp

    if app_name not in stats:
        stats[app_name] = {
            "total_time": 0,
            "last_seen": now,
            "last_session": 0
        }

    entry = stats[app_name]

    delta = now - entry["last_seen"]
    if 0 < delta < 120:
        entry["total_time"] += delta

    entry["last_seen"] = now
    entry["last_session"] = now - data.session_start

    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] "
        f"{app_name} | {data.title} | "
        f"Сессия: {entry['last_session']} c | "
        f"Всего: {entry['total_time']} c"
    )

    return {
        "status": "ok",
        "app": app_name,
        "last_session": entry["last_session"],
        "total_time": entry["total_time"]
    }

@app.get("/stats")
def get_stats():
    return stats