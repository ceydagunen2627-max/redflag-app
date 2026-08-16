import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from .engine import get_verdict
from .card_generator import generate_card
from .ai_client import analyze_with_ai

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


@app.route("/")
def root():
    return jsonify({"status": "API çalışıyor"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    nickname = data.get("nickname") or "Anonim"

    if not text or len(text) < 10:
        return jsonify({"error": "Senaryo çok kısa"}), 400

    ai_result = analyze_with_ai(text)
    toxic_pct = ai_result["toxic_percentage"]
    commentary = ai_result["commentary"]
    verdict = get_verdict(toxic_pct)

    card_path = generate_card(nickname, toxic_pct, verdict)
    card_filename = os.path.basename(card_path)

    return jsonify({
        "toxic_percentage": toxic_pct,
        "verdict": verdict,
        "commentary": commentary,
        "card_url": f"/output/{card_filename}"
    })


@app.route("/output/<path:filename>")
def output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)