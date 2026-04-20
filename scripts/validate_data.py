from __future__ import annotations

from typing import Any

from common import RAW_DIR, load_json


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_skill_score(path, data: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    total_score = data.get("total_score")
    if total_score is not None and not is_number(total_score):
        errors.append(f"{path}.total_score: expected number, got {type(total_score).__name__}")

    domain_scores = data.get("domain_scores")
    if domain_scores is None:
        warnings.append(f"{path}: missing domain_scores")
        return
    if not isinstance(domain_scores, dict):
        errors.append(f"{path}.domain_scores: expected dict, got {type(domain_scores).__name__}")
        return

    for key, value in domain_scores.items():
        if not is_number(value):
            warnings.append(f"{path}.domain_scores.{key}: expected number, got {type(value).__name__}")


def validate_skill_radar(path, data: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    items = data.get("items")
    if isinstance(items, list):
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                warnings.append(f"{path}.items[{index}]: expected dict, got {type(item).__name__}")
                continue
            if not isinstance(item.get("label"), str):
                warnings.append(f"{path}.items[{index}].label: expected str")
            if not is_number(item.get("value")):
                warnings.append(f"{path}.items[{index}].value: expected number")
        return

    labels = data.get("labels")
    values = data.get("values")
    if isinstance(labels, list) and isinstance(values, list):
        if len(labels) != len(values):
            warnings.append(f"{path}: labels/values length mismatch")
        return

    warnings.append(f"{path}: missing both items and labels/values radar formats")


def validate_data() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    for filename in ("skill_radar.json", "skill_score.json", "learning_metrics.json", "htb_stats.json"):
        path = RAW_DIR / filename
        if not path.exists():
            errors.append(f"{path}: file not found")
            continue

        data = load_json(path, default={})
        if not isinstance(data, dict):
            errors.append(f"{path}: expected dict, got {type(data).__name__}")
            continue

        if filename == "learning_metrics.json" and "meta" not in data:
            errors.append(f"{path}: missing meta")
        if filename == "htb_stats.json" and "machines" not in data and "total_solves" not in data:
            errors.append(f"{path}: missing machines/total_solves")
        if filename == "skill_score.json":
            validate_skill_score(path, data, errors, warnings)
        if filename == "skill_radar.json":
            validate_skill_radar(path, data, errors, warnings)

    malware_path = RAW_DIR / "malware_stats.json"
    if malware_path.exists():
        data = load_json(malware_path, default={})
        if not isinstance(data, dict):
            errors.append(f"{malware_path}: expected dict, got {type(data).__name__}")
        else:
            if "meta" not in data:
                warnings.append(f"{malware_path}: missing meta")
            if "detection" not in data:
                warnings.append(f"{malware_path}: missing detection")
    else:
        warnings.append(f"{malware_path}: file not found (optional, skipping)")

    if warnings:
        print("\n[WARNING]")
        for warning in warnings:
            print("-", warning)

    if errors:
        print("\n[ERROR]")
        for error in errors:
            print("-", error)
        raise ValueError("Validation failed")

    print("[OK] Validation passed")


if __name__ == "__main__":
    validate_data()
