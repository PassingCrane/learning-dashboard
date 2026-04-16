# learning-dashboard

![Pages](https://img.shields.io/badge/GitHub_Pages-deployed-brightgreen)
![Visibility](https://img.shields.io/badge/visibility-public-blue)

> 5リポジトリ連携エコシステムの可視化専用リポジトリ。`security-learning` / `htb-writeups` / `malware-research-lab` から受け取った raw JSON を加工して GitHub Pages でダッシュボードを配信する。

---

## 概要

| 項目 | 内容 |
|------|------|
| 用途 | 学習統計の GitHub Pages 可視化 |
| 公開設定 | public |
| 関連リポジトリ | security-learning / htb-writeups / malware-research-lab |

---

## エコシステム内の位置づけ

```
[security-learning] ──→  data/raw/learning_metrics.json
                    ──→  data/raw/skill_score.json
                    ──→  data/raw/skill_radar.json
                    ──→  data/raw/htb_stats.json       （htb-writeups から転送）

[malware-research-lab] ──→  data/raw/malware_stats.json

[learning-dashboard] ◀── このリポジトリ（可視化専用・正本データなし）
    ▼
  GitHub Pages 公開
```

このリポジトリは **表示専用**。正本データは持たず、受け取った raw JSON を加工してページを生成する。

---

## 目的

1. raw JSON の受け取り先
2. processed JSON の生成
3. Markdown / HTML ページのレンダリング
4. GitHub Pages 配信用 `docs/` の生成

---

## ディレクトリ構成

```text
learning-dashboard/
├── README.md
├── HANDOVER.md            # 運用引き継ぎメモ
├── data/
│   ├── raw/               # 外部リポジトリから受け取る（手編集不可）
│   │   ├── htb_stats.json
│   │   ├── learning_metrics.json
│   │   ├── skill_radar.json
│   │   ├── skill_score.json
│   │   └── malware_stats.json   # malware-research-lab から push（optional）
│   └── processed/         # build_site.py の成果物（手編集不可）
├── docs/                  # GitHub Pages 配信ファイル（手編集不可）
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   ├── index.md
│   ├── htb-overview.md
│   ├── recent-activity.md
│   ├── skill-radar.html
│   └── technical-score.md
├── scripts/
│   ├── common.py
│   ├── validate_data.py
│   ├── build_dashboard_data.py
│   ├── render_markdown_pages.py
│   ├── render_html_pages.py
│   ├── copy_assets.py
│   └── build_site.py       # 統合入口
├── templates/
│   ├── markdown/
│   └── html/
└── .github/workflows/
    └── build-pages.yml
```

---

## Scripts

| スクリプト | 役割 |
|---|---|
| `validate_data.py` | `data/raw/` の JSON を検証（malware_stats は optional） |
| `build_dashboard_data.py` | raw → processed 変換。malware 統計も含む |
| `render_markdown_pages.py` | テンプレートから `docs/*.md` を生成 |
| `render_html_pages.py` | テンプレートから `docs/*.html` を生成 |
| `copy_assets.py` | CSS / JS / img を `docs/assets/` に反映 |
| `build_site.py` | 上記5ステップの統合入口 |

---

## GitHub Actions

| ワークフロー | 実行タイミング | 処理内容 |
|---|---|---|
| `build-pages.yml` | `data/raw/**` / `scripts/**` / `templates/**` / `assets/**` への push 時 | `build_site.py` 実行 → GitHub Pages デプロイ |

---

## ビルド方針

- Markdown 主体で運用（HTML は必要ページのみ補助的に使う）
- データ整形は Python 側で完了させる
- ワークフローは `python scripts/build_site.py` を呼ぶだけ
- `data/raw/` と `docs/` は手編集しない（templates / scripts で管理）

---

## ローカル実行

```bash
python scripts/build_site.py
```

---

## データ追加の手順

1. `data/raw/` に新しい JSON ファイルを配置
2. `scripts/validate_data.py` の `SCHEMAS` にスキーマを追加
3. `scripts/build_dashboard_data.py` に変換ロジックを追加
4. 対応するテンプレートにプレースホルダーを追加
5. `scripts/render_markdown_pages.py` でプレースホルダーに値を渡す
