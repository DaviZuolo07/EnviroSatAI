import streamlit as st


def inject_styles():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800&family=Share+Tech+Mono&display=swap');

    /* =========================================================
       GLOBAL
    ========================================================= */

    html, body, [class*="css"] {
        font-family: 'Exo 2', sans-serif;
        background: #050805;
        color: #d1fae5;
        overflow-x: hidden;
    }

    body {
        background:
            radial-gradient(circle at top, rgba(30,60,30,.15), transparent 40%),
            linear-gradient(180deg, #040704 0%, #071107 100%);
    }

    .stApp {
        background:
            radial-gradient(circle at top, rgba(30,60,30,.12), transparent 40%),
            linear-gradient(180deg, #040704 0%, #071107 100%);
        color: #d1fae5;
    }

    /* REMOVE BARRAS BRANCAS */
    header {
        background: transparent !important;
    }

    .stAppHeader {
        background: transparent !important;
    }

    div[data-testid="stToolbar"] {
        background: transparent !important;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        background: transparent !important;
        padding-top: 0.8rem;
        max-width: 100%;
        padding-bottom: 1rem;
    }

    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg,#020502 0%,#071107 100%);
        border-right: 1px solid rgba(74,222,128,.08);
        width: 290px !important;
    }

    .sidebar-logo-wrap {
        padding-top: 18px;
        text-align:center;
    }

    .sidebar-brand{
        color:#4ade80;
        font-size:.95rem;
        font-weight:800;
        letter-spacing:.12em;
        margin-top:8px;
    }

    .sidebar-sub{
        color:#4a7a4a;
        font-size:.58rem;
        letter-spacing:.12em;
        margin-top:2px;
    }

    .sidebar-stars{
        color:#1f3b1f;
        margin-top:8px;
        font-size:.65rem;
    }

    .sidebar-status{
        padding:10px 0;
    }

    .sidebar-status-dot{
        width:8px;
        height:8px;
        background:#4ade80;
        border-radius:50%;
        display:inline-block;
        margin-right:6px;
        box-shadow:0 0 10px #4ade80;
    }

    .sidebar-operator{
        margin-top:12px;
        display:flex;
        gap:12px;
        align-items:center;
        padding:12px;
        border:1px solid rgba(74,222,128,.08);
        background:#071107;
        border-radius:6px;
    }

    .op-avatar{
        width:52px;
        height:52px;
        border-radius:6px;
        background:linear-gradient(180deg,#0b140b,#121d12);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:1.4rem;
        border:1px solid rgba(74,222,128,.1);
    }

    .op-name{
        color:#d1fae5;
        font-size:.8rem;
        font-weight:700;
        letter-spacing:.08em;
    }

    .op-level{
        color:#4ade80;
        font-size:.72rem;
        font-weight:700;
        letter-spacing:.08em;
    }

    /* =========================================================
       TOPBAR
    ========================================================= */

    .topbar {
        background:
            linear-gradient(90deg,#061106,#081808);
        border: 1px solid rgba(74,222,128,.08);
        padding: 18px 22px;
        border-radius: 6px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:22px;
    }

    .topbar-title{
        color:#ecfdf5;
        font-size:1rem;
        font-weight:800;
        letter-spacing:.2em;
    }

    .topbar-sub{
        color:#4ade80;
        font-size:.68rem;
        letter-spacing:.18em;
        margin-top:4px;
    }

    .topbar-time{
        font-family:'Share Tech Mono', monospace;
        color:#4ade80;
        font-size:.95rem;
    }

    .topbar-date{
        font-size:.62rem;
        color:#4a7a4a;
        letter-spacing:.15em;
    }

    /* =========================================================
       STATUS BADGE
    ========================================================= */

    .status-badge{
        border:1px solid rgba(74,222,128,.15);
        background:#071407;
        padding:10px 14px;
        border-radius:4px;
    }

    .status-badge-label{
        color:#4a7a4a;
        font-size:.55rem;
        letter-spacing:.12em;
    }

    .status-badge-value{
        color:#4ade80;
        font-size:.78rem;
        font-weight:700;
        letter-spacing:.15em;
    }

    /* =========================================================
       PANELS
    ========================================================= */

    .panel,
    .metric-card,
    .alert-card,
    .map-container,
    .sat-bar,
    .globe-container {
        background:
            linear-gradient(180deg,#061006 0%,#081408 100%);
        border:1px solid rgba(74,222,128,.08);
        border-radius:6px;
        box-shadow:
            inset 0 0 0 1px rgba(255,255,255,.01),
            0 0 18px rgba(0,0,0,.35);
    }

    /* =========================================================
       METRIC CARD
    ========================================================= */

    .metric-card{
        position:relative;
        padding:22px;
        min-height:130px;
        overflow:hidden;
    }

    .metric-label{
        color:#5a8a5a;
        font-size:.62rem;
        letter-spacing:.2em;
        margin-bottom:14px;
    }

    .metric-value{
        color:#f0fdf4;
        font-size:2.3rem;
        font-weight:800;
        line-height:1;
    }

    .metric-delta{
        margin-top:10px;
        color:#4ade80;
        font-size:.72rem;
        letter-spacing:.08em;
    }

    .metric-delta.neg{
        color:#ef4444;
    }

    .metric-icon{
        position:absolute;
        right:18px;
        top:16px;
        opacity:.35;
        font-size:1.4rem;
    }

    /* =========================================================
       SECTION HEADER
    ========================================================= */

    .section-header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:14px;
    }

    .section-title{
        color:#d1fae5;
        font-size:.78rem;
        letter-spacing:.2em;
        font-weight:700;
    }

    .section-action{
        color:#5a8a5a;
        font-size:.62rem;
        letter-spacing:.15em;
    }

    /* =========================================================
       ALERTS
    ========================================================= */

    .alert-card{
        padding:12px;
        display:flex;
        align-items:center;
        gap:12px;
    }

    .alert-thumb{
        width:46px;
        height:46px;
        border-radius:4px;
        background:#101510;
        display:flex;
        align-items:center;
        justify-content:center;
    }

    .alert-title{
        color:#ecfdf5;
        font-size:.78rem;
        font-weight:700;
        letter-spacing:.06em;
    }

    .alert-loc,
    .alert-time{
        color:#4a7a4a;
        font-size:.62rem;
    }

    .badge-critico{
        background:#3a1010;
        color:#ef4444;
        border:1px solid rgba(239,68,68,.2);
        padding:4px 6px;
        font-size:.52rem;
        letter-spacing:.1em;
    }

    /* =========================================================
       SAT BAR
    ========================================================= */

    .sat-bar{
        padding:18px;
    }

    .sat-item{
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:4px;
    }

    .sat-name{
        color:#d1fae5;
        font-size:.72rem;
        font-weight:700;
    }

    .sat-status{
        color:#4ade80;
        font-size:.65rem;
        letter-spacing:.08em;
    }

    /* =========================================================
       GLOBE
    ========================================================= */

    .globe-container{
        position:relative;
        display:flex;
        justify-content:center;
        align-items:center;
        padding-top:10px;
        overflow:hidden;
    }

    .globe-coverage{
        position:absolute;
        bottom:12px;
        font-size:.7rem;
        letter-spacing:.15em;
        color:#2d7a2d;
        font-family:'Share Tech Mono',monospace;
    }

    /* =========================================================
       TELEMETRY
    ========================================================= */

    .telemetry-row{
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:14px 6px;
        border-bottom:1px solid rgba(74,222,128,.06);
    }

    .telem-label{
        color:#5a8a5a;
        font-size:.68rem;
        letter-spacing:.12em;
    }

    .telem-value{
        color:#d1fae5;
        font-weight:700;
    }

    .telem-value.alto{
        color:#ef4444;
    }

    /* =========================================================
       DATAFRAME
    ========================================================= */

    .stDataFrame {
        border:1px solid rgba(74,222,128,.08);
        border-radius:6px;
        overflow:hidden;
    }

    /* TABELA TELEMETRIA */

    .stDataFrame div[role="grid"] {
        background:#071107 !important;
        color:#4ade80 !important;
    }

    .stDataFrame div[role="columnheader"]{
        background:#0a140a !important;
        color:#4ade80 !important;
    }

    /* =========================================================
       BUTTONS
    ========================================================= */

    .stButton > button {
        background:#081408;
        color:#4ade80;
        border:1px solid rgba(74,222,128,.15);
        border-radius:4px;
        letter-spacing:.15em;
        font-size:.72rem;
        transition:.2s;
        min-height:42px;
    }

    .stButton > button:hover{
        border-color:#4ade80;
        color:#d1fae5;
    }

    </style>
    """, unsafe_allow_html=True)