# designer.py - FC CONSTRÓI v3.1.1 - CORES ANTERIORES + RELÓGIO AO VIVO
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
        .fc-header h1 { 
            color: #FFFFFF !important; 
            font-size: 22px !important; 
            font-weight: 800 !important; 
            margin: 0 !important; 
        }
        .fc-header p { 
            color: #9CA3AF !important; 
            font-size: 12px !important; 
            margin: 4px 0 0 0 !important;
        }
        .fc-clock {
            color: #FF6B00 !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            font-family: 'Courier New', monospace;
            background: #1F2937;
            padding: 10px 16px;
            border-radius: 8px;
            border: 1px solid #374151;
        }
        [data-testid="stMetric"] {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

def mostrar_header_com_logo():
    fuso_bahia = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso_bahia)
    
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    dia_semana = dias[agora.weekday()]
    data_str = f"{dia_semana}, {agora.day} de {meses[agora.month]} de {agora.year}"
    hora_str = agora.strftime("%H:%M:%S")
    
    st.markdown(f"""
    <div class="fc-header">
        <div>
            <h1>FC CONSTRÓI • GROWTH AI v3.1.1</h1>
            <p>Construção • Porcelanato • Inteligência de Vendas • Irará/BA</p>
        </div>
        <div class="fc-clock">
            📅 {data_str} • ⏰ {hora_str}
        </div>
    </div>
    """, unsafe_allow_html=True)

