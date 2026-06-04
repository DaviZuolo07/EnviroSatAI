import streamlit as st
from frontend.components.topbar import render_topbar
from frontend.components.header import render_page_header
from frontend.components.cards import section_header

REPORTS = [
    ("REL-042", "RELATÓRIO DIÁRIO DE MONITORAMENTO",  "24/05/2025", "AUTOMÁTICO", "CONCLUÍDO", "📋"),
    ("REL-041", "ANÁLISE DE FOCOS DE QUEIMADA – Q2",  "23/05/2025", "ANALISTA",   "CONCLUÍDO", "🔥"),
    ("REL-040", "VARIAÇÃO DE COBERTURA VEGETAL",       "22/05/2025", "AUTOMÁTICO", "CONCLUÍDO", "🌳"),
    ("REL-039", "ALERTA DE DESMATAMENTO – PARÁ",       "21/05/2025", "COMANDO",    "REVISÃO",   "⚠️"),
    ("REL-038", "ÍNDICE DE RISCO AMBIENTAL MENSAL",    "20/05/2025", "ANALISTA",   "PENDENTE",  "📊"),
]

STATUS_COLOR = {"CONCLUÍDO": "#4ade80", "REVISÃO": "#f59e0b", "PENDENTE": "#6b9c6b"}


def render_reports():
    render_topbar("RELATÓRIOS", "HISTÓRICO E GERAÇÃO DE DOCUMENTOS")
    render_page_header("RELATÓRIOS DO SISTEMA", "BASE DOCUMENTAL")

    c1, c2, c3 = st.columns(3)
    for col, (label, val) in zip(
        [c1, c2, c3],
        [("TOTAL GERADOS", "042"), ("ESTE MÊS", "18"), ("PENDENTES", "03")],
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:2rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick generate
    section_header("GERAR RELATÓRIO", "")
    g1, g2 = st.columns([2, 1])
    with g1:
        report_type = st.selectbox(
            "", ["RELATÓRIO DIÁRIO", "ANÁLISE DE INCIDENTES", "COBERTURA VEGETAL",
                 "ÍNDICE DE QUEIMADAS", "RESUMO EXECUTIVO"],
            label_visibility="collapsed"
        )
    with g2:
        if st.button("⚙️  GERAR AGORA", use_container_width=True):
            st.success(f"✅ {report_type} adicionado à fila de geração.")

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("RELATÓRIOS RECENTES", "VER TODOS")

    for rep_id, title, date, author, status, emoji in REPORTS:
        sc = STATUS_COLOR.get(status, "#6b9c6b")
        st.markdown(f"""
        <div class="alert-card" style="margin-bottom:8px;">
            <div class="alert-thumb" style="background:linear-gradient(135deg,#0a120a,#1a2a1a);">
                {emoji}
            </div>
            <div class="alert-info" style="flex:1;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="font-family:'Share Tech Mono',monospace;font-size:.65rem;color:#4a7a4a;">{rep_id}</span>
                    <span class="alert-title">{title}</span>
                </div>
                <div class="alert-loc">{author}</div>
                <div class="alert-time">{date}</div>
            </div>
            <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
                <span style="background:{sc}22;color:{sc};border:1px solid {sc}44;
                             font-size:.55rem;padding:2px 8px;border-radius:2px;letter-spacing:.1em;font-weight:700;">
                    {status}
                </span>
                <span style="font-size:.6rem;color:#4a7a4a;cursor:pointer;letter-spacing:.1em;">↓ BAIXAR</span>
            </div>
        </div>
        """, unsafe_allow_html=True)