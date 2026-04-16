from __future__ import annotations

from common import RAW_DIR, load_json


SCHEMAS = {
    "skill_radar.json": {
        "type": dict,
        "additional_properties_type": ("number",),
        "strict": False,  # ← ここ重要
    },
    "skill_score.json": {
        "type": dict,
        "additional_properties_type": ("number",),
        "strict": False,
    },
    "learning_metrics.json": {
        "type": dict,
        "required": ["meta"],
        "strict": True,
    },
    "htb_stats.json": {
        "type": dict,
        "required": ["machines"],
        "strict": True,
    },
    # malware-research-lab の export-summary.yml が生成・push する統計ファイル。
    # ファイルが存在しない場合は警告のみ（optional）。
    "malware_stats.json": {
        "type": dict,
        "required": ["meta", "detection"],
        "strict": False,
        "optional": True,
    },
}


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate_data():
    errors = []
    warnings = []

    for filename, schema in SCHEMAS.items():
        path = RAW_DIR / filename

        if not path.exists():
            if schema.get("optional"):
                warnings.append(f"{path}: file not found (optional, skipping)")
                continue
            errors.append(f"{path}: file not found")
            continue

        data = load_json(path)

        # =========================
        # additional_properties
        # =========================
        if "additional_properties_type" in schema:
            expected = schema["additional_properties_type"]
            strict = schema.get("strict", True)

            for key, value in data.items():
                if not is_number(value):
                    msg = f"{path}.{key}: expected number, got {type(value).__name__}"

                    if strict:
                        errors.append(msg)
                    else:
                        warnings.append(msg)

    # =========================
    # 出力
    # =========================
    if warnings:
        print("\n[WARNING]")
        for w in warnings:
            print("-", w)

    if errors:
        print("\n[ERROR]")
        for e in errors:
            print("-", e)
        raise ValueError("Validation failed")

    print("[OK] Validation passed")