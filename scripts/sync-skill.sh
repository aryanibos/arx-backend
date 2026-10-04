#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE="$ROOT/skills/arx-be"
TARGET="$ROOT/plugins/arx-be/skills/arx-be"

if [ ! -f "$SOURCE/SKILL.md" ]; then
  echo "Source skill not found: $SOURCE" >&2
  exit 1
fi

rm -rf "$TARGET"
mkdir -p "$(dirname -- "$TARGET")"
cp -R "$SOURCE" "$TARGET"

echo "Synced skills/arx-be -> plugins/arx-be/skills/arx-be"
