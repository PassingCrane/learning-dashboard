# learning-dashboard

`learning-dashboard` は 4リポジトリ構成のうち、**GitHub Pages による可視化専用** の public リポジトリです。正本データは持たず、`security-learning` と `htb-writeups` から受け取った raw JSON を加工して、Markdown / HTML ページを生成します。fileciteturn0file5

## 役割

- 表示専用 repo
- raw data の受け取り先
- processed data の生成
- GitHub Pages 配信用 `docs/` の生成

この repo の責務分離は、4リポジトリ構成の前提とも一致しています。`learning-dashboard` は可視化、`security-learning` は内部データ正本、`htb-writeups` は HTB 作業本体、`security-portfolio` は公開成果物です。fileciteturn0file0

## 想定ディレクトリ

```text
learning-dashboard/
├── README.md
├── HANDOVER.md
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── assets/
├── templates/
│   ├── markdown/
│   └── html/
├── scripts/
│   ├── common.py
│   ├── validate_data.py
│   ├── build_dashboard_data.py
│   ├── render_markdown_pages.py
│   ├── render_html_pages.py
│   ├── copy_assets.py
│   └── build_site.py
└── .github/
    └── workflows/
        └── build-pages.yml
```

## ビルド方針

- Markdown 主体で運用する
- HTML は必要ページだけ補助的に使う
- データ整形は Python 側で完了させる
- workflow からは `python scripts/build_site.py` を統合入口として呼ぶ

この方針は `learning-dashbord_setting.md` の「Markdown主体 + 一部HTML補助」と一致しています。fileciteturn0file5

## scripts の役割

### `validate_data.py`
- raw JSON の存在確認
- JSON構文チェック
- 必須キー確認

### `build_dashboard_data.py`
- raw → processed 変換
- Markdown / HTML 共通の表示用 JSON を生成
- `top_skills` では数値化可能な項目のみ採用

### `render_markdown_pages.py`
- `templates/markdown/*.template.md` から `docs/*.md` を生成

### `render_html_pages.py`
- `templates/html/*.template.html` から `docs/*.html` を生成
- 初期想定は `skill-radar.html`

### `copy_assets.py`
- CSS / JS / img を `docs/assets/` に反映

### `build_site.py`
- validate → processed 生成 → Markdown 描画 → HTML 描画 → asset 反映の統合入口

## ローカル実行

```bash
python scripts/build_site.py
```

## GitHub Actions 例

```yaml
- name: Build site
  run: python scripts/build_site.py
```

## 補足

現時点での最小完成系は、raw JSON を受け取り、processed JSON を作り、Markdown ページを生成できる構成です。今後は必要に応じて `skill-radar.html` のような一部HTMLページだけ追加していく運用が保守しやすいです。fileciteturn0file5
