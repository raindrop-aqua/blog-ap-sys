# ブログのしくみ解説スライド（AI重点版・40枚）

`../blog-mechanism-slides/`（23枚版）とは別のバージョン。AIに興味がある聴衆向けに、スキルとサブエージェントの説明を厚くし、パートの間に「扉」スライドを入れてある。中学生にも伝わる言葉で書き、最後のページにブログへのQRコードが入る。

- 公開先: https://claude.ai/artifact/J3QXCeXQemaw3u6YEhHSmW （Claudeのスライド Artifact。非公開なので、見せるには作成者が共有設定をする）
- 構成: 1 ブログのしくみ / 2 AIのしくみ / 3 スキル / 4 サブエージェント / 5 人とAIの分担。各パートの先頭に、5パートの現在地を示す扉スライドが入る
- `project/deck.json` — スライドの順番・章立て・書体
- `project/slides/*.html` — 1枚1ファイル。発表者ノートは各ファイル末尾の `<aside>`
- `build.py` — 上の `project/` を書き出すスクリプト。内容を直すときはここを編集して再実行する

## 作り直し

QRコードの生成に `segno` が要る。

```sh
python3 -m venv .venv && .venv/bin/pip install segno
.venv/bin/python build.py
```

出力した `project/` を Artifact に上げ直すと反映される。スキルやサブエージェントを増減したときは、`.claude/skills/`・`.claude/agents/` の中身と合わせて直す。
