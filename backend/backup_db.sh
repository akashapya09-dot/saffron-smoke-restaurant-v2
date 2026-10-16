#!/bin/bash
set -euo pipefail
DB_PATH="${1:-/opt/saffron-smoke-backend/saffron_smoke.db}"
BACKUP_DIR="${2:-$HOME/saffron-db-backups}"
if [ ! -f "$DB_PATH" ]; then
  echo "Database not found: $DB_PATH" >&2
  exit 1
fi
mkdir -p "$BACKUP_DIR"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DEST="$BACKUP_DIR/saffron_smoke_$STAMP.db"
python3 - "$DB_PATH" "$DEST" <<'PY'
import sqlite3, sys
source, destination = sys.argv[1:]
with sqlite3.connect(source) as src, sqlite3.connect(destination) as dst:
    src.backup(dst)
print(destination)
PY
