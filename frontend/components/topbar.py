import streamlit as st
from datetime import datetime, timezone

def render_topbar(title: str, subtitle: str):
    now = datetime.now(timezone.utc)
    time_str = now.strftime("%H:%M:%S UTC")
    date_str = now.strftime("%d %b %Y").upper()

    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">{title}</div>
            <div class="topbar-sub">● {subtitle}</div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="text-align:right;">
                <div class="topbar-time">{time_str}</div>
                <div class="topbar-date">{date_str}</div>
            </div>
            <div class="status-badge">
                <div>
                    <div class="status-badge-label">STATUS GERAL</div>
                    <div class="status-badge-value">NOMINAL</div>
                </div>
            </div>
            <div style="font-size:1rem;opacity:.5;cursor:pointer;">🔔</div>
        </div>
    </div>
    """, unsafe_allow_html=True)