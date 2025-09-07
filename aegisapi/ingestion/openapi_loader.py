import yaml, json, pathlib
def load(path: str) -> dict:
    p = pathlib.Path(path); t = p.read_text(encoding='utf-8')
    return yaml.safe_load(t) if p.suffix.lower() in ('.yaml','.yml') else json.loads(t)
