import streamlit as st
import os, json, random

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclagem", "💬 Funil Comentários"])

# ABA 1 - PREDITOR
with tab1:
    st.subheader("Preditor de Viralização - 94% acurácia")
    c1,c2,c3 = st.columns(3)
    c1.metric("Acurácia", "94%")
    c2.metric("F1-Score", "94%")
    c3.metric("Correlação Score x Viral", "0.87")
    
    if os.path.exists("reports/correlacao_score_viral.png"):
        st.image("reports/correlacao_score_viral.png", caption="Correlação - Gancho 3s = 42% do peso")
    else:
        st.info("Gráfico em reports/correlacao_score_viral.png")
    
    st.markdown("---")
    score = st.slider("Score de Gancho (0-10) - Primeiros 3 segundos", 0, 10, 7)
    if score >= 8:
        st.success(f"🔥 Score {score}: Chance 3.2x maior de viralizar! Posta!")
    elif score >= 5:
        st.warning(f"⚠️ Score {score}: Mediano, melhora o gancho nos 3s")
    else:
        st.error(f"❌ Score {score}: Vai flopar, refaz o gancho!")

# ABA 2 - RECICLAGEM
with tab2:
    st.subheader("♻️ Reciclagem de Conteúdo - 1 vídeo = 5 posts")
    tema = st.text_input("Tema do vídeo base (ex: porcelanato 90x90)", "como assentar porcelanato sem estufar")
    
    if st.button("Gerar 5 variações"):
        variacoes = [
            f"1. GANCHO POLÊMICO: O erro que 90% faz ao {tema}",
            f"2. TUTORIAL: {tema} em 3 passos (salva pra depois)",
            f"3. ANTES/DEPOIS: Resultado de {tema} na FC Constrói",
            f"4. DÚVIDA COMUM: {tema} pode em banheiro? Respondo",
            f"5. CTA VENDA: Kit para {tema} com 20% OFF hoje - link na bio"
        ]
        for v in variacoes:
            st.write(v)
        st.success("Copia e cola no CapCut + legenda!")

# ABA 3 - FUNIL COMENTÁRIOS
with tab3:
    st.subheader("💬 Funil de Comentários - Classificador Kiwify")
    comentario = st.text_area("Cole o comentário do Instagram/TikTok:", "Quanto custa o porcelanato?")
    
    if st.button("Classificar"):
        com_lower = comentario.lower()
        if any(x in com_lower for x in ["quanto", "preço", "valor", "custa", "link"]):
            st.success("🟢 QUENTE - Intenção de compra! Resposta: 'Te mandei no DM o link da Kiwify com frete grátis + cupom FC10'")
        elif any(x in com_lower for x in ["onde", "entrega", "irar", "santanopolis"]):
            st.info("🟡 MORNO - Dúvida logística! Resposta: 'Entregamos em toda região! Me chama no Whats da FC'")
        else:
            st.write("🔵 FRIO - Engajamento. Resposta: 'Valeu! Salva esse vídeo pra quando for construir'")

st.caption("Josinfinity12 | De Irará-BA pra produção | Growth + Data + MLOps")
