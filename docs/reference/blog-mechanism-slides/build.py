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


# ---------------------------------------------------------------- 1 cover
add("cover",
    col(
        p("「明日使える生成AI」ブログのひみつ", 32, D_ACC, 700, extra="letter-spacing:2px")
        + f'<h1 style="font-family:{DISPLAY}; font-size:88px; font-weight:900; line-height:1.25; color:{D_TEXT}">'
          f'文章を書いて送ると、<br><span style="color:{SUN}">自動でWebサイト</span>になる</h1>'
        + p("ブログのしくみと、その中で働くAIのしくみ", 40, D_TEXT, 400, extra="padding-top:24px"),
        gap=24, extra="width:1100px"),
    "はじめに自己紹介。このブログ「明日使える生成AI」は、ふつうのブログサービスにある『投稿ボタン』がありません。文章のファイルを置いて送るだけで、ロボットがサイトを作って公開してくれます。今日はそのしくみを、中学生でもわかる言葉で説明します。特にAIの話は、いつもより丁寧にやります。",
    bg=INK, dark=True, footer=False, justify="center",
    backdrop=(f'<x-shape kind="ellipse" style="position:absolute; left:1232px; top:200px; width:560px; height:560px; background:{BLUE}; opacity:0.45"></x-shape>'
              f'<x-shape kind="ellipse" style="position:absolute; left:1552px; top:640px; width:200px; height:200px; background:{SUN}"></x-shape>'),
    section=("s1", "今日の話の入り口と全体の流れ"))

# ---------------------------------------------------------------- 2 agenda
def ag(num, title, sub, bg, fg, sf):
    return card(
        f'<p style="font-family:{DISPLAY}; font-size:96px; font-weight:900; line-height:1; color:{fg}">{num}</p>'
        + h3(title, 44, fg) + p(sub, 28, sf, extra="padding-top:8px"),
        bg=bg, border=bg, pad="44px 44px 48px", gap=16, extra="flex:1")

add("agenda",
    head("AGENDA", "今日の流れ")
    + row(
        ag("1", "ブログのしくみ", "書いた文章が、どうやってWebサイトになるのか", CARD, BLUE_T, MUTED)
        + ag("2", "AIのしくみ", "生成AIは中で何をしているのか。ここを一番くわしく", BLUE, "#FFFFFF", "#E8EEFF")
        + ag("3", "AIとブログ", "AIに任せる部分と、人にしかできない部分", CARD, BLUE_T, MUTED),
        gap=36, extra="flex:1"),
    "全体は3つのパートです。1つ目はブログそのものの仕組み。2つ目がAIの仕組みで、今日の一番のメインです。3つ目は、その2つがどう組み合わさってこのブログができているか。",
    section=None)

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
    section=("s2", "記事がWebサイトになって公開されるまでのしくみ"))

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
add("ai-divider",
    col(
        p("PART 2", 32, D_ACC, 700, extra="letter-spacing:4px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:96px; font-weight:900; line-height:1.25; color:{D_TEXT}">ここからは、<br><span style="color:{SUN}">AI</span>のしくみ</h2>'
        + p("このブログの記事づくりを手伝っている「生成AI」は、中で何をしているのか。", 36, D_MUTED, extra="padding-top:16px"),
        gap=20, extra="width:1200px"),
    "ここからがメインのAIの話です。ブログを書くとき、私はClaudeというAIに手伝ってもらっています。そのAIが、中で何をしているのか。難しい数式は使わずに、たとえ話で説明します。",
    bg=INK, dark=True, footer=False, justify="center",
    backdrop=(f'<x-shape kind="ellipse" style="position:absolute; left:1352px; top:520px; width:440px; height:440px; background:{BLUE}; opacity:0.4"></x-shape>'
              f'<x-shape kind="ellipse" style="position:absolute; left:1232px; top:760px; width:160px; height:160px; background:{SUN}"></x-shape>'),
    section=("s3", "生成AIが文章を作るしくみを、たとえ話で順番に"))

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

# ---------------------------------------------------------------- 19 helpers
def li(name, body):
    return card(p(name, 28, BLUE_T, 700, extra=f"font-family:{MONO}", lh=1.3) + p(body, 26, INK, lh=1.5), pad="16px 28px", gap=2)

add("helpers",
    head("PART 3 ／ AIとブログ", "ルールブック3冊と、AIの助っ人")
    + row(
        col(
            h3("ルールブック（人が決める）", 36, INK)
            + li("content-strategy.md", "だれに向けて、どんな分類で書くか。ブログの方針")
            + li("article-backlog.md", "書きたい記事のストック帳。順番のきまりも")
            + li("writing-style.md", "文章の口調と、体験談を書くときの守りごと"),
            gap=14, extra="flex:1")
        + col(
            h3("AIの助っ人（手順書を渡してある）", 36, INK)
            + li("/add-idea", "思いつきや今日の出来事を、記事のネタに足す")
            + li("/write-post", "ネタ選びから下書き・保存まで、質問しながら進める")
            + li("post-reviewer", "🖍️ アカネ。書き上がった下書きを、ルールブックに照らして点検")
            + li("/add-infographic", "記事の一番上に載せる、図解の画像を作る"),
            gap=14, extra="flex:1"),
        gap=48, extra="flex:1"),
    "このブログには、記事の作り方の決まりがあります。ルールは3冊のルールブックにまとめてあって、これは人が決めます。作業のほうは、AIに手順書を渡して手伝ってもらっています。ネタを足す、下書きを書く、ルールブックに照らして点検する、記事の上に載せる図解を作る、といった助っ人が用意してあります。AIは、ルールブックを毎回読み直して、その決まりに沿って動きます。")

# ---------------------------------------------------------------- 20 chain
def cstep(num, title, cmd, human=False):
    return card(
        row(p(num, 44, INK if human else BLUE_T, 900, extra=f"font-family:{DISPLAY}", lh=1.2)
            + col(h3(title, 32) + p(cmd, 24, INK if human else MUTED, extra=f"font-family:{MONO}", lh=1.3), gap=4), gap=20, extra="align-items:center"),
        bg=SUN_SOFT if human else CARD, border=SUN if human else LINE, pad="28px 32px", gap=8, extra="flex:1")

add("chain",
    head("PART 3 ／ AIとブログ", "記事ができるまでの6ステップ")
    + col(
        row(cstep("1", "ネタを出す", "/add-idea") + cstep("2", "自分の体験を話す", "人がやる", True) + cstep("3", "下書きを作る", "/write-post"), gap=24)
        + row(cstep("4", "点検する", "🖍️ アカネ") + cstep("5", "図解をつける", "/add-infographic") + cstep("6", "送る（push）", "人がやる", True), gap=24),
        gap=24)
    + p("黄色が、人にしかできない部分。それ以外は、AIが手伝う。", 32, MUTED),
    "記事ができるまでは6ステップです。1つ目のネタ出しは、AIが切り口をいくつも出してくれます。2つ目が大事で、私が自分の体験を話します。3つ目でAIが下書きを作り、4つ目で別のAI、校閲担当のアカネがルールブックに照らして点検し、5つ目で図解を作ります。そして6つ目、pushして公開するのは人です。黄色い2つが人の仕事です。")

# ---------------------------------------------------------------- 21 human statement
add("human",
    col(
        p("PART 3 ／ AIとブログ", 26, "#DCE6FF", 700, extra="letter-spacing:3px")
        + f'<h2 style="font-family:{DISPLAY}; font-size:72px; font-weight:900; line-height:1.3; color:#FFFFFF">「AIに聞けば出てくる答え」ではなく、<br><span style="color:{SUN}">実際にやってみた体験</span>を載せる</h2>'
        + row(
            pill("うまくいかなかったことも含む体験", "#FFFFFF", BLUE_T, 28)
            + pill("同じ現場で働く人の視点", "#FFFFFF", BLUE_T, 28)
            + pill("最初に何を学ぶかの選び方", "#FFFFFF", BLUE_T, 28), gap=16, extra="flex-wrap:wrap")
        + p("ChatGPTに聞いても同じ答えが出るなら、書く意味がない。だから、AIには書けない部分を人が担当する。", 32, "#E8EEFF", extra="padding-top:16px"),
        gap=28),
    "このブログの方針です。AIに聞けば出てくる答えは載せません。載せるのは、実際にやってみた体験、失敗も含めて。同じ現場で働く人の視点。そして、最初に何を学んで何を後回しにするかという選び方。この3つのどれかが入っていない記事は、書く意味が薄いと考えています。だから助っ人のAIは、まず私に体験をたずねて、それを文章の形に整える役をしています。",
    bg=BLUE, dark=True, justify="center", footer=False)

# ---------------------------------------------------------------- 22 summary
def sm(num, title, body):
    return row(
        f'<p style="flex:none; width:96px; height:96px; text-align:center; font-family:{DISPLAY}; font-size:56px; font-weight:900; line-height:96px; background:{BLUE}; color:#FFFFFF; border-radius:48px">{num}</p>'
        + col(h3(title, 40) + p(body, 30, MUTED), gap=4, extra="flex:1; justify-content:center"),
        gap=32, extra="align-items:center; background:%s; border:2px solid %s; border-radius:28px; padding:24px 36px" % (CARD, LINE))

add("summary",
    head("まとめ", "今日の3つのポイント", )
    + col(
        sm("1", "人は「書く」と「送る」だけ", "組み立ても公開も、GitHub のロボットが自動でやってくれる。")
        + sm("2", "AIは「次のことば」を予想する機械", "大量の文章から学んだパターンで、1語ずつ書き足す。もっともらしい嘘も書くので、人が確かめる。")
        + sm("3", "AIは助っ人。体験は人が書く", "AIに任せる部分と、人にしかできない部分を分けると、いい記事になる。"),
        gap=20),
    "まとめです。1つ目、このブログは人が書いて送るだけで、あとは自動で公開されます。2つ目、AIは次のことばを予想する機械で、大量の文章から学んだパターンで1語ずつ書き足します。もっともらしい嘘も書くので、人が確かめます。3つ目、AIは助っ人で、体験を書くのは人。AIに任せる部分と人にしかできない部分を分けると、いい記事になります。",
    section=("s4", "まとめと、ブログへの案内"))

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
