#!/usr/bin/env bash
# 要求仕様の Agent Skills と docs/requirements/ を導入先のプロジェクトに配置する。
#
#   bash scripts/install.sh <導入先> [--skills-dir DIR] [--with-agents-md]
#
# 既定のスキル配置先は .agents/skills(Cursor / Codex が直接読み、Claude Code は
# Cursor Knowledge Management System の init.sh が作る .claude/skills のリンク経由で読む)。
# スキルは配布物なので、再実行すると最新の内容で置き換える。docs/requirements/ の
# 既存ファイルは変更しない。--with-agents-md は導入先の AGENTS.md に要求仕様の節を
# 追記する(再実行すると同じ節を置き換える)。
set -eu

ROOT=$(cd "$(dirname "$0")/.." && pwd)
SKILLS="requirements-spec draft-spec review-spec"
SKILLS_DIR=".agents/skills"
WITH_AGENTS_MD=false
TARGET=""

usage() {
  sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
}

while [ $# -gt 0 ]; do
  case "$1" in
    --skills-dir)
      [ $# -ge 2 ] || { echo "--skills-dir には配置先を指定してください" >&2; exit 2; }
      SKILLS_DIR=$2
      shift
      ;;
    --with-agents-md) WITH_AGENTS_MD=true ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "不明なオプション: $1" >&2; usage >&2; exit 2 ;;
    *)
      [ -z "$TARGET" ] || { echo "導入先は1つだけ指定してください" >&2; exit 2; }
      TARGET=$1
      ;;
  esac
  shift
done

[ -n "$TARGET" ] || { usage >&2; exit 2; }
[ -d "$TARGET" ] || { echo "導入先のディレクトリがありません: $TARGET" >&2; exit 1; }
TARGET=$(cd "$TARGET" && pwd)
[ "$TARGET" != "$ROOT" ] || { echo "このリポジトリ自身には導入できません" >&2; exit 1; }

VERSION=$(git -C "$ROOT" describe --tags --always 2>/dev/null || echo "不明")

mkdir -p "$TARGET/$SKILLS_DIR"
for skill in $SKILLS; do
  dest="$TARGET/$SKILLS_DIR/$skill"
  rm -rf "$dest"
  cp -R "$ROOT/skills/$skill" "$dest"
  echo "スキルを配置: $SKILLS_DIR/$skill"
done

mkdir -p "$TARGET/docs/requirements/assets/screens"
index="$TARGET/docs/requirements/README.md"
if [ -e "$index" ]; then
  echo "既存のため変更しない: docs/requirements/README.md"
else
  cat > "$index" <<'INDEX'
# 要求仕様書

このディレクトリには Webアプリの要求仕様書を置きます。書き方は `requirements-spec` スキルを参照してください。画面の画像は `assets/screens/<プロジェクト識別子>/` に置きます。

| 仕様書 | 概要 | ステータス |
| --- | --- | --- |
INDEX
  echo "作成: docs/requirements/README.md"
fi

if [ "$WITH_AGENTS_MD" = true ]; then
  agents="$TARGET/AGENTS.md"
  snippet="$ROOT/templates/AGENTS.requirements.md"
  begin="<!-- requirements-to-spec-template:begin -->"
  end="<!-- requirements-to-spec-template:end -->"
  if [ ! -e "$agents" ]; then
    printf '# AGENTS.md\n\n' > "$agents"
    cat "$snippet" >> "$agents"
    echo "作成: AGENTS.md"
  elif grep -qF "$begin" "$agents"; then
    tmp=$(mktemp)
    SNIPPET="$snippet" BEGIN_MARK="$begin" END_MARK="$end" awk '
      $0 == ENVIRON["BEGIN_MARK"] { while ((getline line < ENVIRON["SNIPPET"]) > 0) print line; skip = 1; next }
      $0 == ENVIRON["END_MARK"] { skip = 0; next }
      !skip { print }
    ' "$agents" > "$tmp"
    cat "$tmp" > "$agents"
    rm -f "$tmp"
    echo "要求仕様の節を置き換え: AGENTS.md"
  else
    printf '\n' >> "$agents"
    cat "$snippet" >> "$agents"
    echo "要求仕様の節を追記: AGENTS.md"
  fi
fi

echo "requirements-to-spec-template $VERSION を $TARGET に導入しました"
