from .ingestion import openapi_loader
from .telemetry import log_event
def build_plan(spec_path, base_url):
    spec=openapi_loader.load(spec_path); eps=[]
    for path,item in (spec.get("paths") or {}).items():
        for m in (item or {}).keys():
            if m.lower() not in ("get","post","put","patch","delete","options","head"): continue
            eps.append({"path":path,"method":m.upper(),"risk":0.5})
    log_event({"type":"plan_created","summary":f"{len(eps)} endpoints planned"})
    return {"base_url":base_url,"endpoints":eps,"coverage_target":0.9}
