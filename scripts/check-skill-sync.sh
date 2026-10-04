#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE="$ROOT/skills/arx-be"
TARGET="$ROOT/plugins/arx-be/skills/arx-be"

if diff -ru "$SOURCE" "$TARGET"; then
  echo "Skill distributions are synchronized."
  exit 0
fi

echo "Skill distributions differ. Run ./scripts/sync-skill.sh and commit the result." >&2
exit 1
