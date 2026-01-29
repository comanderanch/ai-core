from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # /home/commandDev/work/ai-core-v1.01
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

APP = FastAPI()

class RunReq(BaseModel):
    lines: list[str]

def run_lines(lines: list[str]):
    payload = "\n".join(lines + [":quit"])
    p = subprocess.run(
        ["python3", "scripts/interactive_ai_core.py"],
        input=payload, text=True, capture_output=True, cwd=str(ROOT)
    )
    out = (p.stdout or "")[-8000:]
    err = (p.stderr or "")
    return {"ok": p.returncode == 0, "stdout": out, "stderr": err, "code": p.returncode}

@APP.get("/api/ping")
def ping(): return {"ok": True}

@APP.post("/api/run")
def api_run(req: RunReq): return run_lines(req.lines)

class ImagineReq(BaseModel):
    text: str

@APP.post("/api/imagine")
def api_imagine(req: ImagineReq):
    try:
        from scripts.imagination_bridge import imagine as _imagine
        draft = _imagine(req.text)
        return {"ok": True, "draft": draft}
    except Exception as e:
        return {"ok": False, "error": repr(e)}

APP.mount("/", StaticFiles(directory=ROOT / "webui" / "static", html=True), name="static")
app = APP
