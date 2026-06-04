import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from frontend.styles import inject_styles

def main():
    st.set_page_config(
        page_title="EnviroSat AI – Mission Control",
        page_icon="🛰️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        from frontend.auth import login_screen
        login_screen()
        return

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    from frontend.components.sidebar import render_sidebar
    render_sidebar()

    page = st.session_state.current_page

    if page == "Dashboard":
        from frontend.views.dashboard import render_dashboard
        render_dashboard()
    elif page == "Telemetria":
        from frontend.views.telemetry import render_telemetry
        render_telemetry()
    elif page == "Incidentes":
        from frontend.views.incidents import render_incidents
        render_incidents()
    elif page == "Operadores":
        from frontend.views.operators import render_operators
        render_operators()
    elif page == "Relatórios":
        from frontend.views.reports import render_reports
        render_reports()

if __name__ == "__main__":
    main()