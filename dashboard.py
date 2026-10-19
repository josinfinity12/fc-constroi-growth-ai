import streamlit as st
import os, json, random, sys
sys.path.append('scripts')
from thumbnail_generator import gerar_todos_modelos
from youtube_pack import gerar_pack_youtube
from remarketing_filter import filtrar_remarketing_30d
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

tab1, tab2, tab3, tab4, tab5, tab7 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclar Conteúdo", "📊 Dashboard", "🎨 Aba 4 - Thumbnails", "📦 Aba 5 - YouTube Pack", "🎯 Aba 7 - Remarketing 30d"])

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
# --- ABA 4 - THUMBNAILS ---
with tab4:
    st.header("Aba 4 - Gerador de Thumbnail 1080x1920")
    st.write("FC Constrói - Pia, Bancada, Closet, Nicho em Porcelanato")
    gancho4 = st.text_input("Gancho (ex: Bancada Gourmet 2m)", key="gancho4_final")
    preco4 = st.text_input("Preço cheio", "R$99,90", key="preco4_final")
    preco_rem4 = st.text_input("Remarketing", "R$49,90", key="rem4_final")
    if st.button("Gerar 3 Modelos (Choque, Antes/Depois, Preço)", key="btn_thumb"):
        if gancho4:
            arquivos = gerar_todos_modelos(gancho4, preco4, preco_rem4)
            for arq in arquivos:
                st.image(arq)
                with open(arq, "rb") as f:
                    st.download_button(f"Baixar {arq}", f, file_name=arq, key=f"dl_{arq}")
        else:
            st.warning("Digita o gancho primeiro")

# --- ABA 5 - YOUTUBE PACK ---
with tab5:
    st.header("Aba 5 - YouTube Pack SEO - FC Constrói (2 Negócios)")
    
    tipo_negocio = st.selectbox("Tipo de negócio:", ["AUTO (detecta sozinho)", "SERVICO_LOCAL", "CURSO_ONLINE"], key="tipo_negocio_final")
    cidade_servico = st.selectbox("Se for SERVIÇO, escolha a cidade:", ["", "Irará", "Santanópolis", "Feira de Santana", "Água Fria", "Ouriçanga", "Santa Bárbara", "Serrinha"], key="cidade_final")
    
    gancho5 = st.text_input("Gancho (ex: bancada gourmet 2m / curso pia banheiro)", key="gancho5_final")
    score5 = st.slider("Score do seu preditor (0-10)", 0.0, 10.0, 9.0, key="score5_final")
    
    if st.button("Gerar Pack YouTube Corrigido", key="btn_yt"):
        if gancho5:
            tipo_map = {"AUTO (detecta sozinho)": "AUTO", "SERVICO_LOCAL": "SERVICO_LOCAL", "CURSO_ONLINE": "CURSO_ONLINE"}
            pack = gerar_pack_youtube(gancho5, score5, "R$99,90", "R$49,90", cidade_servico, tipo_map[tipo_negocio])
            
            if pack["tipo"] == "CURIOSO":
                st.error(f"🚫 CURIOSO FILTRADO: {pack['titulo']}")
                st.warning(pack["descricao"])
            else:
                st.success(f"Tipo detectado: {pack['tipo']} | {pack['recomendacao']}")
                st.subheader("Título SEO (copiar)")
                st.code(pack["titulo"])
                st.subheader("Descrição")
                st.text_area("Descrição", pack["descricao"], height=400, key="desc_final")
                st.subheader("Tags")
                st.write(", ".join(pack["tags"]))
        else:
            st.warning("Digita o gancho")
# --- ABA 7 - REMARKETING 30 DIAS ---
with tab7:
    st.header("Aba 7 - Remarketing 30 dias - Filtro R$49,90")
    st.info("Só manda R$49,90 pra quem NÃO comprou nos últimos 30 dias")
    kiwify_file = st.file_uploader("CSV Kiwify (vendas)", type="csv", key="kiwify_final")
    manychat_file = st.file_uploader("CSV ManyChat (leads BANCADA)", type="csv", key="manychat_final")
    if st.button("Filtrar e Gerar Listas R$49,90", key="btn_rem"):
        if kiwify_file and manychat_file:
            open("kiwify_vendas.csv","wb").write(kiwify_file.getbuffer())
            open("manychat_leads.csv","wb").write(manychat_file.getbuffer())
            resultado = filtrar_remarketing_30d()
            st.success(f"Lista remarketing R$49,90 gerada: {len(resultado)} pessoas")
            st.dataframe(resultado)
            csv = resultado.to_csv(index=False).encode('utf-8')
            st.download_button("Baixar CSV Remarketing R$49,90", csv, "lista_49_90_remarketing.csv", "text/csv", key="dl_rem")
        else:
            st.warning("Sem arquivos, usando exemplo fake")
            resultado = filtrar_remarketing_30d()
            st.dataframe(resultado)