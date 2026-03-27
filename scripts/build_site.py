from __future__ import annotations

import sys
import traceback
from pathlib import Path

# scripts ディレクトリを import path に追加
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

# 各処理をインポート
from validate_data import validate_data
from build_dashboard_data import build_dashboard_data
from render_markdown_pages import render_markdown_pages
from render_html_pages import render_html_pages
from copy_assets import copy_assets


def run_step(name: str, func):
    """
    各ステップを安全に実行し、ログを強化する
    """
    print(f"\n[START] {name}")

    try:
        func()
        print(f"[OK] {name}")

    except Exception as e:
        print(f"[ERROR] {name}")
        print(f"Reason: {e}")

        # 詳細スタックトレース
        traceback.print_exc()

        # どのステップで落ちたか明確にする
        raise RuntimeError(f"Build failed at step: {name}") from e


def main():
    print("===================================")
    print("   Learning Dashboard Build Start")
    print("===================================")

    # 実行順序（重要）
    steps = [
        ("validate_data", validate_data),
        ("build_dashboard_data", build_dashboard_data),
        ("render_markdown_pages", render_markdown_pages),
        ("render_html_pages", render_html_pages),
        ("copy_assets", copy_assets),
    ]

    for name, func in steps:
        run_step(name, func)

    print("\n===================================")
    print("   Build Complete")
    print("===================================")


if __name__ == "__main__":
    main()