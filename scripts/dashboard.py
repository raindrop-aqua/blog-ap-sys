#!/usr/bin/env python3
"""ブログの現状とこれからを1枚にまとめたダッシュボードを作る。

リポジトリの中身（投稿・下書き・ネタ帳・検証フォルダ・git）だけを読み、
dashboard/index.html に書き出す。手で書き足す情報は持たないので、
実行し直せば常に今の状態になる。

    python3 scripts/dashboard.py          # 作って開く
    python3 scripts/dashboard.py --no-open
"""

import datetime as dt
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "site" / "_posts"
DRAFTS = ROOT / "site" / "_drafts"
BACKLOG = ROOT / "docs" / "planning" / "article-backlog.md"
STRATEGY = ROOT / "docs" / "planning" / "content-strategy.md"
VERIFICATION = ROOT / "verification"
OUT = ROOT / "dashboard" / "index.html"

# article-backlog.md 0章。backlog_id を必須にした日（これ以降に公開する記事は持つ）
BACKLOG_ID_SINCE = dt.date(2026, 9, 25)
# content-strategy.md 6章の本数トリガー
COUNT_TRIGGERS = [10, 20]

ID_RE = re.compile(r"(?:KH|PR|GK|TL|TP|NW|DV)\d*-\d{2}")
TODAY = dt.date.today()


# ---------- 読み取り ----------

def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        kv = re.match(r"(\w+):\s*(.*)", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip().strip('"')
        elif line.strip().startswith("path:"):
            fm["image_path"] = line.split(":", 1)[1].strip()
    return fm


def load_posts():
    posts = []
    for path in sorted(POSTS.glob("*.md")):
        fm = front_matter(path)
        date = dt.date.fromisoformat(path.name[:10])
        posts.append({
            "slug": path.stem,
            "file": path.relative_to(ROOT),
            "date": date,
            "fm_date": fm.get("date", ""),
            "title": fm.get("title", path.stem),
            "category": fm.get("categories", "").strip("[]"),
            "backlog_id": fm.get("backlog_id", ""),
            "image": fm.get("image_path", ""),
            "state": "公開済み" if date <= TODAY else "予約",
        })
    drafts = []
    for path in sorted(DRAFTS.glob("*.md")):
        fm = front_matter(path)
        drafts.append({
            "slug": path.stem,
            "file": path.relative_to(ROOT),
            "title": fm.get("title", path.stem),
            "category": fm.get("categories", "").strip("[]"),
            "backlog_id": fm.get("backlog_id", ""),
            "mtime": dt.date.fromtimestamp(path.stat().st_mtime),
        })
    return posts, drafts


def sections(path):
    """'## N. 見出し' ごとに本文を切り分ける。キーは番号の文字列。"""
    out, key = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"## (\d+)\.", line)
        if m:
            key = m.group(1)
            out[key] = []
        elif key:
            out[key].append(line)
    return out


def infer_ids(posts, backlog):
    """backlog_id の無い投稿に、ネタ帳の3章・4章の「YYYY-MM-DD公開」からIDを当てる。"""
    by_date = {p["date"].isoformat(): p for p in posts}
    # その記事自身の行だけを見る（3章の表の行、4章の「N. 📝ID」の項目）。
    # 説明文の中で他の記事の公開日に触れている行を拾わないため
    own = re.compile(r"^\s*(?:\|\s*\d+\s*\||\d+\.)\s*(?:\*\*)?📝(" + ID_RE.pattern + ")")
    for key in ("3", "4"):
        for line in backlog.get(key, []):
            m = own.match(line)
            if not m:
                continue
            for d in re.findall(r"(\d{4}-\d{2}-\d{2})公開", line):
                p = by_date.get(d)
                if p and not p["backlog_id"] and not p.get("inferred_id"):
                    p["inferred_id"] = m.group(1)
    for p in posts:
        p["id"] = p["backlog_id"] or p.get("inferred_id", "")


def strip_md(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.replace("`", "").replace("📝", "")


def load_order(backlog, id_state):
    rows = []
    for line in backlog.get("3", []):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[0].isdigit():
            continue
        ids = ID_RE.findall(cells[1])
        if not ids:
            continue
        aid = ids[0]
        title = strip_md(cells[1])
        title = re.sub(r"^" + re.escape(aid) + r"\s*", "", title)
        title = re.split(r"（", title)[0].strip()
        note = "再検討中" if "再検討中" in cells[1] else ""
        rows.append({
            "no": cells[0], "id": aid, "title": title,
            "category": cells[2].strip("`"), "note": note,
            "state": id_state.get(aid, "未着手"),
        })
    return rows


def unchecked(lines):
    items = []
    for line in lines:
        m = re.match(r"- \[ \] (.*)", line)
        if m:
            items.append(m.group(1))
    return items


def link_items(backlog, id_state):
    items = []
    for text in unchecked(backlog.get("2", [])):
        head = re.split(r"（", text, maxsplit=1)[0]
        parts = re.split(r"→|⇄", head, maxsplit=1)
        src = ID_RE.findall(parts[0])
        dst = ID_RE.findall(parts[1]) if len(parts) > 1 else []
        src_pub = bool(src) and all(id_state.get(i) == "公開済み" for i in src)
        dst_pub = bool(dst) and any(id_state.get(i) == "公開済み" for i in dst)
        if src_pub and dst_pub:
            kind = "now"      # 両方公開済み。追記して済ませられる
        elif dst_pub:
            kind = "write"    # リンク先はある。リンク元を書くときに張る
        else:
            kind = "wait"
        items.append({"head": strip_md(head), "full": strip_md(text), "kind": kind})
    return items


def pending_verifications(id_state, posts):
    out = []
    if not VERIFICATION.exists():
        return out
    by_id = {p["id"]: p for p in posts if p["id"]}
    for d in sorted(VERIFICATION.iterdir()):
        if not d.is_dir() or not d.name.startswith("_pending-"):
            continue
        ids = ID_RE.findall(d.name)
        post = by_id.get(ids[0]) if ids else None
        if post:
            note = f"投稿ファイルが決まった → verification/{post['slug']}/ へ改名"
        elif not ids:
            note = "フォルダ名にIDが無い（_pending-<ID>-<slug> の形に直す）"
        else:
            note = ""
        out.append({"name": d.name, "note": note, "action": bool(note)})
    return out


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def git_state():
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    dirty = [l for l in git("status", "--porcelain").splitlines() if l]
    unmerged = [b.strip(" *") for b in git("branch", "--no-merged", "main").splitlines() if b.strip()]
    merged = [b.strip(" *") for b in git("branch", "--merged", "main").splitlines()
              if b.strip(" *") and b.strip(" *") != "main"]
    ahead = git("rev-list", "--count", "origin/main..main") or "0"
    return {"branch": branch, "dirty": dirty, "unmerged": unmerged,
            "merged": merged, "ahead": ahead}


# ---------- 組み立て ----------

def monday(d):
    return d - dt.timedelta(days=d.weekday())


def weeks(posts):
    """先々週の月曜から8週先までを週単位で並べる。"""
    start = monday(TODAY) - dt.timedelta(weeks=2)
    rows = []
    for i in range(11):
        mon = start + dt.timedelta(weeks=i)
        in_week = [p for p in posts if mon <= p["date"] < mon + dt.timedelta(days=7)]
        rows.append({"monday": mon, "posts": in_week,
                     "past": mon + dt.timedelta(days=6) < TODAY,
                     "current": mon <= TODAY < mon + dt.timedelta(days=7)})
    return rows


def post_checks(p):
    issues = []
    if p["fm_date"] and p["fm_date"] != p["date"].isoformat():
        issues.append("front matter の date がファイル名と違う")
    if not p["backlog_id"] and p["category"] != "お知らせ" and p["date"] >= BACKLOG_ID_SINCE:
        issues.append("backlog_id 未記入" + (f"（{p['inferred_id']} と推定）" if p.get("inferred_id") else ""))
    if not p["image"]:
        issues.append("ヘッダー画像なし")
    elif not (ROOT / "site" / p["image"].lstrip("/")).exists():
        issues.append("ヘッダー画像のファイルが無い")
    return issues


# ---------- HTML ----------

e = html.escape
WD = "月火水木金土日"


def fmt(d):
    return f"{d.month}/{d.day}（{WD[d.weekday()]}）"


def pill(text, kind):
    return f'<span class="pill {kind}">{e(text)}</span>'


def render(posts, drafts, order, links, todos, pending, g):
    published = [p for p in posts if p["state"] == "公開済み"]
    scheduled = [p for p in posts if p["state"] == "予約"]
    week_rows = weeks(posts)

    # --- 次にやること ---
    actions = []
    empty = [w for w in week_rows if w["monday"] >= TODAY and not w["posts"]]
    next_up = [r for r in order if r["state"] == "未着手"]
    if empty:
        cand = f"公開順の次は {next_up[0]['id']} {next_up[0]['title']}" + (
            f"（{next_up[0]['note']}）" if next_up and next_up[0]["note"] else "") if next_up else ""
        actions.append(("warn", f"{fmt(empty[0]['monday'])} の枠が空いています", cand))
    missed = [w for w in week_rows if w["past"] and not w["posts"]]
    if len(missed) >= 2:
        actions.append(("bad", "2週続けて公開できていません",
                        "content-strategy.md 6章のトリガー。投稿頻度とネタの選び方を見直す"))
    for p in posts:
        for issue in post_checks(p):
            actions.append(("warn", f"{p['date'].isoformat()} の記事: {issue}", str(p["file"])))
    for l in links:
        if l["kind"] == "now":
            actions.append(("warn", "リンクを追記できます", l["head"]))
    for v in pending:
        if v["action"]:
            actions.append(("info", f"検証フォルダ {v['name']}", v["note"]))
    n = len(published)
    nxt = next((t for t in COUNT_TRIGGERS if t > n), None)
    if g["dirty"]:
        actions.append(("info", f"未コミットの変更が {len(g['dirty'])} 件", "ブランチ: " + g["branch"]))
    for b in g["unmerged"]:
        actions.append(("info", f"main に未マージのブランチ: {b}", "作業途中なら再開、不要なら削除"))

    parts = []
    parts.append(f"""
<header>
  <div>
    <h1>明日使える生成AI ― 運営ダッシュボード</h1>
    <p class="sub">{TODAY.isoformat()} 時点 ／ <code>python3 scripts/dashboard.py</code> で作り直し</p>
  </div>
  <div class="stats">
    <div><b>{len(published)}</b><span>公開済み</span></div>
    <div><b>{len(scheduled)}</b><span>予約</span></div>
    <div><b>{len(drafts)}</b><span>下書き</span></div>
    <div><b>{len(todos)}</b><span>未完ToDo</span></div>
  </div>
</header>""")

    # 次にやること
    items = "".join(
        f'<li class="{k}"><b>{e(t)}</b>{f"<span>{e(d)}</span>" if d else ""}</li>' for k, t, d in actions
    ) or '<li class="ok"><b>今すぐ片付けるものはありません</b></li>'
    trig = f"content-strategy.md 6章の見直しトリガー（公開{nxt}本）まで あと{nxt - n}本" if nxt else ""
    parts.append(f'<section class="wide"><h2>次にやること</h2><ul class="actions">{items}</ul>'
                 f'<p class="note">{e(trig)}</p></section>')

    # 週ごとの公開予定
    rows = []
    for w in week_rows:
        cls = "current" if w["current"] else ("past" if w["past"] else "")
        if w["posts"]:
            cell = "".join(
                f'<div>{pill(p["state"], "pub" if p["state"] == "公開済み" else "sch")} '
                f'<span class="id">{e(p["id"])}</span> {e(p["title"])}'
                f'<small>{e(fmt(p["date"]))} ・ {e(p["category"])}</small></div>' for p in w["posts"])
        else:
            cell = pill("未公開", "bad") if w["past"] else pill("空き", "warn")
        rows.append(f'<tr class="{cls}"><th>{e(fmt(w["monday"]))}〜</th><td>{cell}</td></tr>')
    parts.append('<section class="wide"><h2>週ごとの公開予定</h2>'
                 '<p class="note">週1本・月曜公開。先々週から8週先まで。</p>'
                 f'<table class="weeks">{"".join(rows)}</table></section>')

    # 公開順
    rows = []
    for r in order:
        kind = {"公開済み": "pub", "予約": "sch"}.get(r["state"], "todo")
        rows.append(f'<tr class="{kind}"><td>{e(r["no"])}</td><td class="id">{e(r["id"])}</td>'
                    f'<td>{e(r["title"])}{" " + pill(r["note"], "warn") if r["note"] else ""}</td>'
                    f'<td>{pill(r["state"], kind)}</td></tr>')
    parts.append('<section><h2>公開順（ネタ帳 3章）</h2>'
                 f'<table class="list">{"".join(rows)}</table></section>')

    # 下書き
    rows = "".join(
        f'<li><b>{e(d["title"])}</b><small>{e(d["category"])} ・ 最終更新 {e(d["mtime"].isoformat())}'
        f' ・ {e(str(d["file"]))}</small></li>' for d in drafts) or "<li>なし</li>"
    pend = "".join(
        f'<li><b>{e(v["name"])}</b>{f"<small>{e(v["note"])}</small>" if v["note"] else ""}</li>'
        for v in pending) or "<li>なし</li>"
    parts.append(f'<section><h2>書きかけ</h2><h3>下書き（site/_drafts）</h3><ul class="plain">{rows}</ul>'
                 f'<h3>公開前の検証データ（verification/_pending-*）</h3><ul class="plain">{pend}</ul></section>')

    # ToDo
    rows = "".join(
        f'<li><span class="src">{e(src)}</span>{e(strip_md(t))}</li>' for src, t in todos)
    parts.append(f'<section><h2>未完のToDo</h2><ul class="todo">{rows}</ul></section>')

    # リンク待ち
    label = {"now": ("追記できる", "warn"), "write": ("リンク元を書くときに張る", "sch"), "wait": ("リンク先待ち", "todo")}
    rows = []
    for kind in ("now", "write", "wait"):
        for l in [x for x in links if x["kind"] == kind]:
            t, c = label[kind]
            rows.append(f'<li><details><summary>{pill(t, c)} {e(l["head"])}</summary>'
                        f'<p>{e(l["full"])}</p></details></li>')
    parts.append('<section><h2>リンク待ち（ネタ帳 2章）</h2>'
                 '<p class="note">IDの公開状況から自動判定。細部は各行を開いて確認する。</p>'
                 f'<ul class="links">{"".join(rows)}</ul></section>')

    # 記事一覧
    rows = []
    for p in reversed(posts):
        issues = post_checks(p)
        vdir = (VERIFICATION / p["slug"]).exists()
        idcell = e(p["backlog_id"]) or (f'<span class="muted">{e(p.get("inferred_id", ""))}?</span>'
                                         if p.get("inferred_id") else "")
        rows.append(
            f'<tr><td>{e(p["date"].isoformat())}</td>'
            f'<td>{pill(p["state"], "pub" if p["state"] == "公開済み" else "sch")}</td>'
            f'<td class="id">{idcell}</td><td>{e(p["title"])}<small>{e(p["category"])}</small></td>'
            f'<td>{"✓" if p["image"] else "—"}</td><td>{"✓" if vdir else "—"}</td>'
            f'<td>{"".join(pill(i, "warn") for i in issues)}</td></tr>')
    parts.append('<section class="wide"><h2>記事一覧</h2>'
                 '<p class="note">ID の「?」は backlog_id が無く、ネタ帳の日付から推定したもの。</p>'
                 '<div class="scroll"><table class="list posts"><tr><th>日付</th><th>状態</th><th>ID</th>'
                 '<th>タイトル</th><th>画像</th><th>検証</th><th>要確認</th></tr>'
                 f'{"".join(rows)}</table></div></section>')

    # git
    merged = ", ".join(g["merged"]) or "なし"
    parts.append(f'<section class="wide"><h2>git</h2><ul class="plain">'
                 f'<li><b>現在のブランチ</b><small>{e(g["branch"])} ・ 未コミット {len(g["dirty"])} 件'
                 f' ・ origin より {e(g["ahead"])} コミット先行</small></li>'
                 f'<li><b>main に未マージ</b><small>{e(", ".join(g["unmerged"]) or "なし")}</small></li>'
                 f'<li><b>マージ済みで残っているブランチ（{len(g["merged"])}本）</b><small>{e(merged)}</small></li>'
                 '</ul></section>')

    return TEMPLATE.replace("{{BODY}}", "\n".join(parts))


TEMPLATE = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>運営ダッシュボード</title>
<style>
:root {
  --bg: #f6f5f2; --card: #ffffff; --ink: #1f2328; --muted: #6b7078; --line: #e3e1dc;
  --pub: #2f7d4f; --pub-bg: #e3f2e8; --sch: #2f5f9e; --sch-bg: #e4edf8;
  --warn: #8a5a00; --warn-bg: #fbf0d9; --bad: #a33a2c; --bad-bg: #f8e2de;
  --todo: #5c6370; --todo-bg: #eceef1; --accent: #2f5f9e;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #16181c; --card: #1f2227; --ink: #e6e6e3; --muted: #9aa0a8; --line: #2e3238;
    --pub: #7fcf9c; --pub-bg: #1d3326; --sch: #8fb6ea; --sch-bg: #1c2a3d;
    --warn: #e8c070; --warn-bg: #3a2f17; --bad: #ef9486; --bad-bg: #3d1f1b;
    --todo: #b0b6bf; --todo-bg: #2a2e34; --accent: #8fb6ea;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); line-height: 1.7;
  font-family: "BIZ UDPGothic", "Hiragino Sans", "Hiragino Kaku Gothic ProN", sans-serif; }
main { max-width: 1180px; margin: 0 auto; padding: 24px 16px 64px;
  display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 480px), 1fr)); gap: 16px; }
header { grid-column: 1 / -1; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: end; gap: 16px; }
h1 { font-size: 1.4rem; margin: 0; }
.sub { margin: 4px 0 0; color: var(--muted); font-size: .85rem; }
.stats { display: flex; gap: 10px; }
.stats div { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 8px 14px; text-align: center; min-width: 76px; }
.stats b { display: block; font-size: 1.5rem; line-height: 1.2; font-variant-numeric: tabular-nums; }
.stats span { font-size: .75rem; color: var(--muted); }
section { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px 20px; min-width: 0; }
section.wide { grid-column: 1 / -1; }
h2 { font-size: 1.05rem; margin: 0 0 10px; }
h3 { font-size: .9rem; margin: 14px 0 6px; color: var(--muted); }
.note { color: var(--muted); font-size: .8rem; margin: 0 0 10px; }
small { display: block; color: var(--muted); font-size: .78rem; }
code { font-size: .85em; }
ul { list-style: none; margin: 0; padding: 0; }
.actions li { padding: 8px 12px; border-left: 4px solid var(--todo); background: var(--todo-bg); border-radius: 6px; margin-bottom: 6px; }
.actions li.warn { border-color: var(--warn); background: var(--warn-bg); }
.actions li.bad { border-color: var(--bad); background: var(--bad-bg); }
.actions li.ok { border-color: var(--pub); background: var(--pub-bg); }
.actions span { display: block; font-size: .82rem; color: var(--muted); }
.pill { display: inline-block; font-size: .72rem; padding: 1px 8px; border-radius: 99px; white-space: nowrap; font-weight: bold; margin-right: 2px; }
.pill.pub { color: var(--pub); background: var(--pub-bg); }
.pill.sch { color: var(--sch); background: var(--sch-bg); }
.pill.warn { color: var(--warn); background: var(--warn-bg); }
.pill.bad { color: var(--bad); background: var(--bad-bg); }
.pill.todo { color: var(--todo); background: var(--todo-bg); }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
td, th { padding: 7px 8px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
.weeks th { width: 7.5em; white-space: nowrap; font-weight: normal; color: var(--muted); }
.weeks tr.current th { color: var(--accent); font-weight: bold; }
.weeks tr.current td, .weeks tr.current th { background: color-mix(in srgb, var(--sch-bg) 50%, transparent); }
.weeks tr.past { opacity: .6; }
.weeks td div + div { margin-top: 6px; }
.id { font-family: ui-monospace, "SF Mono", monospace; font-size: .8rem; white-space: nowrap; color: var(--accent); }
.muted { color: var(--muted); }
.list tr.pub td:not(:last-child) { color: var(--muted); }
.posts th { font-size: .78rem; color: var(--muted); font-weight: normal; }
.scroll { overflow-x: auto; }
.plain li { padding: 6px 0; border-bottom: 1px solid var(--line); }
.plain li:last-child { border-bottom: 0; }
.todo li { padding: 7px 0; border-bottom: 1px solid var(--line); font-size: .88rem; }
.src { display: inline-block; font-size: .7rem; color: var(--muted); border: 1px solid var(--line); border-radius: 4px; padding: 0 5px; margin-right: 6px; }
.links li { border-bottom: 1px solid var(--line); font-size: .86rem; }
.links summary { padding: 6px 0; cursor: pointer; }
.links details p { margin: 0 0 8px; color: var(--muted); font-size: .8rem; }
</style>
</head>
<body><main>
{{BODY}}
</main></body>
</html>
"""


def main():
    posts, drafts = load_posts()
    backlog = sections(BACKLOG)
    strategy = sections(STRATEGY)
    infer_ids(posts, backlog)
    id_state = {}
    for p in posts:
        if p["id"]:
            id_state[p["id"]] = p["state"]
    order = load_order(backlog, id_state)
    links = link_items(backlog, id_state)
    todos = [("ネタ帳 5章", t) for t in unchecked(backlog.get("5", []))] + \
            [("方針 7章", t) for t in unchecked(strategy.get("7", []))]
    pending = pending_verifications(id_state, posts)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(render(posts, drafts, order, links, todos, pending, git_state()), encoding="utf-8")
    print(OUT.relative_to(ROOT))
    if "--no-open" not in sys.argv and sys.platform == "darwin":
        subprocess.run(["open", str(OUT)])


if __name__ == "__main__":
    main()
