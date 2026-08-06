from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .models import ScenarioRequest
from .engine import get_verdict
from .card_generator import generate_card
from .ai_client import analyze_with_ai

app = FastAPI(title="Red Flag / Green Flag Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/output", StaticFiles(directory="output"), name="output")

@app.post("/analyze")
def analyze(request: ScenarioRequest):
    ai_result = analyze_with_ai(request.text)
    toxic_pct = ai_result["toxic_percentage"]
    commentary = ai_result["commentary"]
    verdict = get_verdict(toxic_pct)

    card_path = generate_card(request.nickname, toxic_pct, verdict)

    return {
        "toxic_percentage": toxic_pct,
        "verdict": verdict,
        "commentary": commentary,
        "card_url": f"/{card_path}"
    }

@app.get("/")
def root():
    return {"status": "API çalışıyor"}