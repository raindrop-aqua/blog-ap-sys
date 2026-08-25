#!/bin/sh
# インフォグラフィックHTMLをPNGに焼く。
#   usage: ./render.sh src/xxx.html [幅 高さ]
# 既定の 1600x840 は 40:21。Chirpy の preview-img 枠(aspect-ratio: 40/21)と
# OGP画像の 1200x630 がどちらも同じ比率なので、上下を切られずに収まる。
# Chrome headless でレンダリングするので、Webフォント(BIZ UDPGothic)や
# CSS Grid がそのまま使える。出力は out/ に 2倍解像度で置く。
set -e

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SRC="$1"
W="${2:-1600}"
H="${3:-840}"

[ -f "$SRC" ] || { echo "no such file: $SRC" >&2; exit 1; }

DIR=$(cd "$(dirname "$0")" && pwd)
BASE=$(basename "$SRC" .html)
OUT="$DIR/out/$BASE.png"
ABS=$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")

mkdir -p "$DIR/out"

"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=2 \
  --window-size="$W,$H" \
  --virtual-time-budget=10000 \
  --screenshot="$OUT" \
  "file://$ABS" >/dev/null 2>&1

# 平坦な色面ばかりなので減色してもほぼ劣化しない。ファイルサイズを1/3程度に落とす
magick "$OUT" -strip -colors 200 -define png:compression-level=9 "$OUT"

echo "$OUT  ($(du -h "$OUT" | cut -f1))"
