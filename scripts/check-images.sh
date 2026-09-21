#!/bin/sh
# ビルド済みサイト（_site）の <img> を全ページ分たどり、参照先のファイルが実在するか確かめる。
# 1件でも無ければ非0で終わるので、CI に置けばデプロイ前に止められる。
#
# 使い方: scripts/check-images.sh [サイトのディレクトリ] [baseurl]
#   既定は _site と /blog-ap-sys（_config.yml の baseurl と同じ値を渡すこと）
#
# 拾える例:
#   - 本文に {{ site.baseurl }}/assets/... と書いて baseurl が二重になった（Chirpy が自動で付けるため）
#   - baseurl が付いていない（/assets/... のまま出ている）
#   - ファイル名の打ち間違い、PNG の入れ忘れ
set -eu

cd "$(dirname "$0")/.."

SITE="${1:-_site}"
BASEURL="${2:-/blog-ap-sys}"
BASEURL="${BASEURL%/}"

if [ ! -d "$SITE" ]; then
  echo "エラー: $SITE がありません。先に jekyll build を実行してください" >&2
  exit 2
fi

errors=0
checked=0

# 1行1参照で「HTMLファイル<TAB>参照先」を作る。lazy-load 用の data-src も見る
refs=$(find "$SITE" -name '*.html' -print0 \
  | xargs -0 grep -oE '<img[^>]*>' /dev/null \
  | awk '{
      i = index($0, ":"); page = substr($0, 1, i - 1); tag = substr($0, i + 1)
      while (match(tag, /(data-)?src="[^"]*"/)) {
        attr = substr(tag, RSTART, RLENGTH); tag = substr(tag, RSTART + RLENGTH)
        sub(/^[^"]*"/, "", attr); sub(/"$/, "", attr)
        printf "%s\t%s\n", page, attr
      }
    }' || true)

while IFS="$(printf '\t')" read -r page ref; do
  [ -n "$ref" ] || continue
  case "$ref" in
    http://*|https://*|//*|data:*) continue ;;
  esac

  ref_path="${ref%%[?#]*}"
  checked=$((checked + 1))

  case "$ref_path" in
    /*)
      if [ -n "$BASEURL" ]; then
        case "$ref_path" in
          "$BASEURL"/*) target="$SITE${ref_path#"$BASEURL"}" ;;
          *)
            echo "NG  $page"
            echo "    $ref  ← baseurl($BASEURL) が付いていない"
            errors=$((errors + 1))
            continue
            ;;
        esac
      else
        target="$SITE$ref_path"
      fi
      ;;
    *) target="$(dirname "$page")/$ref_path" ;;
  esac

  if [ ! -e "$target" ]; then
    echo "NG  $page"
    case "$ref_path" in
      "$BASEURL$BASEURL"/*)
        echo "    $ref  ← baseurl が二重（本文の画像パスに {{ site.baseurl }} を書いていないか）" ;;
      *)
        echo "    $ref  ← ファイルがない（探した先: $target）" ;;
    esac
    errors=$((errors + 1))
  fi
done <<EOT
$refs
EOT

if [ "$errors" -gt 0 ]; then
  echo "画像リンク切れ: $errors 件（確認した参照 $checked 件）" >&2
  exit 1
fi
echo "画像リンクOK（確認した参照 $checked 件）"
