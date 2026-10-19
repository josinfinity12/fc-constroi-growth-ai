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
    st.header("Aba 4 - Thumbnail 1080x1920")
    gancho4 = st.text_input("Gancho", key="g4")
    if st.button("Gerar 3 Modelos", key="btn_thumb"):
        if gancho4:
            arquivos = gerar_todos_modelos(gancho4, "R$99,90", "R$49,90")
            for arq in arquivos:
                st.image(arq)

with tab5:
    st.header("Aba 5 - YouTube Pack - 2 Negócios")
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
    st.header("Aba 7 - Remarketing 30d - R$49,90")
    kiwify_file = st.file_uploader("CSV Kiwify", type="csv", key="kiwify7")
    manychat_file = st.file_uploader("CSV ManyChat", type="csv", key="manychat7")
    if st.button("Filtrar R$49,90", key="btn_rem7"):
        resultado = filtrar_remarketing_30d()
        st.dataframe(resultado)

with tab8:
    st.header("Aba 8 - CAC, CPA, CPC, ROAS - Onde investir")
    st.write("Meta vs Google vs Orgânico - Onde tá o lucro")
    c1, c2 = st.columns(2)
    with c1:
        meta_file = st.file_uploader("Meta ADS CSV (custo,cliques,conversoes)", type="csv", key="meta8")
    with c2:
        google_file = st.file_uploader("Google ADS CSV", type="csv", key="google8")
    kiwify_file = st.file_uploader("Kiwify CSV (data_compra,valor,origem,email)", type="csv", key="kiwify8")
    organico_file = st.file_uploader("Orgânico CSV (views,comentarios,coment_bancada)", type="csv", key="org8")
    if st.button("Calcular CAC CPA ROAS e Gerar Relatório", key="btn_metrics8"):
        if not kiwify_file:
            df_kiwify = pd.DataFrame({
                'data_compra': ['2026-10-15','2026-10-16','2026-10-17','2026-10-17','2026-10-18'],
                'valor': [99.90, 49.90, 99.90, 99.90, 49.90],
                'origem': ['meta','meta','google','organico','organico'],
                'email': ['a@a.com','b@b.com','c@c.com','d@d.com','e@e.com']
            })
        else:
            df_kiwify = pd.read_csv(kiwify_file)
        if not meta_file:
            df_meta = pd.DataFrame({'custo': [200, 150], 'cliques': [500, 300], 'conversoes': [2, 1]})
        else:
            df_meta = pd.read_csv(meta_file)
        if not google_file:
            df_google = pd.DataFrame({'custo': [180], 'cliques': [200], 'conversoes': [1]})
        else:
            df_google = pd.read_csv(google_file)
        if not organico_file:
            df_org = pd.DataFrame({'views': [5000, 3000], 'comentarios': [100, 80], 'coment_bancada': [40, 30]})
        else:
            df_org = pd.read_csv(organico_file)
        meta_metrics = calcular_metricas_pagas(df_meta, df_kiwify, "meta")
        google_metrics = calcular_metricas_pagas(df_google, df_kiwify, "google")
        df_kiwify_org = df_kiwify[df_kiwify['origem'] == 'organico'] if 'origem' in df_kiwify.columns else pd.DataFrame()
        org_metrics = calcular_metricas_organicas(df_org, df_kiwify_org)
        df_comp = pd.DataFrame([meta_metrics, google_metrics, org_metrics])
        st.subheader("📊 Comparativo Lucro")
        st.dataframe(df_comp, width='stretch')
        st.subheader("📈 ROAS por Canal")
        st.bar_chart(df_comp.set_index('plataforma')['ROAS'])
        st.subheader("💡 Onde investir")
        rec = gerar_recomendacao(df_comp)
        st.text_area("Relatório", rec, height=300, key="rec8")
        csv = df_comp.to_csv(index=False).encode('utf-8')
        st.download_button("Baixar Relatório", csv, "relatorio_cac_roas.csv", "text/csv", key="dl8")