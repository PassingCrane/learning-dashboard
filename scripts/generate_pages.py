import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DOCS_DIR = BASE_DIR / "docs"


def load_json(name: str):
    path = PROCESSED_DIR / name
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index():
    data = load_json("dashboard_summary.json")

    headline = data.get("headline", "Learning Dashboard")
    total_score = data.get("total_score", 0)
    top_skills = data.get("top_skills", [])
    current_focus = data.get("current_focus", [])
    recent_updates = data.get("recent_updates", [])

    top_skills_md = "\n".join(
        f"- {item.get('name', 'unknown')}: {item.get('score', 0)}"
        for item in top_skills
    ) or "- No data"

    current_focus_md = "\n".join(
        f"- {item}" if isinstance(item, str) else f"- {item.get('title', 'unknown')}"
        for item in current_focus
    ) or "- No data"

    recent_updates_md = "\n".join(
        f"- {item}" if isinstance(item, str) else f"- {item.get('title', 'unknown')}"
        for item in recent_updates
    ) or "- No data"

    content = f"""# Learning Dashboard

## Summary
- Headline: {headline}
- Total Score: {total_score}

## Top Skills
{top_skills_md}

## Current Focus
{current_focus_md}

## Recent Updates
{recent_updates_md}
"""

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    with open(DOCS_DIR / "index.md", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    build_index()


if __name__ == "__main__":
    main()