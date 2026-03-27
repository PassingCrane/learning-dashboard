from __future__ import annotations

from pathlib import Path
from typing import Any

from common import RAW_DIR, load_json


# =========================
# Schema
# =========================
SCHEMAS = {
    "learning_metrics.json": {
        "type": dict,
        "required": ["meta"],
        "properties": {
            "headline": {"type": str},
            "meta": {
                "type": dict,
                "required": [],
                "properties": {
                    "last_updated": {"type": str},
                    "source_repo": {"type": str},
                },
            },
            "recent_activity": {
                "type": list,
                "items": {
                    "type": dict,
                    "properties": {
                        "date": {"type": str},
                        "title": {"type": str},
                        "summary": {"type": str},
                    },
                },
            },
        },
    },
    "skill_score.json": {
        "type": dict,
        "additional_properties_type": ("number",),
    },
    "skill_radar.json": {
        "type": dict,
        "additional_properties_type": ("number",),
    },
    "htb_stats.json": {
        "type": dict,
        "required": ["machines"],
        "properties": {
            "machines": {
                "type": dict,
                "required": ["total"],
                "properties": {
                    "total": {"type": ("number",)},
                },
            }
        },
    },
}


# =========================
# Utils
# =========================
def is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def match_type(value: Any, expected: Any) -> bool:
    if expected == ("number",) or expected == "number":
        return is_number(value)

    if isinstance(expected, tuple):
        return any(match_type(value, t) for t in expected)

    if expected == dict:
        return isinstance(value, dict)
    if expected == list:
        return isinstance(value, list)
    if expected == str:
        return isinstance(value, str)

    return isinstance(value, expected)


def normalize_required(schema: dict) -> list[str]:
    """
    required を必ず list にする（今回のバグ対策）
    """
    required = schema.get("required", [])

    if required is True:
        return []  # Trueは無視
    if required is False:
        return []
    if isinstance(required, list):
        return required

    return []


# =========================
# Validation
# =========================
def validate_against_schema(data: Any, schema: dict, path: str) -> list[str]:
    errors: list[str] = []

    # 型チェック
    expected_type = schema.get("type")
    if expected_type and not match_type(data, expected_type):
        errors.append(f"{path}: expected {expected_type}, got {type(data).__name__}")
        return errors

    # dict
    if isinstance(data, dict):
        required_keys = normalize_required(schema)
        properties = schema.get("properties", {})
        additional_type = schema.get("additional_properties_type")

        # requiredチェック
        for key in required_keys:
            if key not in data:
                errors.append(f"{path}.{key}: missing required key")

        # propertiesチェック
        for key, value in data.items():
            sub_path = f"{path}.{key}"

            if key in properties:
                errors.extend(
                    validate_against_schema(value, properties[key], sub_path)
                )
            elif additional_type:
                if not match_type(value, additional_type):
                    errors.append(
                        f"{sub_path}: expected {additional_type}, got {type(value).__name__}"
                    )

    # list
    elif isinstance(data, list):
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(data):
                errors.extend(
                    validate_against_schema(item, item_schema, f"{path}[{i}]")
                )

    return errors


# =========================
# Entry
# =========================
def validate_data() -> None:
    errors: list[str] = []

    for filename, schema in SCHEMAS.items():
        path = RAW_DIR / filename

        if not path.exists():
            errors.append(f"{path}: file not found")
            continue

        try:
            data = load_json(path)
        except Exception as e:
            errors.append(f"{path}: JSON parse error: {e}")
            continue

        errors.extend(validate_against_schema(data, schema, str(path)))

    if errors:
        print("\n".join(errors))
        raise ValueError("Validation failed")

    print("[OK] Validation passed")


if __name__ == "__main__":
    validate_data()