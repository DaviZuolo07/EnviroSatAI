import streamlit as st
import streamlit.components.v1 as components
import time
import random
from datetime import datetime, timezone

from frontend.components.topbar import render_topbar
from frontend.components.header import render_page_header
from frontend.components.cards  import section_header
from frontend.data_service      import get_cycle_data, get_db_incidents

SEVERITY_COLOR = {"CRÍTICO": "#ef4444", "MODERADO": "#f59e0b", "BAIXO": "#4ade80"}
STATUS_COLOR   = {
    "CONFIRMADO":  "#ef4444",
    "EM ANÁLISE":  "#f59e0b",
    "MONITORANDO": "#60a5fa",
    "PENDENTE":    "#6b9c6b",
}

CATEGORIAS = {
    "🔥 INCÊNDIOS":         {"keywords": ["FOCO","INCÊNDIO","QUEIMADA","FUMAÇA","ANOMALIA TÉRMICA"], "cor": "#ef4444"},
    "🌳 DESMATAMENTO":      {"keywords": ["DESMATAMENTO","CORTE","ÁREA DEGRADADA"],                  "cor": "#f59e0b"},
    "⛏️ EXTRAÇÃO ILEGAL":   {"keywords": ["EXTRAÇÃO","MINERAÇÃO"],                                   "cor": "#fb923c"},
    "💧 RECURSOS HÍDRICOS": {"keywords": ["HÍDRICA","HÍDRICO","RISCO HÍDRICO"],                     "cor": "#60a5fa"},
    "⚠️ RISCO GERAL":       {"keywords": ["RISCO","ÁREA DE RISCO","INCÊNDIO CRÍTICO","MONITORAMENTO","EMERGÊNCIA","DEGRADAÇÃO","CONGESTIONAMENTO","FALHA"], "cor": "#6b9c6b"},
}

_BASE_INCIDENTS = [
    ("DESMATAMENTO ILEGAL",        "AMAZÔNIA LEGAL – PA", "CRÍTICO",  "09:42 UTC", "EM ANÁLISE",  "🌳"),
    ("FOCO DE INCÊNDIO",           "MATO GROSSO – MT",    "CRÍTICO",  "08:15 UTC", "CONFIRMADO",  "🔥"),
    ("EXTRAÇÃO NÃO AUTORIZADA",    "RONDÔNIA – RO",       "CRÍTICO",  "06:33 UTC", "EM ANÁLISE",  "⛏️"),
    ("QUEIMADA IRREGULAR",         "TOCANTINS – TO",      "CRÍTICO",  "05:12 UTC", "CONFIRMADO",  "🔥"),
    ("DESMATAMENTO PROGRESSIVO",   "PARÁ – PA",           "MODERADO", "03:44 UTC", "MONITORANDO", "🌳"),
    ("ALTERAÇÃO HÍDRICA",          "AMAZONAS – AM",       "MODERADO", "01:20 UTC", "MONITORANDO", "💧"),
    ("ÁREA DE RISCO IDENTIFICADA", "MARANHÃO – MA",       "BAIXO",    "00:05 UTC", "PENDENTE",    "⚠️"),
]

_TEMPLATES = [
    ("NOVO FOCO DETECTADO",       "MATO GROSSO – MT",  "🔥"),
    ("QUEIMADA EM EXPANSÃO",      "PARÁ – PA",         "🔥"),
    ("DESMATAMENTO DETECTADO",    "RONDÔNIA – RO",     "🌳"),
    ("ANOMALIA TÉRMICA",          "TOCANTINS – TO",    "🌡️"),
    ("FUMAÇA DENSA IDENTIFICADA", "AMAZONAS – AM",     "💨"),
    ("ÁREA DEGRADADA",            "MARANHÃO – MA",     "⚠️"),
    ("CORTE IRREGULAR",           "ACRE – AC",         "⛏️"),
    ("RISCO HÍDRICO",             "MINAS GERAIS – MG", "💧"),
]

_STATUS_BY_SEV = {
    "CRÍTICO":  ["EM ANÁLISE", "CONFIRMADO"],
    "MODERADO": ["MONITORANDO", "EM ANÁLISE"],
    "BAIXO":    ["PENDENTE", "MONITORANDO"],
}


def _categoria(title):
    t = title.upper()
    for cat, cfg in CATEGORIAS.items():
        if any(k in t for k in cfg["keywords"]):
            return cat
    return "⚠️ RISCO GERAL"


def _severity_from_score(score):
    if score >= 45: return "CRÍTICO"
    if score >= 20: return "MODERADO"
    return "BAIXO"


def _init():
    if "incidents" not in st.session_state:
        st.session_state.incidents     = [(f"INC-{i+1:03d}",) + inc for i, inc in enumerate(_BASE_INCIDENTS)]
        st.session_state.inc_counter   = len(_BASE_INCIDENTS) + 1
        st.session_state.last_inc_time = time.time()
        st.session_state.novo_id       = None

        # Carrega incidentes reais do banco ao inicializar
        for db_inc in get_db_incidents():
            alerts = db_inc["alerts"]
            if not alerts:
                continue
            title  = alerts[0][:40].upper()
            ts     = db_inc["timestamp"][:16].replace("T", " ") + " UTC"
            sev    = db_inc["severity"] if db_inc["severity"] in SEVERITY_COLOR else "BAIXO"
            status = random.choice(_STATUS_BY_SEV[sev])
            inc_id = f"INC-{st.session_state.inc_counter:03d}"
            st.session_state.incidents.append((inc_id, title, "BANCO DE DADOS", sev, ts, status, "📡"))
            st.session_state.inc_counter += 1


def _maybe_add(scenario):
    if time.time() - st.session_state.last_inc_time < 45:
        return False
    data              = get_cycle_data(scenario)
    sev               = _severity_from_score(data["risk_score"])
    title, loc, emoji = random.choice(_TEMPLATES)
    status            = random.choice(_STATUS_BY_SEV[sev])
    now               = datetime.now(timezone.utc).strftime("%H:%M UTC")
    inc_id            = f"INC-{st.session_state.inc_counter:03d}"
    st.session_state.incidents.insert(0, (inc_id, title, loc, sev, now, status, emoji))
    st.session_state.inc_counter  += 1
    st.session_state.last_inc_time = time.time()
    st.session_state.novo_id       = inc_id
    return True


def _render_aria(data: dict):
    aria = data["aria_analise"].replace("\n", "<br>")
    acoes = data.get("acoes", [])

    acoes_html = ""
    if acoes:
        itens = "".join(
            f'<div style="padding:4px 0;border-bottom:1px solid #1a3a1a;font-size:.78rem;color:#a0d0a0;">'
            f'<span style="color:#4ade80;margin-right:8px;">▶</span>{a}</div>'
            for a in acoes
        )
        acoes_html = f"""
<div style="margin-top:14px;padding-top:12px;border-top:1px solid #1a4a1a;">
  <div style="font-size:.6rem;letter-spacing:.2em;color:#4a7a4a;margin-bottom:8px;">AÇÕES AUTOMÁTICAS EXECUTADAS</div>
  {itens}
</div>"""

    st.markdown(f"""
<div style="background:rgba(4,16,4,0.7);border:1px solid #1a4a1a;border-left:4px solid #4ade80;
            border-radius:8px;padding:16px 20px;margin:16px 0 20px 0;">
  <div style="font-size:.6rem;letter-spacing:.2em;color:#4ade80;margin-bottom:12px;">
    ⚡ RELATÓRIO ARIA — AUTOMATED RISK INTELLIGENCE ANALYST
  </div>
  <div style="font-size:.82rem;color:#a0d0a0;line-height:1.8;font-family:'Share Tech Mono',monospace;white-space:pre-wrap;">
    {aria}
  </div>
  {acoes_html}
</div>""", unsafe_allow_html=True)


def _build_html(grupos, novo_id):
    blocos = ""
    for idx, (cat, items) in enumerate(grupos.items()):
        if not items:
            continue
        cor     = CATEGORIAS[cat]["cor"]
        n_crit  = sum(1 for i in items if i[3] == "CRÍTICO")
        aberto  = "true" if n_crit > 0 else "false"
        display = "block" if n_crit > 0 else "none"
        crit_tag = (
            f'<span style="color:#ef4444;margin-left:8px;font-size:.75rem;">'
            f'&#128308; {n_crit} CR&#205;TICO{"S" if n_crit>1 else ""}</span>'
        ) if n_crit else ""

        cards = ""
        for inc in items:
            inc_id, title, loc, sev, t, stat, emoji = inc
            sc       = SEVERITY_COLOR[sev]
            stc      = STATUS_COLOR[stat]
            border_c = "#4ade80" if inc_id == novo_id else f"{cor}66"
            new_tag  = '<span style="font-size:.7rem;color:#4ade80;font-weight:700;">&#9679; NOVO</span>' if inc_id == novo_id else ""
            cards += f"""
<div style="display:flex;align-items:center;gap:14px;padding:12px 16px;
            margin-bottom:6px;background:rgba(5,12,5,0.7);
            border-radius:6px;border-left:3px solid {border_c};">
  <div style="font-size:1.4rem;width:28px;text-align:center;flex-shrink:0;">{emoji}</div>
  <div style="flex:1;">
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
      <span style="font-family:monospace;font-size:.72rem;color:#4a8a4a;">{inc_id}</span>
      <span style="font-size:.95rem;font-weight:700;letter-spacing:.06em;color:#e2fce8;">{title}</span>
      {new_tag}
    </div>
    <div style="font-size:.8rem;color:#6aaa6a;margin-bottom:2px;">{loc}</div>
    <div style="font-family:monospace;font-size:.7rem;color:#4a7a4a;">{t}</div>
  </div>
  <div style="display:flex;flex-direction:column;align-items:flex-end;gap:5px;flex-shrink:0;">
    <span style="color:{sc};border:1px solid {sc}55;background:{sc}18;
                 font-size:.68rem;padding:3px 10px;border-radius:3px;
                 letter-spacing:.1em;font-weight:700;">{sev}</span>
    <span style="color:{stc};border:1px solid {stc}55;background:{stc}18;
                 font-size:.68rem;padding:3px 10px;border-radius:3px;
                 letter-spacing:.1em;">{stat}</span>
  </div>
</div>"""

        blocos += f"""
<div style="margin-bottom:12px;">
  <button onclick="toggle({idx})" style="
      width:100%;display:flex;align-items:center;justify-content:space-between;
      padding:10px 16px;background:rgba(5,18,5,0.7);
      border:1px solid {cor}44;border-left:4px solid {cor};
      border-radius:6px;cursor:pointer;text-align:left;">
    <div style="display:flex;align-items:center;gap:10px;">
      <span style="color:{cor};font-size:.85rem;font-weight:700;letter-spacing:.12em;">{cat}</span>
      <span style="color:#5a8a5a;font-size:.75rem;">{len(items)} ocorr&#234;ncia{"s" if len(items)>1 else ""}</span>
      {crit_tag}
    </div>
    <span id="arrow-{idx}" style="color:{cor};font-size:1rem;">{"&#9660;" if aberto=="true" else "&#9654;"}</span>
  </button>
  <div id="cat-{idx}" style="display:{display};padding:8px 4px 0 4px;">
    {cards}
  </div>
</div>"""

    return f"""
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:transparent;font-family:'Segoe UI',sans-serif;}}
  button:hover{{background:rgba(10,30,10,0.9)!important;}}
</style>
{blocos}
<script>
function toggle(idx){{
  var c=document.getElementById('cat-'+idx);
  var a=document.getElementById('arrow-'+idx);
  if(c.style.display==='none'){{c.style.display='block';a.innerHTML='&#9660;'}}
  else{{c.style.display='none';a.innerHTML='&#9654;'}}
}}
</script>"""


def render_incidents():
    _init()

    scenario  = st.session_state.get("scenario", "normal")
    novo      = _maybe_add(scenario)
    novo_id   = st.session_state.novo_id
    incidents = st.session_state.incidents
    data      = get_cycle_data(scenario)

    render_topbar("INCIDENTES", "REGISTRO E MONITORAMENTO DE OCORRÊNCIAS")
    render_page_header("GESTÃO DE INCIDENTES", "OCORRÊNCIAS ATIVAS")

    total    = len(incidents)
    criticos = sum(1 for i in incidents if i[3] == "CRÍTICO")
    moderado = sum(1 for i in incidents if i[3] == "MODERADO")
    baixo    = sum(1 for i in incidents if i[3] == "BAIXO")

    c1, c2, c3, c4 = st.columns(4)
    for col, (label, val, color) in zip(
        [c1, c2, c3, c4],
        [("TOTAL ATIVOS", total,    "#d1fae5"),
         ("CRÍTICOS",     criticos, "#ef4444"),
         ("MODERADOS",    moderado, "#f59e0b"),
         ("BAIXO RISCO",  baixo,    "#4ade80")],
    ):
        with col:
            st.markdown(f"""
<div class="metric-card">
  <div class="metric-label">{label}</div>
  <div class="metric-value" style="font-size:2rem;color:{color};">{val}</div>
</div>""", unsafe_allow_html=True)

    # ── Relatório ARIA ──
    _render_aria(data)

    remaining = max(0, int(45 - (time.time() - st.session_state.last_inc_time)))
    st.markdown(f"""
<div style="font-family:monospace;font-size:.7rem;color:#4a7a4a;text-align:right;margin-bottom:16px;">
  PRÓXIMO CICLO EM: <span style="color:#4ade80;">{remaining}s</span>
  {"&nbsp;&nbsp;<span style='color:#4ade80;'>&#9889; NOVO INCIDENTE GERADO</span>" if novo else ""}
</div>""", unsafe_allow_html=True)

    section_header("FILTROS", "")
    f1, f2, _ = st.columns(3)
    with f1:
        filt_sev  = st.selectbox("SEV",  ["TODOS","CRÍTICO","MODERADO","BAIXO"],
                                 label_visibility="collapsed", key="filt_sev")
    with f2:
        filt_stat = st.selectbox("STAT", ["TODOS","CONFIRMADO","EM ANÁLISE","MONITORANDO","PENDENTE"],
                                 label_visibility="collapsed", key="filt_stat")

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("OCORRÊNCIAS POR CATEGORIA", "")

    grupos: dict[str, list] = {cat: [] for cat in CATEGORIAS}
    for inc in incidents:
        _, title, _, sev, _, stat, _ = inc
        if filt_sev  != "TODOS" and sev  != filt_sev:  continue
        if filt_stat != "TODOS" and stat != filt_stat: continue
        grupos[_categoria(title)].append(inc)

    total_items = sum(len(v) for v in grupos.values())
    altura      = max(400, len([v for v in grupos.values() if v]) * 60 + total_items * 90)

    components.html(_build_html(grupos, novo_id), height=altura, scrolling=False)

    if novo:
        st.rerun()