# blog-ap-sys

明日使える生成AIテクニックを紹介するサイトです。GitHub Pages（Jekyll）で運用しています。

## 公開URL
https://raindrop-aqua.github.io/blog-ap-sys/

## リポジトリ構成
`_config.yml` の `source: site` により、**`site/` フォルダの中身だけがビルド・公開対象**。`Gemfile`や`Dockerfile`、`CLAUDE.md`などリポジトリ直下に置く開発用ファイルは`site/`の外にあるため、`exclude`設定を追加しなくても自動的に公開対象から外れる。新しく開発用ファイルをルート直下に追加する分には気にする必要はない。

- `site/` … 公開されるJekyllサイト本体（`_posts/`、`index.md`など）
- ルート直下 … 開発用ファイル（Gemfile、Dockerfile、preview.shなど）
- `.github/workflows/pages.yml` … GitHub Actionsによるビルド・デプロイ設定

---

## 記事の書き方

### 1. ファイルの作成場所
`site/_posts/` フォルダの中に、以下のファイル名ルールで作成する。

YYYY-MM-DD-記事タイトル(英語・ハイフン区切り).md

例：`2026-08-21-chatgpt-prompt-tips.md`

### 2. Front Matter（ファイル冒頭の必須項目）

```yaml
---
layout: post
title: "記事のタイトル"
date: 2026-08-21
categories: [カテゴリ名]
tags: [タグ1, タグ2, タグ3]
---
```

- **categories**：記事のURLパスにも反映される大分類（例：ChatGPT, 画像生成, 業務効率化）
- **tags**：横断的に付ける詳細キーワード（複数OK）

### 3. 本文
Front Matterの下から、通常のMarkdownで執筆する。

```markdown
## 見出し

本文はここに書く。

- リスト
- も使える

`コード`や\`\`\`コードブロック\`\`\`も使用可。
```

### 4. 公開までの流れ
1. `site/_posts/` に記事ファイルを作成してGitHubにコミット（push）
2. 数分待つ（GitHub Actionsが自動でJekyllビルド）
3. Actionsタブでビルド完了を確認
4. 公開URLで反映を確認

### 5. 注意点
- ファイル名の日付が未来日だと公開されないので注意（`date`はファイル名と一致させる）
- `baseurl` は `_config.yml` に設定済みのため、記事内リンクは相対パスでOK

---

## ローカルプレビュー環境（Apple Container）

Docker Desktopの代わりに、macOS標準の[Apple Container](https://github.com/apple/container)を使ってJekyllのプレビュー環境を動かせます。

### 前提条件
- macOS 26以降 + Apple Silicon
- `container` CLI がインストール済み（`container system status` で `running` になっていること）

### 起動方法

```sh
./preview.sh
```

[preview.sh](preview.sh) がイメージのビルドとコンテナ起動（カレントディレクトリをマウントしてホットリロード）をまとめて行う。`Ctrl-C`で停止すると`--rm`によりコンテナも自動削除される。

起動後、ブラウザで以下にアクセス（`baseurl` が `/blog-ap-sys` のため末尾のパスが必要）。

```
http://localhost:4000/blog-ap-sys/
```

`site/_posts/` や `_config.yml` を編集すると自動的に再ビルドされます（`--force_polling` によりコンテナ越しのファイル変更も検知）。

### 停止方法

```sh
container stop blog-preview
```

バックグラウンドで動かしたい場合は `run` に `-d` を追加する。
