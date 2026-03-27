# Learning Dashboard

## ■ 概要

このリポジトリは、セキュリティ学習の進捗を可視化するためのダッシュボードです。
GitHub Pages を利用し、以下を自動生成・公開します。

- 技術スコア
- スキルレーダー
- HTB統計
- 学習進捗

---

## ■ リポジトリの役割

| 種類 | リポジトリ |
|------|------------|
| 内部データ | security-learning |
| 演習記録 | htb-writeups |
| 可視化 | learning-dashboard |
| 成果物 | security-portfolio |

---

## ■ ディレクトリ構成

```bash

learning-dashboard/
├── data/
│ ├── raw/ # 元データ（他repoから受信）
│ └── processed/ # 表示用データ
├── docs/ # GitHub Pages表示
├── scripts/ # データ加工・生成
├── templates/ # Markdownテンプレート
└── .github/workflows/
```

---

## ■ データフロー

```bash
security-learning
│
├── data/*.json
▼
learning-dashboard/data/raw
▼
scripts/build_dashboard_data.py
▼
data/processed
▼
scripts/generate_pages.py
▼
docs/
▼
GitHub Pages
```

---

## ■ build 手順（ローカル）

```bash
python scripts/validate_data.py
python scripts/build_dashboard_data.py
python scripts/generate_pages.py
```

## ■ GitHub Pages
- docs/ を公開ディレクトリとして使用
- `.nojekyll` によりそのまま配信

## ■ データ更新元

このリポジトリは以下から自動更新されます。

- security-learning
- htb-writeups

※ 手動編集は基本不要

## ■ 更新フロー
1. security-learning が data を生成
2. learning-dashboard に push
3. workflow が pages を再生成
4. GitHub Pages に反映

## ■ 方針
- 表示はここに集約
- データの正本は持たない
- 完全自動更新

## ■ 目的

👉 学習状況を「見える化」し、継続と成長を促進する