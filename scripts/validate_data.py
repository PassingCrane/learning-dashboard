from __future__ import annotations

from pathlib import Path
from typing import Any

from common import RAW_DIR, load_json

# =========================================
# Schema 定義
# =========================================
# 使える型:
# - dict  : object
# - list  : array
# - str/int/float/bool
# - ("number",) : int/float 両対応
# - {"type": ..., "required": [...], "properties": {...}, "items": ...}
# =========================================

SCHEMAS: dict[str, dict[str, Any]] = {
    "learning_metrics.json": {
        "type": dict,
        "required": ["meta"],
        "properties": {
            "headline": {"type": str, "required": False},
            "meta": {
                "type": dict,
                "required": True,
                "properties": {
                    "last_updated": {"type": str, "required": False},
                    "source_repo": {"type": str, "required": False},
                },
            },
            "recent_activity": {
                "type": list,
                "required": False,
                "items": {
                    "type": dict,
                    "required": [],
                    "properties": {
                        "date": {"type": str, "required": False},
                        "title": {"type": str, "required": False},
                        "summary": {"type": str, "required": False},
                    },
                },
            },
        },
    },
    "skill_score.json": {
        "type": dict,
        "required": [],
        "properties": {},
        # 追加キーを許可し、その値は number を想定
        "additional_properties_type": ("number",),
    },
    "skill_radar.json": {
        "type": dict,
        "required": [],
        "properties": {},
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
                    "total": {"type": ("number",), "required": True},
                    "windows": {
                        "type": dict,
                        "required": False,
                        "properties": {
                            "total": {"type": ("number",), "required": False},
                            "easy": {"type": ("number",), "required": False},
                            "medium": {"type": ("number",), "required": False},
                            "hard": {"type": ("number",), "required": False},
                            "insane": {"type": ("number",), "required": False},
                        },
                    },
                    "linux": {
                        "type": dict,
                        "required": False,
                        "properties": {
                            "total": {"type": ("number",), "required": False},
                            "easy": {"type": ("number",), "required": False},
                            "medium": {"type": ("number",), "required": False},
                            "hard": {"type": ("number",), "required": False},
                            "insane": {"type": ("number",), "required": False},
                        },
                    },
                },
            },
            "challenges": {
                "type": dict,
                "required": False,
                "properties": {
                    "total": {"type": ("number",), "required": False},
                    "web": {"type": ("number",), "required": False},
                    "crypto": {"type": ("number",), "required": False},
                    "pwn": {"type": ("number",), "required": False},
                    "misc": {"type": ("number",), "required": False},
                    "forensics": {"type": ("number",), "required": False},
                },
            },
            "academy": {
                "type": dict,
                "required": False,
                "properties": {
                    "total": {"type": ("number",), "required": False},
                },
            },
            "meta": {
                "type": dict,
                "required": False,
                "properties": {
                    "last_updated": {"type": str, "required": False},
                },
            },
        },
    },
}


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _matches_type(value: Any, expected_type: Any) -> bool:
    if expected_type == ("number",) or expected_type == "number":
        return _is_number(value)

    if isinstance(expected_type, tuple):
        for t in expected_type:
            if t == "number" and _is_number(value):
                return True
            if isinstance(t, type) and isinstance(value, t):
                return True
        return False

    if expected_type == dict:
        return isinstance(value, dict)
    if expected_type == list:
        return isinstance(value, list)
    if expected_type == str:
        return isinstance(value, str)
    if expected_type == int:
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == float:
        return isinstance(value, float)
    if expected_type == bool:
        return isinstance(value, bool)

    return False


def _type_name(expected_type: Any) -> str:
    if expected_type == ("number",) or expected_type == "number":
        return "number"
    if isinstance(expected_type, tuple):
        return " or ".join(_type_name(t) for t in expected_type)
    if expected_type == dict:
        return "object"
    if expected_type == list:
        return "array"
    if expected_type == str:
        return "string"
    if expected_type == int:
        return "integer"
    if expected_type == float:
        return "float"
    if expected_type == bool:
        return "boolean"
    if isinstance(expected_type, type):
        return expected_type.__name__
    return str(expected_type)


def validate_against_schema(
    data: Any,
    schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(data, expected_type):
        errors.append(
            f"{path}: expected {_type_name(expected_type)}, got {type(data).__name__}"
        )
        return errors

    if isinstance(data, dict):
        required_keys: list[str] = schema.get("required", [])
        properties: dict[str, Any] = schema.get("properties", {})
        additional_properties_type = schema.get("additional_properties_type")

        for key in required_keys:
            if key not in data:
                errors.append(f"{path}.{key}: missing required key")

        for key, value in data.items():
            key_path = f"{path}.{key}"
            if key in properties:
                errors.extend(validate_against_schema(value, properties[key], key_path))
            elif additional_properties_type is not None:
                if not _matches_type(value, additional_properties_type):
                    errors.append(
                        f"{key_path}: expected {_type_name(additional_properties_type)}, got {type(value).__name__}"
                    )

    elif isinstance(data, list):
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(data):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))

    return errors


def validate_data() -> None:
    errors: list[str] = []

    for filename, schema in SCHEMAS.items():
        path = RAW_DIR / filename

        if not path.exists():
            errors.append(f"{path}: file not found")
            continue

        try:
            data = load_json(path)
        except Exception as exc:
            errors.append(f"{path}: invalid JSON: {exc}")
            continue

        file_errors = validate_against_schema(data, schema, path=str(path))
        errors.extend(file_errors)

    if errors:
        message_lines = ["Validation failed:"]
        message_lines.extend(f"- {error}" for error in errors)
        raise ValueError("\n".join(message_lines))

    print("[OK] Validation passed.")


if __name__ == "__main__":
    validate_data()