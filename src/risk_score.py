# src/risk_score.py

from dataclasses import dataclass, field
from typing import List
from src.telemetria import TelemetriaSnapshot
from config.thresholds import RISK_THRESHOLDS, SEVERITY_LEVELS

@dataclass
class RiskAssessment:
    score: float
    severity: str
    active_alerts: List[str] = field(default_factory=list)
    automated_actions: List[str] = field(default_factory=list)


def calcular_risk_score(t: TelemetriaSnapshot) -> RiskAssessment:
    score = 0.0
    alerts = []
    actions = []
    T = RISK_THRESHOLDS

    if t.thermal_hotspots >= T["hotspots_critical"]:
        score += 40
        alerts.append("INCÊNDIO CRÍTICO — alto número de focos térmicos detectados")
        actions.append("Transmissão emergencial de coordenadas para brigadas")
    elif t.thermal_hotspots >= T["hotspots_warning"]:
        score += 20
        alerts.append("ALERTA DE INCÊNDIO — focos térmicos acima do limiar")
        actions.append("Priorização de transmissão de imagens termais")
    elif t.thermal_hotspots >= T["hotspots_elevated"]:
        score += 8
        alerts.append("MONITORAMENTO ELEVADO — focos térmicos detectados")

    if t.battery_level < T["battery_emergency_critical"]:
        score += 45
        alerts.append("EMERGÊNCIA ENERGÉTICA CRÍTICA — bateria abaixo de 10%")
        actions.append("Power saving mode ativado — desligamento de sensores secundários")
        actions.append("Redução de consumo orbital")
        actions.append("Transmissão de telemetria de emergência iniciada")
    elif t.battery_level < T["battery_emergency"]:
        score += 35
        alerts.append("EMERGÊNCIA ENERGÉTICA — bateria crítica")
        actions.append("Power saving mode ativado — desligamento de sensores secundários")
        actions.append("Redução de consumo orbital")
    elif t.battery_level < T["battery_warning"]:
        score += 15
        alerts.append("BAIXA ENERGIA — bateria abaixo do limiar operacional")
        actions.append("Redução de consumo orbital")

    if t.signal_strength < T["signal_failure"]:
        score += 25
        alerts.append("FALHA DE COMUNICAÇÃO — sinal abaixo do mínimo operacional")
        actions.append("Tentativa de reestabelecimento de canal alternativo")
    elif t.signal_strength < T["signal_degraded"]:
        score += 10
        alerts.append("DEGRADAÇÃO DE SINAL — qualidade de comunicação comprometida")

    if t.geo_accuracy < T["geo_critical"]:
        score += 15
        alerts.append("DEGRADAÇÃO GEOESPACIAL — precisão de posicionamento comprometida")
        actions.append("Recalibração geoespacial solicitada")
    elif t.geo_accuracy < T["geo_degraded"]:
        score += 7
        alerts.append("PRECISÃO GEOESPACIAL REDUZIDA — monitoramento parcialmente comprometido")

    if t.image_buffer_queue > T["buffer_critical"]:
        score += 10
        alerts.append("CONGESTIONAMENTO DE TRANSMISSÃO — buffer de imagens saturando")
        actions.append("Compressão emergencial do buffer de imagens")
    elif t.image_buffer_queue > T["buffer_elevated"]:
        score += 5
        alerts.append("BUFFER ELEVADO — capacidade de transmissão sob pressão")

    if t.optical_integrity < T["optical_failure"]:
        score += 15
        alerts.append("FALHA ÓPTICA — integridade do sensor comprometida")
        actions.append("Diagnóstico do sensor óptico iniciado")
    elif t.optical_integrity < T["optical_degraded"]:
        score += 7
        alerts.append("DEGRADAÇÃO ÓPTICA — qualidade de imagem reduzida")

    score = min(score, 100.0)

    severity = "NOMINAL"
    for level, minimum in sorted(SEVERITY_LEVELS.items(), key=lambda x: x[1], reverse=True):
        if score >= minimum:
            severity = level
            break

    return RiskAssessment(
        score=round(score, 1),
        severity=severity,
        active_alerts=alerts,
        automated_actions=actions,
    )