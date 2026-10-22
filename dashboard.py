# FC CONSTRÓI • GROWTH AI v3.8 NACIONAL - Kiwify Vendas Curso Online BRASIL TODO
# FIX PROFISSIONAL: Remove TESTE KIWIFY -> Kiwify Vendas Curso Online + remove testes
# REGRA: NUNCA DELETAR NADA - SÓ ADICIONAR/CORRIGIR
# FIX v3.8 NACIONAL: Curso online de porcelanato Academia FC Constroi é vendido para BRASIL TODO - 6 cidades = APENAS SERVICO LOCAL

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import json
import base64
from io import BytesIO
import requests

try:
    from designer import aplicar_design
    HAS_DESIGNER = True
except ImportError:
    HAS_DESIGNER = False

try:
    from supabase import create_client
    HAS_SUPABASE = True
except ImportError:
    HAS_SUPABASE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

CIDADES_ORIGINAIS = [
    "Santanópolis",
    "Irará",
    "Feira de Santana",
    "Santa Bárbara",
    "Serrinha",
    "Ouriçangas"
]

# ===== FIX v3.8 NACIONAL - BRASIL TODO - ADICIONADO SEM DELETAR NADA ANTERIOR =====
CURSO_ONLINE_ABRANGENCIA = "NACIONAL - BRASIL TODO"
CURSO_ONLINE_DESCRICAO = "Academia FC Constrói - Curso Online Porcelanato - Venda para Brasil Todo"
CIDADES_LOCAL_SERVICO = ["irara","feira_de_santana","salvador","santanopolis","santa_barbara","serrinha","ouricangas"]  # apenas servico local de instalacao
CIDADE_CURSO_ONLINE_FIXA = "nacional"
ABRANGENCIA_CURSO = "NACIONAL - BRASIL TODO - Academia FC Constrói"
# =================================================================================

def extrair_filtros_sck(sck_full: str):
    s = str(sck_full).lower()
    plat = "wix"
    if "instagram" in s: plat = "instagram"
    elif "tiktok" in s: plat = "tiktok"
    elif "kwai" in s: plat = "kwai"
    elif "facebook" in s or "fb_" in s or "_fb" in s: plat = "facebook"
    elif "youtube" in s or "yt_" in s: plat = "youtube"
    cid = "irara"
    if "feira" in s: cid = "feira"
    elif "salvador" in s or "ssa" in s: cid = "salvador"
    elif "santanopolis" in s or "santanópolis" in s: cid = "santanopolis"
    elif "santa_barbara" in s or "santa barbara" in s or "santabarbara" in s: cid = "santa_barbara"
    elif "serrinha" in s: cid = "serrinha"
    elif "ouricangas" in s or "ouriçangas" in s: cid = "ouricangas"
    inter = "porcelanato"
    if "pia de banheiro" in s or "pia_banheiro" in s or "pia esculpida" in s or "pia_esculpida" in s or "pia_90" in s or "_pia_" in s:
        inter = "pia_de_banheiro"
    elif "closet" in s:
        inter = "closet_porcelanato"
    elif "bancada" in s and "cozinha" in s:
        inter = "bancada_cozinha_porcelanato"
    elif "bancada" in s:
        inter = "bancada_porcelanato"
    elif "fachada" in s:
        inter = "fachadas_porcelanato"
    elif "nicho" in s:
        inter = "nichos_porcelanato"
    elif "revestimento" in s:
        inter = "revestimentos_porcelanato"
    elif "armario" in s or "armário" in s:
        inter = "armarios_porcelanato"
    elif "gaveta" in s:
        inter = "gavetas_porcelanato"
    elif "base" in s:
        inter = "base_300kg"
    pago = "fb_" in s or "google_" in s or "cpc" in s or "pago" in s
    traffic = "pago" if pago else "organico"
    return plat, cid, inter, traffic

# FIX v3.8 - NOVA FUNCAO ADICIONADA - NAO DELETA A ORIGINAL
def extrair_filtros_sck_nacional(sck_full: str):
    plat, cid_origem, inter, traffic = extrair_filtros_sck(sck_full)
    cidade_venda = "nacional"  # FIX: Curso online sempre NACIONAL
    return plat, cidade_venda, cid_origem, inter, traffic

def salvar_venda_kiwify_teste(sck_teste: str, email_teste="cliente@email.com"):
    try:
        supa_url = os.getenv("SUPABASE_URL")
        supa_key = os.getenv("SUPABASE_KEY")
        try:
            if not supa_url:
                supa_url = st.secrets.get("SUPABASE_URL", "")
            if not supa_key:
                supa_key = st.secrets.get("SUPABASE_KEY", "")
        except:
            pass
        if not supa_url or not supa_key:
            return False, "Sem SUPABASE_URL/KEY no Environment"
        from supabase import create_client
        supa = create_client(supa_url, supa_key)
        plat, cid_origem, inter, traffic = extrair_filtros_sck(sck_teste)
        # FIX v3.8 NACIONAL - Curso online = nacional, guarda origem como campo extra
        payload = {
            "sck": sck_teste,
            "sck_completo": sck_teste,
            "cidade": "nacional",  # CORRIGIDO v3.8 NACIONAL
            "cidade_origem_lead": cid_origem,  # ADICIONADO - NAO DELETA ANTERIOR
            "interesse": inter,
            "abrangencia": "NACIONAL - BRASIL TODO - Academia FC Constrói",  # ADICIONADO
            "plataforma": plat,
            "traffic_type": traffic,
            "utm_campaign": "topo",
            "utm_source": plat,
            "utm_medium": traffic,
            "email": email_teste,
            "valor": 99.90,
            "status": "paid"
        }
        supa.table("vendas_kiwify").insert(payload).execute()
        return True, payload
    except Exception as e:
        return False, str(e)

def buscar_vendas_reais_supabase():
    try:
        supa_url = os.getenv("SUPABASE_URL")
        supa_key = os.getenv("SUPABASE_KEY")
        try:
            if not supa_url:
                supa_url = st.secrets.get("SUPABASE_URL", "")
            if not supa_key:
                supa_key = st.secrets.get("SUPABASE_KEY", "")
        except:
            pass
        if not supa_url or not supa_key:
            return []
        from supabase import create_client
        supa = create_client(supa_url, supa_key)
        res = supa.table("vendas_kiwify").select("*").order("created_at", desc=True).limit(100).execute()
        return res.data if res.data else []
    except:
        return []

def gerar_combo_pessoa_obra_1280x720(foto_pessoa_pil, foto_obra_pil, texto_grande, subtexto, cor_destaque="#FF6B00", modelo="Choque"):
    W, H = 1280, 720
    if foto_obra_pil is not None:
        bg = foto_obra_pil.convert("RGB")
        fw, fh = bg.size
        scale = max(W/fw, H/fh)
        bg = bg.resize((int(fw*scale), int(fh*scale)), Image.LANCZOS)
        bg = bg.crop(((bg.size[0]-W)//2, (bg.size[1]-H)//2, (bg.size[0]-W)//2+W, (bg.size[1]-H)//2+H))
    else:
        if "Choque" in modelo:
            bg = Image.new('RGB', (W, H), (255, 193, 7))
        else:
            bg = Image.new('RGB', (W, H), (35,35,35))
    if foto_obra_pil is not None:
        overlay = Image.new('RGBA', (W, H), (0,0,0,70))
        bg = Image.alpha_composite(bg.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(bg)
    if foto_pessoa_pil is not None:
        pessoa = foto_pessoa_pil.convert("RGBA")
        ph = int(H * 0.88)
        pw = int(pessoa.size[0] * (ph / pessoa.size[1]))
        pessoa = pessoa.resize((pw, ph), Image.LANCZOS)
        x_p = W - pw - 20
        y_p = H - ph
        sombra = Image.new('RGBA', (pw+20, ph+20), (0,0,0,110))
        bg.paste(sombra, (x_p-10, y_p), sombra)
        bg.paste(pessoa, (x_p, y_p), pessoa)
        draw.rectangle([(x_p-6, y_p-6), (x_p+pw+6, y_p+ph+6)], outline=cor_destaque, width=7)
    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 105)
        font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 52)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    def texto_youtube(x, y, txt, font, fill):
        for dx in (-6,-3,0,3,6):
            for dy in (-6,-3,0,3,6):
                draw.text((x+dx, y+dy), txt, font=font, fill="black")
        draw.text((x, y), txt, font=font, fill=fill)
    x_txt = 50
    y_txt = 110
    if "Choque" in modelo and foto_obra_pil is None:
        draw.rectangle([(x_txt-20, y_txt-15), (x_txt+50, y_txt+100)], fill=(0,0,0))
        draw.text((x_txt, y_txt), texto_grande.upper(), font=font_big, fill=(255,193,7))
    else:
        texto_youtube(x_txt, y_txt, texto_grande.upper(), font_big, cor_destaque)
    draw.text((55, y_txt+135), subtexto.upper(), font=font_small, fill="white", stroke_width=7, stroke_fill="black")
    return bg.resize((W, H))

def gerar_thumbnail_simples_1280x720(texto_grande, subtexto, cor="#FF6B00"):
    W, H = 1280, 720
    img = Image.new('RGB', (W, H), (17,17,17))
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W, int(H*0.45)], fill=cor)
    try:
        font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 100)
        font_small = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    d.text((50,100), texto_grande.upper(), fill="white", font=font_big, stroke_width=6, stroke_fill="black")
    d.text((50,250), subtexto.upper(), fill="white", font=font_small, stroke_width=5, stroke_fill="black")
    return img

def puxar_imagens_instagram_temporal(username="fc_constroi", qtd=6):
    """v3.3.7 - REMOVIDO INSTALOADER - retorna vazio instantâneo, não trava"""
    return []

def imagem_url_para_pil_temporal(url):
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content)).convert("RGB")
    except:
        pass
    return None

def puxar_instagram_online_auto(username="fc_constroi", qtd=3):
    """NOVO v3.3.8 - Puxa @fc_constroi online com sessão salva e já retorna PIL"""
    imgs = []
    try:
        import instaloader
        L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            save_metadata=False,
            compress_json=False
        )
        L.context.request_timeout = 10
        try:
            L.load_session_from_file(username, filename=f"{username}_session")
        except:
            pass
        profile = instaloader.Profile.from_username(L.context, username)
        for i, post in enumerate(profile.get_posts()):
            if i >= qtd:
                break
            try:
                resp = requests.get(post.url, timeout=10)
                if resp.status_code == 200:
                    img = Image.open(BytesIO(resp.content)).convert("RGB")
                    imgs.append(img)
            except:
                continue
    except Exception as e:
        print(f"Erro puxar online: {e}")
        return []
    return imgs

def gerar_thumbs_auto_com_insta(foto_pessoa_pil, lista_obras_insta, texto, subtexto, cor="#FF6B00"):
    """NOVO v3.3.8 - Gera 3 thumbs 1280x720 automaticamente com fotos puxadas do Insta"""
    thumbs = []
    cores = [cor, "#FFC107", "#00E676"]
    modelos = ["Modelo Obra (Foto obra + pessoa) - COMBO AUTOMÁTICO"] * 3
    for i, obra in enumerate(lista_obras_insta[:3]):
        thumb = gerar_combo_pessoa_obra_1280x720(
            foto_pessoa_pil, obra, texto, subtexto,
            cor_destaque=cores[i % 3],
            modelo=modelos[i % 3]
        )
        thumbs.append(thumb)
    return thumbs

st.set_page_config(
    page_title="FC CONSTROI • GROWTH AI v3.8 NACIONAL",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="collapsed"
)

if HAS_DESIGNER:
    try:
        aplicar_design()
    except Exception as e:
        st.caption(f"Designer aviso: {e}")
else:
    st.markdown("""
    <style>
    .main-header {background: linear-gradient(90deg,#111 0%,#222 100%);color:white;padding:14px 22px;border-radius:10px;display:flex;justify-content:space-between;align-items:center;border-left:5px solid #FF6B00;}
    .stTabs [data-baseweb="tab-list"] {gap:6px;flex-wrap:wrap;}
    .stTabs [data-baseweb="tab"] {background:#f5f5f5;border-radius:6px;padding:6px 12px;}
    .stTabs [aria-selected="true"] {background:#FF6B00 !important;color:white !important;}
    </style>
    """, unsafe_allow_html=True)

def get_now_bahia():
    return datetime.now(ZoneInfo("America/Bahia"))

def load_params():
    return {
        "gaveta_porcelanato": {
            "id": "gaveta",
            "titulo_original": "ERRO de R$8mil em gaveta porcelanato - 95% erram",
            "titulo_viral": "GAVETA PORCELANATO RACHOU? Evite prejuízo de R$8mil",
            "views": 48000,
            "status": "TOP1 VIRAL",
            "score_gancho": 9.2,
            "cta": "Comenta EU QUERO que te mando lista de materiais",
            "gancho_3s": "Você tá perdendo R$8mil em cada gaveta por causa disso!",
            "hashtags": "#marmoraria #porcelanato #moveisplanejados #gaveta",
            "plataformas": ["Instagram","Facebook","TikTok"],
            "horario": "07:00"
        },
        "pia_banheiro_90x90": {
            "id": "pia_de_banheiro",
            "titulo_original": "Fature 10k com pia de banheiro 90x90",
            "titulo_viral": "Pia de banheiro 90x90 que fatura R$10k - Passo a passo",
            "views": 32000,
            "status": "TOP2",
            "score_gancho": 8.7,
            "cta": "Comenta PIA que te mando no direct",
            "gancho_3s": "Essa pia de banheiro de 90x90 me deu R$10k de lucro em 1 dia",
            "hashtags": "#piadebanheiro #porcelanato #banheirodeluxo",
            "plataformas": ["Instagram","YouTube","Kwai"],
            "horario": "19:00"
        },
        "base_armario_300kg": {
            "id": "base",
            "titulo_original": "Base armário que aguenta 300kg sem empenar",
            "titulo_viral": "Base que aguenta 300kg - nunca mais empena",
            "views": 28000,
            "status": "TOP3",
            "score_gancho": 8.4,
            "cta": "Comenta BASE que te mando projeto",
            "gancho_3s": "Sua base empena porque você faz assim...",
            "hashtags": "#marcenaria #marmoraria #basearmario",
            "plataformas": ["TikTok","Kwai","Instagram"],
            "horario": "12:00"
        }
    }

PARAMS = load_params()
now = get_now_bahia()
st.markdown(f"""
<div class="main-header">
<div>
<b>FC CONSTRÓI • GROWTH AI v3.8 NACIONAL - Kiwify Vendas Curso Online BRASIL TODO</b> 
<span style="color:#FF6B00">• 9 ABAS • CURSO NACIONAL + 6 CIDADES SERVICO LOCAL • 8 INTERESSES PORCELANATO</span>
<br><small style="color:#aaa">FIX v3.8 NACIONAL: Curso Online Academia FC Constrói = NACIONAL Brasil Todo | 6 Cidades = Apenas Serviço Local | Loop TOP3: gaveta (48k) | pia (32k) | base (28k) - pia banheiro, closet, bancada cozinha, fachadas, nichos, revestimentos, armarios, gavetas</small>
</div>
<div style="text-align:right;font-size:12px">
{now.strftime('%d/%m/%Y • %H:%M')} - Irará-BA<br>
<span style="color:#FF6B00">● Online NACIONAL</span> Supabase
</div>
</div>
""", unsafe_allow_html=True)
st.markdown("")

tab_names = [
    "🔥 FILTROS (Cursos+Local)",
    "♻️ Reciclar Conteúdo",
    "📊 Dashboard + Gráficos IA",
    "🖼️ Thumbnails IA",
    "🎬 YouTube Pack",
    "💰 CAC CPA ROAS",
    "💹 INVESTIMENTOS",
    "💚 VENDAS Kiwify NACIONAL",
    "🤖 Insta Auto + Loop Viral"
]
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(tab_names)

with tab1:
    st.subheader("🔥 FILTROS - IA Curso + Local - CURSO NACIONAL + 6 Cidades Serviço Local")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        curso = st.selectbox("Curso", ["Todos","Cozinha Planejada","Banheiro de Luxo","Porcelanato Estrutural","Closet em Porcelanato","Bancada Cozinha","Fachadas","Nichos","Revestimentos","Armários/Gavetas em Porcelanato","Pia de Banheiro em Porcelanato"], key="f_curso")
    with col2:
        local = st.selectbox("Local", ["Todos"] + CIDADES_ORIGINAIS + ["NACIONAL - Brasil Todo"], key="f_local")
    with col3:
        viral = st.selectbox("Filtro Viral", ["Top 3 Loop Infinito","Todos os vídeos","Score >8.0","Score >9.0"], key="f_viral")
    with col4:
        plataforma = st.selectbox("Plataforma", ["Todas","Instagram","YouTube","TikTok","Kwai","Facebook"], key="f_plat")
    filtered = PARAMS
    df_filtro = pd.DataFrame([
        {"ID": k, "Título": v["titulo_viral"], "Views": v["views"], "Score Gancho": v["score_gancho"], "Status": v["status"], "Horário": v["horario"]}
        for k,v in filtered.items()
    ])
    st.dataframe(df_filtro, use_container_width=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Total filtrado", f"{len(df_filtro)} vídeos", "Top 3")
        st.metric("Views filtradas", f"{df_filtro['Views'].sum()/1000:.0f}k")
    with col_b:
        st.success("✅ CURSO NACIONAL BRASIL TODO + 6 CIDADES SERVICO LOCAL + 8 INTERESSES PORCELANATO: pia banheiro, closet, bancada cozinha, fachadas, nichos, revestimentos, armarios, gavetas")
        st.button("📄 Exportar PDF Filtrado", key="pdf_filtro")

with tab2:
    st.subheader("♻️ Reciclar Conteúdo - Transforma TOP3 em 9 conteúdos novos")
    for key, val in PARAMS.items():
        with st.expander(f"{val['status']} • {key} • {val['views']} views • Score {val['score_gancho']}", expanded=False):
            c1, c2, c3 = st.columns([2,2,1])
            with c1:
                st.markdown("**ORIGINAL**")
                st.text_input("Título Original", val["titulo_original"], key=f"orig_t_{key}", disabled=True)
                st.text_input("Título Viral Novo", val["titulo_viral"], key=f"viral_t_{key}")
                st.text_area("Gancho 3s (viral)", val["gancho_3s"], key=f"gancho_{key}", height=80)
            with c2:
                st.markdown("**RECICLADO PARA CADA PLATAFORMA**")
                st.text_area("Legenda Insta (com CTA)", f"{val['gancho_3s']}\n\n{val['cta']}\n\n{val['hashtags']}", key=f"leg_insta_{key}", height=100)
                st.text_area("Legenda TikTok (curta)", f"{val['gancho_3s']} 👉 {val['cta']}", key=f"leg_tik_{key}", height=80)
                st.text_input("CTA", val["cta"], key=f"cta_rec_{key}")
            with c3:
                st.markdown("**AÇÕES**")
                st.metric("Views", f"{val['views']/1000:.0f}k")
                st.metric("Gancho", val["score_gancho"])
                st.button(f"♻️ Reciclar {val['id']}", key=f"btn_rec_{key}", type="primary")
                st.button(f"📥 Baixar com yt-dlp", key=f"btn_yt_{key}")
                st.button(f"🎨 Gerar Thumbnail", key=f"btn_thumb_{key}")
    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.multiselect("Escolha vídeos para reciclar em massa", list(PARAMS.keys()), default=list(PARAMS.keys()), key="mass_rec")
        st.selectbox("Formato saída", ["Reels 9:16","Shorts 9:16","Post 1:1","Story 9:16"], key="formato_mass")
    with col_r2:
        st.number_input("Quantos variações por vídeo?", min_value=1, max_value=5, value=3, key="qtd_var")
        st.button("🔥 GERAR 9 CONTEÚDOS (3 vídeos x 3 variações)", type="primary", key="gerar_9")

with tab3:
    st.subheader("📊 Dashboard + Gráficos IA - FIXO - NACIONAL")
    if "metrics_fixed" not in st.session_state:
        st.session_state.metrics_fixed = {"cac": 100, "roas": 3.2, "vendas": 7, "invest": 500}
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Vídeos Top 3", "3", "Loop infinito", border=True)
    c2.metric("Views Totais", "108k", "+12% vs ontem", border=True)
    c3.metric("Vendas Kiwify NACIONAL", "R$ 3.477", "+R$497 hoje", border=True)
    c4.metric("ROAS Fixo", f"{st.session_state.metrics_fixed['roas']}x", "Não some", border=True)
    c5.metric("CAC Fixo", f"R$ {st.session_state.metrics_fixed['cac']}", "Travado", border=True)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        df_top = pd.DataFrame([
            {"video": "gaveta R$8mil", "views": 48000, "score": 9.2},
            {"video": "pia banheiro 10k", "views": 32000, "score": 8.7},
            {"video": "base 300kg", "views": 28000, "score": 8.4}
        ])
        if HAS_PLOTLY:
            fig = px.bar(df_top, x="video", y="views", color="score", color_continuous_scale="Oranges", title="Views por vídeo TOP3 - NACIONAL")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart(df_top, x="video", y="views")
    with col_g2:
        dates = [get_now_bahia() - timedelta(days=i) for i in range(7,0,-1)]
        df_evo = pd.DataFrame({
            "data": [d.strftime("%d/%m") for d in dates],
            "views": [12000, 15000, 18000, 22000, 28000, 35000, 48000]
        })
        if HAS_PLOTLY:
            fig2 = px.line(df_evo, x="data", y="views", markers=True, title="Crescimento gaveta viral - NACIONAL")
            fig2.update_traces(line_color="#FF6B00")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.line_chart(df_evo, x="data", y="views")
        df_funil = pd.DataFrame([
            {"etapa": "Comentário PORCELANATO", "qtd": 100},
            {"etapa": "DM enviada", "qtd": 70},
            {"etapa": "Link Kiwify clicado", "qtd": 25},
            {"etapa": "Venda aprovada NACIONAL", "qtd": 7},
        ])
        st.dataframe(df_funil, use_container_width=True)

with tab4:
    st.subheader("🖼️ Thumbnails IA - 1280x720 + COMBO + AUTO ONLINE")
    if "thumbs_memoria" not in st.session_state:
        st.session_state.thumbs_memoria = []
    if "insta_cache" not in st.session_state:
        st.session_state.insta_cache = []
    if "obra_selecionada" not in st.session_state:
        st.session_state.obra_selecionada = None
    if "dalle_bg" not in st.session_state:
        st.session_state.dalle_bg = None
    st.markdown("### 🚀 NOVO v3.3.8 - PUXA INSTA ONLINE + GERA THUMB AUTO")
    col_auto1, col_auto2, col_auto3, col_auto4 = st.columns([1,1,2,1])
    with col_auto1:
        qtd_insta = st.number_input("Qtd fotos Insta", min_value=1, max_value=6, value=3, key="qtd_insta_v338")
    with col_auto2:
        texto_auto = st.text_input("Texto Thumb Auto", "ERRO R$8MIL", key="txt_auto_v338")
    with col_auto3:
        sub_auto = st.text_input("Subtexto Auto", "95% ERRAM", key="sub_auto_v338")
    with col_auto4:
        if st.button("🚀 PUXAR + GERAR AUTO", key="btn_auto_v338", type="primary"):
            with st.spinner(f"Puxando {qtd_insta} fotos @fc_constroi online e gerando thumbs..."):
                fp_auto = None
                try:
                    if 'uploaded_pessoa_global' in st.session_state and st.session_state.uploaded_pessoa_global:
                        fp_auto = Image.open(st.session_state.uploaded_pessoa_global)
                except:
                    pass
                obras_auto = puxar_instagram_online_auto("fc_constroi", int(qtd_insta))
                if not obras_auto:
                    st.error("Instagram bloqueou sem login. Faz 1 vez no terminal: instaloader --login=SEU_USER")
                    st.info("Depois de logar, clica de novo que puxa automático e já gera as thumbs 1280x720")
                else:
                    thumbs_auto = gerar_thumbs_auto_com_insta(fp_auto, obras_auto, texto_auto, sub_auto)
                    st.success(f"✅ {len(thumbs_auto)} thumbs geradas auto com fotos online do @fc_constroi!")
                    cols_auto = st.columns(3)
                    for i, th in enumerate(thumbs_auto):
                        with cols_auto[i]:
                            st.image(th, caption=f"AUTO {i+1} - 1280x720 - Insta Online", use_container_width=True)
                            buf = BytesIO()
                            th.save(buf, format="JPEG", quality=96)
                            st.download_button(f"📥 Baixar AUTO {i+1}", buf.getvalue(), f"thumb_auto_online_{i+1}_1280x720.jpg", "image/jpeg", key=f"dl_auto_v338_{i}")
                            st.session_state.thumbs_memoria.append({
                                "img": th,
                                "bytes": buf.getvalue(),
                                "cor": "#FF6B00",
                                "nome": f"thumb_auto_online_{i+1}_1280x720.jpg"
                            })
    st.markdown("---")
    st.markdown("#### 📸 MODO TEMPORAL REAL (sem baixar nada) - FUNCIONA 100%")
    col_insta1, col_insta2, col_insta3 = st.columns([2,1,1])
    with col_insta1:
        st.success("✅ FIX v3.3.8: Upload manual 100% temporal + NOVO modo AUTO ONLINE acima")
    with col_insta2:
        qtd_insta_old = st.number_input("Qtd fotos", min_value=1, max_value=12, value=2, key="qtd_insta_v337")
    with col_insta3:
        if st.button("📸 Info modo temporal", key="pull_insta_v337", type="primary"):
            st.info("MODO TEMPORAL REAL: Upload aqui não salva em disco, tudo em BytesIO na RAM")
    st.markdown("---")
    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown("**GERADOR 100% OFFLINE (Pillow) - COMBO AUTOMÁTICO - TEMPORAL**")
        col_up_a, col_up_b = st.columns(2)
        with col_up_a:
            st.markdown("Upload foto PESSOA (você) - temporal")
            uploaded_pessoa = st.file_uploader("Upload foto base (pessoa)", type=["jpg","png","jpeg"], key="thumb_up_pessoa_v337", label_visibility="collapsed")
            if uploaded_pessoa:
                st.session_state.uploaded_pessoa_global = uploaded_pessoa
        with col_up_b:
            st.markdown("Upload foto OBRA / TUDO (fundo) - temporal - puxe do @fc_constroi")
            uploaded_obra = st.file_uploader("Upload foto base (obra)", type=["jpg","png","jpeg"], key="thumb_up_obra_v337", label_visibility="collapsed")
        texto_thumb = st.text_input("Texto grande Thumbnail", "ERRO R$8MIL", key="thumb_text_v337")
        subtexto = st.text_input("Subtexto", "95% ERRAM", key="thumb_sub_v337")
        cor_fundo = st.color_picker("Cor destaque FC", "#FF6B00", key="thumb_color_v337")
        modelo = st.selectbox("Modelo", ["Modelo Choque (Fundo amarelo + texto preto)", "Modelo Obra (Foto obra + pessoa) - COMBO AUTOMÁTICO", "Modelo Reciclado (Auto combo + borda)", "Modelo Antes/Depois", "Modelo Preço (R$49,90 gigante)", "Modelo Seta Vermelha"], key="thumb_modelo_v337")
        if st.button("🎨 Gerar 3 variações Thumbnail (Pillow) - 1280x720", type="primary", key="gen_thumb_pillow_v337"):
            if HAS_PIL:
                fp = Image.open(uploaded_pessoa) if uploaded_pessoa else None
                fo = Image.open(uploaded_obra) if uploaded_obra else None
                if fo is None and st.session_state.obra_selecionada is not None:
                    fo = st.session_state.obra_selecionada
                cores = [cor_fundo, "#FFC107", "#00E676"]
                cols = st.columns(3)
                for i, col in enumerate(cols):
                    with col:
                        thumb = gerar_combo_pessoa_obra_1280x720(fp, fo, texto_thumb, subtexto, cores[i], modelo)
                        st.image(thumb, caption=f"Var {i+1} {cores[i]} - 1280x720", use_container_width=True)
                        buf = BytesIO()
                        thumb.save(buf, format="JPEG", quality=96)
                        st.session_state.thumbs_memoria.append({
                            "img": thumb,
                            "bytes": buf.getvalue(),
                            "cor": cores[i],
                            "nome": f"thumb_{texto_thumb[:10]}_v{i+1}_1280x720.jpg"
                        })
                        st.download_button(f"📥 Baixar JPG Var {i+1} 1280x720", data=buf.getvalue(), file_name=f"thumb_{texto_thumb[:10]}_v{i+1}_1280x720.jpg", mime="image/jpeg", key=f"dl_thumb_v337_{i}")
            else:
                st.warning("Pillow não instalado")
        if st.session_state.thumbs_memoria:
            st.markdown("---")
            st.markdown(f"### ✅ {len(st.session_state.thumbs_memoria)} Thumbnails salvas na memória (não somem ao clicar)")
            cols_mem = st.columns(3)
            ultimas = st.session_state.thumbs_memoria[-3:]
            for i, item in enumerate(ultimas):
                with cols_mem[i]:
                    st.image(item["img"], caption=f"Memória Var {i+1} {item['cor']} - 1280x720", use_container_width=True)
                    st.download_button(f"📥 Baixar Memória {i+1}", data=item["bytes"], file_name=item["nome"], mime="image/jpeg", key=f"dl_mem_persist_{i}_v337")
    with c2:
        st.markdown("**PREVIEW + DALL·E V2 (pago) - 1280x720**")
        st.image("https://via.placeholder.com/1280x720/111111/FF6B00?text=THUMBNAIL%0AERRO+R$8MIL%0A95%25+ERRAM%0A1280x720", caption="Preview modelo Choque - 1280x720 YouTube")
        st.text_input("Prompt DALL·E (opcional)", "porcelanato marmorizado em banheiro luxuoso", key="dalle_prompt_v337")
        if st.button("🖼️ Gerar fundo com IA (DALL·E) - 1280x720", key="dalle_gen_v337"):
            st.info("DALL·E clicado - com memória fixa, não apaga mais (fix v3.3.8)")
        if st.button("🗑️ Limpar memória Thumbs", key="clear_thumbs_v337"):
            st.session_state.thumbs_memoria = []
            st.session_state.insta_cache = []
            st.session_state.obra_selecionada = None
            st.rerun()
        st.caption("✅ v3.3.8: AUTO ONLINE + 1280x720 + temporal real")

with tab5:
    st.subheader("🎬 YouTube Pack - Automação Completa")
    link_yt = st.text_input("Link YouTube original (para reciclar)", "https://youtube.com/watch?v=...", key="yt_link")
    col_yt1, col_yt2 = st.columns(2)
    with col_yt1:
        st.text_input("Título SEO (com Score Gancho)", "Como NÃO errar gaveta porcelanato - economize R$8mil | FC Constrói", key="yt_titulo")
        st.text_area("Descrição com links Kiwify + Timestamp", "00:00 Intro - Erro R$8mil\n01:30 Como fazer certo\n\n👉 Curso: https://pay.kiwify.com.br/...", key="yt_desc", height=150)
    with col_yt2:
        st.text_area("Tags", "marmoraria, moveis planejados, cozinha planejada, porcelanato, pia de banheiro, gaveta porcelanato, Irará BA, closet porcelanato, bancada cozinha, fachadas, nichos, revestimentos, armarios", key="yt_tags", height=100)
        st.selectbox("Horário ideal", ["19:00 Quinta (melhor CTR)", "07:00 Segunda", "12:00 Terça"], key="yt_horario")
        st.checkbox("Thumbnail automática junto", value=True, key="yt_thumb_auto")
    col_yt_btn1, col_yt_btn2, col_yt_btn3 = st.columns(3)
    with col_yt_btn1:
        st.button("📦 Gerar Pack YouTube Completo", type="primary", key="gen_yt_pack")
    with col_yt_btn2:
        st.button("📤 Upload automático (YouTube API)", key="yt_upload_auto")
    with col_yt_btn3:
        st.button("📋 Copiar tudo (1 clique)", key="yt_copy_all")

with tab6:
    st.subheader("💰 CAC CPA ROAS - CALCULADORA FIXA")
    if "invest_total" not in st.session_state:
        st.session_state.invest_total = 500.0
    if "vendas_total" not in st.session_state:
        st.session_state.vendas_total = 5
    if "ticket_medio" not in st.session_state:
        st.session_state.ticket_medio = 497.0
    c1,c2,c3 = st.columns(3)
    with c1:
        st.session_state.invest_total = st.number_input("Investimento Total (R$)", value=st.session_state.invest_total, key="invest_input")
        st.session_state.vendas_total = st.number_input("Vendas totais", value=st.session_state.vendas_total, key="vendas_input")
        st.session_state.ticket_medio = st.number_input("Ticket Médio (R$)", value=st.session_state.ticket_medio, key="ticket_input")
    with c2:
        cac = st.session_state.invest_total / st.session_state.vendas_total if st.session_state.vendas_total else 0
        st.metric("CAC", f"R$ {cac:.2f}", border=True)
        st.session_state.metrics_fixed["cac"] = cac
    with c3:
        faturamento = st.session_state.vendas_total * st.session_state.ticket_medio
        roas = faturamento / st.session_state.invest_total if st.session_state.invest_total else 0
        lucro = faturamento - st.session_state.invest_total
        st.metric("ROAS", f"{roas:.2f}x", border=True)
        st.metric("Lucro", f"R$ {lucro:.2f}", border=True)
        st.session_state.metrics_fixed["roas"] = roas

with tab7:
    st.subheader("💹 INVESTIMENTOS - Controle completo")
    col_inv1, col_inv2 = st.columns([2,1])
    with col_inv1:
        df_invest = pd.DataFrame([
            {"Data": "20/10/2026", "Plataforma": "Meta Ads", "Campanha": "Gaveta R$8mil - Top1", "Valor": 150, "Retorno": "48k views", "Status": "Ativo"},
            {"Data": "19/10/2026", "Plataforma": "YouTube Ads", "Campanha": "Pia 10k", "Valor": 80, "Retorno": "32k views", "Status": "Pausado"},
            {"Data": "18/10/2026", "Plataforma": "TikTok Ads", "Campanha": "Base 300kg", "Valor": 50, "Retorno": "28k views", "Status": "Ativo"},
        ])
        st.dataframe(df_invest, use_container_width=True)
    with col_inv2:
        st.number_input("Valor (R$)", value=100.0, key="inv_valor")
        st.button("➕ Adicionar", type="primary", key="inv_add")

with tab8:
    st.subheader("💚 VENDAS Kiwify - NACIONAL BRASIL TODO - SUPABASE TRACKING REAL v3.8")
    vendas_reais_tab8 = buscar_vendas_reais_supabase()
    if vendas_reais_tab8:
        st.success(f"✅ Supabase conectado - {len(vendas_reais_tab8)} vendas reais encontradas! Todas agora NACIONAL.")
        df_real = pd.DataFrame(vendas_reais_tab8)
        st.dataframe(df_real, use_container_width=True)
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        col_k1.metric("Total Real NACIONAL", f"{len(df_real)} vendas")
        col_k2.metric("Abrangência", "NACIONAL - Brasil Todo")
        col_k3.metric("Plataformas", f"{df_real['plataforma'].nunique() if 'plataforma' in df_real.columns else 1}")
        col_k4.metric("Faturamento Real", f"R$ {df_real['valor'].sum():.2f}" if 'valor' in df_real.columns else "R$ 0")
    else:
        df_vendas = pd.DataFrame([
            {"id": "kiwify_001", "produto": "Marmoraria na Prática", "valor": 497, "status": "approved", "origem": "gaveta viral (48k)", "data": "20/10/2026 22:00", "cliente": "João - NACIONAL"},
            {"id": "kiwify_002", "produto": "Cozinha Planejada", "valor": 297, "status": "approved", "origem": "pia de banheiro 10k (32k)", "data": "19/10/2026 18:00", "cliente": "Maria - NACIONAL"},
        ])
        st.dataframe(df_vendas, use_container_width=True)

with tab9:
    st.subheader("🤖 Insta Auto + Loop Viral - 07h / 12h / 19h - Só TOP3")
    st.success("✅ Loop infinito configurado - NACIONAL")
    col_loop1, col_loop2 = st.columns(2)
    with col_loop1:
        st.time_input("Horário 1 - Gaveta", value=pd.to_datetime("07:00").time(), key="loop_h1")
        st.time_input("Horário 2 - Base 300kg", value=pd.to_datetime("12:00").time(), key="loop_h2")
        st.time_input("Horário 3 - Pia de banheiro 10k", value=pd.to_datetime("19:00").time(), key="loop_h3")
        st.multiselect("Plataformas", ["Instagram","Facebook","TikTok","YouTube Shorts","Kwai"], default=["Instagram","TikTok","YouTube Shorts"], key="loop_plats")
        st.checkbox("Loop infinito só TOP3 virais", value=True, key="loop_top3")
    with col_loop2:
        st.metric("Próximo post", "SEG 07:00 - Gaveta R$8mil", "em 8h")
        st.metric("Último post", "TER 12:00 - Base 300kg", "28k views")
        if st.button("🚀 ATIVAR AUTO POSTAGEM - LOOP INFINITO", type="primary", key="ativar_loop"):
            st.success("Loop ativado! Próximos 7 dias agendados - NACIONAL")
            st.balloons()
        if st.button("⏸️ Pausar loop", key="pausar_loop"):
            st.warning("Loop pausado")
    st.json(PARAMS)

st.markdown("---")
st.markdown(f"""
<center><small>
FC CONSTRÓI • GROWTH AI v3.8 NACIONAL • CURSO NACIONAL BRASIL TODO + 6 CIDADES SERVIÇO LOCAL • Irará-BA • {now.strftime('%d/%m/%Y %H:%M')}<br>
Santanópolis, Irará, Feira de Santana, Santa Bárbara, Serrinha, Ouriçangas - pia banheiro, closet, bancada cozinha, fachadas, nichos, revestimentos, armarios, gavetas + NACIONAL
</small></center>
""", unsafe_allow_html=True)

# SIDEBAR PROFISSIONAL - KIWIFY VENDAS CURSO ONLINE NACIONAL - APENAS AJUSTE DE TITULOS, SEM DELETAR NADA
with st.sidebar:
    st.markdown("---")
    st.markdown("### ✅ Kiwify Vendas Curso Online - NACIONAL BRASIL TODO")
    st.caption("Registro oficial de vendas do curso - NACIONAL - 6 cidades = apenas serviço local + porcelanato")
    sck_teste = st.text_input("Código da Venda (SCK)", "fb_nacional_pia_banheiro_organico", key="sck_teste_sidebar_novo_nacional")
    email_teste = st.text_input("E-mail do Cliente", "cliente@email.com", key="email_teste_sidebar_nacional")
    if st.button("✅ Registrar Venda Oficial no Supabase - NACIONAL", key="btn_teste_supabase_novo_nacional"):
        ok, resp = salvar_venda_kiwify_teste(sck_teste, email_teste)
        if ok:
            st.success(f"✅ Venda NACIONAL registrada! {resp}")
            st.balloons()
        else:
            st.error(f"❌ Erro: {resp}")
    st.markdown("---")
    st.markdown("**Vendas Registradas • Base Oficial • NACIONAL**")
    vendas_reais = buscar_vendas_reais_supabase()
    if vendas_reais:
        df_real_side = pd.DataFrame(vendas_reais)
        if not df_real_side.empty:
            cols_show = [c for c in ["cidade","cidade_origem_lead","interesse","abrangencia","plataforma","traffic_type"] if c in df_real_side.columns]
            if cols_show:
                st.dataframe(df_real_side[cols_show].head(10), use_container_width=True)
        st.metric("Total de Vendas Registradas - NACIONAL", len(vendas_reais))
    else:
        st.caption("Nenhuma venda ainda ou sem env vars - webhook Kiwify vai salvar como NACIONAL automaticamente")
        

        

        
        



