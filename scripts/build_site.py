from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / 'scripts'

STEPS = [
    'validate_data.py',
    'build_dashboard_data.py',
    'render_markdown_pages.py',
    'render_html_pages.py',
    'copy_assets.py',
]


def run_step(filename: str) -> None:
    script = SCRIPTS_DIR / filename
    print(f'==> Running {filename}')
    subprocess.run([sys.executable, str(script)], check=True)


def main() -> int:
    for step in STEPS:
        run_step(step)
    print('Site build completed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
