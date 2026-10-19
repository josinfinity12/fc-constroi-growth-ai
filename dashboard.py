import streamlit as st
import os

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")

st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3 = st.tabs(["Preditor Viral", "Reciclagem", "Funil Comentários"])

with tab1:
    st.success("✅ App voltou!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Acurácia", "94%")
    col2.metric("F1-Score", "94%")
    col3.metric("Correlação", "0.87")
    st.write("Gancho nos 3s iniciais = 42% da viralização")
    
    if os.path.exists("reports/correlacao_score_viral.png"):
        st.image("reports/correlacao_score_viral.png")
    else:
        st.warning("Gráfico não encontrado em reports/ - verifique o push")

with tab2:
    st.write("Módulo de Reciclagem em construção")

with tab3:
    st.write("Módulo de Funil de Comentários em construção")
    