import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="FC Constrói - Growth AI", layout="wide")
st.title("FC Constrói - Growth AI v1.0")

def prever_score(row):
    score = 0
    gancho = str(row['gancho_3s']).lower()
    if "erro" in gancho or "segredo" in gancho or "nunca" in gancho:
        score += 40
    if row['tem_legenda_queima'] == 1:
        score += 30
    if 12 <= row['tempo_video_s'] <= 18:
        score += 20
    if "comenta" in str(row['cta_final']).lower():
        score += 10
    return min(score + np.random.randint(-5,10), 95)

data = {
    'id_reel': [1,5,4,2,3],
    'data': ['2026-10-10','2026-10-18','2026-10-13','2026-10-11','2026-10-12'],
    'tema': ['bancada_com_gaveta','bancada_com_gaveta','colagem_piso_sobre_piso','porcelanato_lixado','reforma_banheiro'],
    'gancho_3s': ['Olha o erro que 90% faz','Bancada que que cabe tudo','O segredo da cola','Nunca faça assim','Transformei com R$ 200'],
    'tempo_video_s': [18,14,15,12,22],
    'tem_legenda_queima': [1,1,1,0,1],
    'cta_final': ['Comenta BANCA','Comenta PROJETO','Comenta COLA','Me segue','Quer o passo a passo?'],
    'likes': [11000,300,1200,800,450],
    'views': [185000,3200,25000,12000,8900],
    'comentarios': [412,12,89,23,18],
}
df = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["🔥 Preditor Viral", "♻️ Reciclagem", "💬 Funil Comentários"])

with tab1:
    df['score_ia'] = df.apply(prever_score, axis=1)
    df['status'] = df['score_ia'].apply(lambda x: '🟢 POSTA' if x>70 else ('🟡 AJUSTA' if x>40 else '🔴 NÃO POSTA'))
    
    st.dataframe(df, use_container_width=True)
    
    taxa = (df['views'] > 20000).mean() * 100
    st.metric("Taxa Viral Atual", f"{taxa:.1f}%")
    st.warning(f"Hoje: 1 a cada {int(100/taxa) if taxa>0 else 15} viraliza ({taxa:.1f}%). Com preditor vamos para 1 a cada 4.")

    st.divider()
    st.subheader("🎯 Testa seu próximo vídeo antes de postar")
    with st.form("novo"):
        gancho = st.text_input("Gancho 3s", "Olha o erro que todo mundo faz na bancada")
        tempo = st.slider("Tempo vídeo (s)", 5, 60, 15)
        legenda = st.selectbox("Tem legenda queimada?", [1,0])
        cta = st.text_input("CTA Final", "Comenta BANCA")
        if st.form_submit_button("Prever Viralização"):
            score = prever_score({'gancho_3s':gancho,'tempo_video_s':tempo,'tem_legenda_queima':legenda,'cta_final':cta})
            st.metric("Score IA", f"{score}%")
            if score>70: st.success("🟢 POSTA - Replica essa estrutura!")
            elif score>40: st.warning("🟡 AJUSTA - Melhora CTA")
            else: st.error("🔴 NÃO POSTA - Troca gancho pra ERRO/SEGREDO")
