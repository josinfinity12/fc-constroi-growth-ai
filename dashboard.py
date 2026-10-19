import streamlit as st
import os, json

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

# Abas
tab1, tab2, tab3 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclagem", "💬 Funil Comentários"])

with tab1:
    st.subheader("Preditor de Viralização")
    st.write("Modelo com **94% de acurácia** | Correlação Score x Viral: **0.87**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Acurácia", "94%")
    c2.metric("F1-Score", "94%")
    c3.metric("ROC AUC", "96%")
    
    # Imagem segura
    img_path = "reports/correlacao_score_viral.png"
    if os.path.exists(img_path):
        st.image(img_path)
    else:
        st.info("📊 Gráfico em reports/correlacao_score_viral.png - faça push para aparecer")
    
    st.markdown("---")
    st.write("**Como funciona:** Gancho nos 3s iniciais responde por 42% da viralização.")

with tab2:
    st.subheader("Reciclagem de Conteúdo")
    st.write("Em breve: gerador automático de variações de legenda + CTA")

with tab3:
    st.subheader("Funil de Comentários")
    st.write("Em breve: classificação de comentários por intenção de compra")

st.caption("FC Constrói | JosInfinity12 | Growth + Data Science + MLOps")
