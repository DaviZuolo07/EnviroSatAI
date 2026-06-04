import streamlit as st

def render_page_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="margin-bottom:18px;">
        <div style="font-family:'Exo 2',sans-serif;font-size:1.6rem;font-weight:800;
                    letter-spacing:.15em;color:#d1fae5;border-left:4px solid #4ade80;
                    padding-left:14px;line-height:1.1;">
            {title}
        </div>
        {"<div style='font-size:.7rem;letter-spacing:.2em;color:#4ade80;padding-left:18px;margin-top:3px;'>● " + subtitle + "</div>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)