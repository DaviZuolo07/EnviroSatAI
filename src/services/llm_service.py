# src/services/llm_service.py

import os
import requests
from typing import Optional
from dotenv import load_dotenv
from src.telemetria import TelemetriaSnapshot
from src.risk_score import RiskAssessment

load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:120b-cloud")


def construir_prompt(
    t: TelemetriaSnapshot,
    r: RiskAssessment,
    scenario: str,
    historico: Optional[list] = None,
) -> str:
    alertas_fmt = "\n".join(f"  - {a}" for a in r.active_alerts) or "  - Nenhum alerta ativo"
    acoes_fmt = "\n".join(f"  - {a}" for a in r.automated_actions) or "  - Nenhuma ação automática executada"

    historico_fmt = ""
    if historico:
        historico_fmt = "\n### Histórico dos últimos ciclos (mais antigo → mais recente):\n"
        for h in historico:
            historico_fmt += (
                f"  [{h['timestamp'][:19]}] "
                f"hotspots={h['thermal_hotspots']} "
                f"battery={h['battery_level']}% "
                f"risk={h['risk_score']} ({h['severity']})\n"
            )

    return f"""
## ESTADO ATUAL DA MISSÃO ENVIROSAT

**Cenário operacional:** {scenario.upper()}
**Risk Score calculado pelo sistema:** {r.score}/100 ({r.severity})

### Telemetria atual do satélite:
- Focos térmicos detectados: {t.thermal_hotspots}
- Nível de bateria: {t.battery_level:.1f}%
- Força do sinal: {t.signal_strength:.1f}%
- Precisão geoespacial: {t.geo_accuracy:.1f}%
- Fila de imagens no buffer: {t.image_buffer_queue} imagens
- Integridade óptica: {t.optical_integrity:.1f}%

### Alertas ativos (gerados pelo sistema Python):
{alertas_fmt}

### Ações automáticas já executadas pelo sistema:
{acoes_fmt}
{historico_fmt}
Forneça sua análise operacional conforme instruído.
""".strip()


def carregar_system_prompt() -> str:
    try:
        with open("prompts/system_prompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return FALLBACK_SYSTEM_PROMPT


def consultar_llm(
    t: TelemetriaSnapshot,
    r: RiskAssessment,
    scenario: str,
    historico: Optional[list] = None,
) -> str:
    system_prompt = carregar_system_prompt()
    user_prompt = construir_prompt(t, r, scenario, historico)

    headers = {"Content-Type": "application/json"}

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 600,
        },
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return formatar_analise(data["message"]["content"])
    except requests.exceptions.ConnectionError:
        return "[LLM INDISPONÍVEL] Ollama não está rodando. Execute: ollama serve"
    except requests.exceptions.Timeout:
        return "[LLM INDISPONÍVEL] Timeout — modelo demorou mais de 60s para responder."
    except KeyError:
        return f"[LLM ERRO] Resposta inesperada da API: {data}"
    except Exception as e:
        return f"[LLM INDISPONÍVEL] Erro na consulta: {e}"
    
def formatar_analise(texto: str) -> str:
    import re

    # Remove asteriscos de bold
    texto = re.sub(r'\*+', '', texto)

    # Substitui apenas a parte do header, preservando o texto após
    texto = re.sub(r'(?i)(#+\s*)?situa[cç][aã]o orbital\s*:?', '🛰️  Situação Orbital\n', texto)
    texto = re.sub(r'(?i)(#+\s*)?impacto terrestre\s*:?',      '🌎 Impacto Terrestre\n', texto)
    texto = re.sub(r'(?i)(#+\s*)?recomenda[cç][aã]o ao operador\s*:?', '⚡ Recomendação ao Operador\n', texto)

    return texto.strip()


FALLBACK_SYSTEM_PROMPT = """Você é ARIA (Automated Risk Intelligence Analyst), analista de IA do centro de controle da missão EnviroSat.
Seu papel é interpretar o estado operacional do satélite e traduzir riscos técnicos em impacto para o território terrestre.
Seja técnico, objetivo e direto. Nunca invente dados que não estão na telemetria fornecida.
Sempre estruture sua resposta em três blocos: Situação Orbital, Impacto Terrestre, Recomendação ao Operador."""