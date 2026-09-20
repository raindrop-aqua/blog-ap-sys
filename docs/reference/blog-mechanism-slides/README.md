# ブログのしくみ解説スライド

ブログの仕組み（公開の流れ・Jekyll・フォルダ構成）と、生成AIのしくみをプレゼンで説明するための23枚のスライドの元データ。中学生にも伝わる言葉で書いてあり、最後のページにブログへのQRコードが入る。

- 公開先: https://claude.ai/artifact/E6DbJCMxvrMnwgHzLKC8tM （Claudeのスライド Artifact。非公開なので、見せるには作成者が共有設定をする）
- `project/deck.json` — スライドの順番・章立て・書体
- `project/slides/*.html` — 1枚1ファイル。発表者ノートは各ファイル末尾の `<aside>`
- `build.py` — 上の `project/` を書き出すスクリプト。内容を直すときはここを編集して再実行する

## 作り直し

QRコードの生成に `segno` が要る。

```sh
python3 -m venv .venv && .venv/bin/pip install segno
.venv/bin/python build.py
```

出力した `project/` を Artifact に上げ直すと反映される。ブログの仕組みが変わったら、`../blog-mechanism.html` と合わせて直す。
