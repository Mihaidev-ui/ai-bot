import os, time, threading
from datetime import datetime

_LOG_DIR = os.environ.get("BOT_LOG_DIR", "/mnt/data/BOT_AI_REBUILD/logs")
os.makedirs(__LOG_DIR, exist_ok=True)

_level_order = {"DEBUG":10, "INFO":20, "WARN":30, "ERROR":40}
_current_level = _level_order.get(os.environ.get("BOT_LOG_LEVEL","INFO").upper(), 20)
_lock = threading.Lock()

def _fmt(ts, level, msg):
    return f"{ts} [{level}] {msg}"

def set_level(level:str):
    global _current_level
    _current_level = _level_order.get(level.upper(), 20)

def log(message:str, level:str="INFO"):
    if _level_order.get(level.upper(), 20) < _current_level:
        return
    ts = datetime.utcnow().isoformat(timespec="seconds")+"Z"
    line = _fmt(ts, level.upper(), message)
    with _lock:
        print(line)
        try:
            with open(os.path.join(_LOG_DIR, "bot.log"), "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception as e:
            print(_fmt(ts, "ERROR", f"Logger failed: {e}"))
