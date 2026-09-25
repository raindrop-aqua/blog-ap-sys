import json, os, math, datetime
import segno

ROOT = os.path.dirname(os.path.abspath(__file__))  # writes ./project/
os.makedirs(os.path.join(ROOT, "project", "slides"), exist_ok=True)

URL = "https://raindrop-aqua.github.io/blog-ap-sys/"

# palette
INK = "#16233B"; PAPER = "#F4F7FC"; CARD = "#FBFCFE"; TINT = "#E1EAFF"
BLUE = "#2F62E6"; BLUE_T = "#2350C9"  # BLUE_T: blue used as text on light backgrounds
SUN = "#FFC83D"; SUN_SOFT = "#FFF0BD"
MUTED = "#56647E"; LINE = "#D3DBEA"
OK = "#157A4B"; NO = "#B83B37"
D_TEXT = "#F4F7FC"; D_MUTED = "#A9B6D0"; D_ACC = "#86A8FF"; D_CARD = "#1F3050"; D_LINE = "#34466B"

DISPLAY = "'Zen Maru Gothic', 'BIZ UDPGothic', sans-serif"
BODY = "'BIZ UDPGothic', sans-serif"
MONO = "'Source Code Pro', monospace"

slides = []  # (id, html-template, section-desc or None)


def esc(s):
    return s


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


def arrow_r(color=BLUE):
    return f'<x-shape kind="arrow-right" style="flex:none; align-self:center; width:56px; height:32px; background:{color}"></x-shape>'


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
                f'明日使える生成AI ／ ブログのしくみ</p>'
                f'<p style="position:absolute; right:128px; bottom:64px; width:300px; text-align:right; font-size:24px; color:{fcol}; line-height:1.4">'
                f'@@N@@ / @@T@@</p>')
    html = (f'<section id="{sid}" data-transition="{transition}" style="background:{bg}; color:{color}; font-family:{BODY}; '
            f'padding:{pad}; display:flex; flex-direction:{direction}; gap:{gap}px; justify-content:{justify}; align-items:{align}">'
            f'{backdrop}{body}{foot}<aside>{notes}</aside></section>')
    slides.append((sid, html, section))


PARTS = ["ブログのしくみ", "AIのしくみ", "スキル", "サブエージェント", "人とAI"]


def hl(t):
    return f'<span style="color:{SUN}">{t}</span>'


def divider(sid, n, title_html, sub, notes):
    tracker = ""
    for i, name in enumerate(PARTS, 1):
        if i == n:
            st = f"background:{SUN}; color:{INK}; border:2px solid {SUN}"
        elif i < n:
            st = f"background:{D_CARD}; color:{D_TEXT}; border:2px solid {D_CARD}"
        else:
            st = f"background:transparent; color:{D_MUTED}; border:2px solid {D_LINE}"
        tracker += (f'<p style="flex:1; text-align:center; font-size:28px; font-weight:700; line-height:1.4; '
                    f'padding:14px 8px; border-radius:999px; {st}">{i} {name}</p>')
    top = col(
        p(f"PART {n} ／ 5", 32, D_ACC, 700, extra="letter-spacing:4px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:96px; font-weight:900; line-height:1.25; color:{D_TEXT}">{title_html}</h2>'
        + p(sub, 36, D_MUTED, extra="padding-top:16px"),
        gap=20, extra="width:1150px")
    backdrop = (f'<p style="position:absolute; right:128px; top:112px; width:640px; text-align:right; font-family:{DISPLAY}; '
                f'font-size:420px; font-weight:900; line-height:1; color:#22355A">{n}</p>'
                f'<x-shape kind="ellipse" style="position:absolute; left:1560px; top:600px; width:120px; height:120px; background:{SUN}"></x-shape>')
    add(sid, top + row(tracker, gap=16), notes, bg=INK, dark=True, footer=False, justify="space-between",
        pad="128px", transition="push", backdrop=backdrop, section=(f"s{n + 1}", sub))


def codebox(fname, lines, width=900):
    return col(
        p(fname, 26, "#FFFFFF", 500, extra=f"font-family:{MONO}; background:{BLUE}; padding:14px 32px; border-radius:20px 20px 0 0")
        + f'<div style="background:#0F1B33; padding:24px 36px; display:flex; flex-direction:column; border-radius:0 0 20px 20px">{"".join(lines)}</div>',
        gap=0, extra=f"flex:none; width:{width}px")


def cl(text, color="#E6EDFB"):
    return f'<p style="font-family:{MONO}; font-size:24px; font-weight:500; line-height:1.7; color:{color}; white-space:nowrap">{text}</p>'


def kv(key, rest):
    return cl(f'<span style="color:#8FB4FF">{key}</span>{rest}')


def grid22(cards):
    r1 = row(cards[0] + cards[1], gap=24, extra="flex:1")
    r2 = row(cards[2] + cards[3], gap=24, extra="flex:1")
    return col(r1 + r2, gap=24, extra="flex:1")


def numcard(num, title, body, hot=False):
    return card(
        row(f'<p style="flex:none; width:64px; height:64px; text-align:center; font-family:{DISPLAY}; font-size:36px; font-weight:900; line-height:64px; '
            f'background:{BLUE}; color:#FFFFFF; border-radius:32px">{num}</p>'
            + h3(title, 36, INK, extra="flex:1"), gap=20, extra="align-items:center")
        + p(body, 28, MUTED, lh=1.55),
        pad="28px 36px 32px", gap=14, extra="flex:1; justify-content:center")


def arrow_left_shape(color=MUTED):
    return f'<x-shape kind="arrow-left" style="flex:none; align-self:center; width:56px; height:32px; background:{color}"></x-shape>'


# ---------------------------------------------------------------- 1 cover
add("cover",
    col(
        p("「明日使える生成AI」ブログのひみつ", 32, D_ACC, 700, extra="letter-spacing:2px")
        + f'<h1 style="font-family:{DISPLAY}; font-size:88px; font-weight:900; line-height:1.25; color:{D_TEXT}">'
          f'文章を書いて送ると、<br><span style="color:{SUN}">自動でWebサイト</span>になる</h1>'
        + p("ブログのしくみと、AIの助っ人たち（スキルとサブエージェント）", 40, D_TEXT, 400, extra="padding-top:24px"),
        gap=24, extra="width:1100px"),
    "はじめに自己紹介。このブログ「明日使える生成AI」は、ふつうのブログサービスにある『投稿ボタン』がありません。文章のファイルを置いて送るだけで、ロボットがサイトを作って公開してくれます。今日はそのしくみを、中学生でもわかる言葉で説明します。特に、AIの助っ人である『スキル』と『サブエージェント』の話は、いつもより丁寧にやります。",
    bg=INK, dark=True, footer=False, justify="center",
    backdrop=(f'<x-shape kind="ellipse" style="position:absolute; left:1232px; top:200px; width:560px; height:560px; background:{BLUE}; opacity:0.45"></x-shape>'
              f'<x-shape kind="ellipse" style="position:absolute; left:1552px; top:640px; width:200px; height:200px; background:{SUN}"></x-shape>'),
    section=("s1", "今日の話の入り口と、全体の流れ"))

# ---------------------------------------------------------------- 2 agenda
def agrow(num, title, sub, hot=False):
    return row(
        f'<p style="flex:none; width:72px; height:72px; text-align:center; font-family:{DISPLAY}; font-size:44px; font-weight:900; line-height:72px; '
        f'background:{"#FFFFFF" if hot else BLUE}; color:{BLUE_T if hot else "#FFFFFF"}; border-radius:36px">{num}</p>'
        + f'<h3 style="flex:none; width:400px; font-family:{DISPLAY}; font-size:40px; font-weight:900; line-height:1.3; color:{"#FFFFFF" if hot else INK}">{title}</h3>'
        + p(sub, 28, "#E8EEFF" if hot else MUTED, lh=1.4, extra="flex:1"),
        gap=32,
        extra=f"align-items:center; background:{BLUE if hot else CARD}; border:2px solid {BLUE if hot else LINE}; border-radius:28px; padding:14px 36px")

add("agenda",
    head("AGENDA ／ 青いところが、今日のメイン", "今日の流れ")
    + col(
        agrow("1", "ブログのしくみ", "書いた文章が、Webサイトになって公開されるまで")
        + agrow("2", "AIのしくみ", "生成AIは、中で何をしているのか")
        + agrow("3", "スキル", "AIに渡す「手順書」。作り方と、使い方", True)
        + agrow("4", "サブエージェント", "AIの「専門担当」。何を任せているか", True)
        + agrow("5", "人とAIの分担", "AIに任せる部分と、人にしかできない部分"),
        gap=12),
    "全体は5つのパートです。1つ目はブログそのものの仕組み。2つ目は生成AIの仕組みで、ここは短いたとえ話で進めます。そして今日のメインが青い3つ目と4つ目、スキルとサブエージェントです。AIに『こういう手順で仕事をして』と渡す手順書がスキル、別の部屋で専門の仕事だけをやってくれる担当者がサブエージェント。このブログでは、それぞれ3つ、3人が働いています。最後の5つ目で、AIに任せる部分と人にしかできない部分をまとめます。パートが変わるときは、黒い大きな扉のスライドが入ります。",
    section=None)

# ---------------------------------------------------------------- part 1 divider
divider("part1-divider", 1, f"まずは、{hl('ブログ')}の<br>しくみ", "書いた文章が、どうやって公開されるのか。",
        "パート1は、ブログそのものの仕組みです。ふつうのブログサービスにある『投稿ボタン』が無いのに、どうやって記事が公開されるのか。ここから先、パートが変わるたびにこの黒い扉のスライドが出ます。一番下の5つの丸が、今どこにいるかの目印です。")

# ---------------------------------------------------------------- 3 overview
def big_pill(text, auto):
    bg = SUN if auto else BLUE
    fg = INK if auto else "#FFFFFF"
    return f'<p style="flex:1; text-align:center; font-family:{DISPLAY}; font-size:44px; font-weight:900; line-height:1.3; background:{bg}; color:{fg}; padding:44px 16px; border-radius:32px">{text}</p>'

add("overview",
    head("PART 1 ／ ブログのしくみ", "全体像：人がやるのは2つだけ")
    + col(
        row(big_pill("書く", False) + arrow_r(MUTED) + big_pill("送る", False) + arrow_r(MUTED)
            + big_pill("自動で<br>組み立てる", True) + arrow_r(MUTED) + big_pill("自動で<br>公開される", True), gap=20)
        + row(
            p("<b>青</b>：人がやる", 32, BLUE_T, extra="flex:2")
            + p("<b>黄色</b>：ロボットがやる", 32, INK, extra="flex:2"), gap=20, extra="padding-top:8px")
        + p("記事を1本足すたびに、この流れが自動で最初から最後まで動きます。", 32, MUTED, extra="padding-top:24px"),
        gap=28),
    "このブログの仕組みを一言でいうと、書く、送る、そのあとは自動、です。人がやるのは最初の2つだけ。黄色い部分はロボットが担当します。この4つがそれぞれ何をしているのかを、次のスライドから見ていきます。",
    section=None)

# ---------------------------------------------------------------- 4 flow
def node(step, title, desc, icon, auto=False):
    pc = SUN if auto else BLUE
    pf = INK if auto else "#FFFFFF"
    return card(
        pill(step, pc, pf, 26, extra="align-self:flex-start")
        + icon_tile(icon, BLUE, "#FFFFFF", 96, 56)
        + h3(title, 32) + p(desc, 26, MUTED, lh=1.55),
        pad="28px 24px 32px", gap=16, extra="flex:1")

add("flow",
    head("PART 1 ／ ブログのしくみ", "記事が読者に届くまでの5つの場所")
    + row(
        node("① 書く", "自分の<br>パソコン", "記事を Markdown という書き方で書く場所", "Code")
        + arrow_r()
        + node("② 送る", "GitHub", "ファイルと変更の歴史を預かる、ネット上の倉庫", "Database")
        + arrow_r()
        + node("③ 組み立て", "GitHub Actions", "荷物が届くと動き出す、サイトを組み立てるロボット", "Settings", True)
        + arrow_r()
        + node("④ 公開", "GitHub Pages", "できあがったサイトを世界に並べる店先", "Cloud", True)
        + arrow_r()
        + node("⑤ 読む", "読む人の<br>ブラウザ", "URLを開くと、Chrome や Safari に記事が出る", "Globe"),
        gap=14, extra="flex:1"),
    "登場する場所は5つ。1つ目は自分のパソコンで、文章を書く。2つ目はGitHubという、ファイルを預かってくれるネット上の倉庫。ここに送ることを『push』といいます。3つ目がGitHub Actionsで、倉庫に荷物が届くと自動で目を覚ますロボット。4つ目がGitHub Pagesで、完成したサイトを公開する店先。最後に読者のブラウザに表示されます。黄色いカードの2つが、人が何もしなくても動く部分です。")

# ---------------------------------------------------------------- 5 file anatomy
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
    head("PART 1 ／ ブログのしくみ", "記事の正体は、1つのテキストファイル")
    + row(
        col(
            p("2026-09-28-sample-post.md", 28, "#FFFFFF", 500, extra=f"font-family:{MONO}; background:{BLUE}; padding:14px 32px; border-radius:20px 20px 0 0")
            + f'<div style="background:#0F1B33; padding:28px 36px; display:flex; flex-direction:column; gap:20px; border-radius:0 0 20px 20px">'
              + code_meta + f'<hr style="border-top:2px dashed {CM}; width:100%">' + code_body + '</div>',
            gap=0, extra="flex:none; width:940px")
        + col(
            card(p("ファイル名", 26, BLUE_T, 700) + p("<b>公開する日</b> ＋ <b>英語のタイトル</b>", 32), pad="24px 32px", gap=4)
            + card(p("上の部分：名札", 26, BLUE_T, 700) + p("タイトル・日付・分類を書く。専門用語で front matter", 30), pad="24px 32px", gap=4)
            + card(p("下の部分：本文", 26, BLUE_T, 700) + p("ふつうの文章。記号で見出しや箇条書きを作る", 30), pad="24px 32px", gap=4)
            + card(p("<b>ルール</b>：ファイル名の日付が未来だと、その記事は公開されない。", 30), bg=SUN_SOFT, border=SUN, pad="24px 32px", gap=4),
            gap=18, extra="flex:1"),
        gap=48),
    "記事1本はファイル1つです。WordやSNSの投稿画面は使いません。ファイル名には公開する日付と英語のタイトルを付けます。ファイルの上の部分は『名札』と呼ばれる部分で、タイトルや日付、カテゴリーを書きます。下は本文で、記号を付けるだけで見出しや箇条書きが作れます。この書き方をMarkdown、マークダウンといいます。注意点として、ファイル名の日付が未来だと、その記事は公開されません。")

# ---------------------------------------------------------------- 6 jekyll
def mat(icon, title, sub):
    return card(icon_tile(icon, TINT, BLUE_T, 80, 48) + h3(title, 32) + p(sub, 24, MUTED, extra="font-family:%s" % MONO, lh=1.4),
                pad="24px 16px 28px", gap=10, extra="flex:1; align-items:center; text-align:center")

add("jekyll",
    head("PART 1 ／ ブログのしくみ", "Jekyll は「組み立てる機械」")
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
            card(h3("記事", 32, BLUE_T) + p("自分で書いた Markdown。中身だけに集中できる。", 30), pad="22px 32px", gap=4)
            + card(h3("デザイン", 32, BLUE_T) + p("Chirpy（チャーピー）という、公開されている着せ替えセットを借りている。", 30), pad="22px 32px", gap=4)
            + card(h3("設定", 32, BLUE_T) + p("サイトの名前やURL、どのフォルダを材料にするかのメモ。", 30), pad="22px 32px", gap=4)
            + p("同じ機械が同じ手順で全ページを作り直すから、人が手で直す場所がほとんどない。", 30, MUTED, extra="padding-top:6px"),
            gap=16, extra="flex:1"),
        gap=56),
    "Webページの正体はHTMLというファイルです。でも記事ごとに手でHTMLを書くのは大変なので、Jekyllという機械にまかせています。材料は3つ。自分で書いた記事、借りてきたデザイン、設定のメモ。この3つを入れると、記事の数だけHTMLのページができます。デザインはChirpyという公開されているテーマを使っているので、全部の記事が同じ見た目になります。")

# ---------------------------------------------------------------- 7 public / private
def frow(name, what, ok, indent=0, base=False):
    if base:
        tag = pill("ここだけが材料", BLUE, "#FFFFFF", 26)
    elif ok:
        tag = pill("公開される", "#DBF4E7", OK, 26)
    else:
        tag = pill("出ない", "#FCE3E1", NO, 26)
    return (f'<div style="display:flex; flex-direction:row; align-items:center; gap:24px; background:{CARD}; border:2px solid {LINE}; '
            f'border-radius:20px; padding:14px 28px 14px {28 + indent}px">'
            f'<p style="flex:none; width:{250 - indent}px; font-family:{MONO}; font-size:28px; font-weight:500; color:{INK}; line-height:1.4">{name}</p>'
            f'<p style="flex:1; font-size:26px; color:{MUTED}; line-height:1.4">{what}</p>{tag}</div>')

add("folders",
    head("PART 1 ／ ブログのしくみ", "公開されるものと、されないもの")
    + row(
        col(
            frow("site/", "Jekyll が材料にする場所", True, base=True)
            + frow("_posts/", "完成した記事", True, 48)
            + frow("_drafts/", "書きかけの記事", False, 48)
            + frow("assets/", "記事の画像など", True, 48)
            + frow("docs/", "企画メモ・ルールブック", False)
            + frow("verification/", "数字を確かめた生データ", False)
            + frow("CLAUDE.md", "AIに読ませる説明書", False),
            gap=10, extra="flex:none; width:1010px")
        + col(
            card(h3("許可する範囲を、1つだけ決める", 36, "#FFFFFF")
                 + p("「これは出さない」という禁止リストではなく、「site/ の中だけを材料にする」と決めている。", 30, "#E8EEFF")
                 + p("書き忘れが起きないので、うっかり公開の事故を、しくみで防げる。", 30, "#E8EEFF"),
                 bg=BLUE, border=BLUE, pad="36px 40px", gap=16, extra="flex:1"),
            gap=16, extra="flex:1"),
        gap=44, extra="flex:1"),
    "このプロジェクトには、記事以外にも企画メモやAI向けの説明書が入っています。これがうっかりネットに出たら困ります。そこで、『これは出さない』という禁止リストを作るのではなく、『siteフォルダの中だけを材料にする』と、許可する範囲を1つだけ決めています。リストへの書き忘れが起きないので、事故がしくみで防げます。ちなみに、書きかけの記事を入れるdraftsフォルダは、本番のビルドには入りません。")

# ---------------------------------------------------------------- 8 preview
def pbox(title, body, hot=False):
    return card(h3(title, 40, "#FFFFFF" if hot else INK) + p(body, 28, "#E8EEFF" if hot else MUTED),
                bg=BLUE if hot else CARD, border=BLUE if hot else LINE, pad="36px 36px 40px", gap=14, extra="flex:1")

add("preview",
    head("PART 1 ／ ブログのしくみ", "公開する前は、自分のパソコンで確認")
    + row(
        pbox("ファイルを保存", "Markdown を書き換えて、保存するだけ。書きかけの記事も見える。")
        + col(arrow_r(MUTED) + p("保存のたびに<br>自動で作り直す", 24, MUTED, extra="text-align:center"), gap=8, extra="flex:none; justify-content:center; width:200px")
        + pbox("コンテナ", "パソコンの中に作る、小さなお試し用パソコン。中で Jekyll が動く。", True)
        + col(arrow_r(MUTED) + p("自分だけに<br>見せる", 24, MUTED, extra="text-align:center"), gap=8, extra="flex:none; justify-content:center; width:200px")
        + pbox("ブラウザ", "localhost:4000 を開くと、本番と同じ見た目が出る。"),
        gap=8, extra="flex:none")
    + p("push した瞬間に世界へ出るので、その前にここで見た目を確かめる。", 32, MUTED),
    "pushした瞬間に世界に公開されるので、その前に自分のパソコンの中でサイトを動かして確認します。コンテナというのは、パソコンの中に作る小さなお試し用の部屋で、その中でJekyllが動きます。保存するたびに自動で作り直されるので、書きながら見た目を確認できます。")

# ---------------------------------------------------------------- 9 divider AI
divider("ai-divider", 2, f"ここからは、<br>{hl('AI')}のしくみ", "AIは、中で何をしているのか。難しい数式は使わない。",
        "パート2は、生成AIの仕組みです。ブログを書くとき、私はClaudeというAIに手伝ってもらっています。そのAIが中で何をしているのかを、難しい数式は使わずに、たとえ話で説明します。この仕組みを知っておくと、あとの『スキル』や『サブエージェント』がなぜ必要なのかが分かります。")

# ---------------------------------------------------------------- 10 generative
add("generative",
    head("PART 2 ／ AIのしくみ", "生成AIは、文章を「新しく作る」AI")
    + row(
        card(
            icon_tile("Search", TINT, BLUE_T, 96, 56)
            + h3("検索エンジン", 44)
            + p("すでにあるページを<b>探して</b>、見せてくれる。", 32)
            + p("答え：だれかが書いたものが、そのまま出る", 28, MUTED),
            pad="44px 44px 48px", gap=20, extra="flex:1")
        + card(
            icon_tile("Lightbulb", SUN, INK, 96, 56)
            + h3("生成AI", 44, "#FFFFFF")
            + p("質問に合わせて、文章を<b>その場で作り出す</b>。", 32, "#FFFFFF")
            + p("答え：世界に1つだけの文章が、毎回できる", 28, "#E8EEFF"),
            bg=BLUE, border=BLUE, pad="44px 44px 48px", gap=20, extra="flex:1"),
        gap=40, extra="flex:1")
    + p("ChatGPT・Claude・Gemini などが、ここに入ります。", 30, MUTED),
    "まず、生成AIとは何かを、検索エンジンと比べて説明します。検索エンジンは、すでに存在するページを探して見せてくれます。生成AIは、こちらの質問に合わせて、文章をその場で作り出します。同じ質問をしても、毎回少しずつ違う文章が出るのはそのためです。ChatGPT、Claude、Geminiなどがこの仲間です。")

# ---------------------------------------------------------------- 11 next-word prediction
def bar(label, pct, hot=False):
    w = int(760 * pct / 100)
    c = BLUE if hot else "#9DB4EE"
    return (f'<div style="display:flex; flex-direction:row; align-items:center; gap:24px">'
            f'<p style="flex:none; width:140px; font-family:{DISPLAY}; font-size:40px; font-weight:700; color:{INK}; line-height:1.3">{label}</p>'
            f'<div style="width:{w}px; height:56px; background:{c}; border-radius:14px"></div>'
            f'<p style="font-size:32px; font-weight:700; color:{INK}; line-height:1.3">{pct}%</p></div>')

add("predict",
    head("PART 2 ／ AIのしくみ", "中身は、「次のことば」の予想")
    + row(
        col(
            p("たとえば、この続きは？", 32, MUTED)
            + f'<p style="font-family:{DISPLAY}; font-size:72px; font-weight:900; color:{INK}; line-height:1.3">明日の天気は、</p>'
            + p("スマホの「予測変換」を、とてつもなく大きくしたもの。", 32, INK, extra="padding-top:16px")
            + card(p("AIは、これまでに読んだ大量の文章をもとに、「次に来やすいことば」を数字にして並べる。いちばん出やすいことばを選ぶこともあれば、少し違うことばを選ぶこともある。", 28, INK),
                   bg=SUN_SOFT, border=SUN, pad="24px 32px", extra="margin:0"),
            gap=16, extra="flex:1")
        + col(
            p("AIが並べた「次のことば」の予想", 28, BLUE_T, 700)
            + bar("晴れ", 60, True) + bar("曇り", 25) + bar("雨", 10) + bar("ほか", 5)
            + p("数字はイメージです", 24, MUTED, extra="padding-top:8px"),
            gap=22, extra="flex:none; width:1000px"),
        gap=48, extra="flex:1"),
    "生成AIの中身を一言でいうと、次に来ることばを予想する機械です。スマホで文字を打つと、次の候補が出る予測変換がありますよね。あれをとてつもなく大きくしたものだと思ってください。『明日の天気は、』の続きは、晴れが一番ありそう、曇りも、雨もある、というふうにAIは数字で並べます。ここの数字はイメージです。いつも一番の候補を選ぶわけではなく、ときどき別の候補も選ぶので、同じ質問でも毎回少し違う答えになります。")

# ---------------------------------------------------------------- 12 loop
def seq_row(step, base, new):
    return (f'<div style="display:flex; flex-direction:row; align-items:center; gap:20px; background:{CARD}; border:2px solid {LINE}; border-radius:24px; padding:20px 32px">'
            f'<p style="flex:none; width:210px; font-size:28px; font-weight:700; color:{BLUE_T}; line-height:1.4">{step}</p>'
            f'<p style="font-family:{DISPLAY}; font-size:48px; font-weight:700; color:{INK}; line-height:1.3">{base}</p>'
            f'<p style="font-family:{DISPLAY}; font-size:48px; font-weight:900; color:{INK}; line-height:1.3; background:{SUN}; padding:2px 20px; border-radius:14px">{new}</p></div>')

add("loop",
    head("PART 2 ／ AIのしくみ", "1語ずつ書き足して、文章になる")
    + col(
        seq_row("1回目の予想", "明日の天気は", "晴れ")
        + seq_row("2回目の予想", "明日の天気は晴れ", "です")
        + seq_row("3回目の予想", "明日の天気は晴れです", "。"),
        gap=20)
    + card(p("<b>答えを1語ずつ足しては、また予想する。</b>これを何百回もくりかえして、長い文章ができあがる。AIは、最初から全文を思い描いているわけではない。", 32, INK),
           bg=TINT, border=TINT, pad="28px 36px"),
    "AIは次のことばを1つ予想して、それを文章の最後にくっつけます。そして、くっつけた文章全体をもう一度読んで、また次のことばを予想します。これを何百回もくりかえして、長い文章ができあがります。人間が文章を書くときのように、最初から全体を考えているわけではなく、1語ずつ書き足しているのです。黄色い部分が、その回に足されたことばです。")

# ---------------------------------------------------------------- 13 tokens
def chunk(text, num):
    return card(
        f'<p style="font-family:{DISPLAY}; font-size:48px; font-weight:900; color:{INK}; line-height:1.3; text-align:center">{text}</p>'
        f'<hr style="border-top:2px solid {LINE}; width:100%">'
        f'<p style="font-family:{MONO}; font-size:28px; font-weight:500; color:{BLUE_T}; line-height:1.4; text-align:center">{num}</p>',
        pad="20px 28px", gap=10, extra="align-items:center")

add("tokens",
    head("PART 2 ／ AIのしくみ", "AIは文字を「トークン」に区切って読む")
    + col(
        p("「生成AIは、明日から使える」を区切ると…", 30, MUTED)
        + row(chunk("生成", "4821") + chunk("AI", "907") + chunk("は", "12") + chunk("、", "6") + chunk("明日", "2210") + chunk("から", "35") + chunk("使える", "3077"), gap=14)
        + p("上：ことばのかたまり（トークン）　下：AIが使う番号　※区切り方と番号は例です", 24, MUTED),
        gap=18)
    + row(
        card(h3("文字ではなく数字で計算", 36, BLUE_T) + p("AIの中は数字の世界。文章は、いったんトークンの番号に置きかえてから計算する。", 30), pad="28px 36px", gap=8, extra="flex:1")
        + card(h3("読める量も、料金も、これで数える", 36, BLUE_T) + p("「一度に読める量」や利用料金は、トークンの数で決まる。", 30), pad="28px 36px", gap=8, extra="flex:1"),
        gap=32),
    "AIは、私たちのように文字をそのまま読んでいるわけではありません。文章をトークンという、ことばのかたまりに区切って、それぞれに番号を付けて計算します。区切り方はAIごとに違い、ここの番号もイメージです。大事なのは、AIが一度に読める量や、利用料金が、このトークンの数で決まるということです。後で出てくる、AIの弱点の話にもつながります。")

# ---------------------------------------------------------------- 14 training
def tstep(num, icon, title, body):
    return card(
        row(icon_tile(icon, BLUE, "#FFFFFF", 88, 52)
            + col(p(num, 26, BLUE_T, 700, lh=1.3) + h3(title, 36), gap=2, extra="justify-content:center"), gap=20)
        + p(body, 28, INK),
        pad="32px 32px 36px", gap=20, extra="flex:1")

add("training",
    head("PART 2 ／ AIのしくみ", "AIは、こうして賢くなる")
    + row(
        tstep("STEP 1", "Book", "大量の文章を読む", "本やWebの文章の一部を隠して、次に来ることばを当てる練習を、何度もくりかえす。")
        + arrow_r(MUTED)
        + tstep("STEP 2", "GraduationCap", "答え方を教わる", "人がお手本を見せたり、よい答えに点を付けたりして、役に立つ答え方を身につける。")
        + arrow_r(MUTED)
        + tstep("STEP 3", "Chat", "質問に答える", "学び終わったAIに、私たちが質問する。学んだ予想の力で文章を作る。"),
        gap=16)
    + card(p("つまりAIは、<b>ことばの並びのパターン</b>を、人間が一生かけても読めない量の文章から身につけている。", 32, INK),
           bg=SUN_SOFT, border=SUN, pad="26px 36px"),
    "AIの学び方は3段階です。まず、本やWebにある大量の文章を読み、文章の一部を隠して次のことばを当てる練習を何度もくりかえします。これが一番大きな学習です。次に、人がお手本を見せたり、よい答えに点数を付けたりして、役に立つ答え方を教えます。最後に、私たちが質問して使う段階です。つまりAIは、意味を人間と同じように理解しているかどうかは別として、ことばの並びのパターンを、人間が一生かけても読めない量から身につけている、といえます。")

# ---------------------------------------------------------------- 15 neural net
def nn_svg():
    W, H = 760, 500
    layers = [3, 5, 5, 2]
    xs = [90, 270, 490, 670]
    pos = []
    for li, n in enumerate(layers):
        gapy = 90
        top = H / 2 - gapy * (n - 1) / 2
        pos.append([(xs[li], top + gapy * i) for i in range(n)])
    lines = []
    for li in range(len(layers) - 1):
        for (x1, y1) in pos[li]:
            for (x2, y2) in pos[li + 1]:
                lines.append(f'M{x1} {y1}L{x2} {y2}')
    strong = [(0, 1, 2, 3), (1, 2, 2, 1), (2, 3, 3, 0)]
    hl = []
    for (l, i, j, _) in [(0, 1, 2, 0), (1, 2, 1, 0), (2, 1, 0, 0)]:
        x1, y1 = pos[l][i]; x2, y2 = pos[l + 1][j]
        hl.append(f'M{x1} {y1}L{x2} {y2}')
    circles = []
    colors = ["#9DB4EE", "#2F62E6", "#2F62E6", "#FFC83D"]
    for li, pts in enumerate(pos):
        for (x, y) in pts:
            circles.append(f'<circle cx="{x}" cy="{y}" r="26" fill="{colors[li]}" stroke="#16233B" stroke-width="3"/>')
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-label="入力、2つの中間層、出力がつながった、ニューラルネットワークの図">'
            f'<path d="{"".join(lines)}" stroke="#B9C6E4" stroke-width="2" fill="none"/>'
            f'<path d="{"".join(hl)}" stroke="#2F62E6" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'{"".join(circles)}</svg>')

add("network",
    head("PART 2 ／ AIのしくみ", "中身は、数字でできた巨大な網")
    + row(
        col(nn_svg()
            + row(p("入力（文章）", 26, MUTED, extra="width:200px; text-align:left")
                  + p("つなぎ目の強さ＝数字", 26, BLUE_T, 700, extra="flex:1; text-align:center")
                  + p("出力（予想）", 26, MUTED, extra="width:200px; text-align:right"), gap=0),
            gap=8, extra="flex:none; width:760px")
        + col(
            card(h3("脳の仕組みをヒントにした計算", 36, BLUE_T) + p("神経細胞のつながりをまねた「ニューラルネットワーク」。丸が計算の部品で、線がつなぎ目。", 30), pad="28px 32px", gap=8)
            + card(h3("学習 ＝ つなぎ目の数字を調整", 36, BLUE_T) + p("予想が外れたら、つなぎ目の強さを少しだけ直す。これを、とんでもない回数くりかえす。", 30), pad="28px 32px", gap=8)
            + card(h3("知識の正体は、数字の表", 36, "#FFFFFF") + p("調整された数字は、大きなAIでは何十億〜何千億個以上。これが「AIの頭の中」。", 30, "#E8EEFF"),
                   bg=BLUE, border=BLUE, pad="28px 32px", gap=8),
            gap=16, extra="flex:1"),
        gap=48, extra="flex:1"),
    "AIの中身を、もう少しだけのぞいてみます。予想を行っているのは、ニューラルネットワークと呼ばれる計算のしくみです。脳の神経細胞のつながりをヒントにしています。丸が小さな計算の部品、線がつなぎ目で、つなぎ目には強さを表す数字が付いています。予想が外れたら、この数字を少しだけ直す。これをものすごい回数くりかえすのが学習です。学習が終わったAIの頭の中は、大きなモデルだと何十億から何千億個以上の数字の表です。ちなみに、AIの中に文章や画像がそのまま保存されているわけではありません。")

# ---------------------------------------------------------------- 16 prompt
add("prompt",
    head("PART 2 ／ AIのしくみ", "プロンプトは、AIへの指示書")
    + row(
        card(
            pill("うすい指示", "#FCE3E1", NO, 26, extra="align-self:flex-start")
            + f'<p style="font-family:{DISPLAY}; font-size:44px; font-weight:700; line-height:1.4; color:{INK}">ブログ記事を書いて</p>'
            + p("だれに向けて？　どのくらい？　何について？　AIは、ふつうの文章を予想するしかない。", 30, MUTED),
            pad="36px 40px 40px", gap=20, extra="flex:1")
        + card(
            pill("具体的な指示", "#DBF4E7", OK, 26, extra="align-self:flex-start")
            + f'<p style="font-family:{DISPLAY}; font-size:44px; font-weight:700; line-height:1.4; color:{INK}">中学生向けに、たとえ話を1つ入れて、400字で、ChatGPTの使い方を書いて</p>'
            + p("条件が多いほど、「次のことば」の候補がしぼられて、ねらった文章に近づく。", 30, MUTED),
            bg=CARD, border=OK, pad="36px 40px 40px", gap=20, extra="flex:1"),
        gap=36, extra="flex:1")
    + p("AIに出す指示のことを「プロンプト」という。このブログには、その書き方を扱う「プロンプト設計」のカテゴリーがある。", 28, MUTED),
    "AIに出す指示のことをプロンプトといいます。AIは次のことばを予想する機械なので、指示がうすいと、ふつうの文章を予想するしかありません。だれに向けて、どのくらいの長さで、何を入れて、と条件を足すほど、次のことばの候補がしぼられて、ねらった文章に近づきます。このブログにはプロンプト設計というカテゴリーがあって、この書き方を扱っています。")

# ---------------------------------------------------------------- 17 weaknesses
def weak(num, title, body, tail):
    return card(
        f'<p style="font-family:{DISPLAY}; font-size:64px; font-weight:900; line-height:1; color:{BLUE_T}">{num}</p>'
        + h3(title, 36) + p(body, 28, INK) + p(tail, 26, MUTED),
        pad="36px 32px 40px", gap=14, extra="flex:1")

add("weakness",
    head("PART 2 ／ AIのしくみ", "AIにも、苦手なことがある")
    + row(
        weak("1", "もっともらしい嘘", "「次のことば」を予想して書くので、知らないことでも、自然な文で書いてしまう。", "ハルシネーションと呼ばれる")
        + weak("2", "最新のことは知らない", "学習した時点までの知識しか持っていない。", "検索ツールとつなぐと補える")
        + weak("3", "一度に覚えられる量に限り", "一度に読める量にはトークンの上限がある。長い会話の最初のほうは、忘れることがある。", "「コンテキスト」と呼ばれる"),
        gap=24, extra="flex:1")
    + card(p("<b>だからAIの答えは、人が確かめる。</b>使う側が弱点を知っていると、安心して任せられる部分が見えてくる。", 30, INK),
           bg=SUN_SOFT, border=SUN, pad="24px 36px"),
    "AIにも苦手なことが3つあります。1つ目はもっともらしい嘘です。次のことばを予想して書くので、知らないことでも自然な文章で書いてしまいます。ハルシネーションと呼ばれます。2つ目は最新のことを知らないこと。学習した時点までの知識しかありません。ただし検索ツールとつなぐと補えます。3つ目は、一度に覚えていられる量に限りがあること。長い会話の最初のほうを忘れることがあります。だから、AIの答えは人が確かめる、というのが大事です。")

# ---------------------------------------------------------------- 18 agent
def astep(num, title, body, hot=False):
    return card(
        f'<p style="font-family:{DISPLAY}; font-size:56px; font-weight:900; line-height:1; color:{"#FFFFFF" if hot else BLUE_T}">{num}</p>'
        + h3(title, 36, "#FFFFFF" if hot else INK) + p(body, 28, "#E8EEFF" if hot else MUTED),
        bg=BLUE if hot else CARD, border=BLUE if hot else LINE, pad="28px 28px 32px", gap=12, extra="flex:1")

add("agent",
    head("PART 2 ／ AIのしくみ", "AIエージェントは、道具を使って作業する")
    + row(
        astep("1", "目的を受けとる", "「この記事の下書きを作って」")
        + arrow_r(MUTED)
        + astep("2", "考えて計画する", "まず何を読めばいいか、順番を考える", True)
        + arrow_r(MUTED)
        + astep("3", "道具を使う", "ファイルを読む、書く、実行する")
        + arrow_r(MUTED)
        + astep("4", "結果を見て決める", "うまくいったか確認して、次の手を選ぶ", True),
        gap=12)
    + f'<div style="border:3px dashed {BLUE}; border-radius:24px; padding:18px 32px; display:flex; flex-direction:row; justify-content:center"><p style="font-size:32px; font-weight:700; color:{BLUE_T}; line-height:1.4">ゴールに着くまで、2 → 3 → 4 をくりかえす</p></div>'
    + p("ふつうのチャットAIは「答える」まで。エージェントは、自分で道具を使って「やりとげる」まで。このブログの手伝いをしているのは Claude Code。", 28, MUTED),
    "ふつうのチャットAIは、質問に答えるところまでです。AIエージェントは、道具を使って、作業をやりとげるところまで進みます。目的を受け取り、考えて計画し、ファイルを読んだり書いたりコマンドを実行したりする道具を使い、結果を見て次の手を決める。うまくいくまでこれをくりかえします。このブログの手伝いをしているClaude Codeは、このAIエージェントのひとつで、私のパソコンの中でファイルを直接読み書きします。")

# ================================================================ PART 3 : skills
divider("part3-divider", 3, f"AIの助っ人①<br>{hl('スキル')}", "AIに渡す「手順書」。このブログでは3つ使っている。",
        "ここからが今日のメインです。AIの助っ人の1つ目、スキル。スキルは、AIに渡す手順書のことです。このブログでは、ネタ出し、記事を書く、図解をつける、の3つの手順書を用意しています。")

# ---------------------------------------------------------------- roles
def role(icon, tag, tagbg, tagfg, name, like, body, path, hot=False):
    return card(
        pill(tag, tagbg, tagfg, 26, extra="align-self:flex-start")
        + icon_tile(icon, TINT, BLUE_T, 80, 48)
        + h3(name, 40) + p(like, 28, BLUE_T, 700, lh=1.4)
        + p(body, 28, MUTED, lh=1.5)
        + p(path, 24, INK, 500, extra=f"font-family:{MONO}", lh=1.4),
        pad="28px 32px 32px", gap=14, extra="flex:1")

add("roles",
    head("PART 3 ／ スキル", "ブログを手伝うAIに渡しているもの")
    + row(
        role("Book", "人が決める", "#FFFFFF", BLUE_T, "ルールブック", "たとえるなら：校則",
             "何を、どんな方針で書くかの決まり。AIは毎回読み直す。", "docs/planning/ の3冊")
        + role("CheckCircle", "AIが実行する", BLUE, "#FFFFFF", "スキル", "たとえるなら：レシピ",
               "どう進めるかの手順書。今日の1つ目。", ".claude/skills/ に3つ")
        + role("Users", "AIが別室で実行", SUN, INK, "サブエージェント", "たとえるなら：専門の担当者",
               "頼まれた仕事だけをして、結果を返す。今日の2つ目。", ".claude/agents/ に3人"),
        gap=24, extra="flex:1"),
    "ブログを手伝うAIには、3種類のものを渡しています。1つ目はルールブック。何を、どんな方針で書くかの決まりで、これは人が決めます。校則のようなものです。2つ目がスキルで、どう進めるかの手順書。レシピのようなものです。3つ目がサブエージェントで、別の部屋で頼まれた仕事だけをして、結果を返してくれる専門の担当者です。今日はこの2つ目と3つ目を、順番にくわしく見ていきます。")

# ---------------------------------------------------------------- skill-what
add("skill-what",
    head("PART 3 ／ スキル", "スキルは、AIに渡す「手順書」")
    + row(
        col(
            p("たとえるなら", 28, "#E8EEFF", 700)
            + f'<h3 style="font-family:{DISPLAY}; font-size:64px; font-weight:900; line-height:1.2; color:#FFFFFF">料理のレシピ</h3>'
            + p("レシピがあれば、初めて作る人でも、いつも同じ味に近づける。", 30, "#FFFFFF", lh=1.6, extra="padding-top:12px")
            + p("手順書があれば、AIは毎回、同じ順番で仕事を進める。", 30, "#FFFFFF", lh=1.6),
            gap=10, extra=f"flex:none; width:600px; background:{BLUE}; border-radius:28px; padding:44px 44px 48px")
        + col(
            card(h3("日本語の文章で書く", 36, BLUE_T) + p("プログラムではなく、ふつうの文章で手順を書く。書き換えれば、AIの動きも変わる。", 28, INK, lh=1.5), pad="22px 36px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("呼び方は2通り", 36, BLUE_T) + p("/write-post のように名前で呼ぶ。用件に合えば、AIが自分で選ぶこともある。", 28, INK, lh=1.5), pad="22px 36px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("動く前に、必ず読む", 36, BLUE_T) + p("AIは手順書を読んでから動き出す。だから、同じ決まりを毎回守らせやすい。", 28, INK, lh=1.5), pad="22px 36px 26px", gap=6, extra="flex:1; justify-content:center"),
            gap=16, extra="flex:1"),
        gap=40, extra="flex:1"),
    "スキルをひとことで言うと、AIに渡す手順書です。たとえるなら料理のレシピ。レシピがあれば初めて作る人でもいつも同じ味に近づけるように、手順書があればAIは毎回同じ順番で仕事を進めます。ポイントは3つ。1つ目、手順書はプログラムではなく、ふつうの日本語の文章で書きます。文章を書き換えれば、AIの動きも変わります。2つ目、呼び方は2通りあって、スラッシュのあとに名前を打って呼ぶか、用件に合っていればAIが自分で選ぶこともあります。3つ目、AIは動き出す前に必ず手順書を読みます。だから同じ決まりを毎回守らせやすいのです。")

# ---------------------------------------------------------------- skill-file
add("skill-file",
    head("PART 3 ／ スキル", "スキルの中身は、1つの文書ファイル")
    + row(
        codebox(".claude/skills/write-post/SKILL.md", [
            cl("---", CM),
            kv("name:", " write-post"),
            kv("description:", " 記事を書きたい・ネタを"),
            cl("  相談したい・書きかけを再開したい"),
            cl("  ときに使う。…"),
            cl("---", CM),
            cl(f'<span style="color:{K}"># </span>記事執筆アシスタント'),
            cl(f'<span style="color:{K}">## </span>設計書の扱い'),
            cl(f'<span style="color:{K}">## </span>会話のしかた'),
            cl(f'<span style="color:{K}">## </span>フェーズ0: 状況確認'),
            cl(f'<span style="color:{K}">## </span>フェーズ1: テーマを決める'),
            cl("　…", CM),
            cl(f'<span style="color:{K}">## </span>フェーズ7: 後片付け'),
        ], width=860)
        + col(
            card(h3("名札：name と description", 34, BLUE_T) + p("名前と、「いつ使うか」の説明。AIはこれを見て、使うかどうかを決める。", 28, INK, lh=1.5), pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("本文：役割 → 決まり → 手順", 34, BLUE_T) + p("最初に「あなたは何の役か」を書き、次に守ることを書き、最後に順番を書く。", 28, INK, lh=1.5), pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("これだけで動く", 34, "#FFFFFF") + p("特別なソフトは要らない。文書を1つ置けば、AIの新しい仕事ができる。", 28, "#E8EEFF", lh=1.5), bg=BLUE, border=BLUE, pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center"),
            gap=16, extra="flex:1"),
        gap=40, extra="flex:1"),
    "スキルの実物を見てみましょう。これは記事を書くためのスキル、write-postの手順書の冒頭です。ブログの記事と同じ、Markdownという書き方のファイルです。上の名札には、名前と、いつ使うかの説明が書いてあります。AIはこの説明を見て、今の用件に合うかどうかを判断します。その下が本文で、最初に『あなたは何の役割か』、次に『守ること』、最後に『フェーズ0からフェーズ7までの順番』が並んでいます。特別なソフトは要りません。この文書を1つ置くだけで、AIに新しい仕事を覚えさせられます。")

# ---------------------------------------------------------------- skill-list
def skill_card(cmd, title, summary, steps, helper):
    return card(
        pill(cmd, BLUE, "#FFFFFF", 26, extra=f"align-self:flex-start; font-family:{MONO}")
        + h3(title, 40) + p(summary, 26, MUTED, lh=1.5)
        + col("".join(p(s, 26, INK, lh=1.45) for s in steps), gap=0)
        + p(helper, 24, BLUE_T, 700, extra=f"font-family:{MONO}", lh=1.5),
        pad="28px 32px 32px", gap=12, extra="flex:1")

add("skill-list",
    head("PART 3 ／ スキル", "このブログにある、3つのスキル")
    + row(
        skill_card("/add-idea", "ネタを出す", "思いつきや今日の出来事を、記事のネタにする。",
                   ["1　起点を見分ける", "2　素材を掘る", "3　切り口を立てる", "4　1本に絞る", "5　審査して書き込む"],
                   "呼ぶ担当：<br>💡 ヒラク<br>🗃️ クラ")
        + skill_card("/write-post", "記事を書く", "テーマ決めから保存まで、質問しながら1本仕上げる。",
                     ["0〜1　状況確認・テーマ", "2　体験のヒアリング", "3〜4　構成・下書き", "5　校閲", "6〜7　保存・後片付け"],
                     "呼ぶ担当：<br>🖍️ アカネ")
        + skill_card("/add-infographic", "図解をつける", "記事の一番上に載せる、図解の画像を作る。",
                     ["1　対象の記事を決める", "2　載せる要素を決める", "3　HTMLを作る", "4　画像にして確認", "5　記事に付ける"],
                     "呼ぶ担当：<br>なし"),
        gap=24, extra="flex:1"),
    "このブログには、3つのスキルがあります。1つ目のadd-ideaは、思いつきや今日あった出来事を、記事のネタにして残すスキルです。起点を見分けて、素材を掘って、切り口を立てて、1本に絞って、審査してネタ帳に書き込む、という5段階です。2つ目のwrite-postは、記事を書くスキルで、テーマ決めから保存までを質問しながら進めます。3つ目のadd-infographicは、記事の一番上に載せる図解の画像を作ります。下に書いてある名前は、そのスキルが途中で呼ぶ専門担当、つまりサブエージェントです。これは次のパートで説明します。")

# ---------------------------------------------------------------- write-post flow
def wp(step, title, body, kind="n"):
    if kind == "h":
        bg, bd, pc, pf = SUN_SOFT, SUN, SUN, INK
    elif kind == "a":
        bg, bd, pc, pf = BLUE, BLUE, "#FFFFFF", BLUE_T
    else:
        bg, bd, pc, pf = CARD, LINE, BLUE, "#FFFFFF"
    tc = "#FFFFFF" if kind == "a" else INK
    bc = "#E8EEFF" if kind == "a" else MUTED
    return card(pill(step, pc, pf, 26, extra="align-self:flex-start") + h3(title, 32, tc) + p(body, 26, bc, lh=1.5),
                bg=bg, border=bd, pad="22px 24px 26px", gap=10, extra="flex:1")

add("write-post-flow",
    head("PART 3 ／ スキル", "「記事を書く」スキルは、8つのステップ")
    + col(
        row(wp("0", "状況確認", "書きかけがないか、まず確認する")
            + wp("1", "テーマ決め", "次に書く候補を、理由つきで2〜3本出す")
            + wp("2", "体験の聞き取り", "一番時間をかける。うまくいかなかった話を必ず聞く", "h")
            + wp("3", "構成", "見出し案と、冒頭の2文を先に見せる"), gap=20, extra="flex:1")
        + row(wp("4", "下書き", "話してもらった言葉を、できるだけそのまま使う")
              + wp("5", "校閲", "校閲担当のAIに、点検を任せる", "a")
              + wp("6", "保存", "日付とカテゴリを決めて、ファイルにする")
              + wp("7", "後片付け", "ネタ帳を更新し、次に書く記事を提案する"), gap=20, extra="flex:1"),
        gap=20, extra="flex:1")
    + row(pill("黄色：一番の山場。人が話す", SUN, INK, 26) + pill("青：別のAIに任せる", BLUE, "#FFFFFF", 26), gap=16),
    "記事を書くスキルは、0番から7番までの8つのステップです。0番で書きかけがないか確認し、1番でテーマを決め、2番で私の体験を聞き取ります。この2番が手順書の中でも一番時間をかける場所で、『うまくいかなかったことはありませんでしたか』を必ず聞くと書いてあります。3番で構成、4番で下書き、5番で校閲、これは別のAIに任せます。6番で保存、7番でネタ帳などの後片付けと次の記事の提案です。人の体験を引き出すのが山場で、そこを飛ばして書き始めないように、手順書で順番を固定しています。")

# ---------------------------------------------------------------- dialog
def bubble(text, ai=True):
    return (f'<div style="display:flex; flex-direction:column; background:{CARD if ai else TINT}; border:2px solid {LINE if ai else "#B9CBFA"}; '
            f'border-radius:24px; padding:20px 28px; width:{820 if ai else 720}px; align-self:{"flex-start" if ai else "flex-end"}">'
            f'<p style="font-size:26px; line-height:1.6; color:{INK}">{text}</p></div>')

add("skill-dialog",
    head("PART 3 ／ スキル", "手順書どおりに動くと、こんな会話になる")
    + row(
        col(
            bubble("[2/7 聞き取り] このツールを試したのは、いつですか。うまくいかなかったことや、期待と違ったことはありませんでしたか。")
            + bubble("先週です。期待どおりに動かなくて、指示を3回書き直しました。", False)
            + bubble("その「期待どおりに動かなかった」話が、記事の芯になります。3回直したうち、最初の指示をそのまま教えてください。")
            + p("※手順書に書かれた質問とほめ方から作ったイメージで、実際の会話の記録ではありません。", 24, MUTED, lh=1.5),
            gap=16, extra="flex:none; width:900px")
        + col(
            p("手順書に書いてある決まり", 30, BLUE_T, 700)
            + card(p("<b>質問は1回に1〜2問まで</b><br>質問攻めにすると、書き手が疲れて続かない。", 26, INK, lh=1.5), pad="18px 28px", gap=4)
            + card(p("<b>今の現在地を見せる</b><br>「2/7 聞き取り」のように、いま何番目かを毎回示す。", 26, INK, lh=1.5), pad="18px 28px", gap=4)
            + card(p("<b>ほめるときは具体的に</b><br>「ありがとう」で終えず、どこが記事の武器になるかを言う。", 26, INK, lh=1.5), pad="18px 28px", gap=4),
            gap=14, extra="flex:1"),
        gap=44, extra="flex:1"),
    "手順書どおりに動くと、AIはこんな会話をします。これは手順書に書かれた質問とほめ方から作ったイメージで、実際の会話の記録ではありません。まず、いつ試したか、うまくいかなかったことはないかを聞きます。答えが返ってきたら、その中のどこが記事の芯になるかを具体的に言います。手順書には、質問は1回に1〜2問まで、いま何番目のステップかを毎回示す、ほめるときは具体的に、という決まりが書いてあります。質問攻めにされると書き手が疲れて、ブログが続かなくなるからです。")

# ---------------------------------------------------------------- infographic skill
add("skill-infographic",
    head("PART 3 ／ スキル", "図解のスキルには「破ってはいけない4つ」がある")
    + grid22([
        numcard("1", "画角は 1600×840", "ブログの画像枠と同じ縦横比。ちがうと、上下が切れてしまう。")
        , numcard("2", "文字は19px以上", "本文の幅では約8pxまで縮む。それより小さいと読めない。")
        , numcard("3", "収まらなければ、削る", "文字を小さくせず、載せる要素を減らす。")
        , numcard("4", "事実は、記事から取る", "記事に書いていない数字や断定を、図で足さない。")])
    + card(p("<b>焼いたあと、AI自身が縮めた画像を見て、全部の文字が読めるかを確かめる。</b>読めなければ、要素を削ってやり直す。", 28, INK, lh=1.55),
           bg=SUN_SOFT, border=SUN, pad="20px 36px", gap=0),
    "3つ目のスキルは、図解を作るスキルです。この手順書の特徴は、破ってはいけない4つのルールを最初に書いてあること。1つ目、画像の縦横比。2つ目、文字は19ピクセル以上。ブログの本文の幅では画像が縮むので、それより小さい文字は読めません。3つ目、入りきらないときは文字を小さくせず、載せるものを減らす。4つ目、図に書く事実はすべて記事から取る。そして最後に、AI自身が縮めた画像を見て、全部読めるかを確かめます。人に『よく見てね』と頼むのではなく、確認の手順まで手順書に書いておくのがコツです。")

# ---------------------------------------------------------------- skill design
add("skill-design",
    head("PART 3 ／ スキル", "手順書を書くときの、4つの工夫")
    + grid22([
        numcard("1", "役割と目的を、最初に書く", "「代筆ではなく、体験を引き出す役」と書いておくと、AIの動きがぶれない。")
        , numcard("2", "手順に番号をつけ、読む文書も決める", "段階ごとに「この文書を開く」と指定して、記憶で書かせない。")
        , numcard("3", "質問は1回に1〜2問まで", "一度にたくさん聞くと、答える人が疲れて続かない。")
        , numcard("4", "やってはいけないことも書く", "「たぶんこうなるはず」で書かせない。中身のないお世辞は挟まない。")]),
    "手順書を書くときの工夫を4つ挙げます。1つ目、役割と目的を最初に書く。このブログのスキルには、代筆ではなく体験を引き出す役だと書いてあります。2つ目、手順に番号をつけて、どの段階でどの文書を読むかも決める。AIに記憶で書かせず、その場で最新のルールを読ませます。3つ目、質問は1回に1〜2問まで。4つ目、やってはいけないことも書く。体験が無いのに、たぶんこうなるはずで書かせない、という具合です。AIには、してほしいことだけでなく、してほしくないことも言葉にして渡すのがコツです。")

# ================================================================ PART 4 : sub-agents
divider("part4-divider", 4, f"AIの助っ人②<br>{hl('サブエージェント')}", "別の部屋で働く「専門担当」。このブログでは3人いる。",
        "2つ目の助っ人は、サブエージェントです。スキルが手順書だったのに対して、サブエージェントは専門の担当者です。メインのAIから頼まれて、別の部屋で自分の専門の仕事だけをして、結果を返してくれます。")

# ---------------------------------------------------------------- agent-what
def reason(title, body):
    return card(h3(title, 34, BLUE_T) + p(body, 26, INK, lh=1.5), pad="22px 28px 26px", gap=6, extra="flex:1")

add("agent-what",
    head("PART 4 ／ サブエージェント", "サブエージェントは、別の部屋で働く専門担当")
    + row(
        card(icon_tile("Chat", BLUE, "#FFFFFF", 80, 48) + h3("メインのAI", 40) + p("書き手と会話しながら、仕事全体を進める。", 28, MUTED, lh=1.5),
             pad="28px 32px 32px", gap=12, extra="flex:none; width:560px")
        + col(
            p("① お願いする", 28, INK, 700, extra="text-align:center", lh=1.4)
            + p("「この下書きを点検して」", 26, MUTED, extra="text-align:center", lh=1.4)
            + arrow_r()
            + arrow_left_shape()
            + p("② 結果だけを返す", 28, INK, 700, extra="text-align:center", lh=1.4),
            gap=8, extra="flex:1; justify-content:center")
        + card(icon_tile("Search", SUN, INK, 80, 48) + h3("サブエージェント", 40) + p("別の部屋で、頼まれた仕事だけをする専門担当。", 28, INK, lh=1.5),
               bg=SUN_SOFT, border=SUN, pad="28px 32px 32px", gap=12, extra="flex:none; width:560px"),
        gap=16, extra="flex:none")
    + row(
        reason("専門に集中できる", "「校閲だけ」「ネタ出しだけ」と、役割を絞れる。")
        + reason("持ち物を絞れる", "必要な道具だけ渡せる。書き換える道具は渡さない、もできる。")
        + reason("メインの頭が散らからない", "調べものの途中経過は持ち帰らず、結果だけ受け取る。"),
        gap=20),
    "サブエージェントは、別の部屋で働く専門担当です。仕組みはこうです。メインのAIが、この下書きを点検してとお願いする。サブエージェントは別の部屋で、頼まれた仕事だけをやる。そして結果だけをメインのAIに返す。これで得られることが3つあります。1つ目、校閲だけ、ネタ出しだけと、役割を絞って専門に集中できる。2つ目、持ち物を絞れる。必要な道具だけ渡して、書き換える道具は渡さない、ということもできます。3つ目、調べものの途中経過は持ち帰らず結果だけ受け取るので、メインのAIの頭が散らかりません。")

# ---------------------------------------------------------------- agent-file
add("agent-file",
    head("PART 4 ／ サブエージェント", "サブエージェントも、1つの文書ファイル")
    + row(
        codebox(".claude/agents/post-reviewer.md", [
            cl("---", CM),
            kv("name:", " post-reviewer"),
            kv("description:", " 🖍️ アカネ。記事の下書きを、"),
            cl("  書き方のルールに照らして校閲する。…"),
            kv("color:", " red"),
            cl(f'<span style="color:{SUN}">tools: Read, Grep, Glob, Bash</span>'),
            cl("---", CM),
            cl("あなたはこのブログの校閲担当、"),
            cl("アカネ🖍️です。"),
            cl("下書きのパスを受け取り、"),
            cl("照合結果だけを返します。"),
            cl("ファイルは編集しません。"),
        ], width=860)
        + col(
            card(h3("name と description", 34, BLUE_T) + p("name は呼び出しに使うID。人向けの名前「アカネ」と「いつ頼むか」は description に書く。", 28, INK, lh=1.5), pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("tools：持ち物リスト", 34, "#FFFFFF") + p("読む・探す・実行する道具はある。文章を直す道具（Edit・Write）は持たせていない。", 28, "#E8EEFF", lh=1.5), bg=BLUE, border=BLUE, pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center")
            + card(h3("本文：役割と、返すもの", 34, BLUE_T) + p("「あなたは校閲担当、アカネです」と役割を決め、何を返すかを書く。", 28, INK, lh=1.5), pad="22px 32px 26px", gap=6, extra="flex:1; justify-content:center"),
            gap=16, extra="flex:1"),
        gap=40, extra="flex:1"),
    "サブエージェントの実物も、スキルと同じく1つの文書ファイルです。これは校閲担当、アカネの冒頭です。nameのpost-reviewerは呼び出しに使うIDで、人と話すときの名前アカネは、いつ頼むかの説明と一緒にdescriptionに書いてあります。colorは画面に出る色で、アカネは赤です。そして黄色い行のtools、これが持ち物リストです。ファイルを読む、探す、コマンドを実行する道具は渡してありますが、文章を書き換える道具は持たせていません。本文は『あなたはこのブログの校閲担当、アカネです』で始まり、下書きのパスを受け取って、照合結果だけを返す、ファイルは編集しない、と書いてあります。校閲担当は指摘しかできない作りになっています。")

# ---------------------------------------------------------------- skill vs agent
def trs(rows, widths, size=32):
    out = f'<table style="font-family:{BODY}; font-size:{size}px; color:{INK}">'
    for ri, r in enumerate(rows):
        bgc = BLUE if ri == 0 else (CARD if ri % 2 else TINT)
        out += f'<tr style="background:{bgc}">'
        for ci, c in enumerate(r):
            if ri == 0:
                out += f'<th style="width:{widths[ci]}%; color:#FFFFFF; text-align:left">{c}</th>'
            else:
                out += f'<td style="text-align:left">{"<b>" + c + "</b>" if ci == 0 else c}</td>'
        out += '</tr>'
    return out + '</table>'

add("skill-vs-agent",
    head("PART 4 ／ サブエージェント", "スキルとサブエージェントのちがい")
    + trs([
        ["", "スキル", "サブエージェント"],
        ["たとえ", "手順書（レシピ）", "専門の担当者"],
        ["どこで動く", "メインのAIが、会話しながら実行", "別の部屋で、頼まれた仕事だけ"],
        ["書き手と話す？", "話す。質問しながら進める", "話さない。結果を返すだけ"],
        ["持ち物", "メインのAIと同じ", "役割に必要な道具だけ"],
        ["このブログでは", "3つ（ネタ・記事・図解）", "3人（ネタ出し・審査・校閲）"],
    ], [24, 38, 38, ], 32)
    + p("スキルが仕事の段取りを決め、途中で専門担当を呼ぶ。この組み合わせで動いている。", 32, MUTED),
    "スキルとサブエージェントのちがいを表にまとめました。スキルは手順書で、メインのAIが書き手と会話しながら実行します。だから質問もします。サブエージェントは専門の担当者で、別の部屋で頼まれた仕事だけをして、結果を返します。書き手と直接は話しません。持ち物も、サブエージェントは役割に必要な道具だけです。このブログでは、スキルが3つ、サブエージェントが3人います。スキルが仕事の段取りを決めて、途中で専門担当を呼ぶ、という組み合わせで動いています。")

# ---------------------------------------------------------------- agents three
def ag3(name, nick, role_, ask, keep):
    return card(
        pill(name, BLUE, "#FFFFFF", 24, extra=f"align-self:flex-start; font-family:{MONO}")
        + row(h3(nick, 40) + p(role_, 28, MUTED, 700, lh=1.3), gap=16, extra="align-items:baseline")
        + p("頼まれること", 24, BLUE_T, 700, lh=1.4) + p(ask, 26, INK, lh=1.5)
        + p("守っていること", 24, BLUE_T, 700, lh=1.4, extra="padding-top:8px") + p(keep, 26, INK, lh=1.5),
        pad="28px 32px 32px", gap=8, extra="flex:1")

add("agents-three",
    head("PART 4 ／ サブエージェント", "このブログで働く、3人の専門担当")
    + row(
        ag3("idea-generator", "💡 ヒラク", "ネタ出し担当", "思いつきや外部の記事から、記事ネタの切り口を3〜5案出す。",
            "案ごとに「何で勝負するか」を名指しする。書き手が話していない体験は、でっち上げない。")
        + ag3("idea-reviewer", "🗃️ クラ", "ネタ帳の門番", "ネタ帳に積んでよいか審査する。重複・分類・価値、ChatGPTで代わりが利かないかを見る。",
              "落とすときは、素材が活きる別の置き場所を必ず示す。")
        + ag3("post-reviewer", "🖍️ アカネ", "校閲担当", "書き上がった下書きを、書き方のルールに照らして点検する。",
              "直す価値があるものだけを、直し文つきで返す。粗探しで件数を稼がない。"),
        gap=24, extra="flex:1"),
    "このブログで働くサブエージェントは3人います。1人目はネタ出し担当のヒラク。切り口を拓くからヒラクです。思いつきや外部の記事から、記事ネタの切り口を3〜5案出します。守っているのは、案ごとに何で勝負するかを名指しすること、そして書き手が話していない体験をでっち上げないことです。2人目はネタ帳の門番、クラ。ネタ帳という蔵の番をするのでクラです。ネタ帳に積んでよいかを審査します。既存のネタと重なっていないか、価値があるか、ChatGPTで代わりが利かないか。落とすときは、その素材が活きる別の置き場所を必ず示す決まりです。3人目が校閲担当のアカネで、原稿に赤を入れるからアカネ。書き上がった下書きを点検します。直す価値があるものだけを、直し文つきで返します。名前をつけたのは、会話の中で『アカネに見てもらいます』と呼べると、いま誰が何をしているかを追いやすいからです。")

# ---------------------------------------------------------------- post-reviewer detail
def chk(letter, title, body, hot=False):
    return card(
        row(f'<p style="flex:none; width:52px; height:52px; text-align:center; font-family:{DISPLAY}; font-size:30px; font-weight:900; line-height:52px; '
            f'background:{SUN if hot else BLUE}; color:{INK if hot else "#FFFFFF"}; border-radius:26px">{letter}</p>'
            + h3(title, 32, INK, extra="flex:1"), gap=16, extra="align-items:center")
        + p(body, 26, MUTED, lh=1.5),
        bg=SUN_SOFT if hot else CARD, border=SUN if hot else LINE, pad="18px 28px 22px", gap=8, extra="flex:1")

add("post-reviewer",
    head("PART 4 ／ サブエージェント", "校閲担当のアカネは、6つの観点で下書きを点検する")
    + col(
        row(chk("A", "言い回し", "「〜と言えるでしょう」など、避ける表現がないか") + chk("B", "固有性（最重要）", "体験・失敗・実測の数字・判断の理由が入っているか", True), gap=20, extra="flex:1")
        + row(chk("C", "守秘", "常駐先の人が読んで、自社だと分かる書き方でないか") + chk("D", "型と構成", "冒頭で「誰の悩みか」を示しているか"), gap=20, extra="flex:1")
        + row(chk("E", "構造の癖", "太字の連打や、機械的な長所・短所の対がないか") + chk("F", "公開前の一問", "ChatGPTに聞けば、同じ答えが出ないか"), gap=20, extra="flex:1"),
        gap=20, extra="flex:1")
    + card(p("<b>返すもの</b>：判定（公開可／要修正）と、直す箇所を「必須・推奨・好み」の3段階で。直し文と、良かった点もつける。", 28, INK, lh=1.55),
           bg=TINT, border="#B9CBFA", pad="18px 32px", gap=0),
    "校閲担当のアカネがどんな観点で見ているかを、もう少し詳しく見ます。6つあります。A、避ける言い回しがないか。B、固有性。これが最重要で、体験、失敗、実測の数字、判断の理由のどれかが入っているかを見ます。C、守秘。常駐先の人が読んで自社のことだと分かる書き方になっていないか。D、記事の型と構成。E、構造の癖。太字の連打などです。F、公開前の一問。ChatGPTに聞けば同じ答えが返ってくるなら、書く意味がない。この観点は、ルールブックの文書から取っています。返すものも決まっていて、判定と、必須・推奨・好みの3段階の指摘、直し文、良かった点です。粗探しで件数を稼がないよう、好みの指摘は多くても2件までと決めています。")

# ================================================================ PART 5 : division of labour
divider("part5-divider", 5, f"{hl('人とAI')}の分担", "スキルとサブエージェントを、どうつなぐか。人が決めるのはどこか。",
        "最後のパートです。ここまで見てきたスキルとサブエージェントを、実際にどうつないでいるのか。そして、AIに任せていない部分、人が決めている部分はどこかを見ます。")

# ---------------------------------------------------------------- teamwork
def chip(title, sub, kind, mono=False):
    if kind == "s":
        bg, bd, tc, sc = BLUE, BLUE, "#FFFFFF", "#E8EEFF"
    elif kind == "a":
        bg, bd, tc, sc = CARD, BLUE, BLUE_T, MUTED
    elif kind == "h":
        bg, bd, tc, sc = SUN, SUN, INK, INK
    else:
        bg, bd, tc, sc = CARD, LINE, INK, MUTED
    tstyle = f"font-family:{MONO}; font-size:24px; font-weight:500" if mono else f"font-family:{DISPLAY}; font-size:28px; font-weight:900"
    return (f'<div style="flex:1; display:flex; flex-direction:column; gap:6px; background:{bg}; border:3px solid {bd}; border-radius:24px; padding:18px 16px 20px">'
            f'<p style="{tstyle}; line-height:1.4; color:{tc}">{title}</p>'
            f'<p style="font-size:24px; line-height:1.45; color:{sc}">{sub}</p></div>')

def lane(label, chips):
    inner = ""
    for i, c in enumerate(chips):
        if i:
            inner += arrow_r(MUTED).replace("width:56px", "width:40px")
        inner += c
    return col(p(label, 28, BLUE_T, 700, lh=1.4) + row(inner, gap=8, extra="align-items:stretch"), gap=10)

add("teamwork",
    head("PART 5 ／ 人とAIの分担", "スキルとサブエージェントは、こうつながる")
    + col(
        lane("ネタを積む", [
            chip("/add-idea", "起点を見分けて、素材を掘る", "s", True),
            chip("💡 ヒラク", "切り口を3〜5案返す", "a"),
            chip("人が選ぶ", "1本に絞る", "h"),
            chip("🗃️ クラ", "重複と価値を審査する", "a"),
            chip("ネタ帳に追加", "公開順への影響も確認", "o")])
        + lane("記事を書く", [
            chip("/write-post", "テーマを決めて、質問する", "s", True),
            chip("人が話す", "失敗談も含めて", "h"),
            chip("/write-post", "話した言葉を活かして下書き", "s", True),
            chip("🖍️ アカネ", "6つの観点で点検する", "a"),
            chip("人が直す", "最終判断は書き手", "h")]),
        gap=24)
    + row(pill("スキル（手順書）", BLUE, "#FFFFFF", 26) + pill("サブエージェント（専門担当）", "#FFFFFF", BLUE_T, 26, extra=f"border:3px solid {BLUE}")
          + pill("人", SUN, INK, 26), gap=16),
    "この2つを、実際にどうつないでいるかを図にしました。上の段がネタを積むとき。add-ideaのスキルが起点を見分けて素材を掘り、ネタ出し担当のヒラクが切り口を3〜5案返します。ここで人が1本に選びます。そのあと門番のクラが審査して、ネタ帳に追加します。下の段が記事を書くとき。write-postのスキルがテーマを決めて質問し、私が体験を話し、それを活かして下書きを書き、校閲担当のアカネが点検して、最後は人が直します。黄色が人、青がスキル、白が専門担当のサブエージェントです。人が入る場所は、選ぶ、話す、直す。つまり判断が必要なところです。")

# ---------------------------------------------------------------- rules
add("rules",
    head("PART 5 ／ 人とAIの分担", "AIに任せるときに決めている、4つのルール")
    + grid22([
        numcard("1", "「点検する」と「直す」を分ける", "点検・審査のAIは、指摘だけを返す。直すかどうかは、人が決める。")
        , numcard("2", "持ち物を絞る", "役割に要らない道具は渡さない。校閲担当には、文章を書き換える道具を持たせない。")
        , numcard("3", "毎回、最新のルールを読ませる", "記憶で判断させず、その場でルールブックを開かせる。")
        , numcard("4", "最後の決定は、人", "何を書くか、どう言うか、いつ公開するかは、書き手が決める。")]),
    "AIに任せるときに決めている4つのルールです。1つ目、点検することと直すことを分ける。点検するAIは指摘だけを返し、直すかどうかは人が決めます。2つ目、持ち物を絞る。役割に要らない道具は渡しません。3つ目、毎回最新のルールを読ませる。記憶で判断させず、その場でルールブックを開かせます。ルールは更新されるからです。4つ目、最後の決定は人。何を書くか、どう言うか、いつ公開するかは書き手が決めます。AIをうまく使うコツは、何でも任せることではなく、任せる範囲と任せない範囲を先に決めておくことだと考えています。")

# ---------------------------------------------------------------- human statement
add("human",
    col(
        p("PART 5 ／ 人とAIの分担", 26, "#DCE6FF", 700, extra="letter-spacing:3px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:72px; font-weight:900; line-height:1.3; color:#FFFFFF">「AIに聞けば出てくる答え」ではなく、<br><span style="color:{SUN}">実際にやってみた体験</span>を載せる</h2>'
        + row(
            pill("うまくいかなかったことも含む体験", "#FFFFFF", BLUE_T, 28)
            + pill("同じ現場で働く人の視点", "#FFFFFF", BLUE_T, 28)
            + pill("最初に何を学ぶかの選び方", "#FFFFFF", BLUE_T, 28), gap=16, extra="flex-wrap:wrap")
        + p("ChatGPTに聞いても同じ答えが出るなら、書く意味がない。だから、AIには書けない部分を人が担当する。", 32, "#E8EEFF", extra="padding-top:16px"),
        gap=28),
    "このブログの方針です。AIに聞けば出てくる答えは載せません。載せるのは、実際にやってみた体験、失敗も含めて。同じ現場で働く人の視点。そして、最初に何を学んで何を後回しにするかという選び方。この3つのどれかが入っていない記事は、書く意味が薄いと考えています。だから助っ人のAIは、まず私に体験をたずねて、それを文章の形に整える役をしています。校閲担当が最後に必ず出す『公開前の一問』も、この方針から来ています。",
    bg=BLUE, dark=True, justify="center", footer=False)

# ---------------------------------------------------------------- 22 summary
def sm(num, title, body):
    return row(
        f'<p style="flex:none; width:80px; height:80px; text-align:center; font-family:{DISPLAY}; font-size:48px; font-weight:900; line-height:80px; background:{BLUE}; color:#FFFFFF; border-radius:40px">{num}</p>'
        + col(h3(title, 36) + p(body, 28, MUTED, lh=1.5), gap=2, extra="flex:1; justify-content:center"),
        gap=28, extra="align-items:center; background:%s; border:2px solid %s; border-radius:28px; padding:18px 32px" % (CARD, LINE))

add("summary",
    head("まとめ", "今日の4つのポイント")
    + col(
        sm("1", "人は「書く」と「送る」だけ", "組み立ても公開も、GitHub のロボットが自動でやる。")
        + sm("2", "AIは「次のことば」を予想する機械", "もっともらしい嘘も書くので、人が確かめる。")
        + sm("3", "スキルは手順書、サブエージェントは専門担当", "手順書で進め方を決め、専門担当に点検を任せる。")
        + sm("4", "任せる範囲と、任せない範囲を先に決める", "体験と最終決定は、人がやる。"),
        gap=16),
    "まとめです。1つ目、このブログは人が書いて送るだけで、あとは自動で公開されます。2つ目、AIは次のことばを予想する機械で、もっともらしい嘘も書くので人が確かめます。3つ目、今日のメインです。スキルは手順書、サブエージェントは専門担当。手順書で進め方を決めて、専門担当に点検を任せます。4つ目、任せる範囲と任せない範囲を先に決めておく。体験と最終決定は人がやります。",
    section=("s7", "まとめと、ブログへの案内"))

# ---------------------------------------------------------------- 23 QR
def qr_svg(url, px=560):
    q = segno.make(url, error="m")
    m = [list(r) for r in q.matrix]
    n = len(m)
    border = 4
    parts = []
    for y, r in enumerate(m):
        x = 0
        while x < n:
            if r[x]:
                s = x
                while x < n and r[x]:
                    x += 1
                parts.append(f'M{s + border} {y + border}h{x - s}v1h-{x - s}z')
            else:
                x += 1
    tot = n + border * 2
    return (f'<svg width="{tot * 10}" height="{tot * 10}" viewBox="0 0 {tot} {tot}" shape-rendering="crispEdges" aria-label="ブログ {url} を開くQRコード">'
            f'<rect width="{tot}" height="{tot}" fill="#FFFFFF"/><path d="{"".join(parts)}" fill="#000000"/></svg>'), tot * 10

svg, side = qr_svg(URL)
add("qr",
    col(
        p("ぜひ、読みにきてください", 32, D_ACC, 700, extra="letter-spacing:2px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:88px; font-weight:900; line-height:1.25; color:{D_TEXT}">明日使える<br><span style="color:{SUN}">生成AI</span></h2>'
        + p("スマホでQRコードを読みとると、ブログが開きます。", 32, D_TEXT, extra="padding-top:16px")
        + p("raindrop-aqua.github.io/blog-ap-sys", 32, D_ACC, 500, extra=f"font-family:{MONO}; padding-top:8px"),
        gap=12, extra="flex:1")
    + f'<div style="flex:none; width:{side + 80}px; height:{side + 80}px; background:#FFFFFF; border-radius:40px; padding:40px; display:flex; align-items:center; justify-content:center">{svg}</div>',
    "最後まで聞いてくださってありがとうございます。右のQRコードを読みとると、このブログが開きます。書いている記事は、実際にAIを使ってみた体験がベースです。ぜひ読みに来てください。",
    bg=INK, dark=True, footer=False, direction="row", align="center", gap=96, pad="128px 128px 128px")

# ---------------------------------------------------------------- write
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
    "title": "ブログのしくみ解説スライド",
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
