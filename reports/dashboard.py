import streamlit as st
import pandas as pd

st.set_page_config(page_title="FC Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclagem", "💬 Funil Comentários"])

with tab1:
    df = pd.read_csv('data/reels_historico.csv')
    st.dataframe(df)
    taxa_viral = df['viralizou_11k'].mean() * 100
    st.metric("Taxa Viral Atual", f"{taxa_viral:.1f}%", "Meta: 25%")
    st.warning("Hoje: 1 a cada 15 viraliza (6.6%). Com preditor vamos pra 1 a cada 4.")

with tab2:
    st.metric("IG", "270k", "Estagnado")
    st.metric("YT", "18.3k", "-70% perdido")
    st.info("Rotina: Todo Reel postado no IG -> automaticamente vira Short + Título Longo. 1 gravação = 3 posts.")

with tab3:
    df_com = pd.read_csv('data/comentarios_funnel.csv')
    st.dataframe(df_com)
    st.success(f"{len(df_com)} comentários viraram leads hoje. Sem responder manual.")
    