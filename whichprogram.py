import time
import win32gui
import win32process
import psutil
import requests

API_URL = "http://127.0.0.1:8000/api/activity"
INTERVAL = 30

last_app = None
session_start = None

def get_active_app():
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None, None

    title = win32gui.GetWindowText(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        proc = psutil.Process(pid)
        return proc.name(), title
    except psutil.Error:
        return None, None

while True:
    now = int(time.time())
    app, title = get_active_app()

    if app != last_app:
        session_start = now
        last_app = app

    if session_start is None:
        session_start = now

    payload = {
        "app": app if app else "Unknown",
        "title": title if title else "",
        "session_start": int(session_start),
        "timestamp": now
    }

    try:
        requests.post(API_URL, json=payload, timeout=3)
    except requests.RequestException:
        pass

    time.sleep(INTERVAL)
