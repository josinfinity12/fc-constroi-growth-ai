import streamlit as st
from datetime import datetime
import pytz

CORES_FC = {
    "laranja_principal": "#FF6B00",
    "preto_header": "#111111",
    "branco": "#FFFFFF"
}

def get_cores():
    return CORES_FC

def aplicar_design():
    st.markdown("""
    <style>
    .stApp { background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

def mostrar_header_com_logo():
    fuso = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso)
    st.markdown(f"""
    <style>
    .header-fc {{
        background: #111111;
        color: white;
        padding: 12px 20px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 18px;
        flex-wrap: nowrap;
        overflow: hidden;
    }}
    .header-fc b {{ font-size: 17px; white-space: nowrap; }}
    .header-fc span {{ font-size: 13px; opacity: 0.9; white-space: nowrap; margin-left: 15px; }}
    </style>
    <div class="header-fc">
        <b>FC CONSTRÓI • GROWTH AI v3.1.5</b>
        <span>{agora.strftime("%d/%m/%Y • %H:%M:%S")} • Irará-BA</span>
    </div>
    """, unsafe_allow_html=True)

def mostrar_footer():
    st.markdown("<center style='opacity:0.5; margin-top:30px;'>FC CONSTRÓI v3.1.5 • Growth AI • Irará-BA</center>", unsafe_allow_html=True)
    



