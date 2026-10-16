#!/usr/bin/env python3
"""Read-only overview of the Saffron & Smoke SQLite database."""
from pathlib import Path
import sqlite3
import sys

DEFAULT_DB = Path(__file__).resolve().parent / "saffron_smoke.db"
DB_PATH = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else DEFAULT_DB

if not DB_PATH.exists():
    print(f"Database file not found: {DB_PATH}")
    print("If deployed with setup_backend.sh, the live database is normally:")
    print("  /opt/saffron-smoke-backend/saffron_smoke.db")
    sys.exit(1)

con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
try:
    print(f"Database: {DB_PATH}")
    tables = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    if not tables:
        print("No application tables found.")
    for (table,) in tables:
        cols = con.execute(f'PRAGMA table_info("{table}")').fetchall()
        count = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        print(f"\n{table} — {count} row(s)")
        print("  columns: " + ", ".join(c[1] for c in cols))
finally:
    con.close()
