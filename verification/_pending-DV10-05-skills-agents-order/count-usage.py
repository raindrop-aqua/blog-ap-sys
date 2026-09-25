#!/usr/bin/env python3
"""Claude Codeのセッションログから、自作スキル・エージェントの呼び出し回数を数える。

数えるのは名前・件数・日付だけで、会話の本文は出力しない。

使い方:
    python3 count-usage.py [ログのフォルダ] [--exclude-session セッションID]

ログのフォルダの既定は ~/Documents/claude-logs-blog-ap-sys（退避先）。
サブフォルダ（サブエージェントのログ）も含めて再帰的に読む。

何を数えるか:
    スキル     : Skill ツールの呼び出し ＋ ユーザーが /名前 と打った回数
    エージェント: Agent（旧名 Task）ツールの subagent_type
同じ呼び出しが再開・圧縮で複数回ログに載る場合があるので、ツール呼び出しはid、
スラッシュコマンドはuuidで重複を除く。日付はログの記録どおりUTC。
"""
import argparse
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

SKILLS = ["write-post", "add-idea", "add-infographic"]
AGENTS = ["idea-generator", "idea-reviewer", "post-reviewer"]

SLASH = re.compile(
    r"^\s*<command-message>[^<]*</command-message>\s*<command-name>/([^<\s]+)</command-name>"
)


def text_of(content):
    """メッセージ本文から、tool_resultを除いたテキストだけを取り出す。"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def short(name):
    """プラグイン名の接頭辞（plugin:name）を落とす。"""
    return name.split(":")[-1] if isinstance(name, str) else str(name)


def scan(root, exclude_session):
    events = []  # (kind, name, via, session, date)
    seen = set()
    files = []
    for f in sorted(Path(root).rglob("*.jsonl")):
        if ".git" in f.parts:
            continue
        session = f.relative_to(root).parts[0].replace(".jsonl", "")
        if session == exclude_session:
            continue
        files.append(f)
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                msg = d.get("message") or {}
                content = msg.get("content")
                date = (d.get("timestamp") or "")[:10]

                if msg.get("role") == "user":
                    m = SLASH.match(text_of(content))
                    if m:
                        key = ("slash", d.get("uuid") or (session, date, m.group(0)))
                        if key not in seen:
                            seen.add(key)
                            events.append(("skill", short(m.group(1)), "slash", session, date))

                if isinstance(content, list):
                    for b in content:
                        if not isinstance(b, dict) or b.get("type") != "tool_use":
                            continue
                        key = ("tool", b.get("id"))
                        if b.get("id") and key in seen:
                            continue
                        seen.add(key)
                        inp = b.get("input") or {}
                        if b.get("name") == "Skill" and inp.get("skill"):
                            events.append(("skill", short(inp["skill"]), "tool", session, date))
                        elif b.get("name") in ("Agent", "Task") and inp.get("subagent_type"):
                            events.append(("agent", short(inp["subagent_type"]), "tool", session, date))
    return files, events


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", nargs="?", default="~/Documents/claude-logs-blog-ap-sys")
    ap.add_argument("--exclude-session", default=None, help="除外するセッションID（例: 今書いている会話）")
    args = ap.parse_args()
    root = os.path.expanduser(args.dir)

    files, events = scan(root, args.exclude_session)
    dates = sorted(e[4] for e in events if e[4])
    print(f"読んだファイル: {len(files)}本 / 集計した呼び出し: {len(events)}件 / 期間: {dates[0] if dates else '-'} 〜 {dates[-1] if dates else '-'}（UTC）")
    print()

    by = defaultdict(list)
    for e in events:
        by[(e[0], e[1])].append(e)

    print(f"種類  {'名前':<18}{'呼び出し':>8}  {'内訳':<16}{'セッション数':>8}  {'最初':<11}{'最後':<11}")
    print("-" * 84)
    for kind, names in (("スキル", SKILLS), ("エージェント", AGENTS)):
        for n in names:
            evs = by.get(("skill" if kind == "スキル" else "agent", n), [])
            ds = sorted(e[4] for e in evs if e[4])
            via = Counter(e[2] for e in evs)
            detail = f"/打鍵{via['slash']} 自動{via['tool']}" if kind == "スキル" else ""
            print(
                f"{kind}  {n:<18}{len(evs):>8}  {detail:<16}"
                f"{len({e[3] for e in evs}):>8}  {ds[0] if ds else '-':<11}{ds[-1] if ds else '-':<11}"
            )

    print()
    print("月別の呼び出し回数")
    months = sorted({e[4][:7] for e in events if e[4]})
    targets = [("skill", n) for n in SKILLS] + [("agent", n) for n in AGENTS]
    print(f"{'名前':<18}" + "".join(f"{m:>9}" for m in months))
    for k, n in targets:
        c = Counter(e[4][:7] for e in by.get((k, n), []) if e[4])
        print(f"{n:<18}" + "".join(f"{c.get(m, 0):>9}" for m in months))

    print()
    print("参考: 上の6本以外で、呼び出しが多かった名前（上位8）")
    mine = set(targets)
    others = Counter()
    for (k, n), evs in by.items():
        if (k, n) not in mine:
            others[(k, n)] = len(evs)
    for (k, n), c in others.most_common(8):
        print(f"  {'スキル' if k == 'skill' else 'エージェント'}  {n}: {c}")


if __name__ == "__main__":
    main()
