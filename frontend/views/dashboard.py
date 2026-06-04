import streamlit as st
from frontend.components.topbar import render_topbar
from frontend.components.header import render_page_header
from frontend.components.cards  import metric_card, alert_card, telemetry_row, section_header
from frontend.data_service import get_cycle_data

MAP_HTML = """
<div class="map-container">
    <div style="padding:10px 14px 6px;">
        <div class="section-title">MAPA DE SITUAÇÃO</div>
    </div>
    <div style="position:relative;height:270px;background:linear-gradient(160deg,#050c05,#081408,#060d06);overflow:hidden;">
        <svg viewBox="0 0 500 460" width="100%" height="100%" style="position:absolute;top:0;left:0;">
            <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#0f2a0f" stroke-width="0.5"/>
                </pattern>
                <radialGradient id="gr" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#ef4444" stop-opacity="0.5"/>
                    <stop offset="100%" stop-color="#ef4444" stop-opacity="0"/>
                </radialGradient>
                <radialGradient id="go" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.4"/>
                    <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <rect width="500" height="460" fill="url(#grid)"/>
            <path d="M180,18 L210,14 L245,22 L270,18 L295,30 L320,28 L345,42
                     L368,52 L385,70 L400,88 L415,108 L425,130 L432,155
                     L435,180 L430,205 L420,228 L408,248 L395,268
                     L378,285 L362,300 L345,315 L325,328 L305,340
                     L285,350 L265,358 L245,362 L225,360 L205,352
                     L185,340 L168,325 L152,308 L138,290 L126,270
                     L116,250 L108,228 L104,205 L102,182 L104,158
                     L108,135 L116,113 L126,93 L140,75 L155,58 L168,42 Z"
                  fill="rgba(15,40,15,0.7)" stroke="#2d7a2d" stroke-width="1.2"/>
            <path d="M200,80 L280,75 L340,100 L360,150 L340,200 L300,230 L250,240 L200,220 L170,180 L175,130 Z"
                  fill="none" stroke="#1a4a1a" stroke-width="0.6" stroke-dasharray="4,3"/>
            <circle cx="220" cy="140" r="18" fill="url(#gr)"/>
            <polygon points="220,126 228,140 212,140" fill="#ef4444" style="filter:drop-shadow(0 0 5px #ef4444)"/>
            <circle cx="220" cy="140" r="22" fill="none" stroke="#ef4444" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>
            <circle cx="265" cy="195" r="16" fill="url(#gr)" opacity="0.7"/>
            <polygon points="265,182 273,196 257,196" fill="#ef4444" style="filter:drop-shadow(0 0 5px #ef4444)"/>
            <circle cx="235" cy="230" r="14" fill="url(#go)" opacity="0.7"/>
            <polygon points="235,219 242,231 228,231" fill="#f59e0b" style="filter:drop-shadow(0 0 4px #f59e0b)"/>
            <circle cx="305" cy="210" r="10" fill="rgba(74,222,128,0.12)"/>
            <text x="305" y="215" text-anchor="middle" font-size="12">🛡</text>
            <circle cx="380" cy="80" r="8" fill="none" stroke="#4ade80" stroke-width="1" opacity="0.6"/>
            <line x1="372" y1="80" x2="388" y2="80" stroke="#4ade80" stroke-width="0.8" opacity="0.6"/>
            <line x1="380" y1="72" x2="380" y2="88" stroke="#4ade80" stroke-width="0.8" opacity="0.6"/>
            <text x="110" y="454" font-family="monospace" font-size="7" fill="#2d7a2d">-15.78° S  -47.93° W</text>
            <text x="360" y="454" font-family="monospace" font-size="7" fill="#2d7a2d">ZOOM: 1x | MERCATOR</text>
        </svg>
    </div>
    <div class="map-legend">
        <div class="legend-item"><span style="color:#ef4444;">▲</span> ALERTA CRÍTICO</div>
        <div class="legend-item"><span style="color:#f59e0b;">▲</span> ALERTA MODERADO</div>
        <div class="legend-item"><span style="color:#4ade80;">🛡</span> VIGILÂNCIA</div>
    </div>
</div>
"""

GLOBE_HTML = """
<div class="globe-container" style="min-height:190px;">
    <svg width="170" height="170" viewBox="0 0 170 170" fill="none">
        <circle cx="85" cy="85" r="68" stroke="#1e4d1e" stroke-width="1.5" fill="rgba(6,14,6,0.8)"/>
        <ellipse cx="85" cy="85" rx="68" ry="25" stroke="#1a3a1a" stroke-width="0.8"/>
        <ellipse cx="85" cy="85" rx="68" ry="48" stroke="#162e16" stroke-width="0.6"/>
        <ellipse cx="85" cy="85" rx="30" ry="68" stroke="#1a3a1a" stroke-width="0.8"/>
        <path d="M78,55 L92,52 L100,62 L104,78 L100,95 L92,108 L82,115 L72,108 L68,92 L70,75 Z"
              fill="rgba(30,77,30,0.5)" stroke="#2d7a2d" stroke-width="0.8"/>
        <ellipse cx="85" cy="85" rx="82" ry="22" stroke="#4ade80" stroke-width="0.8"
                 stroke-dasharray="4,3" opacity="0.4"/>
        <circle cx="148" cy="68" r="3.5" fill="#4ade80" style="filter:drop-shadow(0 0 5px #4ade80)"/>
        <circle cx="28"  cy="102" r="2.5" fill="#4ade80" opacity="0.7"/>
        <circle cx="155" cy="100" r="2"   fill="#4ade80" opacity="0.5"/>
        <line x1="148" y1="68" x2="85" y2="85" stroke="#4ade80" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.3"/>
    </svg>
    <div style="position:absolute;bottom:8px;font-size:.6rem;letter-spacing:.15em;color:#2d7a2d;font-family:'Share Tech Mono',monospace;">
        COBERTURA: {cobertura}
    </div>
</div>
"""


def render_dashboard():
    scenario = st.session_state.get("scenario", "normal")
    data = get_cycle_data(scenario)

    render_topbar("CENTRO DE COMANDO ENVIROSAT AI", "MONITORAMENTO AMBIENTAL ORBITAL")
    render_page_header("DASHBOARD OPERACIONAL", "VISÃO GERAL DA SITUAÇÃO AMBIENTAL")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("ÁREAS MONITORADAS", "128",                        "+ 8 ÚLTIMAS 24H", "🎯")
    with c2: metric_card("ALERTAS ATIVOS",    str(data["alertas_ativos"]),  "TEMPO REAL",      "⚠️")
    with c3: metric_card("FOCOS TÉRMICOS",    str(data["hotspots"]),        "DETECTADOS",      "🔥", delta_negative=True)
    with c4: metric_card("COBERTURA ORBITAL", data["cobertura_orbital"],    "NOMINAL",         "🛰️")

    st.markdown("<br>", unsafe_allow_html=True)

    col_map, col_telem, col_alerts = st.columns([2.2, 1.6, 1.4])
    with col_map:
        st.markdown(MAP_HTML, unsafe_allow_html=True)
    with col_telem:
        st.markdown('<div class="panel" style="height:100%;">', unsafe_allow_html=True)
        section_header("TELEMETRIA EM TEMPO REAL")
        telemetry_row("TEMPERATURA",         data["temperatura"],       "", "🌡️", True)
        telemetry_row("UMIDADE",             data["umidade"],           "", "💧", False)
        telemetry_row("COBERTURA VEGETAL",   data["cobertura_vegetal"], "", "🌿", True)
        telemetry_row("ÍNDICE DE QUEIMADAS", data["indice_queimadas"],  "", "🔥", False)
        telemetry_row("NÍVEL DE RISCO",      data["nivel_risco"],       "", "⚠️",
                      data["nivel_risco"] == "NOMINAL", is_risk=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_alerts:
        st.markdown('<div class="panel" style="height:100%;">', unsafe_allow_html=True)
        section_header("ALERTAS CRÍTICOS")
        for alerta in data["alertas"]:
            alert_card(alerta, data["severity"], "", "🔥")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    SAT_ITEMS = "".join([
        f'<div class="sat-item"><div class="sat-icon">🛰️</div><div class="sat-name">E-0{i}</div>'
        f'<div class="sat-status">ONLINE</div></div>'
        for i in range(1, 6)
    ])
    SAT_BAR = f"""
    <div class="sat-bar">
        <div style="font-size:.65rem;letter-spacing:.2em;color:#5a8a5a;">SATÉLITES ATIVOS</div>
        <div style="display:flex;gap:24px;">{SAT_ITEMS}</div>
        <div style="font-family:'Share Tech Mono',monospace;color:#4ade80;font-size:.85rem;">05 / 05</div>
    </div>
    """

    import datetime
    now_utc = datetime.datetime.utcnow()

    col_sat, col_globe = st.columns([2.5, 1])
    with col_sat:
        st.markdown(SAT_BAR, unsafe_allow_html=True)
        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown(f"""
            <div class="panel" style="margin-top:10px;">
                <div style="font-size:.6rem;letter-spacing:.15em;color:#5a8a5a;">ÚLTIMA ATUALIZAÇÃO</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1rem;color:#d1fae5;margin-top:4px;">{now_utc.strftime('%H:%M:%S')} UTC</div>
                <div style="font-size:.65rem;color:#4a7a4a;">{now_utc.strftime('%d/%m/%Y')}</div>
            </div>""", unsafe_allow_html=True)
        with c_b:
            st.markdown("""
            <div class="panel" style="margin-top:10px;">
                <div style="font-size:.6rem;letter-spacing:.15em;color:#5a8a5a;">FREQUÊNCIA DE COLETA</div>
                <div style="font-family:'Share Tech Mono',monospace;font-size:1rem;color:#d1fae5;margin-top:4px;">15 MIN</div>
                <div style="font-size:.65rem;color:#4a7a4a;">ÓRBITA SÍNCRONA</div>
            </div>""", unsafe_allow_html=True)
    with col_globe:
        section_header("COBERTURA ORBITAL", "VER DETALHES")
        st.markdown(GLOBE_HTML.format(cobertura=data["cobertura_orbital"]), unsafe_allow_html=True)