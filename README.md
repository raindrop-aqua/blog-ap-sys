# blog-ap-sys

明日使える生成AIテクニックを紹介するサイトです。GitHub Pages（Jekyll）で運用しています。

- 公開URL: https://raindrop-aqua.github.io/blog-ap-sys/

## ドキュメント

運用ルールは用途ごとに分かれています。本READMEには手順を書きません（二重管理を避けるため）。

| 文書 | 内容 |
|---|---|
| [CLAUDE.md](CLAUDE.md) | 記事の書き方（ファイル名・front matter・カテゴリ）、ローカルプレビュー、公開フロー |
| [docs/planning/content-strategy.md](docs/planning/content-strategy.md) | コンセプト・読者・カテゴリ分類・投稿戦略・記事フォーマット |
| [docs/planning/article-backlog.md](docs/planning/article-backlog.md) | 記事ネタのストックと公開順 |
| [docs/planning/writing-style.md](docs/planning/writing-style.md) | 文体ガイド |

## ローカルプレビュー

macOS 26以降 + Apple Silicon で [Apple Container](https://github.com/apple/container) が必要です。

```sh
./preview.sh
```

起動後 http://localhost:4000/blog-ap-sys/ を開きます。詳細は [CLAUDE.md](CLAUDE.md) を参照してください。
