from flask import Flask, request, jsonify, render_template
import json
from pathlib import Path

app = Flask(__name__)

# Load dummy investor data once at startup
INVESTOR_PATH = Path(__file__).parent / "data" / "investors.json"
with INVESTOR_PATH.open() as f:
    INVESTORS = json.load(f)


# --- Matching logic ---
def match_rule_based(industry: str, stage: str, min_funding: float, max_funding: float):
    """Filter investors by industry, stage, and overlapping funding range"""
    matches = []
    for inv in INVESTORS:
        if (
            inv.get("industry", "").lower() == (industry or "").lower()
            and inv.get("stage", "").lower() == (stage or "").lower()
            # Check funding range overlap (handles open-ended cases)
            and not (inv.get("max_investment", 0) < min_funding or inv.get("min_investment", 0) > max_funding)
        ):
            matches.append(inv)
    return matches


def score_match(inv, industry: str, stage: str, min_funding: float, max_funding: float):
    """Calculate a simple relevance score (0..1)"""
    score = 0.0
    # Industry match
    if inv.get("industry", "").lower() == (industry or "").lower():
        score += 0.4
    # Stage match
    if inv.get("stage", "").lower() == (stage or "").lower():
        score += 0.3
    # Funding overlap closeness
    inv_mid = (inv.get("min_investment", 0) + inv.get("max_investment", 0)) / 2
    req_mid = (min_funding + max_funding) / 2
    diff = abs(inv_mid - req_mid)
    span = max(inv.get("max_investment", 0) - inv.get("min_investment", 0), 1)
    score += max(0.0, 0.3 * (1 - diff / span))
    return round(min(score, 1.0), 3)


@app.route("/")
def home():
    return "Entrepreneurship Unboxed MVP is running!"


# --- Part 1: Investor Matching ---
@app.route("/match", methods=["POST"])
def match_investors():
    payload = request.get_json(silent=True) or {}
    industry = payload.get("industry")
    stage = payload.get("stage")
    min_funding = payload.get("min_funding")
    max_funding = payload.get("max_funding")

    # Basic validation
    errors = {}
    if not industry:
        errors["industry"] = "industry is required"
    if not stage:
        errors["stage"] = "stage is required"

    try:
        min_funding = float(min_funding) if min_funding is not None else 0.0
    except (TypeError, ValueError):
        errors["min_funding"] = "min_funding must be a number"

    try:
        max_funding = float(max_funding) if max_funding is not None else float("inf")
    except (TypeError, ValueError):
        errors["max_funding"] = "max_funding must be a number"

    if errors:
        return jsonify({"ok": False, "errors": errors}), 400

    matches = match_rule_based(industry, stage, min_funding, max_funding)

    # Optional ranking
    rank = request.args.get("rank", "false").lower() == "true"
    if rank:
        ranked = []
        for inv in matches:
            inv_copy = dict(inv)
            inv_copy["score"] = score_match(inv, industry, stage, min_funding, max_funding)
            ranked.append(inv_copy)
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return jsonify({"ok": True, "matches": ranked, "ranked": True})

    return jsonify({"ok": True, "matches": matches, "ranked": False})


# --- Optional helper to browse investors ---
@app.route("/investors", methods=["GET"])
def list_investors():
    return jsonify({"count": len(INVESTORS), "investors": INVESTORS})


# --- Part 2: Founder Dashboard ---
@app.route("/dashboard", methods=["GET"])
def dashboard():
    industries = sorted({inv["industry"] for inv in INVESTORS})
    stages = sorted({inv["stage"] for inv in INVESTORS})

    dummy_data = {
        "startup_name": "My Startup",
        "health": "Healthy",
        "next_action": "Refine pitch deck",
    }
    return render_template("dashboard.html", data=dummy_data,
                           industries=industries, stages=stages)


if __name__ == "__main__":
    # For local dev only
    app.run(debug=True)
