# designer.py - v3.1.6 EMERGENCIA - FUNCIONA 100% + BRANCO ARIAL
import streamlit as st
from datetime import datetime
import pytz

def aplicar_design():
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: Arial, Helvetica, sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_header_com_logo():
    fuso = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso)
    
    dias = ['Segunda','Terca','Quarta','Quinta','Sexta','Sabado','Domingo']
    meses = ['','Janeiro','Fevereiro','Marco','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    
    data_str = f"{dias[agora.weekday()]}, {agora.day} de {meses[agora.month]} de {agora.year}"
    hora_str = agora.strftime("%H:%M:%S")
    
    st.markdown(f"""
    <div style="
        background:#111827;
        padding:18px 24px;
        border-radius:10px;
        border-left:5px solid #FF6B00;
        display:flex;
        justify-content:space-between;
        align-items:center;
        flex-wrap:wrap;
        margin-bottom:20px;
    ">
        <div>
            <div style="font-family:Arial,Helvetica,sans-serif; color:#FFFFFF; font-size:22px; font-weight:700;">FC CONSTRÓI • GROWTH AI v3.1.6</div>
            <div style="font-family:Arial,Helvetica,sans-serif; color:#D1D5DB; font-size:12px; margin-top:4px;">Construção • Porcelanato • Irará/BA</div>
        </div>
        <div style="
            font-family:Arial,Helvetica,sans-serif;
            color:#FFFFFF;
            background:#1F2937;
            padding:10px 18px;
            border-radius:8px;
            border:1px solid #374151;
            font-size:14px;
        ">
            📅 {data_str} • ⏰ {hora_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_footer():
    st.caption("FC CONSTRÓI v3.1.6")

def get_cores():
    return {"laranja":"#FF6B00","preto":"#111827","branco":"#FFFFFF"}

CORES_FC = get_cores()


