# src/database/schema.py

from src.database.connection import get_connection


def inicializar_banco():

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                scenario TEXT NOT NULL,
                thermal_hotspots INTEGER,
                battery_level REAL,
                signal_strength REAL,
                geo_accuracy REAL,
                image_buffer_queue INTEGER,
                optical_integrity REAL,
                risk_score REAL,
                severity TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incident_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                scenario TEXT NOT NULL,
                severity TEXT NOT NULL,
                risk_score REAL,
                alerts TEXT,
                automated_actions TEXT
            )
        """)

        # Índices críticos
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_telemetry_scenario
            ON telemetry_logs(scenario)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp
            ON telemetry_logs(timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_incident_severity
            ON incident_logs(severity)
        """)