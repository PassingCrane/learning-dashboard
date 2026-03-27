from __future__ import annotations

import shutil
from pathlib import Path

from common import DOCS_DIR, ROOT, ensure_dir

SOURCE_ASSETS = ROOT / 'assets'
TARGET_ASSETS = DOCS_DIR / 'assets'


def main() -> None:
    if not SOURCE_ASSETS.exists():
        print('No assets directory found. Skipped.')
        return

    for path in SOURCE_ASSETS.rglob('*'):
        if path.is_dir():
            continue
        relative = path.relative_to(SOURCE_ASSETS)
        target = TARGET_ASSETS / relative
        ensure_dir(target.parent)
        shutil.copy2(path, target)
    print('Assets copied.')


if __name__ == '__main__':
    main()
