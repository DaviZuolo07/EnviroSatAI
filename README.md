# 🛰️ EnviroSat AI — Mission Control
### FIAP · Ciência da Computação · Global Solution 2026.1
### Disciplina: Prompt Engineering and Artificial Intelligence

---

## Integrantes

| Nome | RM | Turma |
|---|---|---|
| Davi Queiroz Zuolo | 571669 | 1CCPK |
| Gustavo Zagato Bottechia | 569420 | 1CCPK |
| Daniel Vilela Mana | 571632 | 1CCPK |

**Modalidade:** Trio

---

## O que o projeto faz

O **EnviroSat AI** simula o centro de controle de uma constelação de satélites ambientais brasileiros, integrando dados reais de queimadas com IA generativa para análise operacional em tempo real. O sistema coleta dados de um dataset público de incêndios florestais, calcula um risk score por meio de lógica Python pura, e aciona a **ARIA** (Automated Risk Intelligence Analyst) — um agente LLM via Ollama Cloud — que produz análises estruturadas em linguagem natural conectando o estado orbital ao impacto terrestre. O sistema possui dois modos de operação: um **dashboard web** em Streamlit com monitoramento visual completo e uma **CLI interativa** via `main.py`, ambos com persistência em banco SQLite.

---

## Trilha

🌳 **Trilha 2 — EnviroSat (Observação Ambiental)**

Satélite simulado com sensor térmico e óptico, similar ao Amazônia-1 e Landsat, monitorando focos de incêndio, desmatamento e riscos ambientais no território brasileiro.

---

## Persona atendida

**Operador de centro de controle ambiental (INPE / órgão estadual)**

O sistema foi projetado para o operador de plantão em um centro de monitoramento ambiental que precisa tomar decisões rápidas com base em dados orbitais. A ARIA traduz telemetria técnica em linguagem operacional acessível, permitindo que o operador avalie criticidade, priorize recursos e acione brigadas sem precisar interpretar dados brutos — simulando o workflow real de sistemas como o DETER/INPE.

---

## 💼 Proposta de valor / modelo de negócio

### 1. Problema real terrestre que esta missão resolve

O Brasil perde em média 3 milhões de hectares de vegetação por ano para queimadas e desmatamento ilegal. O sistema oficial DETER/INPE processa imagens com latência de horas, inviabilizando resposta rápida de brigadas. O EnviroSat AI simula um sistema de detecção em tempo quasi-real que reduz esse gap: ao receber telemetria do satélite a cada ciclo de 15 minutos, o operador sabe imediatamente qual área está em risco crítico e qual ação tomar — sem aguardar análise manual.

### 2. Quem paga pela solução

Modelo híbrido:
- **Setor público:** IBAMA, INPE, secretarias estaduais de meio ambiente — via contratos de licenciamento de software ou concessão de operação de dados orbitais.
- **Setor privado:** seguradoras rurais (compliance e precificação de risco), grandes produtores e cooperativas (certificação ambiental), indústria florestal certificada (FSC, Cerflor).

### 3. Métrica de impacto

Se o sistema operar com cobertura contínua sobre a Amazônia Legal (5 milhões de km²) por 1 ano:
- Redução no tempo médio de detecção de foco ativo de **4–6 horas para 15–30 minutos**
- Cobertura de monitoramento de aproximadamente **500 áreas protegidas** em paralelo
- Estimativa de **1.200 acionamentos de brigada mais precisos** por ano, reduzindo deslocamentos inúteis e aumentando taxa de contenção precoce

### 4. Modelo de negócio

**SaaS + dado-como-serviço:** assinatura anual para órgãos públicos com acesso à plataforma de monitoramento; API de dados orbitais processados vendida como serviço para seguradoras e plataformas de crédito rural (ex: integração com Climate FieldView, Strider).

---

## Tecnologias utilizadas

| Camada | Tecnologia | Versão | Uso |
|---|---|---|---|
| Frontend | Streamlit | 1.57.0 | Interface web interativa estilo Mission Control |
| Visualização | Plotly | — | Gráficos de séries temporais de telemetria |
| Backend | Python | 3.11+ | Lógica, orquestração e serviços |
| Banco de Dados | SQLite3 | embutido | Persistência local de telemetria e incidentes |
| LLM | Ollama Cloud | gpt-oss:120b | Motor da ARIA — análise de risco por IA generativa |
| Dados | CSV (wildfire) | — | Dataset público de queimadas como fonte primária |
| Ambiente | python-dotenv | 1.0.1 | Gestão de credenciais via .env |
| Logging | rich + logging | 15.0.0 | Output formatado e rastreabilidade em log |

---

## Como executar

### Pré-requisitos

- Python 3.11+
- Conta Ollama Cloud com API Key: [https://ollama.com](https://ollama.com)

### 1. Clone o repositório

```bash
git clone https://github.com/DaviZuolo07/EnviroSatAI.git
cd EnviroSatAI
```

### 2. Crie ambiente virtual e instale dependências

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie `.env` na raiz do projeto com base no `.env.example`:

```env
OLLAMA_API_KEY=sua_chave_aqui
OLLAMA_MODEL=gpt-oss:120b
```

### 4. Execute o Dashboard Web

```bash
streamlit run frontend/app.py
```

Acesse em `http://localhost:8501`

### 5. Execute a CLI (opcional)

```bash
python main.py
```

Executa ciclos interativos com output completo da ARIA no terminal.

> O banco de dados `data/telemetry.db` é criado automaticamente na primeira execução.

---

## Demonstração

![Dashboard operacional em situação normal](assets/screenshot_normal.png)

![Escalada de incêndio — alertas críticos e análise da ARIA](assets/screenshot_alerta.png)

![Painel de incidentes com categorias e severidades](assets/screenshot_incidentes.png)

---

## System Prompt

O system prompt completo da ARIA está em [`prompts/system_prompt.md`](prompts/system_prompt.md).

**Resumo da persona e regras:**

A ARIA é instruída a atuar como analista técnica de operações orbitais com especialização em monitoramento ambiental brasileiro. Cada resposta deve conter obrigatoriamente três blocos:

```
🛰️  Situação Orbital     — estado geral do satélite com base nos parâmetros atuais
🌎  Impacto Terrestre    — consequências reais para populações, ecossistemas e brigadas
⚡  Recomendação         — uma ação prioritária e concreta que o operador deve tomar agora
```

Regras do prompt:
- Usa **exclusivamente** os dados fornecidos — nunca inventa valores ou coordenadas
- Sempre conecta o dado orbital ao impacto na Terra (brigadas, populações, ecossistemas)
- Analisa tendências históricas dos últimos 5 ciclos quando disponíveis
- Temperatura de geração: **0.3** para respostas técnicas e consistentes

---

## Cenários de teste demonstrados

| # | Cenário | Condição | Resultado esperado |
|---|---|---|---|
| 1 | ✅ Operação Normal | Todos os parâmetros dentro do range nominal | Risk score < 20, severidade NOMINAL, sem alertas ativos |
| 2 | 🔥 Escalada de Incêndio | Focos térmicos ≥ 25, bateria 30–60% | Risk score 45–69, severidade CRITICAL, ARIA aciona brigadas |
| 3 | 🔋 Emergência Energética | Bateria < 10% | Risk score com +45pts de penalidade, ação automática de redução de consumo |
| 4 | 📡 Falha de Comunicação | Sinal < 20%, geo-precisão < 40% | Alertas de comunicação, ARIA recomenda janela de downlink alternativa |

---

## Arquitetura do sistema

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
│Lê CSV   │  │Score 0-100  │  │Gera análise em │
│Gera     │  │+ alertas    │  │linguagem natural│
│snapshot │  │+ ações auto │  │com impacto     │
└────┬────┘  └──────┬──────┘  │terrestre       │
     │              │          └───────────────┘
┌────▼──────────────▼──────────────────────────────┐
│              SQLite — telemetry.db                │
│       telemetry_logs │ incident_logs              │
└──────────────────────────────────────────────────┘
```

---

## Estrutura de pastas

```
EnviroSatAI/
│
├── frontend/                        # Interface web Streamlit
│   ├── app.py                       # Entry point e roteamento
│   ├── auth.py                      # Autenticação de sessão
│   ├── data_service.py              # Ponte frontend ↔ backend
│   ├── components/                  # Topbar, sidebar, cards reutilizáveis
│   └── views/                       # Dashboard, telemetria, incidentes
│
├── src/                             # Backend e lógica de negócio
│   ├── telemetria.py                # Dataclass TelemetriaSnapshot
│   ├── risk_score.py                # Cálculo de risco e ações automáticas
│   ├── database/                    # Conexão SQLite, schema, repositórios
│   ├── orchestrators/               # MissionOrchestrator — ciclo completo
│   ├── services/                    # TelemetryService, LLMService (ARIA)
│   └── utils/logger.py              # Logger centralizado
│
├── config/
│   ├── scenarios.py                 # Enum Scenario + filtros de dataset
│   └── thresholds.py                # Limiares de risco por métrica
│
├── data/
│   ├── wildfire_dataset.csv         # Dataset público de queimadas
│   └── telemetry.db                 # Banco SQLite (gerado automaticamente)
│
├── prompts/
│   └── system_prompt.md             # System prompt da ARIA (few-shot)
│
├── assets/                          # Screenshots do sistema funcionando
├── logs/                            # Log operacional persistente
├── main.py                          # Entry point da CLI
├── requirements.txt                 # Dependências com versões fixadas
├── .env.example                     # Template de variáveis (sem chave real)
└── .gitignore                       # Ignora .env, __pycache__, telemetry.db
```

---

## Limitações conhecidas

- **Ollama local vs Cloud:** a versão atual usa Ollama local (`localhost:11434`). Para uso com Ollama Cloud API (`gpt-oss:120b` remoto), é necessário ajustar o `OLLAMA_API_URL` no `.env` — o código suporta ambos via configuração.
- **Dataset estático:** os dados de queimadas são de um CSV público pré-carregado — não há integração com APIs em tempo real do INPE/DETER nesta versão.
- **Mapa simplificado:** o mapa de situação no dashboard usa coordenadas simuladas dentro do território brasileiro, não coordenadas reais dos focos do dataset.
- **Sem autenticação robusta:** o sistema de login é por sessão Streamlit, sem banco de usuários — adequado para demonstração, não para produção.
- **Sem testes automatizados:** o arquivo `test.py` contém testes manuais pontuais, não uma suíte de testes completa com pytest.

---

## 🎬 Vídeo de demonstração

🔗 [Assistir demonstração no YouTube](https://www.youtube.com/watch?v=SEU_ID_AQUI)

> Configurado como "Não listado" no YouTube. Duração: menos de 3 minutos.

---

<div align="center">
  <sub>FIAP · Ciência da Computação · Global Solution 2026.1 · Prompt Engineering and Artificial Intelligence</sub>
</div>