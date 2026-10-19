# designer.py - DESIGN SYSTEM FC CONSTRÓI - v3.0.1
import streamlit as st
import os

FC_COLORS = {
    "orange": "#FF6B00",
    "orange_light": "#FF8C00",
    "black": "#111827",
    "black_light": "#1F2937",
    "gray": "#F3F4F6",
    "white": "#FFFFFF"
}

def aplicar_design():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;800&display=swap');
        .stApp {{ background-color: #FAFAFA; font-family: 'Inter', sans-serif; }}
        .fc-header {{
            background: linear-gradient(135deg, {FC_COLORS['black']} 0%, {FC_COLORS['black_light']} 100%);
            padding: 14px 24px; border-radius: 16px; display: flex; align-items: center; gap: 18px;
            margin-bottom: 20px; border-left: 6px solid {FC_COLORS['orange']};
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        .fc-header h1 {{ color: white !important; font-size: 26px !important; font-weight: 800 !important; margin: 0 !important; }}
        .fc-header span {{ color: {FC_COLORS['orange']} !important; font-size: 12px; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; }}
        [data-testid="stMetric"] {{
            background: white; padding: 16px; border-radius: 12px;
            border: 1px solid #E5E7EB; border-left: 4px solid {FC_COLORS['orange']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}
        [data-testid="stMetricLabel"] {{ color: #6B7280 !important; font-weight: 600 !important; text-transform: uppercase; font-size: 11px !important; letter-spacing: 1px; }}
        [data-testid="stMetricValue"] {{ color: {FC_COLORS['black']} !important; font-weight: 800 !important; }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {FC_COLORS['orange']} 0%, {FC_COLORS['orange_light']} 100%) !important;
            color: white !important; border: none !important; border-radius: 10px !important;
            font-weight: 700 !important; text-transform: uppercase; box-shadow: 0 4px 12px rgba(255,107,0,0.3);
        }}
        .stTabs [data-baseweb="tab-list"] {{ gap: 6px; background: #F3F4F6; padding: 6px; border-radius: 12px; }}
        .stTabs [data-baseweb="tab"] {{ border-radius: 8px !important; font-weight: 600 !important; color: #6B7280 !important; }}
        .stTabs [aria-selected="true"] {{ background: {FC_COLORS['black']} !important; color: white !important; }}
        .stDataFrame {{ border-radius: 12px; overflow: hidden; border: 1px solid #E5E7EB; }}
    </style>
    """, unsafe_allow_html=True)

def mostrar_header_com_logo():
    col_logo, col_title = st.columns([0.14, 0.86])
    with col_logo:
        logo_encontrado = False
        for path in ["logo.png", "assets/logo.png", "assets/logo_fc.png", "logo_fc.png"]:
            if os.path.exists(path):
                st.image(path, width=95)
                logo_encontrado = True
                break
        if not logo_encontrado:
            st.markdown(f"<div style='background:{FC_COLORS['black']}; width:75px; height:75px; border-radius:12px; display:flex; align-items:center; justify-content:center; border:2px solid {FC_COLORS['orange']};'><span style='color:{FC_COLORS['orange']}; font-weight:900; font-size:24px;'>FC</span></div>", unsafe_allow_html=True)
    with col_title:
        st.markdown("""
        <div class="fc-header">
            <div>
                <h1>FC CONSTRÓI • GROWTH AI v3.0.1</h1>
                <span>CONSTRUÇÃO • PORCELANATO • INTELIGÊNCIA DE VENDAS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        