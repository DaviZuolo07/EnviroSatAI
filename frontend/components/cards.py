import streamlit as st

def metric_card(label: str, value: str, delta: str = "", icon: str = "", delta_negative: bool = False):
    delta_class = "metric-delta neg" if delta_negative else "metric-delta"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="{delta_class}">{delta}</div>
    </div>
    """, unsafe_allow_html=True)


def alert_card(title: str, location: str, time_str: str, emoji: str = "🔥"):
    st.markdown(f"""
    <div class="alert-card">
        <div class="alert-thumb">{emoji}</div>
        <div class="alert-info">
            <div class="alert-title">{title}</div>
            <div class="alert-loc">{location}</div>
            <div class="alert-time">{time_str}</div>
        </div>
        <span class="badge-critico">CRÍTICO</span>
    </div>
    """, unsafe_allow_html=True)


def telemetry_row(label: str, value: str, delta: str, icon: str = "📊",
                  positive: bool = True, is_risk: bool = False):
    delta_class = "telem-delta pos" if positive else "telem-delta neg"
    value_class = "telem-value alto" if is_risk else "telem-value"
    st.markdown(f"""
    <div class="telemetry-row">
        <div class="telem-label">{icon} &nbsp;{label}</div>
        <div style="display:flex;align-items:center;gap:14px;">
            <div class="{value_class}">{value}</div>
            <div class="{delta_class}">{delta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, action: str = "VER TODOS"):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">{title}</div>
        <div class="section-action">{action}</div>
    </div>
    """, unsafe_allow_html=True)