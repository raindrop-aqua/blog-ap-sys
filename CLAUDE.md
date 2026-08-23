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

1. Add a post file under `site/_posts/` (see naming/front matter rules below) and commit/push to GitHub.
2. GitHub Actions builds the site with Jekyll automatically.
3. Check the Actions tab for build completion.
4. Verify at the public URL.

Important: a post whose filename date is in the future will not be published — the `date` front matter must match the filename date.

## Writing posts

記事を1本書くときは、まず `/write-post` スキル（`.claude/skills/write-post/SKILL.md`）を使う。ネタ選び → 一次体験のヒアリング → 構成 → 下書き → 校閲 → 保存 → 周辺ドキュメント更新までを対話で通す手順書で、`docs/planning/` の3本をフェーズごとに読み直す作りになっている。書き上がった下書きの校閲は `post-reviewer` サブエージェント（`.claude/agents/post-reviewer.md`）が担当する。

書きかけは `site/_drafts/` に置く。GitHub Actions のビルド（`jekyll build`）は `_drafts` を含めないので push しても公開されず、ローカルの `./preview.sh` は `--drafts` 付きで起動するため見た目だけ確認できる。

以下は保存する記事そのものの仕様。

File location: `site/_posts/`, named `YYYY-MM-DD-english-hyphenated-title.md` (e.g. `2026-08-21-chatgpt-prompt-tips.md`).

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

- `categories` is a single large classification. It drives the `/categories/<name>/` listing page and the sidebar's カテゴリー tab — the main way readers reach older posts — but it is *not* part of the post URL (posts live at `/posts/<filename-slug>/`). Keep to the fixed taxonomy in `docs/planning/content-strategy.md` section 3 (`生成AIのきほん`, `プロンプト設計`, `業務効率化`, `ツール比較`, `Tips・小技`, `ニュース`, `開発者向け`, `お知らせ`) unless the strategy doc is updated first — don't invent new categories ad hoc.
- `tags` are cross-cutting keywords (tool name, job role/scene, etc.), multiple allowed. Also add the reader-level tag (`入口` / `ステップアップ` / `現場実践`), which is **determined by the category** — take the default from the category table in `docs/planning/content-strategy.md` section 3 rather than deciding per article. Only `プロンプト設計` and `業務効率化` need a judgment call.
- Every post must carry more than knowledge. Include at least one of: first-hand experience (what actually happened when it was tried, failures included), the shared-constraint perspective (a client-site engineer writing for client-site engineers), or curation (what to learn first, what to ignore). Before finishing, ask "would ChatGPT give an equal or better answer to this same question?" — if yes, one of those three is missing. `開発者向け` posts drift into pure explanation most easily; see `docs/planning/content-strategy.md` sections 1 and 3.
- Body is standard Markdown after the front matter. Internal links can use relative paths — `baseurl` is already handled by `_config.yml`.
- Article shape depends on the category. `docs/planning/content-strategy.md` section 5 maps each category to one of four templates (standard how-to, きほん for concept pieces, comparison, news) and lists the rules for each. Pick the template from that table before drafting — don't default to the how-to shape. Every type leads with the conclusion and states in the first sentence or two whose problem the post solves.

## Theme and layout

The site uses the **Chirpy** theme (`jekyll-theme-chirpy` gem, pinned `~> 7.6` in the root `Gemfile`), not minima. Chirpy needs Jekyll 4.x, so the build no longer goes through the `github-pages` gem — the theme gem pulls in jekyll, jekyll-paginate, jekyll-seo-tag, jekyll-archives, jekyll-sitemap, and jekyll-include-cache as runtime dependencies, and Jekyll auto-requires them. Don't add a `plugins:` list to `_config.yml` for those.

Everything the theme provides (layouts, includes, sass, JS bundles, the `ja-JP` UI locale) lives inside the gem. The repo only holds the small set of files that override or feed it, all under `site/`:

| Path | Role |
|---|---|
| `site/index.html` | Home page (`layout: home`), post list |
| `site/_tabs/*.md` | Sidebar tabs. `order:` sets the position, `icon:` is a Font Awesome class. `about.md` has real content; the other three are just `layout:` stubs the theme fills in |
| `site/_data/contact.yml` | Sidebar contact icons. The email entry is removed on purpose — `social.email` in `_config.yml` is left blank so the address isn't published |
| `site/_data/share.yml` | Share buttons under each post (X / Facebook / はてなブックマーク) |
| `site/_plugins/posts-lastmod-hook.rb` | Sets `last_modified_at` from git history, so edited posts show an updated date |
| `site/_includes/metadata-hook.html` | Chirpy's `<head>` extension point. Loads the Japanese and monospace web fonts |
| `site/assets/css/jekyll-theme-chirpy.scss` | Style overrides (see below) |
| `site/assets/img/favicons/` | Favicons. The PNGs are generated from `favicon.svg` with `rsvg-convert` |

To change a theme layout or include, copy the file out of the gem (`bundle show jekyll-theme-chirpy`) into the matching path under `site/` — the site's copy wins.

### Style overrides

All custom CSS lives in `site/assets/css/jekyll-theme-chirpy.scss`, which re-declares the theme's own entry point. The leading `@use 'abstracts/variables' with (...)` block must stay first — Sass rejects `@use ... with` after any rule. What's overridden and why:

- **Fonts** — Latin stays on the theme's Source Sans Pro / Lato, Japanese falls through to **BIZ UDPGothic**. The theme's default stack ends in `'Microsoft Yahei'`, which renders Japanese with Chinese glyph shapes; never leave it in. Code is Source Code Pro via Bootstrap's `--bs-font-monospace`. The two web fonts BIZ UDPGothic and Source Code Pro are loaded in `site/_includes/metadata-hook.html`; changing the font stack means changing that link too.
- **Line height** — `main` goes from the theme's 1.75 to 1.9 with slight letter-spacing, because Japanese looks cramped at the theme default. Headings and code are exempted.
- **Link color** — desaturated from the theme's `#0056b2`. Chirpy emits its color variables under three selectors (`:root[data-bs-theme='light']`, `:root[data-bs-theme='dark']`, and `:root:not([data-bs-theme])` inside a `prefers-color-scheme` media query). Any color override has to repeat all three **in that order** — specificity is equal, so source order decides which wins.

PWA/service worker is disabled in `_config.yml` (`pwa.enabled: false`) to avoid stale-cache confusion on the `baseurl` sub-path.

## What gets published

`_config.yml` sets `source: site`, so only `site/` is a build input. Files at the repo root (`CLAUDE.md`, `README.md`, `docs/`, `Gemfile`, `Dockerfile`, `preview.sh`) are outside the source tree and can never leak into `_site/` — there is deliberately no `exclude:` list to maintain. Anything that should be published has to go under `site/`.
