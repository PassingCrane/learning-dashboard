from __future__ import annotations

import json

from common import DOCS_DIR, PROCESSED_DIR, TEMPLATES_DIR, load_json, load_text, render_template, save_text


def render_index_html() -> None:
    template = load_text(TEMPLATES_DIR / "html" / "index.template.html")
    summary = load_json(PROCESSED_DIR / "dashboard_summary.json", default={})
    malware = load_json(PROCESSED_DIR / "malware_view.json", default={})

    top_skills = summary.get("top_skills", [])
    if top_skills:
        max_score = max((item["score"] for item in top_skills), default=1) or 1
        skills_html = "<ul class=\"skills-list\">\n" + "\n".join(
            f'  <li><span style="width:80px;display:inline-block">{item["name"]}</span>'
            f'<div class="bar-wrap"><div class="bar" style="width:{int(item["score"] / max_score * 100)}%"></div></div>'
            f'<span>{item["score"]}</span></li>'
            for item in top_skills
        ) + "\n</ul>"
    else:
        skills_html = '<p class="no-data">No data</p>'

    content = render_template(
        template,
        {
            "HEADLINE": summary.get("headline", "Learning Dashboard"),
            "TECHNICAL_SCORE_TOTAL": summary.get("technical_score_total", 0),
            "HTB_TOTAL_MACHINES": summary.get("htb_total_machines", 0),
            "TOP_SKILLS_HTML": skills_html,
            "GENERATED_AT": summary.get("generated_at", ""),
            "MALWARE_YARA_RULES": malware.get("yara_rules", 0),
        },
    )
    save_text(DOCS_DIR / "index.html", content)


def render_skill_radar() -> None:
    template = load_text(TEMPLATES_DIR / "html" / "skill-radar.template.html")
    data = load_json(PROCESSED_DIR / "skill_radar_view.json")

    labels = [item["label"] for item in data.get("items", [])]
    values = [item["value"] for item in data.get("items", [])]

    content = render_template(
        template,
        {
            "RADAR_LABELS_JSON": json.dumps(labels, ensure_ascii=False),
            "RADAR_VALUES_JSON": json.dumps(values, ensure_ascii=False),
            "TABLE_ROWS": "\n".join(
                f"<tr><td>{item['label']}</td><td>{item['value']}</td></tr>"
                for item in data.get("items", [])
            ),
        },
    )
    save_text(DOCS_DIR / "skill-radar.html", content)


def render_html_pages() -> None:
    render_index_html()
    render_skill_radar()
    print("[OK] HTML pages rendered.")


if __name__ == "__main__":
    render_html_pages()