# src/database/connection.py

import sqlite3
import os

DB_PATH = os.path.join("data", "telemetry.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(
        DB_PATH,
        timeout=10,
    )

    conn.row_factory = sqlite3.Row

    # Melhor concorrência
    conn.execute("PRAGMA journal_mode=WAL;")

    # Integridade relacional
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn