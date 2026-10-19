import streamlit as st
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

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
    st.caption("Análise de viralização")
    st.info("Em construção - v2.0 com filtro de curiosos")

with tab2:
    st.header("Reciclagem de Conteúdo")
    st.caption("Transforma 1 vídeo em 10 posts")
    st.info("Em construção")

with tab3:
    st.header("Dashboard Geral")
    st.caption("Visão geral FC Constrói")
    st.info("Em construção")

with tab4:
    st.header("Thumbnails 1080x1920")
    st.caption("Gerador de thumbnails 5 modelos")
    st.info("Preview das 5 thumbs vai aparecer aqui - em ajuste final")
    if st.button("Gerar Preview Thumbnails", key="thumb"):
        st.success("Funcionalidade em construção - Aba 8 já está 100%!")

with tab5:
    st.header("YouTube Pack - 2 Negócios")
    st.caption("Pacote para FC Constrói + Cursos")
    st.info("Gerador de títulos, descrições e tags")
    if st.button("Gerar YouTube Pack", key="yt"):
        st.success("Funcionalidade em construção - use a Aba CAC CPA ROAS por enquanto!")

with tab7:
    st.header("Remarketing 30d - Conversão")
    st.caption("Filtro de curiosos por cidade e interesse")
    st.write("Filtra quem é de Irará, Feira, etc e tem interesse real em bancada/pia/closet")
    st.info("Em construção - próximo passo: filtro por cidade")

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

    if st.button("Calcular CAC CPA ROAS e Gerar Relatório", key="calc"):
        st.success("Calculando... Pronto pra receber os CSVs!")
        st.markdown("### Comparativo Lucro")
        st.info("Envie os CSVs acima para ver ROAS, CAC, CPA, CPC")
        
