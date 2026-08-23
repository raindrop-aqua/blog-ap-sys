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

## Claude Code での作業

やることごとに入口（スキル）が決まっています。**中の手順はスキル側が持っているので、ここには入口だけ書きます。**

| やりたいこと | 入口 | 打ち方の例 |
|---|---|---|
| 記事を1本書く | `/write-post` | `/write-post` （そのままでよい。ネタ選びから始まる） |
| ネタを思いついた | `/add-idea` | `/add-idea 議事録をAIに書かせたら決定事項は拾えたのに誰が言ったかが全部消えた` |
| ニュース・外部記事からネタを起こす | `/add-idea` | `/add-idea https://... 新モデルの話。現場での話のタネになりそう` |
| ネタが浮かばない | `/add-idea` | `/add-idea 何かいいネタある？` |

- **ネタ本体を同じ行に書くと1往復減ります。** `/add-idea` は文面から起点（思いつき／体験／外部情報／起点なし）を見分けて掘り方を変えるため、書いてあるほど早く進みます
- `/` を付けず「ネタ思いついた」「記事書きたい」のような言い方でも起動します。確実に走らせたいときだけ明示してください
- 校閲（`post-reviewer`）・ネタの切り口出し（`idea-generator`）・ネタ帳の審査（`idea-reviewer`）はスキルが自動で呼ぶので、**直接呼ぶ必要はありません**
- 「今日はここまで」と言えばどちらのスキルも途中で切り上げます。`/write-post` は `site/_drafts/` に下書きを、`/add-idea` はネタ帳に1行を残して終わります

各スキルの中身は [.claude/skills/](.claude/skills/)、サブエージェントは [.claude/agents/](.claude/agents/) にあります。

## ローカルプレビュー

macOS 26以降 + Apple Silicon で [Apple Container](https://github.com/apple/container) が必要です。

```sh
./preview.sh
```

起動後 http://localhost:4000/blog-ap-sys/ を開きます。詳細は [CLAUDE.md](CLAUDE.md) を参照してください。
