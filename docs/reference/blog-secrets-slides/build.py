import json, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(ROOT, "project", "slides"), exist_ok=True)
QR_SVG = open(os.path.join(ROOT, "qr.svg")).read()

# palette
INK = "#16233B"; PAPER = "#F4F7FC"; CARD = "#FBFCFE"; TINT = "#E1EAFF"
BLUE = "#2F62E6"; BLUE_T = "#2350C9"
SUN = "#FFC83D"; SUN_SOFT = "#FFF0BD"
MUTED = "#56647E"; LINE = "#D3DBEA"
OK = "#157A4B"; NO = "#B83B37"; OK_BG = "#DBF4E7"; NO_BG = "#FCE3E1"
D_TEXT = "#F4F7FC"; D_MUTED = "#A9B6D0"; D_ACC = "#86A8FF"; D_CARD = "#1F3050"; D_LINE = "#34466B"

DISPLAY = "'Zen Maru Gothic', 'BIZ UDPGothic', sans-serif"
BODY = "'BIZ UDPGothic', sans-serif"
MONO = "'Source Code Pro', monospace"

slides = []


def p(text, size=32, color=INK, weight=400, extra="", lh=1.6):
    return f'<p style="font-size:{size}px; color:{color}; font-weight:{weight}; line-height:{lh}; {extra}">{text}</p>'


def h3(text, size=40, color=INK, extra=""):
    return f'<h3 style="font-family:{DISPLAY}; font-size:{size}px; font-weight:700; line-height:1.3; color:{color}; {extra}">{text}</h3>'


def row(inner, gap=32, extra=""):
    return f'<div style="display:flex; flex-direction:row; gap:{gap}px; {extra}">{inner}</div>'


def col(inner, gap=16, extra=""):
    return f'<div style="display:flex; flex-direction:column; gap:{gap}px; {extra}">{inner}</div>'


def card(inner, bg=CARD, border=LINE, pad="32px 36px", gap=12, extra=""):
    return (f'<div style="display:flex; flex-direction:column; gap:{gap}px; background:{bg}; '
            f'border:2px solid {border}; border-radius:28px; padding:{pad}; {extra}">{inner}</div>')


def pill(text, bg, color, size=28, extra=""):
    return (f'<p style="font-size:{size}px; font-weight:700; line-height:1.4; background:{bg}; color:{color}; '
            f'padding:6px 24px; border-radius:999px; {extra}">{text}</p>')


def arrow_r(color=BLUE, w=56):
    return f'<x-shape kind="arrow-right" style="flex:none; align-self:center; width:{w}px; height:32px; background:{color}"></x-shape>'


def arrow_l(color=BLUE, w=56):
    return f'<x-shape kind="arrow-left" style="flex:none; align-self:center; width:{w}px; height:32px; background:{color}"></x-shape>'


def arrow_d(color=BLUE):
    return f'<x-shape kind="arrow-down" style="flex:none; align-self:center; width:32px; height:48px; background:{color}"></x-shape>'


def icon_tile(name, bg=BLUE, fg="#FFFFFF", size=96, icon=56):
    return (f'<div style="flex:none; width:{size}px; height:{size}px; background:{bg}; border-radius:24px; '
            f'display:flex; align-items:center; justify-content:center">'
            f'<x-icon name="{name}" style="color:{fg}; width:{icon}px; height:{icon}px"></x-icon></div>')


def head(eyebrow, title, dark=False):
    ec = D_ACC if dark else BLUE_T
    tc = D_TEXT if dark else INK
    return col(
        f'<p style="font-size:26px; font-weight:700; letter-spacing:3px; color:{ec}; line-height:1.4">{eyebrow}</p>'
        f'<h2 style="font-family:{DISPLAY}; font-size:64px; font-weight:900; line-height:1.25; color:{tc}">{title}</h2>',
        gap=10)


def add(sid, body, notes, bg=PAPER, dark=False, section=None, footer=True, pad="128px 128px 160px",
        gap=44, justify="flex-start", align="stretch", direction="column", transition="fade", backdrop=""):
    color = D_TEXT if dark else INK
    fcol = D_MUTED if dark else MUTED
    foot = ""
    if footer:
        foot = (f'<p style="position:absolute; left:128px; bottom:64px; width:1100px; font-size:24px; color:{fcol}; line-height:1.4">'
                f'明日使える生成AI ／ ブログのひみつ</p>'
                f'<p style="position:absolute; right:128px; bottom:64px; width:300px; text-align:right; font-size:24px; color:{fcol}; line-height:1.4">'
                f'@@N@@ / @@T@@</p>')
    html = (f'<section id="{sid}" data-transition="{transition}" style="background:{bg}; color:{color}; font-family:{BODY}; '
            f'padding:{pad}; display:flex; flex-direction:{direction}; gap:{gap}px; justify-content:{justify}; align-items:{align}">'
            f'{backdrop}{body}{foot}<aside>{notes}</aside></section>')
    slides.append((sid, html, section))


def eyebrow(part, name, k):
    return f"PART {part} ／ {name}　ひみつ {k}"


def hl(t):
    return f'<span style="color:{SUN}">{t}</span>'


PARTS = ["ブログのしくみ", "ルールブック", "スキル", "エージェント"]


def divider(sid, n, lead, title, sub, secrets, notes):
    tracker = ""
    for i, name in enumerate(PARTS, 1):
        if i == n:
            st = f"background:{SUN}; color:{INK}; border:2px solid {SUN}"
        elif i < n:
            st = f"background:{D_CARD}; color:{D_TEXT}; border:2px solid {D_CARD}"
        else:
            st = f"background:transparent; color:{D_MUTED}; border:2px solid {D_LINE}"
        tracker += (f'<p style="flex:1; text-align:center; font-size:30px; font-weight:700; line-height:1.4; '
                    f'padding:14px 8px; border-radius:999px; {st}">{i}　{name}</p>')
    top = col(
        p(f"PART {n} ／ 4　{secrets}", 32, D_ACC, 700, extra="letter-spacing:4px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:104px; font-weight:900; line-height:1.25; color:{D_TEXT}">{lead}<br>{hl(title)}</h2>'
        + p(sub, 38, D_MUTED, extra="padding-top:16px"),
        gap=20, extra="width:1150px")
    backdrop = (f'<p style="position:absolute; right:128px; top:112px; width:640px; text-align:right; font-family:{DISPLAY}; '
                f'font-size:420px; font-weight:900; line-height:1; color:#22355A">{n}</p>'
                f'<x-shape kind="ellipse" style="position:absolute; left:1560px; top:600px; width:120px; height:120px; background:{SUN}"></x-shape>')
    add(sid, top + row(tracker, gap=16), notes, bg=INK, dark=True, footer=False, justify="space-between",
        pad="128px", transition="push", backdrop=backdrop, section=(f"s{n + 1}", sub))


# ============================================================ 1 cover
add("cover",
    col(
        p("「明日使える生成AI」ブログ　運営の裏側", 32, D_ACC, 700, extra="letter-spacing:2px")
        + f'<h1 style="font-family:{DISPLAY}; font-size:96px; font-weight:900; line-height:1.25; color:{D_TEXT}">'
          f'このブログの<br>{hl("ひみつ")}、ぜんぶ見せます</h1>'
        + p("文章がWebサイトになるしくみと、それを支えるAIの助っ人たち", 40, D_TEXT, 400, extra="padding-top:24px"),
        gap=24, extra="width:1200px"),
    "ここから本題です。今日は、私が運営している『明日使える生成AI』というブログの、ひみつを紹介します。このブログには、ふつうのブログにある『投稿ボタン』がありません。それなのに、文章を書くとWebサイトになって公開されます。なぜそんなことができるのか。そして、裏でAIがどう手伝っているのか。中学生でもわかる言葉で、順番に種明かしします。",
    bg=INK, dark=True, footer=False, justify="center",
    backdrop=(f'<x-shape kind="ellipse" style="position:absolute; left:1232px; top:200px; width:560px; height:560px; background:{BLUE}; opacity:0.45"></x-shape>'
              f'<x-shape kind="ellipse" style="position:absolute; left:1552px; top:640px; width:200px; height:200px; background:{SUN}"></x-shape>'),
    section=("s1", "今日の話の入り口と、全体の流れ"))

# ============================================================ 1b profile
add("profile",
    head("SELF INTRODUCTION", "自己紹介")
    + row(
        card(p("発表する人", 28, "#E8EEFF", 700)
             + f'<h2 style="font-family:{DISPLAY}; font-size:96px; font-weight:900; line-height:1.2; color:#FFFFFF">渥美 政廣</h2>'
             + p("あつみ　まさひろ", 40, "#E8EEFF", 500),
             bg=BLUE, border=BLUE, pad="48px 56px", gap=12, extra="flex:none; width:820px; justify-content:center")
        + col(
            card(row(icon_tile("Code", TINT, BLUE_T, 96, 56)
                     + col(h3("ソフトウエアエンジニア", 40) + p("プログラムやシステムをつくる仕事をしています。", 28, MUTED, lh=1.5), gap=4, extra="flex:1"),
                     gap=28, extra="align-items:center"),
                 pad="32px 40px", extra="flex:1; justify-content:center")
            + card(row(icon_tile("Users", SUN, INK, 96, 56)
                       + col(h3("みんなの助っ人", 40) + p("みんなの悩み事について、助っ人をしています。", 28, MUTED, lh=1.5), gap=4, extra="flex:1"),
                       gap=28, extra="align-items:center"),
                   pad="32px 40px", extra="flex:1; justify-content:center"),
            gap=24, extra="flex:1"),
        gap=32, extra="flex:1"),
    "こんにちは。最初に、簡単に自己紹介をさせてください。渥美政廣、あつみまさひろといいます。ソフトウエアエンジニアをしています。プログラムやシステムをつくる仕事です。そして、みんなの悩み事について、助っ人をしています。今日の話に出てくる、AIという助っ人の話も、この仕事の延長です。",
    section=("s0", "前振り。自己紹介と、運営しているブログの紹介"))

# ============================================================ 1c about blog
def flow_card(icon, hot, title, body):
    return card(icon_tile(icon, SUN if hot else BLUE, INK if hot else "#FFFFFF", 96, 56)
                + h3(title, 38) + p(body, 28, MUTED, lh=1.55),
                pad="32px 32px 36px", gap=14, extra="flex:1")

add("about-blog",
    head("私がやっていること", "私は、情報共有のためにブログをやっています")
    + row(
        flow_card("Home", False, "自社はSES事業", "社員は、お客さんの会社に常駐して、システムの開発や運用をしている。")
        + arrow_r(MUTED, 48)
        + flow_card("Users", False, "現場ごとにバラバラ", "常駐先ごとに、生成AIを使える度合いが違う。")
        + arrow_r(MUTED, 48)
        + flow_card("Book", True, "ブログで情報共有", "社員が生成AIを使いこなせるように、後押ししている。"),
        gap=16, extra="flex:1")
    + card(p("<b>ブログのコンセプト</b>　「明日の現場で、そのまま使える」生成AIの実践知を届ける。", 32, INK),
           bg=SUN_SOFT, border=SUN, pad="24px 36px"),
    "私は、会社の仲間に向けた情報共有として、ブログをやっています。理由はこうです。私の会社はSES事業といって、社員がお客さんの会社に常駐して、システムの開発や運用をする仕事をしています。ただ、常駐先ごとに、生成AIをどこまで使えるかはバラバラです。そこで、社員が生成AIを使いこなせるように、後押しとして、ブログという形で情報を共有しています。コンセプトは、明日の現場で、そのまま使える生成AIの実践知を届けることです。そんなブログを、私は運営しています。今日は、このブログの裏側のひみつを、順番に種明かしします。")

# ============================================================ 2 agenda
def agrow(num, title, sub, secrets):
    return row(
        f'<p style="flex:none; width:80px; height:80px; text-align:center; font-family:{DISPLAY}; font-size:48px; font-weight:900; line-height:80px; '
        f'background:{BLUE}; color:#FFFFFF; border-radius:40px">{num}</p>'
        + f'<h3 style="flex:none; width:420px; font-family:{DISPLAY}; font-size:44px; font-weight:900; line-height:1.3; color:{INK}">{title}</h3>'
        + p(sub, 30, MUTED, lh=1.4, extra="flex:1")
        + pill(secrets, TINT, BLUE_T, 26, extra="flex:none"),
        gap=32, extra=f"align-items:center; background:{CARD}; border:2px solid {LINE}; border-radius:28px; padding:18px 40px")

add("agenda",
    head("AGENDA", "ひみつは全部で14個。4つの部屋で紹介します")
    + col(
        agrow("1", "ブログのしくみ", "書いた文章が、Webサイトになって公開されるまで", "ひみつ 1〜4")
        + agrow("2", "ルールブック", "docs/planning にある、3冊の決まりごと", "ひみつ 5〜8")
        + agrow("3", "スキル", "AIに渡す「手順書」。3つある", "ひみつ 9〜11")
        + agrow("4", "エージェント", "AIの「専門担当」。3人いる", "ひみつ 12〜14"),
        gap=18),
    "今日のひみつは全部で14個。4つの部屋に分けて紹介します。1つ目の部屋は、ブログそのものの仕組み。2つ目は、このブログを運営するための3冊のルールブック。3つ目と4つ目が、AIの助っ人の話で、手順書にあたるスキルと、専門担当にあたるエージェントです。持ち時間が短いので、テンポよく進めます。")

# ============================================================ PART 1
divider("part1-divider", 1, "まずは、", "ブログのしくみ", "書いた文章が、Webサイトになって公開されるまで", "ひみつ 1〜4",
        "ここからパート1、ブログのしくみです。ふつうのブログにある投稿ボタンがないのに、どうやって記事が公開されるのか。ひみつ1から4まで、4つ紹介します。一番下の4つの丸は、今どこにいるかの目印で、黄色が今の場所です。")

# ---- ひみつ1 flow
def node(step, title, desc, icon, auto=False):
    pc = SUN if auto else BLUE
    pf = INK if auto else "#FFFFFF"
    return card(
        pill(step, pc, pf, 26, extra="align-self:flex-start")
        + icon_tile(icon, BLUE, "#FFFFFF", 96, 56)
        + h3(title, 32) + p(desc, 26, MUTED, lh=1.55),
        pad="28px 24px 32px", gap=16, extra="flex:1")

add("flow",
    head(eyebrow(1, "ブログのしくみ", 1), "投稿ボタンのかわりに、ロボットがいる")
    + row(
        node("① 書く", "自分の<br>パソコン", "文章を、決まった書き方のファイルにする", "Code")
        + arrow_r()
        + node("② 送る", "GitHub", "ファイルを預かってくれる、ネット上の倉庫", "Database")
        + arrow_r()
        + node("③ 組み立て", "GitHub Actions", "荷物が届くと目を覚ます、サイトを作るロボット", "Settings", True)
        + arrow_r()
        + node("④ 公開", "GitHub Pages", "できあがったサイトを世界に並べる店先", "Cloud", True)
        + arrow_r()
        + node("⑤ 読む", "読む人の<br>ブラウザ", "URLを開くと、記事が表示される", "Globe"),
        gap=14, extra="flex:1")
    + row(pill("青：人がやる", BLUE, "#FFFFFF", 28) + pill("黄色：ロボットが自動でやる", SUN, INK, 28), gap=20),
    "ひみつ1。このブログには、投稿ボタンがありません。かわりに、ロボットがいます。流れはこうです。まず自分のパソコンで文章を書く。次に、GitHubという、ファイルを預かってくれるネット上の倉庫に送る。すると、倉庫に荷物が届いたことをきっかけに、GitHub Actionsというロボットが目を覚まして、サイトを組み立てます。できあがったサイトはGitHub Pagesが世界に公開して、読む人のブラウザに表示されます。人がやるのは書いて送るところだけ。黄色いところは全部ロボットです。")

# ---- ひみつ2 file
def code_line(text, color="#E6EDFB", size=28):
    return f'<p style="font-family:{MONO}; font-size:{size}px; font-weight:500; line-height:1.7; color:{color}; white-space:nowrap">{text}</p>'

K = "#8FB4FF"; CM = "#8A97B5"
code_meta = col(
    code_line("---", CM)
    + code_line(f'<span style="color:{K}">layout:</span> post')
    + code_line(f'<span style="color:{K}">title:</span> "記事のタイトル"')
    + code_line(f'<span style="color:{K}">date:</span> 2026-09-28')
    + code_line(f'<span style="color:{K}">categories:</span> [生成AIのきほん]')
    + code_line(f'<span style="color:{K}">tags:</span> [ChatGPT, 入口]')
    + code_line("---", CM), gap=0)
code_body = col(
    code_line("結論から書きます。この記事では…")
    + code_line(f'<span style="color:{K}">## </span>見出しは # で作る')
    + code_line(f'<span style="color:{K}">- </span>箇条書きは - をつける'), gap=0)

add("file",
    head(eyebrow(1, "ブログのしくみ", 2), "記事の正体は、1つのテキストファイル")
    + row(
        col(
            p("2026-09-28-sample-post.md", 28, "#FFFFFF", 500, extra=f"font-family:{MONO}; background:{BLUE}; padding:14px 32px; border-radius:20px 20px 0 0")
            + f'<div style="background:#0F1B33; padding:28px 36px; display:flex; flex-direction:column; gap:20px; border-radius:0 0 20px 20px">'
              + code_meta + f'<hr style="border-top:2px dashed {CM}; width:100%">' + code_body + '</div>',
            gap=0, extra="flex:none; width:940px")
        + col(
            card(p("ファイル名", 26, BLUE_T, 700) + p("<b>公開する日</b> ＋ <b>英語のタイトル</b>", 32), pad="24px 32px", gap=4)
            + card(p("上の部分：名札", 26, BLUE_T, 700) + p("タイトル・日付・分類を書く", 30), pad="24px 32px", gap=4)
            + card(p("下の部分：本文", 26, BLUE_T, 700) + p("ふつうの文章。記号で見出しや箇条書きを作る", 30), pad="24px 32px", gap=4)
            + card(p("<b>ルール</b>：ファイル名の日付が未来だと、その記事はまだ公開されない", 30), bg=SUN_SOFT, border=SUN, pad="24px 32px", gap=4),
            gap=18, extra="flex:1"),
        gap=48),
    "ひみつ2。記事1本の正体は、ただのテキストファイルです。ファイル名は、公開する日付と英語のタイトル。中身は2つの部分でできています。上は名札で、タイトルや日付、分類を書きます。下は本文で、シャープ記号をつけると見出し、ハイフンをつけると箇条書きになります。この書き方をマークダウンといいます。そしてルールが1つ。ファイル名の日付が未来だと、その記事は公開されません。これは、あとで出てくる予約投稿につながります。")

# ---- ひみつ3 jekyll
def mat(icon, title, sub):
    return card(icon_tile(icon, TINT, BLUE_T, 80, 48) + h3(title, 32) + p(sub, 24, MUTED, extra=f"font-family:{MONO}", lh=1.4),
                pad="24px 16px 28px", gap=10, extra="flex:1; align-items:center; text-align:center")

add("jekyll",
    head(eyebrow(1, "ブログのしくみ", 3), "Jekyllが、ページを組み立ててくれる")
    + row(
        col(
            row(mat("Book", "記事", "Markdown") + mat("Star", "デザイン", "Chirpy") + mat("Settings", "設定", "_config.yml"), gap=20)
            + arrow_d(MUTED)
            + f'<div style="background:{BLUE}; border-radius:28px; padding:28px; display:flex; flex-direction:column; align-items:center; gap:4px">'
              f'<p style="font-family:{DISPLAY}; font-size:44px; font-weight:900; color:#FFFFFF; line-height:1.3">Jekyll（ジキル）</p>'
              f'<p style="font-size:28px; color:#E8EEFF; line-height:1.5">材料を全部まぜて、ページを作る</p></div>'
            + arrow_d(MUTED)
            + f'<div style="background:{SUN}; border-radius:28px; padding:24px; display:flex; flex-direction:column; align-items:center">'
              f'<p style="font-family:{DISPLAY}; font-size:36px; font-weight:900; color:{INK}; line-height:1.4">記事の数だけ HTML のページ</p></div>',
            gap=14, extra="flex:none; width:900px")
        + col(
            card(h3("記事", 32, BLUE_T) + p("自分で書いた文章。中身だけに集中できる。", 30), pad="22px 32px", gap=4)
            + card(h3("デザイン", 32, BLUE_T) + p("Chirpy（チャーピー）という、公開されている着せ替えセットを借りている。", 30), pad="22px 32px", gap=4)
            + card(h3("設定", 32, BLUE_T) + p("サイトの名前やURL、どのフォルダを材料にするかのメモ。", 30), pad="22px 32px", gap=4)
            + p("同じ機械が、同じ手順で全ページを作る。だから見た目がそろう。", 30, MUTED, extra="padding-top:6px"),
            gap=16, extra="flex:1"),
        gap=56),
    "ひみつ3。Webページの正体はHTMLというファイルですが、記事ごとに手で書くのは大変です。そこで、Jekyllという組み立て機械に任せています。材料は3つ。自分で書いた記事、借りてきたデザイン、設定のメモ。この3つを入れると、記事の数だけHTMLのページができあがります。デザインはChirpyという、公開されている着せ替えセットを使っているので、どの記事も同じ見た目になります。ロボットの中で動いているのが、このJekyllです。")

# ---- ひみつ4 folders + 予約投稿
def frow(name, what, kind, indent=0):
    if kind == "base":
        tag = pill("ここだけが材料", BLUE, "#FFFFFF", 26)
    elif kind == "ok":
        tag = pill("公開される", OK_BG, OK, 26)
    else:
        tag = pill("出ない", NO_BG, NO, 26)
    return (f'<div style="display:flex; flex-direction:row; align-items:center; gap:24px; background:{CARD}; border:2px solid {LINE}; '
            f'border-radius:20px; padding:14px 28px 14px {28 + indent}px">'
            f'<p style="flex:none; width:{270 - indent}px; font-family:{MONO}; font-size:28px; font-weight:500; color:{INK}; line-height:1.4">{name}</p>'
            f'<p style="flex:1; font-size:26px; color:{MUTED}; line-height:1.4">{what}</p>{tag}</div>')

add("folders",
    head(eyebrow(1, "ブログのしくみ", 4), "公開されるのは、siteフォルダの中だけ")
    + row(
        col(
            frow("site/", "サイトの材料の置き場", "base")
            + frow("_posts/", "完成した記事", "ok", 48)
            + frow("_drafts/", "書きかけの記事", "no", 48)
            + frow("assets/", "記事の画像など", "ok", 48)
            + frow("docs/", "ルールブックなど", "no")
            + frow("infographics/", "画像の元データ", "no"),
            gap=10, extra="flex:none; width:1030px")
        + col(
            card(h3("許可する範囲を、1つだけ決める", 34, "#FFFFFF")
                 + p("「これは出さない」のリストは作らない。「siteの中だけ」と決めておけば、書き忘れの事故が起きない。", 28, "#E8EEFF"),
                 bg=BLUE, border=BLUE, pad="32px 36px", gap=12, extra="flex:1")
            + card(h3("予約投稿もできる", 34, INK)
                   + p("未来の日付の記事は、その日まで出ない。ロボットが毎日 0:05 に見に来て、日付が来たら公開する。", 28, INK),
                   bg=SUN_SOFT, border=SUN, pad="32px 36px", gap=12, extra="flex:1"),
            gap=16, extra="flex:1"),
        gap=44, extra="flex:1"),
    "ひみつ4。このプロジェクトには、記事のほかに、企画のメモやAI向けの説明書も入っています。これがうっかりネットに出たら困ります。そこで、出さないもののリストを作るのではなく、siteというフォルダの中だけを材料にする、と許可する範囲を1つだけ決めています。これなら書き忘れが起きません。もう1つのひみつが予約投稿。未来の日付の記事は公開されず、ロボットが毎日夜中の0時5分に見に来て、日付が来ていたら公開してくれます。書きかけの記事を入れるdraftsフォルダも、公開されません。")

# ============================================================ PART 2
divider("part2-divider", 2, "つぎは、", "ルールブック", "docs/planning にある、3冊の決まりごと", "ひみつ 5〜8",
        "ここからパート2、ルールブックです。このブログを運営するために、決まりごとを3冊の本にまとめてあります。ひみつ5から8まで、4つ紹介します。")

# ---- ひみつ5 rulebooks
def book(icon, fname, nick, q, body):
    return card(
        icon_tile(icon, BLUE, "#FFFFFF", 96, 56)
        + p(fname, 26, BLUE_T, 500, extra=f"font-family:{MONO}; line-height:1.4")
        + h3(nick, 48)
        + pill(q, SUN, INK, 30, extra="align-self:flex-start")
        + p(body, 28, MUTED, lh=1.55),
        pad="40px 40px 44px", gap=18, extra="flex:1")

add("rulebooks",
    head(eyebrow(2, "ルールブック（docs/planning）", 5), "ルールブックが、3冊ある")
    + row(
        book("Book", "content-strategy.md", "設計書", "何のために書く？", "ブログのコンセプト、読者、8つのカテゴリ、記事の型。方針は全部ここ。")
        + book("Lightbulb", "article-backlog.md", "ネタ帳", "次に何を書く？", "記事のタネのストックと、公開する順番。")
        + book("Chat", "writing-style.md", "文体ガイド", "どう書く？", "口調、言い換えのルール、書き終えたあとのチェック表。"),
        gap=24, extra="flex:1")
    + p("AIは毎回まっさらな状態で始まる。だから、決まりごとは全部ことばにして書いてある。", 30, MUTED),
    "ここからは2つ目の部屋、ルールブックです。docs/planningというフォルダに、3冊入っています。1冊目は設計書。このブログは何のために、誰に向けて書くのかが書いてあります。2冊目はネタ帳。次に何を書くかと、公開する順番です。3冊目は文体ガイド。どんな言葉遣いで書くか。ポイントは、AIは毎回まっさらな状態で始まるということ。前回何を決めたか覚えていません。だから、決まりごとは頭の中ではなく、ぜんぶ文章にして置いてあります。人もAIも、迷ったらここに戻ります。")

# ---- ひみつ6 strategy
def vcard(num, title, body):
    return card(
        row(f'<p style="flex:none; width:64px; height:64px; text-align:center; font-family:{DISPLAY}; font-size:36px; font-weight:900; line-height:64px; '
            f'background:{BLUE}; color:#FFFFFF; border-radius:32px">{num}</p>'
            + h3(title, 38, INK, extra="flex:1"), gap=20, extra="align-items:center")
        + p(body, 28, MUTED, lh=1.55),
        pad="28px 36px 32px", gap=14, extra="flex:1")

add("strategy",
    head(eyebrow(2, "ルールブック（設計書）", 6), "知識だけの記事は、書かない")
    + p("AIに聞けば分かることを書いても、読む意味がない。だから、どの記事にも次の3つのうち1つは入れる。", 32, INK)
    + row(
        vcard("1", "一次体験", "実際にやってみた結果。うまくいかなかったことも書く。AIには体験できない。")
        + vcard("2", "立ち位置", "読む人と同じ立場の人が書く。同じ現場で働くエンジニアだから、伝わることがある。")
        + vcard("3", "選別と順序", "何から先に知るべきか。今は無視していいのは何か。地図をつくる。"),
        gap=24)
    + card(row(icon_tile("Warning", SUN, INK, 72, 44)
               + p("<b>公開前の一問</b>　この記事、読者がChatGPTに同じ質問をしたら、同じ答えが返ってこないか。返ってくるなら、書き直す。", 30, INK, extra="flex:1"),
               gap=28, extra="align-items:center"),
           bg=SUN_SOFT, border=SUN, pad="24px 36px"),
    "ひみつ6。設計書のいちばん大事なルールは、知識だけの記事は書かない、です。生成AIの一般的な知識は、AIに聞けば出てきます。だから、解説だけの記事には価値がありません。そこで、どの記事にも、この3つのうち最低1つを入れます。1つ目は一次体験。実際にやってみた結果で、失敗も書きます。2つ目は立ち位置。読む人と同じ現場にいる人が書いていること。3つ目は選別と順序。何を先に知るべきかの地図です。そして公開前に、必ず1つ質問をします。読者がChatGPTに同じことを聞いたら、同じ答えが返ってこないか。返ってくるなら、書き直しです。ほかにも、カテゴリは8つに決めてあり、勝手に増やさないというルールも、この設計書にあります。",
    gap=28)

# ---- ひみつ7 backlog
def chain_box(text, sub, hot=False):
    return (f'<div style="display:flex; flex-direction:column; gap:2px; background:{BLUE if hot else CARD}; border:2px solid {BLUE if hot else LINE}; '
            f'border-radius:24px; padding:16px 32px">'
            f'<p style="font-family:{DISPLAY}; font-size:34px; font-weight:900; line-height:1.3; color:{"#FFFFFF" if hot else INK}">{text}</p>'
            f'<p style="font-size:26px; line-height:1.4; color:{"#E8EEFF" if hot else MUTED}">{sub}</p></div>')

def small_arrow_d():
    return f'<x-shape kind="arrow-down" style="flex:none; align-self:center; width:28px; height:36px; background:{MUTED}"></x-shape>'

add("backlog",
    head(eyebrow(2, "ルールブック（ネタ帳）", 7), "ネタは54本。公開の順番にもルールがある")
    + row(
        col(
            card(p("記事のタネのストック", 28, BLUE_T, 700)
                 + f'<p style="font-family:{DISPLAY}; font-size:150px; font-weight:900; line-height:1.1; color:{INK}">54<span style="font-size:64px">本</span></p>'
                 + p("2026年9月20日時点。週1本のペースで、約12か月分。", 28, MUTED),
                 pad="32px 40px", gap=8)
            + card(p("<b>毎週月曜に1本</b>。続けることを最優先にして、増やしすぎない。", 30, INK), bg=SUN_SOFT, border=SUN, pad="24px 36px"),
            gap=20, extra="flex:none; width:760px")
        + col(
            p("先に読んでほしい記事を、先に出す", 32, INK, 700)
            + chain_box("プロンプトの基礎体力", "入門編・全3回")
            + small_arrow_d()
            + chain_box("プロンプト設計の型", "全5回", True)
            + small_arrow_d()
            + chain_box("ステップアップ編", "応用編・全4回")
            + p("前の記事が前提になっているので、順番を逆にしない。", 28, MUTED, extra="padding-top:4px"),
            gap=10, extra="flex:1"),
        gap=56, extra="flex:1"),
    "ひみつ7。ネタ帳には、記事のタネが54本たまっています。週に1本、月曜日に出すペースで、約12か月分です。もう1つのルールが、公開の順番。たとえば、プロンプトの基礎体力という入門編を先に出して、その次に型、最後に応用編、と決めています。算数で、九九を覚える前に文章題をやらないのと同じです。前の記事が前提になっているので、順番を逆にすると、読む人が置いていかれてしまいます。")

# ---- ひみつ8 writing style
def swap(no, ok):
    return row(
        card(p(no, 28, NO, 700, lh=1.4), bg=NO_BG, border=NO_BG, pad="18px 28px", extra="flex:1; justify-content:center")
        + arrow_r(MUTED, 48)
        + card(p(ok, 28, OK, 700, lh=1.4), bg=OK_BG, border=OK_BG, pad="18px 28px", extra="flex:1; justify-content:center"),
        gap=16, extra="align-items:stretch")

add("style",
    head(eyebrow(2, "ルールブック（文体ガイド）", 8), "現場のひみつは、書き方で守る")
    + row(
        col(
            card(h3("口調", 34, BLUE_T) + p("同じ現場の先輩が、休憩中に「これ便利だよ」と教えてくれる感じ。です・ます調でそろえる。", 28), pad="28px 32px", gap=8)
            + card(h3("決まり文句は使わない", 34, BLUE_T) + p("「ぜひ試してみてください」で終わらない。何から試すかまで書く。", 28), pad="28px 32px", gap=8),
            gap=18, extra="flex:none; width:640px")
        + col(
            p("会社や人が分かる書き方は、言い換える", 32, INK, 700)
            + swap("企業名・プロジェクト名", "「ある現場」「10名規模のチーム」")
            + swap("実際の議事録やログ", "同じ形のダミーを作って載せる")
            + swap("「PMの〇〇さん」", "「PM」「レビュー担当者」")
            + p("数字（「30分が5分になった」）は残す。数字だけでは、どこの現場か分からない。", 28, MUTED, extra="padding-top:4px"),
            gap=14, extra="flex:1"),
        gap=48),
    "ひみつ8。文体ガイドには、口調のほかに、大事なルールがあります。書き手は、お客さんの会社に常駐して働くエンジニアで、その現場の情報は外に出せません。でも体験談は、このブログの一番の武器です。そこで、どこで、誰と、は書かずに、どんな状況で、何に困り、どうなったか、だけを書く。会社の名前は、ある現場に。実際の議事録は、同じ形のダミーに。個人名は、役割に。こう言い換えれば、体験の説得力はほとんど落ちません。数字は、どこの現場か分からないので、そのまま残します。")

# ============================================================ PART 3
divider("part3-divider", 3, "そして、", "スキル", "AIに渡す「手順書」。このブログでは3つ使っている", "ひみつ 9〜11",
        "ここからパート3、スキルです。ここからがAIの助っ人の話です。まずは、AIに渡す手順書のスキルから。ひみつ9から11まで、3つ紹介します。")

# ---- ひみつ9 skill-what
def big_node(bg, fg, tag, title, sub, mono=False):
    subst = f"font-family:{MONO}; " if mono else ""
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:8px; background:{bg}; border-radius:28px; padding:28px 32px 32px">'
            f'<p style="font-size:26px; font-weight:700; color:{fg}; line-height:1.4">{tag}</p>'
            f'<p style="font-family:{DISPLAY}; font-size:40px; font-weight:900; line-height:1.3; color:{fg}">{title}</p>'
            f'<p style="{subst}font-size:28px; color:{fg}; line-height:1.5">{sub}</p></div>')

add("skill-what",
    head(eyebrow(3, "スキル", 9), "スキルは、AIに渡す手順書")
    + row(
        big_node(BLUE, "#FFFFFF", "1. 人が呼ぶ", "「/write-post」と打つ", "呼ぶだけでいい")
        + arrow_r(MUTED)
        + big_node(INK, "#FFFFFF", "2. AIが読む", "手順書を開く", "名前はいつも SKILL.md", False)
        + arrow_r(MUTED)
        + big_node(SUN, INK, "3. AIが進める", "手順どおりに動く", "人と会話しながら、記事を仕上げる"),
        gap=16)
    + row(
        card(h3("手順書には、何が書いてある？", 34, BLUE_T)
             + p("どの順番で聞くか。どのルールブックを読むか。どこで専門担当に頼むか。", 28)
             + p(".claude/skills/write-post/SKILL.md", 26, MUTED, 500, extra=f"font-family:{MONO}", lh=1.4),
             pad="28px 32px", gap=8, extra="flex:1")
        + card(h3("なぜ必要？", 34, BLUE_T)
               + p("AIは毎回まっさらで始まる。手順を書いておけば、いつでも同じ進め方になる。", 28)
               + p("たとえると、料理のレシピカード。", 28, MUTED),
               pad="28px 32px", gap=8, extra="flex:1"),
        gap=24),
    "ここからは3つ目の部屋、スキルです。スキルは、AIに渡す手順書のことです。使い方は簡単で、人が、スラッシュ、write-post、と打つだけ。するとAIが、SKILL.mdという名前の手順書を開いて、その順番どおりに、人と会話しながら記事を仕上げます。料理でいうレシピカードです。AIは毎回まっさらな状態で始まるので、手順を書いておかないと、毎回違う進め方になってしまいます。手順書があれば、いつでも同じ進め方ができます。", gap=32)

# ---- ひみつ10 skill-list
def skill_card(icon, cmd, nick, body, when):
    return card(
        icon_tile(icon, BLUE, "#FFFFFF", 96, 56)
        + p(cmd, 32, "#FFFFFF", 500, extra=f"font-family:{MONO}; background:{INK}; padding:8px 24px; border-radius:16px; align-self:flex-start; line-height:1.4")
        + h3(nick, 44)
        + p(body, 28, MUTED, lh=1.55)
        + p(when, 26, BLUE_T, 700, lh=1.5),
        pad="36px 36px 40px", gap=16, extra="flex:1")

add("skill-list",
    head(eyebrow(3, "スキル", 10), "このブログのスキルは、3つ")
    + row(
        skill_card("Book", "/write-post", "記事を書く", "テーマ決めから、体験のヒアリング、下書き、校閲、保存まで、順番に付き合ってくれる。", "使うとき：1本書くとき")
        + skill_card("Lightbulb", "/add-idea", "ネタをためる", "思いつきや、その日の出来事を聞いて、ネタ帳に足してよいか審査する。10分で終わらせる。", "使うとき：ネタを思いついたとき")
        + skill_card("Chart", "/add-infographic", "画像をつくる", "記事から載せる内容を拾って、図入りのヘッダー画像を作り、記事に付ける。", "使うとき：記事に絵を付けたいとき"),
        gap=24, extra="flex:1"),
    "このブログでは、スキルを3つ使っています。1つ目、write-post。記事を1本書くときに使います。2つ目、add-idea。ネタを思いついたときに、10分以内でネタ帳に足すためのものです。3つ目、add-infographic。記事に付ける、図入りのヘッダー画像を作ります。どれも、名前の前にスラッシュをつけて呼ぶだけ。手順書の中身は、ただのテキストファイルなので、いつでも直せます。")

# ---- ひみつ11 write-post flow
def step(num, title, body, kind="normal"):
    if kind == "hot":
        bg, bd, tc, bc, nb, nf = BLUE, BLUE, "#FFFFFF", "#E8EEFF", "#FFFFFF", BLUE_T
    elif kind == "agent":
        bg, bd, tc, bc, nb, nf = SUN, SUN, INK, INK, INK, "#FFFFFF"
    else:
        bg, bd, tc, bc, nb, nf = CARD, LINE, INK, MUTED, BLUE, "#FFFFFF"
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:10px; background:{bg}; border:2px solid {bd}; border-radius:24px; padding:22px 28px 26px">'
            f'<div style="display:flex; flex-direction:row; align-items:center; gap:14px">'
            f'<p style="flex:none; width:48px; height:48px; text-align:center; font-family:{DISPLAY}; font-size:28px; font-weight:900; line-height:48px; background:{nb}; color:{nf}; border-radius:24px">{num}</p>'
            f'<h3 style="font-family:{DISPLAY}; font-size:34px; font-weight:900; line-height:1.3; color:{tc}">{title}</h3></div>'
            f'<p style="font-size:26px; color:{bc}; line-height:1.5">{body}</p></div>')

add("write-post-flow",
    head(eyebrow(3, "スキル", 11), "AIは代筆せず、体験を引き出す")
    + col(
        row(step("1", "状況確認", "書きかけがないか見る")
            + step("2", "テーマ決め", "ネタ帳から今日の1本を選ぶ")
            + step("3", "体験ヒアリング", "やってみたことと、失敗を聞き出す", "hot")
            + step("4", "構成", "型に合わせて見出しを決める"), gap=20)
        + row(step("5", "下書き", "聞いた体験をもとに書く")
              + step("6", "校閲", "専門担当のAIに点検してもらう", "agent")
              + step("7", "保存", "site/_posts/ に置く")
              + step("8", "後片付け", "ネタ帳を更新して、次につなぐ"), gap=20),
        gap=20)
    + p("青は、この手順書の本体。黄色は、専門担当に頼むところ。AIが持っていないのは、書き手の体験だけ。だから、体験を聞き出すことに時間をかける。", 28, MUTED),
    "ひみつ11。write-postの手順を、8つに分けて見てみます。ここで大事なのは、AIが文章を代わりに書いてしまうのではない、という点です。このブログの価値は、書き手が実際にやってみた体験にあります。それはAIの持っていない情報です。だから、3番目の体験ヒアリングが、この手順書の本体です。AIが質問して、やってみたこと、失敗したこと、数字を聞き出して、それをもとに下書きを作ります。6番目の校閲は、次の部屋で出てくる専門担当のAIに任せます。",
    gap=30)

# ============================================================ PART 4
divider("part4-divider", 4, "最後は、", "エージェント", "別の部屋で働く「専門担当」。このブログでは3人いる", "ひみつ 12〜14",
        "ここから最後のパート4、エージェントです。手順書のスキルに続いて、専門担当のAIを紹介します。ひみつ12から14まで。最後の14番目で、今日の部品を全部つなげます。")

# ---- ひみつ12 agent-what
add("agent-what",
    head(eyebrow(4, "エージェント", 12), "エージェントは、別の部屋の専門担当")
    + row(
        card(icon_tile("Chat", BLUE, "#FFFFFF", 80, 48) + h3("メインのAI", 40)
             + p("いつも会話している相手。全体の進行役。", 28, MUTED),
             pad="28px 32px", gap=12, extra="flex:1")
        + col(
            p("「この下書きを点検して」", 26, MUTED, extra="text-align:center", lh=1.4) + arrow_r(BLUE, 120)
            + arrow_l(SUN, 120) + p("「ここを直すと良い」と報告", 26, MUTED, extra="text-align:center", lh=1.4),
            gap=10, extra="flex:none; width:320px; justify-content:center")
        + card(icon_tile("Search", SUN, INK, 80, 48) + h3("専門担当のAI", 40)
               + p("別の部屋で、1つの仕事だけをやる。", 28, MUTED),
               bg=SUN_SOFT, border=SUN, pad="28px 32px", gap=12, extra="flex:1"),
        gap=24, extra="align-items:stretch")
    + row(
        card(h3("会話が散らからない", 32, BLUE_T) + p("調べものは別の部屋。結果だけ戻る。", 26), pad="24px 28px", gap=6, extra="flex:1")
        + card(h3("持つ道具が決まっている", 32, BLUE_T) + p("読む・探すだけ。ファイルは書き換えない。", 26), pad="24px 28px", gap=6, extra="flex:1")
        + card(h3("指示書はファイル1つ", 32, BLUE_T) + p(".claude/agents/名前.md", 26, INK, 500, extra=f"font-family:{MONO}"), pad="24px 28px", gap=6, extra="flex:1"),
        gap=20)
    + p("スキルは、自分が読む手順書。エージェントは、お願いする専門担当。", 30, MUTED),
    "ここからは4つ目の部屋、エージェントです。エージェントは、別の部屋で働く専門担当のAIです。メインのAIが、この下書きを点検して、とお願いすると、専門担当が自分の部屋で作業して、ここを直すといいですよ、と報告だけ返してきます。良いところが3つあります。会話が散らからないこと。持っている道具が決まっていて、このブログの専門担当は、読む、探すだけで、ファイルは書き換えないこと。そして、指示書がファイル1つで済むこと。違いをまとめると、スキルは自分が読む手順書、エージェントはお願いする専門担当です。", gap=28)

# ---- ひみつ13 agents-three
def agent_card(icon, name, role, body, tools, used):
    return card(
        icon_tile(icon, SUN, INK, 96, 56)
        + p(name, 30, "#FFFFFF", 500, extra=f"font-family:{MONO}; background:{INK}; padding:8px 24px; border-radius:16px; align-self:flex-start; line-height:1.4")
        + h3(role, 44)
        + p(body, 28, MUTED, lh=1.55)
        + p(tools, 26, INK, 700, lh=1.5)
        + p(used, 26, BLUE_T, 700, lh=1.5),
        pad="36px 36px 40px", gap=14, extra="flex:1")

add("agents-three",
    head(eyebrow(4, "エージェント", 13), "専門担当は3人。全員、点検するだけ")
    + row(
        agent_card("Search", "idea-generator", "ネタ出し担当", "思いつきから、記事ネタの切り口を複数ならべる。選ぶのは人。", "道具：読む・探す・ネットで調べる", "呼ぶ場面：/add-idea の中")
        + agent_card("Lock", "idea-reviewer", "ネタ帳の門番", "重複していないか、書けるネタか、価値があるかを審査する。落とすときは代わりの置き場所も示す。", "道具：読む・探す", "呼ぶ場面：/add-idea の中")
        + agent_card("CheckCircle", "post-reviewer", "校閲担当", "下書きをルールブックと照らして点検する。直す価値のある指摘だけを、直し方つきで返す。", "道具：読む・探す", "呼ぶ場面：/write-post の校閲"),
        gap=24, extra="flex:1"),
    "このブログの専門担当は3人です。1人目、idea-generator。思いつきから、記事ネタの切り口を複数並べてくれます。どれにするかを選ぶのは人です。2人目、idea-reviewer。ネタ帳に足してよいかを審査する門番で、重複や、書けないネタを見つけます。落とすときも、代わりの置き場所を示します。3人目、post-reviewer。書き上がった下書きを、ルールブックと照らして点検する校閲担当です。3人とも、点検して指摘するだけで、ファイルは書き換えません。直すのは、人とメインのAIの仕事です。")

# ---- ひみつ14 teamwork
KINDS = {
    "human": (BLUE, "#FFFFFF", "人"),
    "skill": (INK, "#FFFFFF", "スキル"),
    "agent": (SUN, INK, "専門担当"),
}

def tnode(kind, title, sub=""):
    bg, fg, tag = KINDS[kind]
    subhtml = (f'<p style="font-family:{MONO}; font-size:24px; font-weight:500; color:{fg}; line-height:1.4">{sub}</p>' if sub else "")
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:4px; background:{bg}; border-radius:22px; padding:16px 18px 20px">'
            f'<p style="font-size:24px; font-weight:700; color:{fg}; line-height:1.4">{tag}</p>'
            f'<p style="font-family:{DISPLAY}; font-size:32px; font-weight:900; line-height:1.3; color:{fg}">{title}</p>{subhtml}</div>')

def lane(label, nodes):
    parts = []
    for i, n in enumerate(nodes):
        if i:
            parts.append(arrow_r(MUTED, 40))
        parts.append(tnode(*n))
    return col(p(label, 28, BLUE_T, 700, lh=1.4) + row("".join(parts), gap=10, extra="align-items:stretch"), gap=8)

add("teamwork",
    head(eyebrow(4, "エージェント", 14), "ぜんぶつなげると、こう動く")
    + lane("ネタをためる", [
        ("human", "思いつき"),
        ("skill", "話を聞く", "/add-idea"),
        ("agent", "切り口を出す", "idea-generator"),
        ("agent", "ネタを審査", "idea-reviewer"),
        ("skill", "ネタ帳に追加"),
    ])
    + lane("記事にする", [
        ("skill", "手順を始める", "/write-post"),
        ("human", "体験を話す"),
        ("skill", "下書きを書く"),
        ("agent", "校閲", "post-reviewer"),
        ("human", "直して送る"),
    ])
    + p("どの担当も、動く前にルールブック（docs/planning）を読む。最後に決めるのは、いつも人。", 28, MUTED),
    "ひみつ14、最後のひみつです。ここまでの部品を、全部つなげてみます。上の段は、ネタをためる流れ。人が思いつきを話すと、add-ideaという手順書が話を聞き、ネタ出し担当が切り口を並べます。ここで、どれで書くかを選ぶのは人です。次に門番が審査して、OKならネタ帳に追加されます。下の段は、記事にする流れ。write-postを始めて、人が体験を話し、AIが下書きを書き、校閲担当が点検し、人が直して送ります。送ったあとは、最初に見たロボットが公開してくれます。どの担当も、動く前にルールブックを読みます。そして、最後に決めるのは、いつも人です。",
    gap=26)

# ============================================================ summary
def sm(num, title, sub):
    return row(
        f'<p style="flex:none; width:80px; height:80px; text-align:center; font-family:{DISPLAY}; font-size:48px; font-weight:900; line-height:80px; '
        f'background:{BLUE}; color:#FFFFFF; border-radius:40px">{num}</p>'
        + col(h3(title, 40) + p(sub, 28, MUTED, lh=1.4), gap=4, extra="flex:1"),
        gap=32, extra=f"align-items:center; background:{CARD}; border:2px solid {LINE}; border-radius:28px; padding:18px 40px")

add("summary",
    head("まとめ", "14個のひみつ、ぎゅっとまとめ")
    + col(
        sm("1", "書いて送るだけ。あとはロボットが公開", "組み立ても公開も、GitHub のロボットが自動でやる。")
        + sm("2", "ルールブックが、方針・順番・書き方を決める", "AIは毎回まっさらだから、決まりごとは全部ことばにしておく。")
        + sm("3", "スキルは、AIに渡す手順書", "/write-post など、名前を呼ぶだけで同じ進め方になる。")
        + sm("4", "エージェントは、点検する専門担当", "指摘するだけ。最後に決めるのは、いつも人。"),
        gap=16),
    "まとめです。1つ目、このブログは、書いて送るだけで、あとはロボットが公開します。2つ目、ルールブック3冊が、方針と順番と書き方を決めています。AIは毎回まっさらなので、全部ことばにしてあります。3つ目、スキルは、AIに渡す手順書です。4つ目、エージェントは、点検する専門担当で、指摘するだけ。最後に決めるのは、いつも人です。",
    section=("s6", "まとめと、ブログへの案内"))

# ============================================================ QR
add("qr",
    col(
        p("ぜひ、読みにきてください", 32, D_ACC, 700, extra="letter-spacing:2px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:88px; font-weight:900; line-height:1.25; color:{D_TEXT}">明日使える<br>{hl("生成AI")}</h2>'
        + p("スマホでQRコードを読みとると、ブログが開きます。", 32, D_TEXT, extra="padding-top:16px")
        + p("raindrop-aqua.github.io/blog-ap-sys", 32, D_ACC, 500, extra=f"font-family:{MONO}; padding-top:8px"),
        gap=12, extra="flex:1")
    + f'<div style="flex:none; width:490px; height:490px; background:#FFFFFF; border-radius:40px; padding:40px; display:flex; align-items:center; justify-content:center">{QR_SVG}</div>',
    "最後まで聞いてくださって、ありがとうございました。右のQRコードを読みとると、このブログが開きます。記事は、実際にAIを使ってみた体験がもとになっています。よかったら、読みにきてください。",
    bg=INK, dark=True, footer=False, direction="row", align="center", gap=96, pad="128px 128px 128px")

# ============================================================ write
_cover = next(x for x in slides if x[0] == "cover")
slides.remove(_cover)
slides.insert([x[0] for x in slides].index("about-blog") + 1, _cover)
total = len(slides)
for i, (sid, html, sec) in enumerate(slides, 1):
    html = html.replace("@@N@@", f"{i:02d}").replace("@@T@@", f"{total:02d}")
    with open(os.path.join(ROOT, "project", "slides", f"{sid}.html"), "w") as f:
        f.write(html)

sections = {}
for sid, _, sec in slides:
    if sec:
        sections[sec[0]] = {"description": sec[1], "start": sid}

deck = {
    "v": 4,
    "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
    "title": "ブログのひみつ（仕組みと運営）",
    "order": [s[0] for s in slides],
    "cover": "cover",
    "sections": sections,
    "faces": {
        "zen-maru-gothic": {"family": "Zen Maru Gothic", "href": "https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900&display=swap"},
        "biz-udpgothic": {"family": "BIZ UDPGothic", "href": "https://fonts.googleapis.com/css2?family=BIZ+UDPGothic:wght@400;700&display=swap"},
        "source-code-pro": {"family": "Source Code Pro", "href": "https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@500&display=swap"},
    },
    "designSystems": [],
}
with open(os.path.join(ROOT, "project", "deck.json"), "w") as f:
    json.dump(deck, f, ensure_ascii=False, indent=1)
print(total, "slides")
