import streamlit as st
from datetime import datetime, timezone

NAV_ITEMS = [
    ("📊", "Dashboard"),
    ("📡", "Telemetria"),
    ("⚠️", "Incidentes"),
    ("👤", "Operadores"),
    ("📋", "Relatórios"),
    ("⚙️", "Configurações"),
]

CENARIO_OPCOES = {
    "🔥 Escalada de Incêndio": "wildfire_escalation",
    "🔋 Emergência Energética": "low_power_emergency",
    "📡 Falha de Comunicação":  "communication_failure",
    "✅ Operação Normal":       "normal",
}

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo-wrap">
            <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
                <circle cx="28" cy="28" r="26" stroke="#4ade80" stroke-width="1" stroke-dasharray="3 2" opacity=".5"/>
                <circle cx="28" cy="28" r="18" stroke="#4ade80" stroke-width="1" opacity=".3"/>
                <circle cx="28" cy="28" r="4" fill="#4ade80"/>
                <path d="M17 12 L28 7 L39 12 L46 18" stroke="#4ade80" stroke-width="1.5" fill="none"/>
                <circle cx="46" cy="18" r="2.5" fill="#4ade80" opacity=".8"/>
                <path d="M10 28 L16 22" stroke="#4ade80" stroke-width="1" opacity=".4"/>
            </svg>
            <div class="sidebar-brand">ENVIROSAT AI</div>
            <div class="sidebar-sub">ORBITAL ENVIRONMENTAL COMMAND</div>
            <div class="sidebar-stars">★ ★ ★</div>
        </div>
        """, unsafe_allow_html=True)

        for icon, label in NAV_ITEMS:
            active = st.session_state.get("current_page") == label
            css_class = "nav-btn active" if active else "nav-btn"
            if st.button(f"{icon}  {label.upper()}", key=f"nav_{label}",
                         use_container_width=True):
                if label != "Configurações":
                    st.session_state.current_page = label
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Cenário operacional ──
        st.markdown("""
        <div style="font-size:.6rem;letter-spacing:.18em;color:#5a8a5a;margin-bottom:6px;">
            CENÁRIO OPERACIONAL
        </div>
        """, unsafe_allow_html=True)
        escolha = st.selectbox(
            label="cenario",
            options=list(CENARIO_OPCOES.keys()),
            index=3,
            label_visibility="collapsed",
            key="cenario_select",
        )
        novo_scenario = CENARIO_OPCOES[escolha]
        if st.session_state.get("scenario") != novo_scenario:
            st.session_state["scenario"] = novo_scenario
            st.cache_data.clear()
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-status">
            <span class="sidebar-status-dot"></span>
            <span style="font-size:.65rem;letter-spacing:.12em;color:#5a8a5a;">SISTEMA OPERACIONAL</span><br>
            <span style="font-size:.6rem;color:#4a7a4a;margin-left:13px;">TODOS OS SISTEMAS NOMINAIS</span>
        </div>
        """, unsafe_allow_html=True)

        op_name  = st.session_state.get("operator_name",  "RANGER-07")
        op_level = st.session_state.get("operator_level", "COMANDO")
        st.markdown(f"""
        <div class="sidebar-operator">
            <div class="op-avatar">🪖</div>
            <div>
                <div style="font-size:.55rem;letter-spacing:.15em;color:#4a7a4a;">OPERADOR</div>
                <div class="op-name">{op_name}</div>
                <div style="font-size:.55rem;letter-spacing:.1em;color:#4a7a4a;">NÍVEL AUTORIZADO</div>
                <div class="op-level">{op_level}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪  ENCERRAR SESSÃO", use_container_width=True, key="logout"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()