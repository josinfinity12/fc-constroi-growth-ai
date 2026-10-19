# designer.py - FC CONSTRÓI • GROWTH AI v3.1.5 - COMPLETO SEM REMOVER NADA
import streamlit as st
from datetime import datetime
import pytz
from PIL import Image
import base64
import io

# ===================================================================
# 1. FUNÇÃO PRINCIPAL - APLICAR DESIGN GLOBAL - CORES ANTERIORES PRESERVADAS
# ===================================================================
def aplicar_design():
    st.markdown("""
    <style>
        /* ============================================ */
        /* TIPOGRAFIA GLOBAL - ARIAL LEGÍVEL */
        /* ============================================ */
        html, body, [class*="css"], .stApp, p, div, span, h1, h2, h3, h4, h5, h6, 
        button, input, textarea, select, label {
            font-family: Arial, Helvetica, sans-serif !important;
        }
        
        /* App background */
        .stApp { 
            background-color: #FFFFFF !important; 
            background: #FFFFFF !important;
        }
        
        /* ============================================ */
        /* HEADER PRETO COM DETALHE LARANJA - PRESERVADO */
        /* ============================================ */
        .fc-header {
            background: #111827 !important;
            background-color: #111827 !important;
            padding: 20px 26px !important;
            border-radius: 12px !important;
            margin-bottom: 24px !important;
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            flex-wrap: wrap !important;
            gap: 16px !important;
            border-left: 6px solid #FF6B00 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        }
        .fc-header h1 { 
            color: #FFFFFF !important; 
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 23px !important; 
            font-weight: 800 !important;
            letter-spacing: 0.3px !important;
            margin: 0 !important;
        }
        .fc-header p { 
            color: #D1D5DB !important; 
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 12.5px !important; 
            margin: 6px 0 0 0 !important;
            font-weight: 400 !important;
        }
        
        /* ============================================ */
        /* RELÓGIO - AGORA BRANCO + ARIAL + LEGÍVEL */
        /* ============================================ */
        .fc-clock, .fc-clock * {
            color: #FFFFFF !important;
            background-color: #1F2937 !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            letter-spacing: 0.5px !important;
            line-height: 1.5 !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .fc-clock {
            padding: 12px 20px !important;
            border-radius: 10px !important;
            border: 1px solid #374151 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
        }
        
        /* ============================================ */
        /* METRICS - CARDS BRANCOS COM BORDA */
        /* ============================================ */
        [data-testid="stMetric"] {
            background: #F9FAFB !important;
            background-color: #F9FAFB !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 10px !important;
            padding: 14px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        }
        [data-testid="stMetricLabel"] {
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 13px !important;
            color: #6B7280 !important;
        }
        [data-testid="stMetricValue"] {
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 22px !important;
            font-weight: 700 !important;
            color: #111827 !important;
        }
        
        /* ============================================ */
        /* TABS - LARANJA QUANDO ATIVA */
        /* ============================================ */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background-color: #F9FAFB !important;
            padding: 6px !important;
            border-radius: 10px !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            color: #6B7280 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FF6B00 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }
        
        /* ============================================ */
        /* BOTÕES - LARANJA FC */
        /* ============================================ */
        .stButton > button[kind="primary"] {
            background-color: #FF6B00 !important;
            color: white !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 20px !important;
        }
        .stButton > button {
            font-family: Arial, Helvetica, sans-serif !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        
        /* ============================================ */
        /* SIDEBAR - BRANCO LIMPO */
        /* ============================================ */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E5E7EB !important;
        }
        [data-testid="stSidebar"] * {
            font-family: Arial, Helvetica, sans-serif !important;
        }
        
        /* ============================================ */
        /* INPUTS E SELECTS */
        /* ============================================ */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            font-family: Arial, Helvetica, sans-serif !important;
            border-radius: 8px !important;
            border: 1px solid #D1D5DB !important;
        }
        
        /* ============================================ */
        /* DATAFRAMES */
        /* ============================================ */
        [data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB !important;
            border-radius: 10px !important;
        }
        
        /* ============================================ */
        /* PROGRESS BAR LARANJA */
        /* ============================================ */
        .stProgress > div > div > div > div {
            background-color: #FF6B00 !important;
        }
        
        /* ============================================ */
        /* UPLOADER */
        /* ============================================ */
        [data-testid="stFileUploader"] {
            border: 1px dashed #D1D5DB !important;
            border-radius: 10px !important;
            background: #F9FAFB !important;
        }
        
        /* FOOTER */
        .fc-footer {
            text-align: center !important;
            color: #9CA3AF !important;
            font-family: Arial, Helvetica, sans-serif !important;
            font-size: 11px !important;
            margin-top: 50px !important;
            padding-top: 20px !important;
            border-top: 1px solid #E5E7EB !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ===================================================================
# 2. HEADER COM LOGO + RELÓGIO BRANCO ARIAL - ATUALIZADO
# ===================================================================
def mostrar_header_com_logo():
    fuso_bahia = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso_bahia)
    
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    meses = ['', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    dia_semana = dias[agora.weekday()]
    data_str = f"{dia_semana}, {agora.day} de {meses[agora.month]} de {agora.year}"
    hora_str = agora.strftime("%H:%M:%S")
    
    # Logo opcional - tenta carregar se existir
    logo_html = ""
    try:
        # Se tiver logo.png na pasta, mostra
        logo = Image.open("logo.png")
        buffered = io.BytesIO()
        logo.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        logo_html = f'<img src="data:image/png;base64,{img_str}" style="height:38px; margin-right:12px; border-radius:6px;">'
    except:
        logo_html = "🏗️"
    
    st.markdown(f"""
    <div class="fc-header">
        <div style="display:flex; align-items:center;">
            <div style="font-size:32px; margin-right:12px;">{logo_html}</div>
            <div>
                <h1 style="font-family: Arial, Helvetica, sans-serif !important; color: #FFFFFF !important;">FC CONSTRÓI • GROWTH AI v3.1.5</h1>
                <p style="font-family: Arial, Helvetica, sans-serif !important; color: #D1D5DB !important;">Construção • Porcelanato • Inteligência de Vendas • Irará/BA</p>
            </div>
        </div>
        <div class="fc-clock" style="font-family: Arial, Helvetica, sans-serif !important; color: #FFFFFF !important; background: #1F2937 !important;">
            <span style="color: #FFFFFF !important; font-family: Arial, Helvetica, sans-serif !important; font-size:14px;">
                📅 {data_str} &nbsp;•&nbsp; ⏰ {hora_str}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# 3. FUNÇÕES EXTRAS PRESERVADAS - NÃO REMOVIDAS
# ===================================================================
def mostrar_footer():
    fuso = pytz.timezone('America/Bahia')
    agora = datetime.now(fuso)
    st.markdown(f"""
    <div class="fc-footer">
        FC CONSTRÓI © {agora.year} • {agora.strftime('%d/%m/%Y %H:%M:%S')} - Irará/BA<br>
        GROWTH AI v3.1.5 • Arial Legível • Branco Cinza Claro • Cores Anteriores Preservadas
    </div>
    """, unsafe_allow_html=True)

def criar_card_metrica(titulo, valor, delta=None):
    """Card de métrica preservado"""
    if delta:
        st.metric(titulo, valor, delta)
    else:
        st.metric(titulo, valor)

def aplicar_estilo_tabela():
    """Estilo extra para tabelas - preservado"""
    st.markdown("""
    <style>
        table { font-family: Arial, Helvetica, sans-serif !important; }
        th { background: #F9FAFB !important; color: #111827 !important; font-weight:700 !important; }
        td { font-family: Arial, Helvetica, sans-serif !important; }
    </style>
    """, unsafe_allow_html=True)

def mostrar_alerta_sucesso(msg):
    st.success(f"✅ {msg}")

def mostrar_alerta_erro(msg):
    st.error(f"❌ {msg}")

def mostrar_alerta_aviso(msg):
    st.warning(f"⚠️ {msg}")

# ===================================================================
# 4. CONFIGURAÇÃO DE CORES PADRÃO FC - PRESERVADAS
# ===================================================================
CORES_FC = {
    "laranja_principal": "#FF6B00",
    "preto_header": "#111827",
    "cinza_escuro": "#1F2937",
    "cinza_borda": "#374151",
    "branco": "#FFFFFF",
    "cinza_claro": "#F9FAFB",
    "cinza_texto": "#6B7280",
    "cinza_claro_texto": "#D1D5DB",
    "branco_puro": "#F9FAFB",
    "verde_sucesso": "#10B981",
    "vermelho_erro": "#EF4444",
    "azul_info": "#3B82F6"
}

def get_cores():
    return CORES_FC


