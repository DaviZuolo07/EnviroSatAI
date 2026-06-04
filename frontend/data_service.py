import streamlit as st
from config.scenarios import Scenario
from src.orchestrators.mission_orchestrator import MissionOrchestrator

_orchestrator = MissionOrchestrator()


def _get_orchestrator() -> MissionOrchestrator:
    return _orchestrator


@st.cache_data(ttl=60, show_spinner=False)
def get_cycle_data(scenario_value: str) -> dict:
    """
    Executa um ciclo completo e retorna dict com todos os dados.
    Cache de 60s — evita re-executar o LLM a cada rerun do Streamlit.
    """
    scenario = Scenario(scenario_value)
    result = _get_orchestrator().executar_ciclo(scenario)

    t = result.telemetry
    r = result.assessment

    return {
        # Telemetria
        "temperatura": f"{t.thermal_hotspots * 0.8 + 22:.1f} °C",
        "umidade": f"{100 - t.battery_level * 0.4:.1f} %",
        "cobertura_vegetal": f"{t.geo_accuracy:.1f} %",
        "indice_queimadas": f"{t.thermal_hotspots / 5:.1f} /10",
        "nivel_risco": r.severity,
        # Cards de métricas
        "alertas_ativos": len(r.active_alerts),
        "hotspots": t.thermal_hotspots,
        "cobertura_orbital": f"{t.signal_strength:.1f}%",
        # Satélites
        "bateria": t.battery_level,
        "sinal": t.signal_strength,
        "buffer": t.image_buffer_queue,
        "integridade_optica": t.optical_integrity,
        # Risk
        "risk_score": r.score,
        "severity": r.severity,
        "alertas": r.active_alerts,
        "acoes": r.automated_actions,
        # ARIA
        "aria_analise": result.llm_analysis,
        # Histórico
        "historico": result.historico,
    }