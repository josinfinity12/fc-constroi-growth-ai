# designer.py - v3.1.8 FIX - MANTEM SEU ORIGINAL + DATA HORA BRANCA
import streamlit as st
from datetime import datetime
import pytz

def aplicar_design():
    st.markdown("""
    <style>
        .stApp { background-color: #FFFFFF; }
        .fc-header {
            background: #111827;
            padding: 18px 24px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            border-left: 5px solid #FF6B00;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_header_com_logo():
    fuso_bahia = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso_bahia)
    dias = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
    meses = ['','Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    data_str = f"{dias[agora.weekday()]}, {agora.day} de {meses[agora.month]} de {agora.year}"
    hora_str = agora.strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="fc-header">
        <div>
            <h1 style="color:#FFFFFF; font-family:Arial,Helvetica,sans-serif; font-size:22px; font-weight:700; margin:0;">FC CONSTRÓI • GROWTH AI v3.1.8</h1>
            <p style="color:#D1D5DB; font-family:Arial,Helvetica,sans-serif; font-size:12px; margin:4px 0 0 0;">Construção • Porcelanato • Inteligência de Vendas</p>
        </div>
        <div style="color:#F9FAFB; background:#1F2937; font-family:Arial,Helvetica,sans-serif; font-size:14px; font-weight:500; padding:10px 18px; border-radius:8px; border:1px solid #374151;">
            📅 {data_str} • ⏰ {hora_str} • Irará/BA
        </div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_footer():
    fuso = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso)
    st.markdown(f"<div style='text-align:center; color:#9CA3AF; font-size:11px; margin-top:40px; border-top:1px solid #E5E7EB; padding-top:15px; font-family:Arial;'>FC CONSTRÓI © {agora.year} • v3.1.8 Arial Branco • {agora.strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)

def get_cores():
    return {"laranja_principal":"#FF6B00","preto_header":"#111827","branco":"#FFFFFF"}

CORES_FC = get_cores()


