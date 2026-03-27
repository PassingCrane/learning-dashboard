from __future__ import annotations

import shutil

from common import DOCS_DIR, ROOT

SOURCE_ASSETS = ROOT / "assets"
TARGET_ASSETS = DOCS_DIR / "assets"


def copy_assets() -> None:
    if not SOURCE_ASSETS.exists():
        print("[INFO] No assets directory found. Skipped.")
        return

    if TARGET_ASSETS.exists():
        shutil.rmtree(TARGET_ASSETS)

    shutil.copytree(SOURCE_ASSETS, TARGET_ASSETS)
    print(f"[OK] Assets copied -> {TARGET_ASSETS}")


if __name__ == "__main__":
    copy_assets()