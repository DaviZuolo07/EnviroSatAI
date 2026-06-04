import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from frontend.components.topbar  import render_topbar
from frontend.components.header  import render_page_header
from frontend.components.cards   import section_header


def _gen_series(n=60, base=50, noise=5, trend=0):
    np.random.seed(42)
    t = np.linspace(0, 4*np.pi, n)
    return base + noise * np.sin(t) + np.cumsum(np.random.randn(n) * .5) + trend * np.arange(n) / n


def _time_labels(n=60):
    return [f"{i}m" for i in range(n, 0, -1)]


PALETTE = {
    "Temperatura":       ("#4ade80", _gen_series(base=28.4, noise=2, trend=1.2)),
    "Umidade":           ("#60a5fa", _gen_series(base=62.7, noise=3, trend=-2.1)),
    "Cobertura Vegetal": ("#34d399", _gen_series(base=73.8, noise=1.5, trend=1.8)),
    "Índice Queimadas":  ("#f87171", _gen_series(base=8.6,  noise=1,   trend=2.3)),
    "Nível de Risco":    ("#fb923c", _gen_series(base=75,   noise=4,   trend=15)),
}


def _hex_to_rgba(hex_color, alpha=0.09):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"


def render_telemetry():
    render_topbar("TELEMETRIA", "DADOS EM TEMPO REAL DOS SATÉLITES")
    render_page_header("TELEMETRIA EM TEMPO REAL", "MONITORAMENTO CONTÍNUO")

    labels = _time_labels()

    # ── Summary metrics ──
    cols = st.columns(5)
    summaries = [
        ("TEMPERATURA",       "28.4 °C",  "+1.2°C"),
        ("UMIDADE",           "62.7 %",   "–2.1%"),
        ("COB. VEGETAL",      "73.8 %",   "+1.8%"),
        ("ÍND. QUEIMADAS",    "8.6/10",   "+2.3"),
        ("NÍVEL DE RISCO",    "ALTO",     "+15%"),
    ]
    for col, (label, val, delta) in zip(cols, summaries):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="font-size:1.5rem;">{val}</div>
                <div class="metric-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("SÉRIES HISTÓRICAS – ÚLTIMAS 60 LEITURAS")

    col1, col2 = st.columns(2)
    items = list(PALETTE.items())

    for idx, (name, (color, values)) in enumerate(items):
        col = col1 if idx % 2 == 0 else col2
        with col:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=labels, y=values,
                mode="lines",
                line=dict(color=color, width=2, shape="spline"),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(color, 0.09),
                name=name,
            ))
            fig.update_layout(
                title=dict(text=name.upper(), font=dict(
                    family="Exo 2, sans-serif", size=11, color="#5a8a5a"),
                    x=0.01),
                height=200,
                margin=dict(l=10, r=10, t=36, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, tickfont=dict(
                    color="#2d5a2d", size=8, family="Share Tech Mono"),
                    tickmode="array",
                    tickvals=labels[::10], ticktext=labels[::10]),
                yaxis=dict(showgrid=True, gridcolor="#1a3a1a",
                           tickfont=dict(color="#2d5a2d", size=8,
                                         family="Share Tech Mono")),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("STATUS DOS SATÉLITES")
    df = pd.DataFrame({
        "SATÉLITE": [f"E-0{i}" for i in range(1, 6)],
        "STATUS":   ["ONLINE"] * 5,
        "SINAL":    ["98.1%", "97.4%", "99.0%", "96.8%", "98.6%"],
        "BATERIA":  ["87%",   "92%",   "78%",   "95%",   "89%"],
        "ÓRBITA":   ["SÍNCRONA"] * 5,
        "ÚLTIMA LEITURA": ["12:45:32", "12:44:58", "12:45:01", "12:43:12", "12:45:30"],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)