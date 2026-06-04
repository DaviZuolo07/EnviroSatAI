# src/database/telemetry_repository.py

from datetime import datetime, timezone

from src.database.connection import get_connection
from src.telemetria import TelemetriaSnapshot
from src.risk_score import RiskAssessment


def salvar_telemetria(
    scenario: str,
    t: TelemetriaSnapshot,
    r: RiskAssessment,
):

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO telemetry_logs (
                timestamp,
                scenario,
                thermal_hotspots,
                battery_level,
                signal_strength,
                geo_accuracy,
                image_buffer_queue,
                optical_integrity,
                risk_score,
                severity
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            scenario,
            t.thermal_hotspots,
            t.battery_level,
            t.signal_strength,
            t.geo_accuracy,
            t.image_buffer_queue,
            t.optical_integrity,
            r.score,
            r.severity,
        ))


def buscar_ultimos_ciclos(
    scenario: str,
    n: int = 5,
) -> list:

    with get_connection() as conn:

        rows = conn.execute("""
            SELECT *
            FROM telemetry_logs
            WHERE scenario = ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            scenario,
            n,
        )).fetchall()

    return [dict(r) for r in reversed(rows)]