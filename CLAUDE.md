# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Jekyll (GitHub Pages) blog, written in Japanese, titled "明日使える生成AI" (Generative AI You Can Use Tomorrow). It publishes practical, business-oriented tips for using ChatGPT/Claude/Copilot. Content and structure decisions should follow the planning docs under `docs/planning/`, split by when you open them:

- `content-strategy.md` — source of truth for concept, personas, category taxonomy, posting cadence, and article format. Open it when deciding direction or where a new idea belongs.
- `article-backlog.md` — the stock of planned articles, per-series plans, and publishing-order dependencies. Open it when choosing what to write next or sequencing posts.
- `writing-style.md` — tone, wording, and the rule for telling first-hand stories without identifying a client site. Open it while actually writing.

Published at: https://raindrop-aqua.github.io/blog-ap-sys/

## Local development

Local preview runs via [Apple Container](https://github.com/apple/container) (not Docker Desktop), requiring macOS 26+ on Apple Silicon with the `container` CLI installed and running (`container system status`).

```sh
./preview.sh
```

This builds the image and runs the container, mounting the current directory for hot reload (`--force_polling` so file changes are detected through the container). Stop with `Ctrl-C` (container auto-removes via `--rm`), or if running detached (`-d`):

```sh
container stop blog-preview
```

Once running, the site is at `http://localhost:4000/blog-ap-sys/` — the `/blog-ap-sys` path suffix is required because `baseurl` is set in `_config.yml`.

There is no separate lint/test/build command — Jekyll build errors surface in the `container` logs when `preview.sh` is running, and the real build happens via GitHub Actions on push (see below).

## Publishing flow

1. Add a post file under `_posts/` (see naming/front matter rules below) and commit/push to GitHub.
2. GitHub Actions builds the site with Jekyll automatically.
3. Check the Actions tab for build completion.
4. Verify at the public URL.

Important: a post whose filename date is in the future will not be published — the `date` front matter must match the filename date.

## Writing posts

File location: `_posts/`, named `YYYY-MM-DD-english-hyphenated-title.md` (e.g. `2026-08-21-chatgpt-prompt-tips.md`).

Required front matter:

```yaml
---
layout: post
title: "記事のタイトル"
date: 2026-08-21
categories: [カテゴリ名]
tags: [ツール名, 職種/シーン, キーワード, 段階タグ]
---
```

- `categories` is a single large classification that also becomes part of the URL path. Keep to the fixed taxonomy in `docs/planning/content-strategy.md` section 3 (`生成AIのきほん`, `プロンプト設計`, `業務効率化`, `ツール比較`, `Tips・小技`, `ニュース`, `開発者向け`, `お知らせ`) unless the strategy doc is updated first — don't invent new categories ad hoc.
- `tags` are cross-cutting keywords (tool name, job role/scene, etc.), multiple allowed. Also add the reader-level tag matching the article's step: `入口` / `ステップアップ` / `現場実践`.
- Every post must carry more than knowledge. Include at least one of: first-hand experience (what actually happened when it was tried, failures included), the shared-constraint perspective (a client-site engineer writing for client-site engineers), or curation (what to learn first, what to ignore). Before finishing, ask "would ChatGPT give an equal or better answer to this same question?" — if yes, one of those three is missing. `開発者向け` posts drift into pure explanation most easily; see `docs/planning/content-strategy.md` sections 1 and 3.
- Body is standard Markdown after the front matter. Internal links can use relative paths — `baseurl` is already handled by `_config.yml`.
- Article shape depends on the category. `docs/planning/content-strategy.md` section 5 maps each category to one of four templates (standard how-to, きほん for concept pieces, comparison, news) and lists the rules for each. Pick the template from that table before drafting — don't default to the how-to shape. Every type leads with the conclusion and states in the first sentence or two whose problem the post solves.

## Build exclusions

`_config.yml`'s `exclude:` list is set explicitly (README, docs/, Dockerfile, preview.sh, Gemfile*, vendor/, node_modules/) because defining a custom `exclude` in Jekyll overrides the default exclude list rather than appending to it. When adding new non-content files/directories to the repo root, add them to this list too or they'll be published into `_site/`.
