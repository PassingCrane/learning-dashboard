import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
OUT_DIR = os.path.join(BASE_DIR, "data", "processed")


def load_json(name):
    path = os.path.join(RAW_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(name, data):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def to_number(value):
    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None

    if isinstance(value, dict):
        for key in ("score", "value", "current", "points"):
            if key in value and isinstance(value[key], (int, float, str)):
                try:
                    return float(value[key])
                except ValueError:
                    return None

    return None


def extract_top_skills(radar):
    if not isinstance(radar, dict):
        return []

    normalized = []

    for key, value in radar.items():
        score = to_number(value)
        if score is not None:
            normalized.append({
                "name": key,
                "score": score
            })

    normalized.sort(key=lambda x: x["score"], reverse=True)
    return normalized[:5]


def build_summary():
    skill = load_json("skill_score.json")
    radar = load_json("skill_radar.json")
    htb = load_json("htb_stats.json")

    total_score = 0
    if isinstance(skill, dict):
        raw_total = skill.get("total", 0)
        try:
            total_score = float(raw_total)
        except (TypeError, ValueError):
            total_score = 0

    machines_total = 0
    if isinstance(htb, dict):
        machines = htb.get("machines", {})
        if isinstance(machines, dict):
            raw_total = machines.get("total", 0)
            try:
                machines_total = int(raw_total)
            except (TypeError, ValueError):
                machines_total = 0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_score": total_score,
        "machines_total": machines_total,
        "top_skills": extract_top_skills(radar)
    }


def build_technical_score():
    return load_json("skill_score.json")


def build_skill_radar():
    return load_json("skill_radar.json")


def build_htb():
    return load_json("htb_stats.json")


def build_recent():
    metrics = load_json("learning_metrics.json")

    if isinstance(metrics, dict):
        recent = metrics.get("recent", [])
        if isinstance(recent, list):
            return recent

    return []


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    save_json("dashboard_summary.json", build_summary())
    save_json("technical_score_view.json", build_technical_score())
    save_json("skill_radar_view.json", build_skill_radar())
    save_json("htb_breakdown.json", build_htb())
    save_json("recent_activity.json", build_recent())

    print("[OK] Processed data generated")


if __name__ == "__main__":
    main()