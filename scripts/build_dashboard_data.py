import json
import os
from datetime import datetime

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

def build_summary():
    skill = load_json("skill_score.json")
    radar = load_json("skill_radar.json")
    htb = load_json("htb_stats.json")

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "total_score": skill.get("total", 0),
        "top_skills": sorted(
            radar.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5],
        "machines_total": htb.get("machines", {}).get("total", 0)
    }

def build_technical_score():
    return load_json("skill_score.json")

def build_skill_radar():
    return load_json("skill_radar.json")

def build_htb():
    return load_json("htb_stats.json")

def build_recent():
    metrics = load_json("learning_metrics.json")
    return metrics.get("recent", [])

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