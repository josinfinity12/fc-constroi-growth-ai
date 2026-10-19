import streamlit as st
import os, json, random, sys
sys.path.append('scripts')
from thumbnail_generator import gerar_todos_modelos
from youtube_pack import gerar_pack_youtube
from remarketing_filter import filtrar_remarketing_30d
try:
    from metrics_paid_organic import calcular_metricas_pagas, calcular_metricas_organicas, gerar_recomendacao
except:
    from scripts.metrics_paid_organic import calcular_metricas_pagas, calcular_metricas_organicas, gerar_recomendacao
import pandas as pd
st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3, tab4, tab5, tab7, tab8 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclar Conteúdo", "📊 Dashboard", "🎨 Thumbnails", "📦 YouTube Pack", "🎯 Remarketing 30d", "💰 CAC CPA ROAS"])

with tab1:
    st.header("Preditor Viral")
    st.write("Seu preditor original")

with tab2:
    st.header("Reciclar Conteúdo")
    st.write("Reciclagem")

with tab3:
    st.header("Dashboard")
    st.write("Dashboard geral")

with tab4:
    st.header("Thumbnail 1080x1920")
    gancho4 = st.text_input("Gancho", key="g4")
    if st.button("Gerar 3 Modelos", key="btn_thumb"):
        if gancho4:
            arquivos = gerar_todos_modelos(gancho4, "R$99,90", "R$49,90")
            for arq in arquivos:
                st.image(arq)

with tab5:
    st.header("YouTube Pack - 2 Negócios")
    tipo_negocio = st.selectbox("Tipo:", ["AUTO (detecta sozinho)", "SERVICO_LOCAL", "CURSO_ONLINE"], key="tipo_final")
    cidade_servico = st.selectbox("Cidade serviço:", ["", "Irará", "Santanópolis", "Feira de Santana", "Água Fria", "Ouriçanga", "Santa Bárbara", "Serrinha"], key="cidade_final")
    gancho5 = st.text_input("Gancho", key="g5")
    score5 = st.slider("Score 0-10", 0.0, 10.0, 9.0, key="s5")
    if st.button("Gerar Pack", key="btn_yt2"):
        if gancho5:
            tipo_map = {"AUTO (detecta sozinho)": "AUTO", "SERVICO_LOCAL": "SERVICO_LOCAL", "CURSO_ONLINE": "CURSO_ONLINE"}
            pack = gerar_pack_youtube(gancho5, score5, "R$99,90", "R$49,90", cidade_servico, tipo_map[tipo_negocio])
            if pack["tipo"] == "CURIOSO":
                st.error(f"🚫 CURIOSO: {pack['titulo']}")
            else:
                st.success(f"{pack['tipo']} | {pack['recomendacao']}")
                st.code(pack["titulo"])
                st.text_area("Descricao", pack["descricao"], height=300, key="desc5")

with tab7:
    st.header("Remarketing 30d - R$49,90")
    kiwify_file = st.file_uploader("CSV Kiwify", type="csv", key="kiwify7")
    manychat_file = st.file_uploader("CSV ManyChat", type="csv", key="manychat7")
    if st.button("Filtrar R$49,90", key="btn_rem7"):
        resultado = filtrar_remarketing_30d()
        st.dataframe(resultado)

with with tab8:
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
        st.success("Calculando... (liga com metrics_paid_organic.py)")
        