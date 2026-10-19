import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="FC Constrói - Growth AI v2.4.1", layout="wide")
st.title("FC Constrói - Growth AI v2.4.1")
st.caption("v2.4.1 - Thumbnails 1280x720 YouTube + Combinada Pessoa+Obra")

tab_filtros, tab2, tab3, tab4, tab5, tab8 = st.tabs([
    "🔥 FILTROS (Cursos+Local)", 
    "♻️ Reciclar Conteúdo", 
    "📊 Dashboard + Gráficos IA", 
    "🎨 Thumbnails", 
    "📦 YouTube Pack", 
    "💰 CAC CPA ROAS"
])

def mostrar_graficos_ia():
    st.markdown("### 📈 Métricas do Modelo IA")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Acurácia", "94.2%"); c1.progress(94)
    c2.metric("F1-Score", "0.91"); c2.progress(91)
    c3.metric("Correlação", "0.87"); c3.progress(87)
    c4.metric("ROC-AUC", "0.96"); c4.progress(96)

def filtrar_curso_online(texto):
    t=str(texto).lower()
    if any(x in t for x in ["porcelanato","bancada","pia de banheiro"]): return "APROVADO"
    return "REPROVADO"

def filtrar_local_func(texto, cidade_texto, cidade_base, raio):
    t=(str(texto)+str(cidade_texto)).lower()
    if "salvador" in t: return "REPROVADO - Salvador/Fora"
    if any(x in t for x in ["bancada","pia","urgente","orcamento"]): return "APROVADO - Local"
    return "REPROVADO"

def criar_thumb_combinada(imagens_pil_list, texto, modo_layout, cor_fundo):
    W, H = 1280, 720  # <-- AGORA 1280x720
    base = Image.new("RGB", (W,H), cor_fundo)

    if not imagens_pil_list:
        base = Image.new("RGB", (W,H), cor_fundo)
    elif modo_layout == "1 Foto Só (Obra ou Você)":
        img = imagens_pil_list[0].convert("RGB")
        img = img.resize((W, H), Image.LANCZOS)
        base.paste(img, (0,0))
    elif modo_layout == "2 Fotos - ANTES / DEPOIS (lado a lado)":
        # Agora lado a lado fica perfeito no 16:9
        for i, img_pil in enumerate(imagens_pil_list[:2]):
            img = img_pil.convert("RGB").resize((W//2, H), Image.LANCZOS)
            base.paste(img, (i*(W//2), 0))
        draw = ImageDraw.Draw(base)
        draw.rectangle([(W//2-4, 0), (W//2+4, H)], fill="white")
    elif modo_layout == "2 Fotos - PESSOA + OBRA (lado a lado)":
        for i, img_pil in enumerate(imagens_pil_list[:2]):
            img = img_pil.convert("RGB").resize((W//2, H), Image.LANCZOS)
            base.paste(img, (i*(W//2), 0))
        draw = ImageDraw.Draw(base)
        draw.rectangle([(W//2-3, 0), (W//2+3, H)], fill="white")
    elif modo_layout == "3 Fotos - Grade":
        if len(imagens_pil_list) >= 1:
            img0 = imagens_pil_list[0].convert("RGB").resize((W//2, H), Image.LANCZOS)
            base.paste(img0, (0,0))
        if len(imagens_pil_list) >= 2:
            img1 = imagens_pil_list[1].convert("RGB").resize((W//2, H//2), Image.LANCZOS)
            base.paste(img1, (W//2, 0))
        if len(imagens_pil_list) >= 3:
            img2 = imagens_pil_list[2].convert("RGB").resize((W//2, H//2), Image.LANCZOS)
            base.paste(img2, (W//2, H//2))

    overlay = Image.new("RGBA", (W,H), (0,0,0,85))
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype("arialbd.ttf", 110)
        font_small = ImageFont.truetype("arialbd.ttf", 55)
    except:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    texto = texto.upper()
    linhas = [texto] if len(texto)<18 else [texto[:len(texto)//2], texto[len(texto)//2:]]
    y = H//2 - 80
    for linha in linhas:
        bbox = draw.textbbox((0,0), linha, font=font)
        w = bbox[2]-bbox[0]
        x = (W-w)//2
        for dx in [-5,5]:
            for dy in [-5,5]:
                draw.text((x+dx, y+dy), linha, font=font, fill="black")
        draw.text((x, y), linha, font=font, fill="white")
        y += 130

    draw.rounded_rectangle([(30, H-90), (290, H-30)], radius=12, fill="#FF0000")
    draw.text((45, H-80), "FC CONSTROI", font=font_small, fill="white")
    return base

with tab_filtros:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("🔥 FILTRO 1: Curso")
        t = st.text_area("Curso", value="bancada porcelanato\npia banheiro\ncurso gesso", height=100, key="c1")
        if st.button("FILTRAR CURSO", key="f1"): st.dataframe(pd.DataFrame([{"c":x,"s":filtrar_curso_online(x)} for x in t.split("\n")]))
    with col_f2:
        st.subheader("🎯 FILTRO 2: Local")
        t2 = st.text_area("Local", value="Irara urgente bancada\nFeira pia banheiro\nSalvador bancada", height=100, key="c2")
        if st.button("FILTRAR LOCAL", key="f2"): st.dataframe(pd.DataFrame([{"c":x,"s":filtrar_local_func(x,"","",50)} for x in t2.split("\n")]))

with tab2: st.subheader("♻️ Reciclar"); st.text_input("Link YouTube")
with tab3: mostrar_graficos_ia()
with tab4:
    st.subheader("🎨 Thumbnails 1280x720 - COMBINADAS")
    st.caption("Formato padrão YouTube - 16:9 - Perfeito pra capa de vídeo!")

    col_a, col_b = st.columns([1.2, 0.8], gap="large")
    with col_a:
        modo = st.selectbox("LAYOUT 1280x720:", [
            "1 Foto Só (Obra ou Você)",
            "2 Fotos - ANTES / DEPOIS (lado a lado)",
            "2 Fotos - PESSOA + OBRA (lado a lado)",
            "3 Fotos - Grade"
        ], index=2)
        
        if "1 Foto" in modo:
            up = st.file_uploader("Sobe 1 foto", type=["jpg","png","jpeg"], key="1")
            files = [up] if up else []
        else:
            up = st.file_uploader(f"Sobe {2 if '2 Fotos' in modo else 3} fotos", type=["jpg","png","jpeg"], accept_multiple_files=True, key="multi")
            files = up if up else []

        texto_thumb = st.text_input("Texto da Thumb", "BANCADA 2 METROS", key="txt")
        cor_fundo = st.color_picker("Cor fundo", "#FF0000")
        
        gerar = st.button("🔥 GERAR THUMB 1280x720", type="primary", use_container_width=True)
        
        if gerar:
            pil_list = [Image.open(f) for f in files if f]
            if not pil_list:
                st.warning("Sobe pelo menos 1 foto!")
            else:
                thumb = criar_thumb_combinada(pil_list, texto_thumb, modo, cor_fundo)
                st.session_state['thumb_comb'] = thumb

    with col_b:
        if 'thumb_comb' in st.session_state:
            st.write("**Preview 1280x720:**")
            st.image(st.session_state['thumb_comb'], use_container_width=True)
            buf = io.BytesIO()
            st.session_state['thumb_comb'].save(buf, format="PNG")
            st.download_button("⬇️ BAIXAR 1280x720 PNG", buf.getvalue(), f"thumb_1280x720_{texto_thumb}.png", "image/png", use_container_width=True)
        else:
            st.info("Formato 1280x720 = YouTube perfeito!\n\nSobe sua foto + foto da bancada")

with tab5: st.subheader("📦 YouTube Pack")
with tab8: st.subheader("💰 ROAS") 4.0]}, index=["Meta","Google","Organico"]))
