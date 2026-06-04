# src/database/incident_repository.py

import json
from datetime import datetime, timezone

from src.database.connection import get_connection
from src.risk_score import RiskAssessment


def salvar_incidente(
    scenario: str,
    r: RiskAssessment,
):

    if not r.active_alerts:
        return

    with get_connection() as conn:

        conn.execute("""
            INSERT INTO incident_logs (
                timestamp,
                scenario,
                severity,
                risk_score,
                alerts,
                automated_actions
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            scenario,
            r.severity,
            r.score,
            json.dumps(r.active_alerts, ensure_ascii=False),
            json.dumps(r.automated_actions, ensure_ascii=False),
        ))