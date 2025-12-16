import re
import sqlite3
from pathlib import Path


def _preview_sqlite_connection(conn: sqlite3.Connection, *, preview_rows: int = 5) -> None:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [r[0] for r in cur.fetchall()]

    print("\n📋 TABLES FOUND:")
    print("-" * 60)
    print(tables)

    if not tables:
        print("No tables found")
        return

    for table in tables:
        print(f"\n📄 PREVIEW FROM TABLE '{table}' (first {preview_rows} rows):")
        print("-" * 60)
        try:
            # Get column names
            cur.execute(f'PRAGMA table_info("{table}")')
            cols = [row[1] for row in cur.fetchall()]  # row[1] is column name
            if cols:
                print("Columns:", cols)

            # Get sample rows
            cur.execute(f'SELECT * FROM "{table}" LIMIT {preview_rows}')
            rows = cur.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print("(no rows)")
        except Exception as e:
            print(f"Could not preview table '{table}': {e}")



def _split_on_go(sql_text: str) -> list[str]:
    # Split batches on lines that are exactly "GO" (SQL Server batch separator)
    # This is a *common* pattern in T-SQL install scripts like InstPubs.SQL
    return [b.strip() for b in re.split(r"(?im)^\s*GO\s*$", sql_text) if b.strip()]


def _looks_like_sql_server(sql_text: str) -> bool:
    return bool(re.search(r"(?im)^\s*GO\s*$|SET\s+NOCOUNT|RAISERROR|SERVERPROPERTY|sysdatabases", sql_text))


def _should_skip_batch_for_sqlite(batch: str) -> bool:
    # Fast skip for clearly non-SQLite / server-level statements
    patterns = [
        r"(?im)^\s*USE\s+\w+",
        r"(?im)^\s*SET\s+NOCOUNT",
        r"(?im)^\s*CHECKPOINT\b",
        r"(?im)\bRAISERROR\b",
        r"(?im)\bSERVERPROPERTY\b",
        r"(?im)\bsysdatabases\b",
        r"(?im)^\s*CREATE\s+DATABASE\b",
        r"(?im)^\s*DROP\s+DATABASE\b",
        r"(?im)^\s*declare\s+@",
    ]
    return any(re.search(p, batch) for p in patterns)


def extract_text(file_path: str) -> None:
    print(f"\n{'='*60}")
    print(f"Processing: {file_path}")
    print("=" * 60)

    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix in {".sqlite", ".db", ".sqlite3"}:
        try:
            conn = sqlite3.connect(str(path))
            _preview_sqlite_connection(conn)
            conn.close()
        except Exception as e:
            print(f"Error reading sqlite file: {e}")
        print("=" * 60)
        return

    if suffix == ".sql":
        sql_text = path.read_text(encoding="utf-8", errors="replace")

        print("\n📄 SQL FILE PREVIEW (first 1000 chars):")
        print("-" * 60)
        print(sql_text[:1000] + ("..." if len(sql_text) > 1000 else ""))

        # Try to execute (best-effort) into SQLite in-memory
        conn = sqlite3.connect(":memory:")
        skipped = []
        failed = []

        try:
            batches = _split_on_go(sql_text) if _looks_like_sql_server(sql_text) else [sql_text]

            for i, batch in enumerate(batches, start=1):
                if _should_skip_batch_for_sqlite(batch):
                    skipped.append(i)
                    continue
                try:
                    conn.executescript(batch)
                except Exception as e:
                    failed.append((i, str(e)))

            print("\n🧪 EXECUTION SUMMARY (SQLite best-effort):")
            print("-" * 60)
            print(f"Batches total: {len(batches)}")
            print(f"Skipped (clearly T-SQL): {len(skipped)}  -> {skipped[:20]}{'...' if len(skipped) > 20 else ''}")
            print(f"Failed (SQLite errors): {len(failed)}")
            if failed:
                print("First few failures:")
                for bi, err in failed[:5]:
                    print(f"  - batch {bi}: {err}")

            _preview_sqlite_connection(conn)

        finally:
            conn.close()

        print("=" * 60)
        return

    print(file_path, "could not be parsed. Please try again with a .sqlite/.db/.sqlite3 or .sql file!")
    print("=" * 60)


if __name__ == "__main__":
    test_files = [
        "test_files/sample.pdf",
        "test_files/sample.docx",
        "test_files/sample.txt",
        "test_files/sample.sqlite",
        "test_files/sample.sql",
    ]

    for file_path in test_files:
        extract_text(file_path)
