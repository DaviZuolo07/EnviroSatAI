# 🛰️ EnviroSat AI — Mission Control

**FIAP — 1CCPK**

| Nome | RM |
|---|---|
| Davi Queiroz Zuolo | 571669 |
| Gustavo Zagato Bottechia | 569420 |
| Daniel Vilela Mana | 571632 |

> Sistema de monitoramento ambiental orbital com inteligência artificial, simulando um centro de comando de satélites para detecção de queimadas, desmatamento e riscos ambientais no Brasil.

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Objetivos](#objetivos)
3. [Arquitetura](#arquitetura)
4. [Tecnologias](#tecnologias)
5. [Dataset](#dataset)
6. [Funcionalidades](#funcionalidades)
7. [Estrutura de Pastas](#estrutura-de-pastas)
8. [Banco de Dados](#banco-de-dados)
9. [Sistema de Risco](#sistema-de-risco)
10. [ARIA — Analista de IA](#aria--analista-de-ia)
11. [Cenários Operacionais](#cenários-operacionais)
12. [Instalação e Execução](#instalação-e-execução)

---

## Sobre o Projeto

O **EnviroSat AI** é um sistema que simula o centro de controle de uma constelação de satélites ambientais. Ele integra dados reais de queimadas (dataset CSV público), um motor de cálculo de risco, um modelo de linguagem local (ARIA/Ollama) e um dashboard web estilo Mission Control construído em Streamlit.

O sistema possui dois modos de operação:

- **Dashboard Web** — interface gráfica completa com monitoramento em tempo real, gestão de incidentes e telemetria orbital
- **Terminal (CLI)** — executa ciclos de análise e exibe os relatórios da ARIA diretamente no console via `main.py`

Todo dado gerado é persistido em um banco SQLite local, mantendo histórico de telemetria e incidentes ao longo da sessão.

---

## Objetivos

- Aplicar modelos de linguagem (LLM) em um contexto operacional real de análise ambiental
- Construir um pipeline completo: ingestão de dados reais → processamento → análise por IA → visualização
- Praticar arquitetura modular em Python com separação de responsabilidades entre frontend, backend e serviços
- Simular um sistema realista de observação terrestre por satélite com múltiplos cenários de risco
- Desenvolver uma interface de comando inspirada em sistemas reais de missão espacial

---

## Arquitetura

```
┌──────────────────────────────────────────────────┐
│              FRONTEND (Streamlit)                 │
│  Dashboard │ Telemetria │ Incidentes │ Relatórios │
└────────────────────┬─────────────────────────────┘
                     │
              data_service.py
              (ponte + cache 60s)
                     │
┌────────────────────▼─────────────────────────────┐
│            MISSION ORCHESTRATOR                   │
│  Coordena o ciclo completo a cada execução        │
└────┬──────────────┬──────────────┬───────────────┘
     │              │              │
┌────▼────┐  ┌──────▼──────┐  ┌───▼────────────┐
│Telemetry│  │ Risk Score  │  │  LLM Service   │
│Service  │  │ Calculator  │  │  (ARIA/Ollama) │
│         │  │             │  │                │
│Lê CSV   │  │Score 0-100  │  │Gera análise e  │
│Gera     │  │+ alertas    │  │recomendações   │
│snapshot │  │+ ações auto │  │operacionais    │
└────┬────┘  └──────┬──────┘  └───────────────┘
     │              │
┌────▼──────────────▼──────────────────────────────┐
│              SQLite — telemetry.db                │
│       telemetry_logs │ incident_logs              │
└──────────────────────────────────────────────────┘
     │
┌────▼──────────────────────────────────────────────┐
│           wildfire_dataset.csv                    │
│  Dados reais filtrados por cenário operacional    │
└───────────────────────────────────────────────────┘
```

---

## Tecnologias

| Camada | Tecnologia | Uso |
|---|---|---|
| Frontend | Streamlit 1.58 | Interface web interativa |
| Visualização | Plotly | Gráficos de séries temporais |
| Backend | Python 3.11+ | Lógica, orquestração e serviços |
| Banco de Dados | SQLite3 | Persistência local de telemetria e incidentes |
| LLM | Ollama (local) | Motor da ARIA — análise de risco por IA |
| Dataset | CSV (wildfire) | Fonte de dados reais de queimadas |
| Logging | Python logging | Rastreabilidade em arquivo de log |

---

## Dataset

**Arquivo:** `data/wildfire_dataset.csv`

Dataset público de ocorrências de incêndios florestais com variáveis meteorológicas e de comportamento do fogo. É a fonte primária de dados do sistema — cada ciclo amostra uma linha do dataset conforme o cenário ativo.

**Colunas utilizadas:**

| Coluna | Descrição |
|---|---|
| `area` | Área queimada (ha) — base para calcular focos térmicos |
| `temp` | Temperatura ambiente (°C) — influencia o score de risco |
| `ISI` | Initial Spread Index — índice de velocidade de propagação |
| `wind` | Velocidade do vento (km/h) — filtra o cenário de falha de comunicação |

**Fórmula de conversão para focos térmicos:**

```python
hotspots = int(clip((area + temp * 0.5 + ISI * 0.3) / 5, 0, 50))
```

---

## Funcionalidades

### Dashboard Operacional
- Métricas em tempo real: alertas ativos, focos térmicos, cobertura orbital
- Mapa de situação com alertas críticos e moderados plotados
- Telemetria ambiental: temperatura, umidade, cobertura vegetal, índice de queimadas, nível de risco
- **Frota Orbital:** status individual dos 5 satélites com barras de bateria, sinal e integridade óptica — todos gerados a partir de dados reais
- **Status da Missão:** risk score 0–100 com barra colorida por severidade, buffer de imagens e integridade óptica
- Troca de cenário operacional na sidebar — todos os dados atualizam instantaneamente via limpeza de cache

### Telemetria
- Séries históricas das últimas 60 leituras em gráficos Plotly interativos
- Tabela de status individual dos satélites da frota

### Gestão de Incidentes
- Relatório completo da **ARIA** exibido no topo de cada atualização
- Ações automáticas executadas listadas abaixo da análise
- Incidentes agrupados por categoria com accordion clicável (categorias críticas abertas por padrão)
- Geração automática de novo incidente a cada **45 segundos** com base no ciclo real do backend
- Filtros por severidade e status operacional
- Integração com `incident_logs` do banco de dados — incidentes reais são carregados ao inicializar

---

## Estrutura de Pastas

```
mission-control-ai/
│
├── frontend/                        # Interface web
│   ├── app.py                       # Entry point e roteamento de páginas
│   ├── auth.py                      # Tela de login com autenticação de sessão
│   ├── styles.py                    # CSS global injetado via Streamlit
│   ├── data_service.py              # Ponte frontend ↔ backend (cache + ciclos)
│   │
│   ├── components/
│   │   ├── topbar.py                # Barra superior com horário UTC ao vivo
│   │   ├── header.py                # Cabeçalho padrão de página
│   │   ├── sidebar.py               # Navegação + seletor de cenário operacional
│   │   └── cards.py                 # Componentes reutilizáveis: metric, alert, telemetry
│   │
│   └── views/
│       ├── dashboard.py             # Dashboard principal com frota orbital
│       ├── telemetry.py             # Gráficos históricos de telemetria
│       ├── incidents.py             # Incidentes + relatório ARIA integrado
│       ├── operators.py             # Painel de operadores
│       └── reports.py               # Relatórios exportáveis
│
├── src/                             # Backend e lógica de negócio
│   ├── telemetria.py                # Dataclass TelemetriaSnapshot (6 métricas)
│   ├── risk_score.py                # Cálculo de risco, alertas e ações automáticas
│   │
│   ├── database/
│   │   ├── connection.py            # Conexão SQLite com WAL mode e foreign keys
│   │   ├── schema.py                # Criação automática das tabelas ao iniciar
│   │   ├── telemetry_repository.py  # Insert e consulta de telemetry_logs
│   │   └── incident_repository.py   # Insert de incident_logs (só se houver alertas)
│   │
│   ├── orchestrators/
│   │   └── mission_orchestrator.py  # Orquestra ciclo: telemetria → risco → DB → LLM
│   │
│   ├── services/
│   │   ├── telemetry_service.py     # Lê CSV, filtra por cenário, gera TelemetriaSnapshot
│   │   └── llm_service.py           # Monta prompt, chama Ollama, formata resposta da ARIA
│   │
│   └── utils/
│       └── logger.py                # Logger centralizado — saída para logs/envirosat.log
│
├── config/
│   ├── scenarios.py                 # Enum Scenario + filtros de dataset por cenário
│   └── thresholds.py                # Limiares de risco para cada métrica de telemetria
│
├── data/
│   ├── wildfire_dataset.csv         # Dataset público de queimadas (fonte primária)
│   └── telemetry.db                 # Banco SQLite gerado automaticamente na primeira run
│
├── logs/
│   └── envirosat.log                # Log operacional persistente
│
├── prompts/
│   └── system_prompt.md             # System prompt da ARIA com exemplos few-shot
│
└── requirements.txt
```

---

## Banco de Dados

O banco SQLite é inicializado automaticamente na primeira execução via `schema.py`. Utiliza **WAL mode** para melhor desempenho em leitura concorrente e **foreign keys** ativas.

### Tabela: `telemetry_logs`

Registra cada ciclo executado com todos os parâmetros do satélite.

```sql
CREATE TABLE IF NOT EXISTS telemetry_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT    NOT NULL,   -- ISO 8601 UTC
    scenario            TEXT    NOT NULL,   -- wildfire_escalation | low_power_emergency | ...
    thermal_hotspots    INTEGER,            -- focos detectados (0–50)
    battery_level       REAL,              -- nível de bateria em % (0–100)
    signal_strength     REAL,              -- força do sinal em % (0–100)
    geo_accuracy        REAL,              -- precisão geoespacial em % (0–100)
    image_buffer_queue  INTEGER,           -- imagens na fila (0–100)
    optical_integrity   REAL,              -- integridade óptica em % (0–100)
    risk_score          REAL,              -- score calculado (0–100)
    severity            TEXT               -- NOMINAL | WARNING | CRITICAL | EMERGENCY
);

CREATE INDEX IF NOT EXISTS idx_telemetry_scenario  ON telemetry_logs(scenario);
CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry_logs(timestamp);
```

### Tabela: `incident_logs`

Registra apenas ciclos com alertas ativos. Alertas e ações são armazenados como JSON.

```sql
CREATE TABLE IF NOT EXISTS incident_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT    NOT NULL,   -- ISO 8601 UTC
    scenario            TEXT    NOT NULL,
    severity            TEXT    NOT NULL,   -- NOMINAL | WARNING | CRITICAL | EMERGENCY
    risk_score          REAL,
    alerts              TEXT,               -- JSON array de strings com alertas ativos
    automated_actions   TEXT                -- JSON array de strings com ações executadas
);

CREATE INDEX IF NOT EXISTS idx_incident_severity ON incident_logs(severity);
```

**Exemplo de registro em `incident_logs`:**

```json
{
  "timestamp": "2026-06-04T14:32:10+00:00",
  "scenario": "wildfire_escalation",
  "severity": "CRITICAL",
  "risk_score": 63.0,
  "alerts": [
    "ALERTA DE INCÊNDIO — focos térmicos acima do limiar",
    "BAIXA ENERGIA — bateria abaixo do limiar operacional"
  ],
  "automated_actions": [
    "Priorização de transmissão de imagens termais",
    "Redução de consumo orbital"
  ]
}
```

---

## Sistema de Risco

O `calcular_risk_score()` avalia 6 métricas independentes e soma penalidades ao score final (máximo 100).

| Métrica | Condição Crítica | Penalidade |
|---|---|---|
| Focos Térmicos | ≥ 25 focos | +40 pts |
| Bateria | < 10% | +45 pts |
| Força do Sinal | < 20% | +25 pts |
| Precisão Geoespacial | < 40% | +15 pts |
| Buffer de Imagens | > 85 imagens | +10 pts |
| Integridade Óptica | < 60% | +15 pts |

**Níveis de severidade (definidos em `thresholds.py`):**

| Score | Severidade |
|---|---|
| 0 – 19 | NOMINAL |
| 20 – 44 | WARNING |
| 45 – 69 | CRITICAL |
| 70 – 100 | EMERGENCY |

Para cada limiar atingido, além da penalidade no score, o sistema gera alertas textuais e ações automáticas que são exibidos no dashboard e persistidos no banco.

---

## ARIA — Analista de IA

**ARIA** (Automated Risk Intelligence Analyst) é o componente de inteligência artificial do sistema. Recebe o snapshot completo de telemetria, o risk score calculado e o histórico dos últimos 5 ciclos, e produz uma análise estruturada em 3 blocos obrigatórios:

```
🛰️  Situação Orbital
    Estado geral do satélite com base nos parâmetros atuais.

🌎 Impacto Terrestre
    Consequências reais para populações, ecossistemas e brigadas em campo.

⚡ Recomendação ao Operador
    Uma ação prioritária e concreta que o operador humano deve tomar agora.
```

**Regras do sistema prompt:**
- Usa **exclusivamente** os dados fornecidos — nunca inventa valores ou coordenadas
- Não reclassifica o risk score (interpreta, não recalcula)
- Não repete ações automáticas já listadas como recomendação
- Analisa tendências históricas quando há ciclos anteriores (escalada, estabilização ou melhora)
- Temperatura de geração: **0.3** — respostas técnicas e objetivas

A ARIA é acionada pelo `MissionOrchestrator` a cada ciclo e sua análise é exibida no topo da página de Incidentes do dashboard.

---

## Cenários Operacionais

Quatro cenários controlam o filtro no dataset e os ranges de geração de telemetria:

| Cenário | Filtro no Dataset | Telemetria Gerada |
|---|---|---|
| 🔥 Escalada de Incêndio | `area > 10` | Muitos focos, bateria 30–60%, sinal 60–85% |
| 🔋 Emergência Energética | `area <= 5` | Bateria crítica 5–18%, sinal degradado 40–65% |
| 📡 Falha de Comunicação | `wind > 5` | Sinal mínimo 5–22%, geo-precisão 30–58% |
| ✅ Operação Normal | `area == 0` | Bateria 72–100%, sinal 82–100%, tudo nominal |

Ao trocar o cenário na sidebar, o `st.cache_data` é limpo e todos os componentes do dashboard recalculam com o novo contexto imediatamente.

---

## Instalação e Execução

### Pré-requisitos

- Python 3.11+
- [Ollama](https://ollama.com) instalado localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie `.env` na raiz do projeto:

```env
OLLAMA_API_URL=http://localhost:11434/api/chat
OLLAMA_MODEL=gpt-oss:120b-cloud
```

### 3. Iniciar o Ollama

```bash
ollama serve
```

### 4. Executar o Dashboard Web

```bash
streamlit run frontend/app.py
```

Acesse em `http://localhost:8501`

### 5. Executar no Terminal (opcional)

```bash
python main.py
```

Executa ciclos interativos com output completo da ARIA no console.

> O banco de dados `data/telemetry.db` é criado automaticamente na primeira execução.

---

<div align="center">
  <sub>FIAP 1CCPK · EnviroSat AI — Orbital Environmental Command</sub>
</div>
