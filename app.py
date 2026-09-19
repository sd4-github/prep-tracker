"""
DSA Prep Tracker — Flask app
============================
Browse coding problems by topic and sub-topic, with company tags and recency.

Run:
    pip install flask
    python app.py          ->  http://localhost:5000

Files (keep this layout):
    app.py
    subtopics.py
    processed_data_fixed.json
    templates/index.html
    static/style.css

Topics come straight from the JSON keys. Nothing about topics is hard-coded here.
Sub-topics (e.g. Arrays & Hashing -> Two Pointers) are worked out at startup by
subtopics.py; the JSON file is never modified.
"""

import json
import os
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode

from flask import Flask, jsonify, render_template, request

from subtopics import classify, sub_order

app = Flask(__name__)

DATA_PATH = Path(__file__).parent / "processed_data_fixed.json"

# Best recency across all companies, most recent first.
RECENCY_RANK = {"30 days": 0, "3 months": 1, "6 months": 2, "6+ months": 3, "all time": 4}

# Recency filter -> (min rank, max rank) of a problem's best recency
RECENCY_FILTERS = {
    "30 days":  (0, 0),   # last 30 days
    "3 months": (0, 1),   # last 3 months (includes the 30-day ones)
    "6 months": (0, 2),   # last 6 months
    "older":    (3, 4),   # nothing in the last 6 months
}


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────

def load_data() -> dict[str, list[dict]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Tag every problem with its sub-topic (in memory only).
    for topic, problems in data.items():
        for p in problems:
            p["sub"] = classify(topic, p)

    # Topic order = JSON order, with "Uncategorized" (if any) pushed to the end.
    return dict(sorted(data.items(), key=lambda kv: kv[0] == "Uncategorized"))


DATA = load_data()
TOPICS = [{"name": name, "total": len(items)} for name, items in DATA.items()]
TOTAL_PROBLEMS = sum(t["total"] for t in TOPICS)

ALL_COMPANIES = sorted({
    c["name"] for items in DATA.values() for p in items for c in p["companies"]
})


# ─────────────────────────────────────────────
# TEMPLATE HELPERS
# ─────────────────────────────────────────────

@app.context_processor
def helpers():
    def qs(**overrides) -> str:
        """Build a '/?a=b' link from the current query string plus overrides.
        Passing None (or 'all' / '') removes that key."""
        args = request.args.to_dict()
        args.update(overrides)
        clean = {k: v for k, v in args.items() if v not in (None, "", "all")}
        return "/?" + urlencode(clean) if clean else "/"
    return {"qs": qs}


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

def apply_filters(problems, difficulty, recency, company, search):
    if difficulty != "all":
        problems = [p for p in problems if p["difficulty"] == difficulty]

    if recency in RECENCY_FILTERS:
        lo, hi = RECENCY_FILTERS[recency]
        problems = [p for p in problems if lo <= RECENCY_RANK.get(p["recency"], 4) <= hi]

    if company != "all":
        problems = [p for p in problems if any(c["name"] == company for c in p["companies"])]

    if search:
        problems = [
            p for p in problems
            if search in p["title"].lower()
            or search in str(p["id"])
            or any(search in c["name"].lower() for c in p["companies"])
        ]
    return problems


@app.route("/")
def index():
    selected = request.args.get("pattern", "")
    if selected not in DATA:
        selected = TOPICS[0]["name"] if TOPICS else ""

    difficulty = request.args.get("difficulty", "all")
    recency = request.args.get("recency", "all")
    company = request.args.get("company", "all")
    search_raw = request.args.get("search", "").strip()
    active_sub = request.args.get("sub", "all")

    topic_problems = DATA.get(selected, [])

    # Filter first, then count sub-topics so chip numbers match what you'd see.
    filtered = apply_filters(topic_problems, difficulty, recency, company, search_raw.lower())
    sub_counts = Counter(p["sub"] for p in filtered)

    subs = [
        {"name": name, "count": sub_counts.get(name, 0)}
        for name in sub_order(selected)
        if sub_counts.get(name, 0) or name == active_sub
    ]
    if active_sub not in {s["name"] for s in subs}:
        active_sub = "all"

    problems = filtered if active_sub == "all" else [p for p in filtered if p["sub"] == active_sub]

    return render_template(
        "index.html",
        topics=TOPICS,
        total_problems=TOTAL_PROBLEMS,
        selected=selected,
        subs=subs,
        active_sub=active_sub,
        problems=problems,
        shown=len(problems),
        topic_total=len(topic_problems),
        difficulty=difficulty,
        recency=recency,
        company=company,
        search=search_raw,
        companies=ALL_COMPANIES,
        has_filters=any([difficulty != "all", recency != "all", company != "all", search_raw]),
    )


@app.route("/api/problems")
def api_problems():
    """JSON endpoint: /api/problems?pattern=Trees&sub=Tries"""
    pattern = request.args.get("pattern", "")
    sub = request.args.get("sub")
    problems = DATA.get(pattern, [])
    if sub:
        problems = [p for p in problems if p["sub"] == sub]
    return jsonify(problems)


if __name__ == "__main__":
    # Local development only. In production, gunicorn imports `app` and this block is skipped.
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    print(f"\n  DSA Prep Tracker")
    print(f"  {TOTAL_PROBLEMS} problems, {len(TOPICS)} topics, {len(ALL_COMPANIES)} companies")
    print(f"  http://{host}:{port}\n")
    app.run(debug=debug, host=host, port=port)
