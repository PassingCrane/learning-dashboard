import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

def load(name):
    with open(os.path.join(DATA_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)

def write(path, content):
    with open(os.path.join(DOCS_DIR, path), "w", encoding="utf-8") as f:
        f.write(content)

def build_index():
    data = load("dashboard_summary.json")

    md = f"""# Learning Dashboard

## Summary

- Total Score: {data['total_score']}
- Machines Solved: {data['machines_total']}

## Top Skills

"""
    for skill, val in data["top_skills"]:
        md += f"- {skill}: {val}\n"

    write("index.md", md)

def build_technical():
    data = load("technical_score_view.json")

    md = "# Technical Score\n\n"
    for k, v in data.items():
        md += f"- {k}: {v}\n"

    write("technical-score.md", md)

def build_radar():
    data = load("skill_radar_view.json")

    md = "# Skill Radar\n\n"
    for k, v in data.items():
        md += f"- {k}: {v}\n"

    write("skill-radar.md", md)

def build_htb():
    data = load("htb_breakdown.json")

    md = "# HTB Overview\n\n"
    md += f"Total Machines: {data['machines']['total']}\n"

    write("htb-overview.md", md)

def build_recent():
    data = load("recent_activity.json")

    md = "# Recent Activity\n\n"
    for item in data:
        md += f"- {item}\n"

    write("recent-activity.md", md)

def main():
    os.makedirs(DOCS_DIR, exist_ok=True)

    build_index()
    build_technical()
    build_radar()
    build_htb()
    build_recent()

    print("[OK] Pages generated")

if __name__ == "__main__":
    main()