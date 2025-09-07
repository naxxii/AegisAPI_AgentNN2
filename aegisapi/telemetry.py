from pathlib import Path; import json, time
TELEMETRY_DIR=Path("data"); TELEMETRY_FILE=TELEMETRY_DIR/"telemetry.jsonl"
def log_event(event): TELEMETRY_DIR.mkdir(parents=True,exist_ok=True); event.setdefault("ts", time.time()); TELEMETRY_FILE.write_text((TELEMETRY_FILE.read_text() if TELEMETRY_FILE.exists() else "")+json.dumps(event)+"\n", encoding="utf-8")
def load_events():
    if not TELEMETRY_FILE.exists(): return []
    return [json.loads(l) for l in TELEMETRY_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
