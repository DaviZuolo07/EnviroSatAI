# src/orchestrators/mission_orchestrator.py

from dataclasses import dataclass
from typing import Optional
from config.scenarios import Scenario
from src.services.telemetry_service import gerar_telemetria_dataset
from src.risk_score import calcular_risk_score, RiskAssessment
from src.telemetria import TelemetriaSnapshot
from src.services.llm_service import consultar_llm
from src.database.schema import inicializar_banco
from src.database.telemetry_repository import salvar_telemetria, buscar_ultimos_ciclos
from src.database.incident_repository import salvar_incidente
from src.utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class CycleResult:
    scenario: Scenario
    telemetry: TelemetriaSnapshot
    assessment: RiskAssessment
    llm_analysis: str
    historico: list

class MissionOrchestrator:

    def __init__(self):
        inicializar_banco()
        logger.info("MissionOrchestrator inicializado.")

    def executar_ciclo(self, scenario: Scenario) -> CycleResult:
        logger.info(f"Iniciando ciclo — cenário: {scenario.name}")

        # 1. Telemetria
        telemetry = gerar_telemetria_dataset(scenario)
        logger.info(f"Telemetria gerada: hotspots={telemetry.thermal_hotspots} battery={telemetry.battery_level}")

        # 2. Risk Score
        assessment = calcular_risk_score(telemetry)
        logger.info(f"Risk Score: {assessment.score}/100 — {assessment.severity}")

        # 3. Persistência
        salvar_telemetria(scenario.value, telemetry, assessment)
        salvar_incidente(scenario.value, assessment)

        # 4. Histórico
        historico = buscar_ultimos_ciclos(scenario.value, n=5)

        # 5. LLM
        logger.info("Consultando ARIA (LLM)...")
        llm_analysis = consultar_llm(telemetry, assessment, scenario.value, historico)

        logger.info("Ciclo concluído.")

        return CycleResult(
            scenario=scenario,
            telemetry=telemetry,
            assessment=assessment,
            llm_analysis=llm_analysis,
            historico=historico,
        )