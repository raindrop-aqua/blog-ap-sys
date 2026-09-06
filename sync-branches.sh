#!/bin/sh
# 記事公開（main へマージ）直後に、作業ブランチを main と同じ内容に揃える。
#
# 前提: feature/post と feature/planning は「main + 執筆中の差分」だけを持つ
# 個人ブランチ。PR を squash merge していると各ブランチは main の祖先で
# なくなるため、fast-forward ではなく main へ hard reset して force push する。
#
# 実行してよいのは「公開直後で、対象ブランチに未マージの作業が無い」とき。
# 未コミット・未 push の変更があるブランチは、その旨を表示してスキップする。

set -eu

BRANCHES="feature/post feature/planning"
CURRENT="$(git rev-parse --abbrev-ref HEAD)"

git fetch origin

# main を最新に
git checkout main
git pull --ff-only origin main
MAIN_REV="$(git rev-parse origin/main)"

for br in $BRANCHES; do
	echo "--- $br ---"

	# ローカルに無ければ origin から作る
	if ! git show-ref --verify --quiet "refs/heads/$br"; then
		git branch "$br" "origin/$br" 2>/dev/null || {
			echo "  origin にも無いのでスキップ"
			continue
		}
	fi

	git checkout "$br"

	# 既に main と同一なら何もしない
	if [ "$(git rev-parse HEAD)" = "$MAIN_REV" ] && \
	   [ "$(git rev-parse "origin/$br" 2>/dev/null || echo -)" = "$MAIN_REV" ]; then
		echo "  既に main と同一"
		continue
	fi

	# 作業ツリーが汚れていたらスキップ（取りこぼし防止）
	if [ -n "$(git status --porcelain)" ]; then
		echo "  未コミットの変更があるためスキップ"
		continue
	fi

	# main に入っていないコミットがあれば警告してスキップ
	AHEAD="$(git rev-list --count "origin/main..$br")"
	if [ "$AHEAD" != "0" ]; then
		echo "  main に未マージのコミットが $AHEAD 件あるためスキップ:"
		git log --oneline "origin/main..$br" | sed 's/^/    /'
		continue
	fi

	git reset --hard origin/main
	git push --force-with-lease "origin" "$br"
	echo "  main に揃えた"
done

git checkout "$CURRENT"
echo "--- done ---"
git branch -vv | grep -E "feature/(post|planning)|(^|\s)main\s"
