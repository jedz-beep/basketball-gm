"""SQLite connection and helpers. Only this module talks to sqlite3 directly."""

import sqlite3
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Union

Params = Union[Iterable[Any], Mapping[str, Any]]

import config

_CONN: Optional[sqlite3.Connection] = None
_SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Open the SQLite connection. Reuses the existing one if already open."""
    global _CONN
    if _CONN is not None:
        return _CONN
    path = Path(db_path) if db_path else Path(config.SAVES_DIR) / config.DEFAULT_DB_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    _CONN = sqlite3.connect(path)
    _CONN.execute("PRAGMA foreign_keys = ON")
    return _CONN


def create_tables() -> None:
    """Run schema.sql to create all tables if they do not exist."""
    conn = connect()
    conn.executescript(_SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()


def _normalize(params: Params):
    """Pass dicts through (named binds), convert iterables to tuple."""
    if isinstance(params, Mapping):
        return params
    return tuple(params)


def query(sql: str, params: Params = ()) -> list[tuple]:
    """Run a SELECT and return all rows."""
    cur = connect().execute(sql, _normalize(params))
    return cur.fetchall()


def execute(sql: str, params: Params = ()) -> int:
    """Run a single INSERT/UPDATE/DELETE. Returns lastrowid."""
    conn = connect()
    cur = conn.execute(sql, _normalize(params))
    conn.commit()
    return cur.lastrowid


def executemany(sql: str, rows: Iterable[Params]) -> None:
    """Bulk insert / update."""
    conn = connect()
    conn.executemany(sql, [_normalize(r) for r in rows])
    conn.commit()


def close() -> None:
    """Close the connection. Used by tests."""
    global _CONN
    if _CONN is not None:
        _CONN.close()
        _CONN = None
