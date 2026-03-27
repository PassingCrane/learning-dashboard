# learning-dashboard HANDOVER

## 1. 位置づけ

`learning-dashboard` は **GitHub Pages による可視化専用 repo** です。正本データを持たず、`security-learning` と `htb-writeups` の raw data を受け取り、Pages 配信用の表示データとページを生成します。fileciteturn0file5turn0file0

## 2. 現方針

- Markdown ベース運用
- 一部ページのみ HTML 補助
- データ整形は Python scripts 側で実施
- workflow は最終的に `build_site.py` を呼ぶ形へ寄せる

この方針は、保守性を重視して Markdown 主体にする設計として整理済みです。fileciteturn0file5

## 3. 現時点の完成形ひな形

### scripts
- `common.py`
- `validate_data.py`
- `build_dashboard_data.py`
- `render_markdown_pages.py`
- `render_html_pages.py`
- `copy_assets.py`
- `build_site.py`

### templates
- `templates/markdown/index.template.md`
- `templates/markdown/technical-score.template.md`
- `templates/markdown/htb-overview.template.md`
- `templates/markdown/recent-activity.template.md`
- `templates/html/skill-radar.template.html`

## 4. build_site.py の役割

統合入口です。以下の順で実行します。

1. `validate_data.py`
2. `build_dashboard_data.py`
3. `render_markdown_pages.py`
4. `render_html_pages.py`
5. `copy_assets.py`

workflow 側を単純化し、今後 HTML ページが増えても Actions を大きく変えずに済むようにしています。これは今後の推奨運用とも一致します。fileciteturn0file5

## 5. build_dashboard_data.py の注意点

過去に `skill_radar.json` の型揺れで `top_skills` ソート時に build が落ちたため、数値化できる値だけ採用する実装にしてあります。`list` や `dict` が入っていてもそのまま比較しない設計にするのが前提です。fileciteturn0file5

## 6. 今後の追加候補

高優先
- `build_navigation.py` の追加
- `navigation.json` の生成
- `.github/workflows/build-pages.yml` を `build_site.py` 呼び出しに統一

中優先
- `docs/assets/css/` と `docs/assets/js/` の整備
- `skill-radar.html` の見た目強化
- `index.html` の補助トップ化

低優先
- UI 強化
- JS グラフ追加
- ナビゲーションの自動埋め込み

## 7. 運用ルール

- `data/raw/` は外部ソースから受け取る
- `data/processed/` は build 成果物
- `docs/` は Pages 配信用の生成物
- 正本データは learning-dashboard に置かない
- ページを手編集しない。変更は `raw/` か `templates/` か `scripts/` で行う

## 8. 次にやるとよいこと

1. 既存 `build-pages.yml` を `python scripts/build_site.py` に寄せる
2. `templates/markdown/` と `templates/html/` をこのひな形に合わせて整える
3. `docs/assets/` の CSS / JS を追加する
4. `navigation.json` とナビ生成を入れる

## 9. 参照元

- `learning-dashbord_setting.md` の運用方針と完成形案fileciteturn0file5
- 4リポジトリ構成の責務分離メモfileciteturn0file0
- 完成形4リポジトリ想定ディレクトリ構造fileciteturn0file2
