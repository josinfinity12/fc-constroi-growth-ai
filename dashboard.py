import streamlit as st
import os, json, random, sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from thumbnail_generator import gerar_todos_modelos
from youtube_pack import gerar_pack_youtube
from remarketing_filter import filtrar_remarketing_30d

try:
    from metrics_paid_organic import calcular_metricas_pagas, calcular_metricas_organicas, gerar_recomendacao
except ImportError:
    from scripts.metrics_paid_organic import calcular_metricas_pagas, calcular_metricas_organicas, gerar_recomendacao

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3, tab4, tab5, tab7, tab8 = st.tabs([
    "🔥 Preditor Viral", 
    "♻️ Reciclar Conteúdo", 
    "📊 Dashboard", 
    "🎨 Thumbnails", 
    "📦 YouTube Pack", 
    "🎯 Remarketing 30d", 
    "💰 CAC CPA ROAS"
])

with tab1:
    st.header("Preditor Viral")

with tab2:
    st.header("Reciclagem de Conteúdo")

with tab3:
    st.header("Dashboard Geral")

with tab4:
    st.header("Thumbnails 1080x1920")
    if st.button("Gerar Thumbnails"):
        gerar_todos_modelos()
        st.success("Thumbnails geradas!")

with tab5:
    st.header("YouTube Pack - 2 Negócios")
    if st.button("Gerar YouTube Pack"):
        gerar_pack_youtube()
        st.success("Pack gerado!")

with tab7:
    st.header("Remarketing 30d - Conversão")
    st.caption("Filtro de curiosos por cidade e interesse")

with tab8:
    st.header("Métricas ROAS - Onde Investir R$300")
    st.caption("Meta vs Google vs Orgânico - Onde tá o lucro do FC Constrói")

    c1, c2 = st.columns(2)
    with c1:
        meta_file = st.file_uploader("Meta ADS CSV (custo,cliques,conversoes)", type="csv", key="meta")
    with c2:
        google_file = st.file_uploader("Google ADS CSV", type="csv", key="google")

    kiwify_file = st.file_uploader("Kiwify CSV (data_compra,valor,origem,email)", type="csv", key="kiwify")
    org_file = st.file_uploader("Orgânico CSV (views,comentarios,coment_bancada)", type="csv", key="org")

    if st.button("Calcular CAC CPA ROAS e Gerar Relatório"):
        st.success("Calculando...")
        