import streamlit as st

def login_screen():
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-box">
            <div class="login-logo">
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                    <circle cx="32" cy="32" r="30" stroke="#4ade80" stroke-width="1.5" stroke-dasharray="4 2"/>
                    <circle cx="32" cy="32" r="20" stroke="#4ade80" stroke-width="1"/>
                    <line x1="32" y1="2"  x2="32" y2="62" stroke="#4ade80" stroke-width="0.5" opacity="0.4"/>
                    <line x1="2"  y1="32" x2="62" y2="32" stroke="#4ade80" stroke-width="0.5" opacity="0.4"/>
                    <circle cx="32" cy="32" r="4" fill="#4ade80"/>
                    <path d="M20 14 L32 8 L44 14" stroke="#4ade80" stroke-width="1.5" fill="none"/>
                    <path d="M44 14 L52 20" stroke="#4ade80" stroke-width="1.5"/>
                    <circle cx="52" cy="20" r="2" fill="#4ade80"/>
                </svg>
            </div>
            <div class="login-title">ENVIROSAT AI</div>
            <div class="login-sub">ORBITAL ENVIRONMENTAL COMMAND</div>
            <div class="login-stars">★ ★ ★</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
        st.markdown('<p class="login-label">IDENTIFICAÇÃO DO OPERADOR</p>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="ID do operador", key="login_user", label_visibility="collapsed")
        st.markdown('<p class="login-label">CÓDIGO DE ACESSO</p>', unsafe_allow_html=True)
        st.text_input("", placeholder="••••••••", type="password", key="login_pass", label_visibility="collapsed")

        if st.button("🔐  AUTENTICAR ACESSO", use_container_width=True, key="login_btn"):
            st.session_state.authenticated = True
            st.session_state.operator_name  = username.upper() if username else "OPERADOR"
            st.session_state.operator_level = "COMANDO"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)