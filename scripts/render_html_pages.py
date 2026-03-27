from __future__ import annotations

import json

from common import DOCS_DIR, PROCESSED_DIR, TEMPLATES_DIR, load_json, load_text, render_template, save_text


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
    render_skill_radar()
    print("[OK] HTML pages rendered.")


if __name__ == "__main__":
    render_html_pages()