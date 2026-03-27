from __future__ import annotations

from common import DOCS_DIR, PROCESSED_DIR, TEMPLATES_DIR, load_json, load_text, render_template, save_text


def render_index() -> None:
    template = load_text(TEMPLATES_DIR / 'markdown' / 'index.template.md')
    summary = load_json(PROCESSED_DIR / 'dashboard_summary.json')
    top_skills_lines = '\n'.join(
        f"- {item['name']}: {item['score']}" for item in summary.get('top_skills', [])
    ) or '- no data'
    content = render_template(template, {
        'HEADLINE': summary.get('headline', 'Learning Dashboard'),
        'TECHNICAL_SCORE_TOTAL': summary.get('technical_score_total', 0),
        'HTB_TOTAL_MACHINES': summary.get('htb_total_machines', 0),
        'TOP_SKILLS': top_skills_lines,
        'GENERATED_AT': summary.get('generated_at', ''),
    })
    save_text(DOCS_DIR / 'index.md', content)


def render_technical_score() -> None:
    template = load_text(TEMPLATES_DIR / 'markdown' / 'technical-score.template.md')
    data = load_json(PROCESSED_DIR / 'technical_score_view.json')
    rows = '\n'.join(f"| {item['category']} | {item['score']} |" for item in data.get('items', []))
    content = render_template(template, {'ROWS': rows or '| No data | 0 |'})
    save_text(DOCS_DIR / 'technical-score.md', content)


def render_htb_overview() -> None:
    template = load_text(TEMPLATES_DIR / 'markdown' / 'htb-overview.template.md')
    data = load_json(PROCESSED_DIR / 'htb_breakdown.json')
    machines = data.get('machines', {})
    content = render_template(template, {
        'TOTAL': machines.get('total', 0),
        'WINDOWS_TOTAL': machines.get('windows', {}).get('total', 0),
        'LINUX_TOTAL': machines.get('linux', {}).get('total', 0),
        'LAST_UPDATED': data.get('meta', {}).get('last_updated', 'n/a'),
    })
    save_text(DOCS_DIR / 'htb-overview.md', content)


def render_recent_activity() -> None:
    template = load_text(TEMPLATES_DIR / 'markdown' / 'recent-activity.template.md')
    data = load_json(PROCESSED_DIR / 'recent_activity.json')
    items = []
    for item in data.get('items', []):
        title = item.get('title', '')
        date = item.get('date', '')
        summary = item.get('summary', '')
        items.append(f"- **{date} {title}**\n  - {summary}".rstrip())
    content = render_template(template, {'ITEMS': '\n'.join(items) or '- no activity'})
    save_text(DOCS_DIR / 'recent-activity.md', content)


def main() -> None:
    render_index()
    render_technical_score()
    render_htb_overview()
    render_recent_activity()
    print('Markdown pages rendered.')


if __name__ == '__main__':
    main()
