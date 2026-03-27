from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from common import RAW_DIR, load_json

REQUIRED_FILES = {
    'learning_metrics.json': ['meta'],
    'skill_score.json': [],
    'skill_radar.json': [],
    'htb_stats.json': ['machines'],
}


def validate_required_keys(path: Path, data: Any, required_keys: list[str]) -> list[str]:
    errors: list[str] = []
    if required_keys and not isinstance(data, dict):
        errors.append(f'{path.name}: root must be an object')
        return errors
    for key in required_keys:
        if key not in data:
            errors.append(f'{path.name}: missing required key: {key}')
    return errors


def main() -> int:
    errors: list[str] = []
    for filename, required_keys in REQUIRED_FILES.items():
        path = RAW_DIR / filename
        if not path.exists():
            errors.append(f'Missing file: {path}')
            continue
        try:
            data = load_json(path)
        except Exception as exc:  # pragma: no cover
            errors.append(f'{filename}: invalid JSON: {exc}')
            continue
        errors.extend(validate_required_keys(path, data, required_keys))

    if errors:
        print('Validation failed:')
        for error in errors:
            print(f'- {error}')
        return 1

    print('Validation passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
