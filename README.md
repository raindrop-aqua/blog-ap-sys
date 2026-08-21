# blog-ap-sys

明日使える生成AIテクニックを紹介するサイトです。GitHub Pages（Jekyll）で運用しています。

## 公開URL
https://raindrop-aqua.github.io/blog-ap-sys/

---

## 記事の書き方

### 1. ファイルの作成場所
`_posts/` フォルダの中に、以下のファイル名ルールで作成する。

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
1. `_posts/` に記事ファイルを作成してGitHubにコミット（push）
2. 数分待つ（GitHub Actionsが自動でJekyllビルド）
3. Actionsタブでビルド完了を確認
4. 公開URLで反映を確認

### 5. 注意点
- ファイル名の日付が未来日だと公開されないので注意（`date`はファイル名と一致させる）
- `baseurl` は `_config.yml` に設定済みのため、記事内リンクは相対パスでOK
