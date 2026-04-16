from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from common import PROCESSED_DIR, RAW_DIR, collect_numeric_items, load_json, save_json


def build_summary() -> dict[str, Any]:
    learning_metrics = load_json(RAW_DIR / "learning_metrics.json", default={})
    skill_score = load_json(RAW_DIR / "skill_score.json", default={})
    skill_radar = load_json(RAW_DIR / "skill_radar.json", default={})
    htb_stats = load_json(RAW_DIR / "htb_stats.json", default={})

    numeric_scores = collect_numeric_items(skill_score if isinstance(skill_score, dict) else {})
    numeric_radar = collect_numeric_items(skill_radar if isinstance(skill_radar, dict) else {})

    top_skills = [
        {"name": name, "score": score}
        for name, score in sorted(numeric_radar, key=lambda x: x[1], reverse=True)[:5]
    ]

    machines = htb_stats.get("machines", {}) if isinstance(htb_stats, dict) else {}
    total_machines = machines.get("total", 0) if isinstance(machines, dict) else 0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": learning_metrics.get("headline", "Learning Dashboard"),
        "technical_score_total": round(sum(score for _, score in numeric_scores), 2),
        "top_skills": top_skills,
        "htb_total_machines": total_machines,
        "meta": learning_metrics.get("meta", {}),
    }


def build_technical_score_view() -> dict[str, Any]:
    skill_score = load_json(RAW_DIR / "skill_score.json", default={})
    items = [
        {"category": name, "score": score}
        for name, score in sorted(
            collect_numeric_items(skill_score if isinstance(skill_score, dict) else {}),
            key=lambda x: x[0].lower(),
        )
    ]
    return {"items": items}


def build_skill_radar_view() -> dict[str, Any]:
    skill_radar = load_json(RAW_DIR / "skill_radar.json", default={})
    items = [
        {"label": name, "value": score}
        for name, score in sorted(
            collect_numeric_items(skill_radar if isinstance(skill_radar, dict) else {}),
            key=lambda x: x[1],
            reverse=True,
        )
    ]
    return {"items": items}


def build_htb_breakdown() -> dict[str, Any]:
    htb_stats = load_json(RAW_DIR / "htb_stats.json", default={})
    machines = htb_stats.get("machines", {}) if isinstance(htb_stats, dict) else {}
    return {
        "machines": machines,
        "challenges": htb_stats.get("challenges", {}),
        "academy": htb_stats.get("academy", {}),
        "meta": htb_stats.get("meta", {}),
    }


def build_recent_activity() -> dict[str, Any]:
    learning_metrics = load_json(RAW_DIR / "learning_metrics.json", default={})
    recent = learning_metrics.get("recent_activity", [])
    if not isinstance(recent, list):
        recent = []

    normalized = []
    for item in recent[:10]:
        if isinstance(item, dict):
            normalized.append(
                {
                    "date": item.get("date", ""),
                    "title": item.get("title", ""),
                    "summary": item.get("summary", ""),
                }
            )
        else:
            normalized.append({"date": "", "title": str(item), "summary": ""})

    return {"items": normalized}


def build_malware_view() -> dict[str, Any]:
    """malware-research-lab の統計を表示用に整形する。
    ファイルが存在しない場合は空データを返す（optional）。
    """
    malware_stats = load_json(RAW_DIR / "malware_stats.json", default={})
    if not isinstance(malware_stats, dict):
        malware_stats = {}

    detection = malware_stats.get("detection", {})
    analysis_tools = malware_stats.get("analysis_tools", {})
    docs = malware_stats.get("docs", {})
    meta = malware_stats.get("meta", {})

    return {
        "available": bool(malware_stats),
        "generated_at": meta.get("generated_at", ""),
        "yara_rules": detection.get("yara_rules", 0),
        "sigma_rules": detection.get("sigma_rules", 0),
        "analysis_tools": analysis_tools.get("python_scripts", 0),
        "docs": docs.get("markdown_files", 0),
    }


def build_navigation() -> dict[str, Any]:
    return {
        "items": [
            {"title": "Dashboard", "path": "index.md"},
            {"title": "Technical Score", "path": "technical-score.md"},
            {"title": "HTB Overview", "path": "htb-overview.md"},
            {"title": "Recent Activity", "path": "recent-activity.md"},
            {"title": "Skill Radar", "path": "skill-radar.html"},
        ]
    }


def build_dashboard_data() -> None:
    save_json(PROCESSED_DIR / "dashboard_summary.json", build_summary())
    save_json(PROCESSED_DIR / "technical_score_view.json", build_technical_score_view())
    save_json(PROCESSED_DIR / "skill_radar_view.json", build_skill_radar_view())
    save_json(PROCESSED_DIR / "htb_breakdown.json", build_htb_breakdown())
    save_json(PROCESSED_DIR / "recent_activity.json", build_recent_activity())
    save_json(PROCESSED_DIR / "malware_view.json", build_malware_view())
    save_json(PROCESSED_DIR / "navigation.json", build_navigation())
    print("[OK] Processed data generated.")


if __name__ == "__main__":
    build_dashboard_data()