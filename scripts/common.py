from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
DOCS_DIR = ROOT / 'docs'
TEMPLATES_DIR = ROOT / 'templates'
ASSETS_DIR = ROOT / 'assets'


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(f'Missing JSON file: {path}')
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    ensure_dir(path.parent)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def load_text(path: Path) -> str:
    with path.open('r', encoding='utf-8') as f:
        return f.read()


def save_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def render_template(template_text: str, context: dict[str, Any]) -> str:
    rendered = template_text
    for key, value in context.items():
        rendered = rendered.replace('{{' + key + '}}', str(value))
    return rendered


def to_number(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def collect_numeric_items(mapping: dict[str, Any]) -> list[tuple[str, float]]:
    items: list[tuple[str, float]] = []
    for key, value in mapping.items():
        number = to_number(value)
        if number is not None:
            items.append((key, number))
    return items
