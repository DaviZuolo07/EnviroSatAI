import streamlit as st
from frontend.components.topbar import render_topbar
from frontend.components.header import render_page_header
from frontend.components.cards import section_header

OPERATORS = [
    ("RANGER-07", "COMANDO",    "ONLINE",  "12:45 UTC", "47", "🪖"),
    ("ALPHA-03",  "ANALISTA",   "ONLINE",  "12:40 UTC", "32", "👤"),
    ("DELTA-11",  "SUPERVISOR", "ONLINE",  "12:38 UTC", "61", "🎖️"),
    ("BRAVO-05",  "ANALISTA",   "OFFLINE", "08:12 UTC", "28", "👤"),
    ("ECHO-09",   "OPERADOR",   "STANDBY", "11:55 UTC", "19", "👤"),
]

STATUS_COLOR = {"ONLINE": "#4ade80", "OFFLINE": "#ef4444", "STANDBY": "#f59e0b"}


def render_operators():
    render_topbar("OPERADORES", "GESTÃO DE EQUIPE E ACESSOS")
    render_page_header("OPERADORES DO SISTEMA", "EQUIPE ATIVA")

    c1, c2, c3 = st.columns(3)
    for col, (label, val, color) in zip(
        [c1, c2, c3],
        [("ONLINE",  "03", "#4ade80"),
         ("STANDBY", "01", "#f59e0b"),
         ("OFFLINE", "01", "#ef4444")],
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:2rem;color:{color};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("LISTA DE OPERADORES", "ADICIONAR")

    for name, level, status, last_seen, incidents, emoji in OPERATORS:
        sc = STATUS_COLOR.get(status, "#6b9c6b")
        st.markdown(f"""
        <div class="alert-card" style="margin-bottom:8px;">
            <div class="alert-thumb" style="background:linear-gradient(135deg,#0a1a0a,#1a3a1a);">
                {emoji}
            </div>
            <div class="alert-info" style="flex:1;">
                <div class="alert-title">{name}</div>
                <div class="alert-loc">{level}</div>
                <div class="alert-time">ÚLTIMO ACESSO: {last_seen}</div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
                <span style="background:{sc}22;color:{sc};border:1px solid {sc}44;
                             font-size:.55rem;padding:2px 8px;border-radius:2px;letter-spacing:.1em;font-weight:700;">
                    {status}
                </span>
                <span style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#4a7a4a;">
                    {incidents} INCIDENTES
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)