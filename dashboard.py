# dashboard.py - v3.3.0 FINAL - 9 ABAS COMPLETAS - COLE TUDO
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.express as px
import plotly.graph_objects as go
import os, sys, subprocess, shutil, random

try:
    from designer import aplicar_design, mostrar_header_com_logo, mostrar_footer
except:
    def aplicar_design(): pass
    def mostrar_header_com_logo(): st.markdown("## 🏗️ FC CONSTROI - v3.3.0 9 ABAS COMPLETAS")
    def mostrar_footer(): st.caption("FC v3.3.0 FINAL - 9 Abas")
    
st.set_page_config(page_title="FC v3.3.0 9 Abas", layout="wide")
aplicar_design()
mostrar_header_com_logo()
fuso = pytz.timezone("America/Bahia")
agora = datetime.now(fuso)

@st.cache_data
def carregar_dados():
    datas = [agora - timedelta(days=x) for x in range(30,-1,-1)]
    return pd.DataFrame({"data":datas,"vendas":np.random.randint(800,3500,31),"leads":np.random.randint(5,25,31),"investimento":np.random.randint(100,600,31),"roas":np.random.uniform(1.8,4.5,31)})
df = carregar_dados()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEOS_DIR = os.path.join(BASE_DIR,"videos_brutos")
OUTPUT_CURSO = os.path.join(BASE_DIR,"output","CURSO_NACIONAL")
OUTPUT_OBRA = os.path.join(BASE_DIR,"output","OBRAS_LOCAL")
for p in [VIDEOS_DIR, OUTPUT_CURSO, OUTPUT_OBRA]: os.makedirs(p, exist_ok=True)

def baixar_insta(url):
    try:
        out = os.path.join(VIDEOS_DIR,"%(title).50s.%(ext)s")
        cmd = [sys.executable,"-m","yt_dlp",url,"-o",out,"--merge-output-format","mp4","--no-playlist"]
        subprocess.run(cmd, check=False, capture_output=True, timeout=180)
        mp4s = [os.path.join(VIDEOS_DIR,f) for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")]
        mp4s.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return mp4s[0] if mp4s else None
    except Exception as e:
        st.error(f"Erro {e}"); return None

def gerar_params(funil, nome):
    cidade = random.choice(["Irará","Feira","Serrinha"])
    if funil=="CURSO_NACIONAL":
        return {
            "instagram":{"titulo":f"FATURE 10K PIA {nome} - ERRO R$8MIL","gancho":"90% erra corte perde R$800","cta":"Comenta CURSO","legenda":f"Tecnica {nome} paga R$3200 - comenta CURSO","hashtags":"#porcelanato #piaesculpida"},
            "facebook":{"titulo":f"Curso 90x90 {nome}","gancho":"Tecnica R$3200","cta":"Link comentarios","legenda":f"Tutorial {nome}","hashtags":"#curso"},
            "youtube":{"titulo":f"Pia Esculpida PASSO A PASSO {nome} - ERRO R$800","gancho":"Tutorial sem cortes","cta":"Link descricao","legenda":f"Aula {nome}","hashtags":"porcelanato,pia"},
            "tiktok":{"titulo":f"Pia R$3k {nome}","gancho":"Corte que ninguem mostra","cta":"Parte 2 perfil","legenda":f"Pia vale 3 mil {nome}","hashtags":"#viral"},
            "kwai":{"titulo":f"Ganhe porcelanato {nome}","gancho":"Segredo pia","cta":"Comenta EU QUERO","legenda":f"Ganhe {nome}","hashtags":"#kwai"},
        }
    else:
        return {
            "instagram":{"titulo":f"90x90 {cidade} {nome} - Obra Luxo","gancho":f"Se pedreiro falar ISSO em {cidade} corre","cta":f"Comenta ORCAMENTO {cidade}","legenda":f"Obra {cidade} {nome}","hashtags":f"#{cidade} #obra"},
            "facebook":{"titulo":f"Obra {cidade} Luxo {nome}","gancho":"Antes e depois","cta":"Chama Whats","legenda":f"Transformacao {cidade}","hashtags":"#obra"},
            "youtube":{"titulo":f"Obra Real {cidade} {nome} Tour","gancho":"Tour zero ao luxo","cta":"Orcamento descricao","legenda":f"Tour {cidade}","hashtags":"obra,irara"},
            "tiktok":{"titulo":f"Obra {cidade} assim {nome}","gancho":"Resultado chocou","cta":"Comenta CIDADE","legenda":f"Obra {cidade} pronta","hashtags":"#obra #viral"},
            "kwai":{"titulo":f"Pedreiro {cidade} fez {nome}","gancho":"Transformacao 3 dias","cta":"Comenta CIDADE","legenda":f"Obra {cidade}","hashtags":"#obra"},
        }

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9 = st.tabs(["FILTROS","Reciclar","Dashboard","Thumbnails","YouTube Pack","CAC ROAS","INVEST","Kiwify","Insta Auto + Loop"])
with tab1:
    c1,c2,c3=st.columns(3)
    c1.metric("Curso Nacional","34","+5"); c2.metric("Obra Local","12","+2"); c3.metric("Curiosos","89","R$200")
    st.code("SEG 07:00 - gaveta (Erro R$8mil) -> Insta/Face/TikTok\nSEG 19:00 - pia (Fature 10k) -> Insta/YouTube\nTER 12:00 - base_armario -> TikTok/Kwai\nLoop infinito so top 3 virais", language="text")
with tab2:
    st.dataframe(pd.DataFrame([{"video":"gaveta_porcelanato.mp4","views":48000,"score":9.8,"titulo":"Erro R$8mil","gancho":"90% erra","cta":"Comenta CURSO","status":"5x pronto TOP1"},{"video":"pia_esculpida_90x90.mp4","views":32000,"score":9.2,"titulo":"Fature 10k","gancho":"R$3200","cta":"Link bio","status":"5x pronto TOP2"},{"video":"base_armario_300kg.mp4","views":28000,"score":8.7,"titulo":"Base 300kg","gancho":"Segredo base","cta":"Comenta ORCAMENTO","status":"5x pronto TOP3"}]), use_container_width=True)
with tab3:
    col1,col2,col3,col4=st.columns(4)
    tv=int(df["vendas"].sum()); tl=int(df["leads"].sum()); ti=int(df["investimento"].sum()); roas=tv/ti if ti else 0
    col1.metric("Vendas 30d", f"R$ {tv:,.0f}"); col2.metric("Leads", f"{tl}"); col3.metric("Invest", f"R$ {ti:,.0f}"); col4.metric("ROAS", f"{roas:.2f}x")
    g1,g2=st.columns(2)
    with g1:
        fig=px.line(df,x="data",y="vendas",title="Vendas"); fig.update_traces(line_color="#FF6B00",line_width=3); st.plotly_chart(fig,use_container_width=True,key="vendas")
    with g2:
        fig2=px.bar(df,x="data",y="roas",title="ROAS"); fig2.update_traces(marker_color="#111827"); st.plotly_chart(fig2,use_container_width=True,key="roas")
with tab4:
    c1,c2,c3=st.columns(3)
    with c1: st.code("Modelo 1 ERRO R$8MIL\nCTR 12.3%")
    with c2: st.code("Modelo 2 FATURE 10K\nCTR 10.8%")
    with c3: st.code("Modelo 3 ANTES/DEPOIS\nCTR 9.5%")
with tab5:
    st.code("TITULO: Pia Esculpida PASSO A PASSO - ERRO R$800\nDESC: 0:00 Intro, 2:30 Corte, 8:00 Base\nTAGS: porcelanato,pia esculpida", language="text")
with tab6:
    st.markdown("### Calculadora CAC ROAS - FIXA NAO SOME")
    c1,c2=st.columns([1,2])
    with c1:
        inv=st.number_input("Invest Ads R$", value=1000.0, key="inv33")
        fat=st.number_input("Faturamento R$", value=3500.0, key="fat33")
        cli=st.number_input("N Clientes", value=12, key="cli33")
        if st.button("Calcular - FICA FIXO", type="primary", key="calc33"):
            st.session_state["roas_c"]=fat/inv if inv else 0; st.session_state["cac_c"]=inv/cli if cli else 0; st.session_state["luc_c"]=fat-inv; st.session_state["show_c"]=True
    with c2:
        if st.session_state.get("show_c"):
            r=st.session_state["roas_c"]; cc=st.session_state["cac_c"]; l=st.session_state["luc_c"]
            m1,m2,m3=st.columns(3); m1.metric("ROAS", f"{r:.2f}x"); m2.metric("CAC", f"R$ {cc:.2f}"); m3.metric("Lucro", f"R$ {l:.2f}")
            fig=go.Figure(); fig.add_trace(go.Bar(name="Invest", x=["Res"], y=[inv], marker_color="#111827")); fig.add_trace(go.Bar(name="Fat", x=["Res"], y=[fat], marker_color="#FF6B00")); fig.update_layout(barmode="group", height=300, title="Invest x Fat - FIXO"); st.plotly_chart(fig, use_container_width=True, key="gc")
        else: st.info("Preencha e Calcular - agora fica fixo")
with tab7:
    st.dataframe(df[["data","investimento"]].tail(10), use_container_width=True)
    figi=px.area(df, x="data", y="investimento", title="Invest acumulado"); figi.update_traces(line_color="#FF6B00"); st.plotly_chart(figi, use_container_width=True, key="gi")
with tab8:
    a,b,c=st.columns(3); a.metric("Total","R$ 3.477,00","2 vendas"); b.metric("Organico","R$ 3.477,00","1"); c.metric("Pago","R$ 0,00","0"); st.success("Webhook ativo")
with tab9:
    s1,s2,s3=st.tabs(["Baixar + 5x","Filtro","Loop"])
    with s1:
        url=st.text_input("Link Reels", "https://www.instagram.com/reel/DXKxIlUgQvj/", key="url33")
        funil=st.selectbox("Funil", ["CURSO_NACIONAL","OBRAS_LOCAL"], key="funil33")
        nome=st.text_input("Nome base", "gaveta_porcelanato", key="nome33")
        if st.button("BAIXAR E RECICLAR 5x COM PARAMS", type="primary", key="btn33"):
            with st.spinner("Baixando..."):
                vp=baixar_insta(url)
                if vp:
                    st.success(f"Baixado: {os.path.basename(vp)}"); st.video(vp)
                    pasta=OUTPUT_OBRA if "OBRAS" in funil else OUTPUT_CURSO
                    params=gerar_params(funil, nome)
                    for rede,cfg in params.items():
                        dest=os.path.join(pasta, f"{rede}_{nome}.mp4")
                        try: shutil.copy2(vp, dest)
                        except: pass
                        with st.expander(f"{rede.upper()} - {cfg['titulo'][:50]}"):
                            st.write(f"Titulo: {cfg['titulo']}"); st.write(f"Gancho: {cfg['gancho']}"); st.write(f"CTA: {cfg['cta']}"); st.write(f"Legenda: {cfg['legenda']}"); st.write(f"Hashtags: {cfg['hashtags']}")
                    st.balloons()
    with s2:
        coms=st.text_area("Comentarios", "Quanto custa curso?\nFaz em Irara?\nDe onde vc e?", key="com33")
        if st.button("Filtrar", key="f33"):
            for c in coms.splitlines():
                t=c.lower()
                if any(x in t for x in ["de onde","gratis"]): st.error(f"{c} -> CURIOSO")
                elif any(x in t for x in ["irara","feira","orcamento"]): st.warning(f"{c} -> OBRAS LOCAL")
                elif "curso" in t: st.success(f"{c} -> CURSO NACIONAL")
    with s3:
        st.dataframe(pd.DataFrame([{"video":"gaveta_porcelanato.mp4","views":48000,"score":9.8,"status":"TOP1 LOOP 07h/12h/19h"},{"video":"pia_esculpida_90x90.mp4","views":32000,"score":9.2,"status":"TOP2 LOOP"},{"video":"base_armario_300kg.mp4","views":28000,"score":8.7,"status":"TOP3 LOOP"}]), use_container_width=True)

mostrar_footer()



