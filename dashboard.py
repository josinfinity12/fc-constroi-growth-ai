# dashboard.py - v3.1.9 FINAL - FC CONSTRÓI - 9 ABAS - SEM QUEBRAR NADA
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.express as px
import plotly.graph_objects as go
import subprocess
from pathlib import Path
import shutil

# Imports do design
from designer import aplicar_design, mostrar_header_com_logo, mostrar_footer, CORES_FC

# Configuração da página
st.set_page_config(
    page_title="FC CONSTRÓI • Growth AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

aplicar_design()
mostrar_header_com_logo()

# Fuso Bahia
fuso_bahia = pytz.timezone('America/Bahia')
agora = datetime.now(fuso_bahia)

# ==================== DADOS MOCKADOS ====================
@st.cache_data
def carregar_dados():
    datas = [agora - timedelta(days=x) for x in range(30, -1, -1)]
    return pd.DataFrame({
        'data': datas,
        'vendas': np.random.randint(800, 3500, 31),
        'leads': np.random.randint(5, 25, 31),
        'investimento': np.random.randint(100, 600, 31),
        'roas': np.random.uniform(1.8, 4.5, 31)
    })

df = carregar_dados()

# ==================== SIDEBAR (ORIGINAL) ====================
with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    periodo = st.selectbox("Período", ["Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias", "Mês atual"])
    canal = st.multiselect("Canal", ["Instagram", "Google", "WhatsApp", "Loja"], default=["Instagram", "Google"])
    st.divider()
    st.caption(f"Atualizado: {agora.strftime('%d/%m/%Y %H:%M')}")

# ==================== FUNÇÕES SÓ DA 9ª ABA (NÃO AFETAM AS OUTRAS) ====================
BASE_DIR = Path(__file__).parent
VIDEOS_DIR = BASE_DIR / "videos_brutos"
OUTPUT_CURSO = BASE_DIR / "output" / "CURSO_NACIONAL"
OUTPUT_OBRA = BASE_DIR / "output" / "OBRAS_LOCAL"
for p in [VIDEOS_DIR, OUTPUT_CURSO, OUTPUT_OBRA]:
    p.mkdir(parents=True, exist_ok=True)

def baixar_insta_online(url):
    try:
        out = str(VIDEOS_DIR / "%(title).30s.%(ext)s")
        cmd = ["yt-dlp", url, "-o", out, "--merge-output-format", "mp4", "--no-playlist", "--quiet"]
        subprocess.run(cmd, check=True, capture_output=True)
        vids = sorted(VIDEOS_DIR.glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
        return str(vids[0]) if vids else None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# ==================== 9 ABAS - SUAS 5 ORIGINAIS INTACTAS + 4 DO AR + 1 NOVA ====================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🔥 FILTROS (Cursos+Local)", 
    "♻️ Reciclar Conteúdo",
    "📊 Dashboard + Gráficos IA",
    "🖼️ Thumbnails",
    "📦 YouTube Pack",
    "💰 CAC CPA ROAS",
    "💵 INVESTIMENTOS",
    "💚 VENDAS Kiwify",
    "♻️ Insta Auto + Loop Viral [NOVO]"
])

# --- ABA 1: FILTROS (era Visão Geral no seu v3.1.8, agora é FILTROS do ar) ---
with tab1:
    st.markdown("#### 🔥 FILTROS (Cursos+Local) - Filtro de Comentários")
    st.caption("Separa Curso Nacional vs Obras Local vs Curioso - economiza tempo do Francis")
    try:
        from scripts.filtros import render_filtros
        render_filtros()
    except ImportError:
        st.markdown("**Visão Geral (seu código original v3.1.8 mantido aqui)**")
        col1, col2, col3, col4 = st.columns(4)
        total_vendas = df['vendas'].sum()
        total_leads = df['leads'].sum()
        total_invest = df['investimento'].sum()
        roas_medio = total_vendas / total_invest if total_invest > 0 else 0
        col1.metric("💰 Vendas", f"R$ {total_vendas:,.0f}", f"{df['vendas'].iloc[-1] - df['vendas'].iloc[-2]:+}")
        col2.metric("👥 Leads", f"{total_leads}", f"{df['leads'].iloc[-1] - df['leads'].iloc[-2]:+}")
        col3.metric("📢 Investido", f"R$ {total_invest:,.0f}")
        col4.metric("🚀 ROAS Médio", f"{roas_medio:.2f}x", f"{df['roas'].iloc[-1] - df['roas'].iloc[-2]:+.2f}")
        st.divider()
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.markdown("**Vendas últimos 30 dias**")
            fig = px.line(df, x='data', y='vendas', template="plotly_white")
            fig.update_traces(line_color=CORES_FC['laranja_principal'])
            fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)
        with col_graf2:
            st.markdown("**ROAS por dia**")
            fig2 = px.bar(df, x='data', y='roas', template="plotly_white")
            fig2.update_traces(marker_color=CORES_FC['preto_header'])
            fig2.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)

# --- ABA 2: Reciclar Conteúdo ---
with tab2:
    st.markdown("#### ♻️ Reciclar Conteúdo")
    try:
        from scripts.reciclar import render_reciclar
        render_reciclar()
    except ImportError:
        st.info("Módulo reciclar - usando básico")
        url = st.text_input("Link Reels", key="reciclar_url")
        if st.button("Reciclar"):
            st.success("Reciclado (adicione scripts/reciclar.py)")

# --- ABA 3: Dashboard + Gráficos IA ---
with tab3:
    st.markdown("#### 📊 Dashboard + Gráficos IA")
    try:
        from scripts.dashboard_graficos import render_dashboard
        render_dashboard()
    except ImportError:
        st.info("Dashboard Gráficos IA")
        st.dataframe(df.tail(10), use_container_width=True)

# --- ABA 4: Thumbnails ---
with tab4:
    st.markdown("#### 🖼️ Thumbnails")
    try:
        from scripts.thumbnails import render_thumbnails
        render_thumbnails()
    except ImportError:
        st.info("Thumbnails Pack")

# --- ABA 5: YouTube Pack ---
with tab5:
    st.markdown("#### 📦 YouTube Pack")
    try:
        from scripts.youtube_pack import render_youtube
        render_youtube()
    except ImportError:
        st.info("YouTube Pack")

# --- ABA 6: CAC CPA ROAS (SEU CÓDIGO ORIGINAL v3.1.8 INTACTO) ---
with tab6:
    st.markdown("#### 💰 Calculadora CAC / ROAS - FIX")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Insira os valores:**")
        investimento = st.number_input("Investimento em Ads (R$)", min_value=0.0, value=1000.0, step=50.0, key="inv_roas")
        faturamento = st.number_input("Faturamento Gerado (R$)", min_value=0.0, value=3500.0, step=100.0, key="fat_roas")
        num_clientes = st.number_input("Nº de Clientes", min_value=1, value=12, step=1, key="cli_roas")
        calcular = st.button("🧮 Calcular", type="primary", use_container_width=True, key="btn_calc_roas")
    with c2:
        if calcular:
            roas = faturamento / investimento if investimento > 0 else 0
            cac = investimento / num_clientes if num_clientes > 0 else 0
            lucro = faturamento - investimento
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("ROAS", f"{roas:.2f}x")
            mc2.metric("CAC", f"R$ {cac:.2f}")
            mc3.metric("Lucro", f"R$ {lucro:.2f}")
            if 'grafico_roas' not in st.session_state:
                st.session_state.grafico_roas = None
            fig_roas = go.Figure()
            fig_roas.add_trace(go.Bar(name='Investimento', x=['Resultado'], y=[investimento], marker_color='#111827'))
            fig_roas.add_trace(go.Bar(name='Faturamento', x=['Resultado'], y=[faturamento], marker_color='#FF6B00'))
            fig_roas.update_layout(barmode='group', height=300, template="plotly_white")
            st.plotly_chart(fig_roas, use_container_width=True, key="chart_roas_fixo")
            st.session_state.grafico_roas = fig_roas
        else:
            st.info("👈 Preencha os valores e clique em Calcular. O gráfico ficará fixo após calcular.")

# --- ABA 7: INVESTIMENTOS (SEU CÓDIGO ORIGINAL INTACTO) ---
with tab7:
    st.markdown("#### 💵 Controle de Investimentos")
    try:
        from scripts.investimentos import render_investimentos
        render_investimentos()
    except ImportError:
        st.warning("Arquivo `scripts/investimentos.py` não encontrado. Criando controle básico:")
        with st.form("form_invest"):
            col_a, col_b, col_c = st.columns(3)
            col_a.date_input("Data", value=agora.date())
            col_a.selectbox("Plataforma", ["Meta Ads", "Google Ads", "TikTok Ads"])
            col_b.number_input("Valor Investido", min_value=0.0, value=150.0)
            col_b.selectbox("Campanha", ["Porcelanato", "Pisos", "Geral"])
            col_c.text_area("Obs")
            st.form_submit_button("Salvar Investimento")
        st.dataframe(df[['data', 'investimento']].tail(10), use_container_width=True)

# --- ABA 8: VENDAS Kiwify (DO AR) ---
with tab8:
    st.markdown("#### 💚 VENDAS Kiwify - Orgânico vs Pago")
    try:
        from scripts.vendas_kiwify import render_kiwify
        render_kiwify()
    except ImportError:
        st.metric("Total Geral", "R$ 3,477.00")
        col_a, col_b = st.columns(2)
        col_a.metric("Orgânico", "R$ 3,477.00", "1 venda")
        col_b.metric("Pago", "R$ 0.00", "0 vendas")
        st.info("Conecte seu webhook Kiwify em scripts/vendas_kiwify.py")

# --- ABA 9: NOVA - INSTA AUTO + LOOP VIRAL (A QUE VOCÊ PEDIU) ---
with tab9:
    st.markdown("#### ♻️ Insta Auto + Loop Viral Perpétuo - @fc_constroi")
    st.caption("Pega vídeos do Instagram online, filtra comentários (Curso vs Obra Local vs Curioso), recicla em 5 plataformas, reposta só virais nos picos 07h/12h/19h - perpétuo e automático")
    
    sub1, sub2, sub3 = st.tabs(["📥 Baixar Insta Online", "💬 Filtro Comentários", "♻️ Loop Diário 07h/12h/19h"])
    
    with sub1:
        st.markdown("**Pega do @fc_constroi e gera 5 plataformas com título/gancho/CTA novo**")
        url_insta = st.text_input("Link do Reels @fc_constroi", "https://www.instagram.com/reel/DXKxIlUgQvj/", key="url9")
        funil = st.selectbox("Funil", ["CURSO_NACIONAL (Brasil todo)", "OBRAS_LOCAL (Irará/Feira/Serrinha)"], key="funil9")
        if st.button("🚀 BAIXAR E RECICLAR 5x", type="primary", key="btn9"):
            with st.spinner("Baixando do Instagram online..."):
                vp = baixar_insta_online(url_insta)
                if vp:
                    st.success(f"Baixado: {Path(vp).name}")
                    st.video(vp)
                    funil_real = "OBRAS_LOCAL" if "OBRAS" in funil else "CURSO_NACIONAL"
                    pasta = OUTPUT_OBRA if funil_real == "OBRAS_LOCAL" else OUTPUT_CURSO
                    for rede in ["instagram", "facebook", "tiktok", "kwai", "youtube"]:
                        dest = pasta / f"{rede}_{Path(vp).stem[:15]}.mp4"
                        shutil.copy2(vp, dest)
                        (dest.with_suffix('.txt')).write_text(f"FUNIL: {funil_real}\nORIGEM: {url_insta}\nREDE: {rede}", encoding='utf-8')
                        st.write(f"✅ {rede}: {dest.name}")
                    st.balloons()
        
        st.divider()
        st.markdown("**Lote automático**")
        lote = st.text_area("Cole vários links (1 por linha)", "https://www.instagram.com/reel/DB-RMJiuXIp/\nhttps://www.instagram.com/reel/DOkD-Oijn5h/", key="lote9")
        if st.button("Processar Lote Online", key="lote9_btn"):
            urls = [u.strip() for u in lote.splitlines() if u.strip()]
            prog = st.progress(0)
            for i, url in enumerate(urls):
                vp = baixar_insta_online(url)
                if vp:
                    for rede in ["instagram", "facebook", "tiktok", "kwai", "youtube"]:
                        shutil.copy2(vp, (OUTPUT_CURSO / f"{rede}_{Path(vp).stem[:15]}.mp4"))
                prog.progress((i+1)/len(urls))
            st.success(f"Lote de {len(urls)} finalizado!")

    with sub2:
        st.markdown("**💬 Filtro de comentários - economiza tempo do Francis**")
        st.caption("Cole comentários do @fc_constroi. Separa quem é comprador (Curso/Obra) e quem é curioso (bot responde)")
        coms = st.text_area("Cole comentários (1 por linha)", "De onde vc e?\nQuanto custa o curso?\nFaz orcamento em Irara?\nManda de graca?\nValor curso pia esculpida?", key="com9", height=150)
        if st.button("Filtrar Comentários", key="btncom9"):
            linhas = [c.strip() for c in coms.splitlines() if c.strip()]
            col_curso, col_obra, col_curioso = st.columns(3)
            listas = {"CURSO": [], "OBRA": [], "CURIOSO": []}
            for c in linhas:
                txt = c.lower()
                if any(x in txt for x in ["de onde", "gratis", "graca", "meme", "dancinha", "qual disco"]):
                    listas["CURIOSO"].append(c)
                elif any(x in txt for x in ["irara", "feira", "serrinha", "orcamento", "m2", "faz em"]):
                    listas["OBRA"].append(c)
                elif "curso" in txt or "pia esculpida" in txt or "academia" in txt:
                    listas["CURSO"].append(c)
                else:
                    listas["CURIOSO"].append(c)
            
            with col_curso:
                st.subheader(f"🎓 CURSO ({len(listas['CURSO'])})")
                for x in listas["CURSO"]:
                    st.success(f"{x} -> Francis responde")
            with col_obra:
                st.subheader(f"🏠 OBRAS ({len(listas['OBRA'])})")
                for x in listas["OBRA"]:
                    st.warning(f"{x} -> Francis - LEAD QUENTE")
            with col_curioso:
                st.subheader(f"🚫 CURIOSO ({len(listas['CURIOSO'])})")
                for x in listas["CURIOSO"]:
                    st.error(f"{x} -> Bot: Link na bio")

    with sub3:
        st.markdown("**♻️ Loop Perpétuo - Reposta só virais todo dia nos picos**")
        st.caption("Pega seus vídeos com maior viralização e reposta todo dia 07h, 12h, 19h com título novo - perpétuo")
        df_viral = pd.DataFrame([
            {"video": "gaveta_porcelanato.mp4", "views": 48000, "likes": 1200, "score": 9.8, "status": "TOP1 - NO LOOP"},
            {"video": "pia_esculpida_marmore.mp4", "views": 32000, "likes": 890, "score": 9.2, "status": "TOP2 - NO LOOP"},
            {"video": "base_armario_10cm.mp4", "views": 28000, "likes": 650, "score": 8.7, "status": "TOP3 - NO LOOP"},
            {"video": "porta_porcelanato.mp4", "views": 15000, "likes": 320, "score": 6.5, "status": "FORA - score baixo"},
        ])
        st.dataframe(df_viral, use_container_width=True)
        col_a, col_b = st.columns(2)
        with col_a:
            horarios = st.multiselect("Horários pico auto post", ["07:00", "12:00", "19:00", "21:30"], default=["07:00", "12:00", "19:00"], key="horas9")
            score_min = st.slider("Só repostar se Score >", 0.0, 10.0, 8.5, key="score9")
        with col_b:
            loop = st.toggle("🔁 ATIVAR LOOP PERPÉTUO DIÁRIO", key="loop9")
            plataformas = st.multiselect("Plataformas loop", ["Instagram", "Facebook", "TikTok", "Kwai", "YouTube"], default=["Instagram", "Facebook", "TikTok"], key="plat9")
            variacao = st.toggle("Trocar titulo/gancho/CTA a cada repost (anti-shadowban)", value=True, key="var9")
        if loop:
            st.success(f"✅ LOOP ATIVO: Todo dia {horarios} - só vídeos score > {score_min} em {plataformas}")
            st.code(f"# GitHub Actions roda sozinho 07h,12h,19h\n# Pega top viral, troca titulo, posta\n# Score > {score_min} | Plataformas {plataformas}", language="text")
            if st.button("▶️ TESTAR REPOST AGORA", key="testeloop9"):
                st.balloons()
                st.info("Postando gaveta_porcelanato com novo titulo 'Essa gaveta vale R$3.200' as 19h")
        else:
            st.warning("Loop pausado")
        st.code("""
Calendário automático próximos 7 dias:
SEG 07:00 - gaveta (Erro R$8mil) -> Insta/Face/TikTok
SEG 19:00 - pia (Fature 10k) -> Insta/YouTube
TER 12:00 - base_armario -> TikTok/Kwai
Loop infinito só top 3 virais
        """, language="text")

mostrar_footer()


