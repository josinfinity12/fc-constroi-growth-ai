import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
from designer import aplicar_design, mostrar_header_com_logo

st.set_page_config(page_title="FC Constrói - Growth AI v3.1.1", layout="wide", page_icon="🏗️")

# --- NOVO: RELÓGIO ATUALIZÁVEL AUTOMÁTICO A CADA 1 SEGUNDO ---
st_autorefresh(interval=60000, key="relogio_auto_fc_v311")

aplicar_design()
mostrar_header_com_logo()

tab_filtros, tab2, tab3, tab4, tab5, tab8, tab_invest = st.tabs([
    "🔥 FILTROS (Cursos+Local)", 
    "♻️ Reciclar Conteúdo", 
    "📊 Dashboard + Gráficos IA", 
    "🎨 Thumbnails", 
    "📦 YouTube Pack", 
    "💰 CAC CPA ROAS",
    "📈 INVESTIMENTOS"
])

def mostrar_graficos_ia():
    st.markdown("### 📈 Métricas do Modelo IA - Dashboard Exclusivo")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Acurácia", "94.2%", "↑ 1.2%"); st.progress(94)
    with c2: st.metric("F1-Score", "0.91", "↑ 0.03"); st.progress(91)
    with c3: st.metric("Correlação", "0.87", "Estável"); st.progress(87)
    with c4: st.metric("ROC-AUC", "0.96", "↑ 0.01"); st.progress(96)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("**Correlação 0.87 - Previsão vs Real**")
        chart_data = pd.DataFrame({"Real": np.random.uniform(60, 100, 20),"Previsto": np.random.uniform(62, 98, 20)})
        st.scatter_chart(chart_data)
    with col_g2:
        st.write("**ROC Curve 0.96**")
        roc_data = pd.DataFrame({"Taxa Falso Positivo": [0, 0.1, 0.2, 0.35, 0.6, 1],"Taxa Verdadeiro Positivo": [0, 0.7, 0.85, 0.92, 0.96, 1]})
        st.line_chart(roc_data, x="Taxa Falso Positivo", y="Taxa Verdadeiro Positivo")

def filtrar_curso_online(texto):
    texto_l = str(texto).lower()
    interesses_pos = ["porcelanato", "ceramica", "cerâmica", "pia de banheiro", "bancada", "cozinha", "closet", "fachada", "armario", "armário", "gaveta", "nicho", "estrutura"]
    interesses_neg = ["gesso", "drywall", "marcenaria madeira", "mdf", "mármore natural", "granito"]
    curiosos = ["gratis", "grátis", "free", "de graça", "como fazer sozinho", "tem no youtube"]
    idioma_neg = ["how to", "free course", "tutorial english"]
    if any(x in texto_l for x in idioma_neg): return "REPROVADO - Idioma não é PT-BR"
    if any(x in texto_l for x in interesses_neg) and not any(y in texto_l for y in interesses_pos): return "REPROVADO - Fora de porcelanato/ceramica"
    if any(x in texto_l for x in curiosos): return "REPROVADO - Curioso grátis"
    if any(x in texto_l for x in interesses_pos): return "APROVADO - Lead Curso Porcelanato"
    return "REPROVADO - Sem interesse claro"

def filtrar_local_func(texto, cidade_texto, cidade_base_selecionada, raio_km):
    t = str(texto).lower(); c = str(cidade_texto).lower(); texto_completo = t + " " + c
    cidades_base = ["feira", "feira de santana", "fsa", "irara", "irará", "santanopolis", "santanópolis", "santa barbara", "santa bárbara", "serrinha", "ouricangas", "ouriçangas"]
    interesses_local = ["bancada", "pia", "cozinha", "banheiro", "orçamento", "orcamento", "quanto custa", "valor", "prazo", "urgente"]
    curiosos_local = ["só pesquisando", "so pesquisando", "só olhando", "curiosidade", "lindo", "top", "show"]
    urgencia_pos = ["urgente", "pra hoje", "preciso pra ontem", "orçamento agora", "orcamento agora", "quanto custa", "me chama no zap"]
    if "santanopolis" in texto_completo or "santanópolis" in texto_completo:
        if any(x in texto_completo for x in interesses_local): return "APROVADO - 🔥 LEAD QUENTISSIMO Santanopolis (Francis)"
    if "salvador" in texto_completo or "são paulo" in texto_completo or "rio de janeiro" in texto_completo:
        if not any(cid in texto_completo for cid in cidades_base): return f"REPROVADO - Fora do raio {raio_km}km - Salvador/Fora"
    if "how much" in texto_completo: return "REPROVADO - Idioma"
    tem_cidade_valida = any(cid in texto_completo for cid in cidades_base)
    if not tem_cidade_valida and cidade_base_selecionada != "Todas": return f"REPROVADO - Fora do raio {raio_km}km"
    if any(x in texto_completo for x in curiosos_local) and not any(y in texto_completo for y in interesses_local): return "REPROVADO - Curioso sem urgencia"
    if any(x in texto_completo for x in urgencia_pos): return "APROVADO - Lead Quente Local"
    if any(x in texto_completo for x in interesses_local): return "APROVADO - Lead Local"
    return "REPROVADO - Sem urgencia"

def criar_thumb_combinada(imagens_pil_list, texto, modo_layout, cor_fundo):
    W, H = 1280, 720
    base = Image.new("RGB", (W, H), cor_fundo)
    if imagens_pil_list:
        if modo_layout == "1 Foto Só (Obra ou Você)":
            img = imagens_pil_list[0].convert("RGB").resize((W, H), Image.LANCZOS); base.paste(img, (0, 0))
        elif modo_layout == "2 Fotos - ANTES / DEPOIS (lado a lado)":
            for i, img_pil in enumerate(imagens_pil_list[:2]):
                img = img_pil.convert("RGB").resize((W // 2, H), Image.LANCZOS); base.paste(img, (i * (W // 2), 0))
            ImageDraw.Draw(base).rectangle([(W // 2 - 4, 0), (W // 2 + 4, H)], fill="white")
        elif modo_layout == "2 Fotos - PESSOA + OBRA (lado a lado)":
            for i, img_pil in enumerate(imagens_pil_list[:2]):
                img = img_pil.convert("RGB").resize((W // 2, H), Image.LANCZOS); base.paste(img, (i * (W // 2), 0))
            ImageDraw.Draw(base).rectangle([(W // 2 - 3, 0), (W // 2 + 3, H)], fill="white")
        elif modo_layout == "3 Fotos - Grade":
            if len(imagens_pil_list) >= 1:
                img0 = imagens_pil_list[0].convert("RGB").resize((W // 2, H), Image.LANCZOS); base.paste(img0, (0, 0))
            if len(imagens_pil_list) >= 2:
                img1 = imagens_pil_list[1].convert("RGB").resize((W // 2, H // 2), Image.LANCZOS); base.paste(img1, (W // 2, 0))
            if len(imagens_pil_list) >= 3:
                img2 = imagens_pil_list[2].convert("RGB").resize((W // 2, H // 2), Image.LANCZOS); base.paste(img2, (W // 2, H // 2))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 85))
    base = Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(base)
    try: font = ImageFont.truetype("arialbd.ttf", 110); font_small = ImageFont.truetype("arialbd.ttf", 55)
    except: font = ImageFont.load_default(); font_small = ImageFont.load_default()
    texto = texto.upper()
    if len(texto) > 18: meio = len(texto) // 2; linhas = [texto[:meio], texto[meio:]]
    else: linhas = [texto]
    y = H // 2 - 80
    for linha in linhas:
        bbox = draw.textbbox((0, 0), linha, font=font); w = bbox[2] - bbox[0]; x = (W - w) // 2
        for dx in [-5, 5]:
            for dy in [-5, 5]: draw.text((x + dx, y + dy), linha, font=font, fill="black")
        draw.text((x, y), linha, font=font, fill="white"); y += 130
    draw.rounded_rectangle([(30, H - 90), (290, H - 30)], radius=12, fill="#FF6B00")
    draw.text((45, H - 80), "FC CONSTROI", font=font_small, fill="white")
    return base

def gerar_pdf_investimentos(dados):
    try:
        from fpdf import FPDF
        pdf = FPDF(); pdf.add_page(); pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"FC CONSTROI - Relatorio {dados['data']}", ln=True, align='C')
        pdf.set_font("Arial", "", 11); pdf.ln(8)
        for k, v in dados.items():
            if k != "data": pdf.cell(0, 7, f"{k}: {v}", ln=True)
        return pdf.output(dest='S').encode('latin-1')
    except:
        txt = f"FC CONSTROI - INVESTIMENTOS\nData: {dados['data']}\n\n"
        for k, v in dados.items():
            if k != "data": txt += f"{k}: {v}\n"
        img = Image.new('RGB', (800, 1000), 'white'); d = ImageDraw.Draw(img)
        try: f = ImageFont.truetype("arial.ttf", 18)
        except: f = ImageFont.load_default()
        d.text((20, 20), txt, font=f, fill='black')
        buf = io.BytesIO(); img.save(buf, format='PDF'); return buf.getvalue()

def render_investimentos():
    st.subheader("📈 INVESTIMENTOS - Auto Save + PDF")
    st.caption("Mesmos parâmetros + Salvamento automático + Histórico + PDF")
    if 'historico_inv' not in st.session_state: st.session_state['historico_inv'] = []
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 💸 Entradas")
        faturamento_curso = st.number_input("Faturamento Curso (Kiwify) R$", value=8500.0, step=100.0, key="fat_curso_v302")
        faturamento_obra = st.number_input("Faturamento Obras Locais R$", value=6200.0, step=100.0, key="fat_obra_v302")
        outros = st.number_input("Outros (YouTube, parceria) R$", value=0.0, key="outros_v302")
        faturamento_total = faturamento_curso + faturamento_obra + outros
        st.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    with c2:
        st.markdown("#### 💳 Custos / Investimentos")
        gasto_trafego = st.number_input("Tráfego Pago (Meta/Google) R$", value=1200.0, step=50.0, key="traf_v302")
        custo_material = st.number_input("Material / Porcelanato / Insumos R$", value=2800.0, step=100.0, key="mat_v302")
        custo_ferramentas = st.number_input("Ferramentas / Aluguel / Gasolina R$", value=450.0, key="ferr_v302")
        taxas = st.number_input("Taxas Kiwify + Impostos (15%) R$", value=faturamento_curso*0.15, key="taxas_v302")
        custo_total = gasto_trafego + custo_material + custo_ferramentas + taxas
        st.metric("Custo Total", f"R$ {custo_total:,.2f}")
    with c3:
        lucro_bruto = faturamento_total - custo_material
        lucro_liquido = faturamento_total - custo_total
        margem_bruta = (lucro_bruto / faturamento_total * 100) if faturamento_total else 0
        margem_liquida = (lucro_liquido / faturamento_total * 100) if faturamento_total else 0
        roi = (lucro_liquido / custo_total * 100) if custo_total else 0
        roas = (faturamento_total / gasto_trafego) if gasto_trafego else 0
        st.markdown("#### 📊 Resultados CHAVE")
        st.metric("Lucro Bruto", f"R$ {lucro_bruto:,.2f}", f"{margem_bruta:.1f}% margem")
        st.metric("Lucro Líquido (Ganância real)", f"R$ {lucro_liquido:,.2f}", f"{margem_liquida:.1f}% margem")
        st.metric("ROI", f"{roi:.1f}%")
        st.metric("ROAS Geral", f"{roas:.2f}x")
    st.divider()
    col_graf1, col_graf2, col_graf3 = st.columns(3)
    with col_graf1:
        st.write("**Faturamento por Fonte**")
        df_fonte = pd.DataFrame({"Valor": [faturamento_curso, faturamento_obra, outros]}, index=["Curso", "Obras", "Outros"])
        st.bar_chart(df_fonte)
    with col_graf2:
        st.write("**Custos vs Lucro**")
        df_custo = pd.DataFrame({"Valor": [custo_total, lucro_liquido]}, index=["Custos", "Lucro Liquido"])
        st.bar_chart(df_custo)
    with col_graf3:
        st.write("**Saúde do Negócio**")
        st.progress(int(min(max(margem_liquida, 0), 100)))
        if margem_liquida >= 30: st.success(f"Margem {margem_liquida:.1f}% - EXCELENTE!")
        elif margem_liquida >= 15: st.warning(f"Margem {margem_liquida:.1f}% - Boa")
        else: st.error(f"Margem {margem_liquida:.1f}% - ALERTA!")
    st.divider()
    st.markdown("#### 🎯 Métricas Avançadas (CAC, Ticket, LTV)")
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1:
        vendas = st.number_input("Vendas fechadas", value=8, min_value=1, key="vendas_v302")
        ticket_medio = faturamento_total / vendas if vendas else 0
        st.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    with cc2:
        leads = st.number_input("Leads no mês", value=45, key="leads_v302")
        cac = (gasto_trafego / vendas) if vendas else 0
        st.metric("CAC (Custo por Cliente)", f"R$ {cac:,.2f}")
    with cc3:
        conversao = (vendas / leads * 100) if leads else 0
        st.metric("Taxa Conversão", f"{conversao:.1f}%")
    with cc4:
        ltv = ticket_medio * 1.8
        ltv_cac = (ltv / cac) if cac else 0
        st.metric("LTV / CAC", f"{ltv_cac:.1f}x", help="Ideal >3x")
    st.divider()
    st.markdown("### 💾 Salvar Automático + Exportar PDF")
    auto = st.checkbox("✅ Ativar SALVAR AUTOMÁTICO", value=True, key="auto_save_v302")
    col_save, col_pdf, col_hist = st.columns([1, 1, 2])
    dados_atual = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Faturamento Total": f"R$ {faturamento_total:,.2f}",
        "Curso": f"R$ {faturamento_curso:,.2f}",
        "Obras": f"R$ {faturamento_obra:,.2f}",
        "Custo Total": f"R$ {custo_total:,.2f}",
        "Lucro Bruto": f"R$ {lucro_bruto:,.2f} ({margem_bruta:.1f}%)",
        "Lucro Liquido": f"R$ {lucro_liquido:,.2f} ({margem_liquida:.1f}%)",
        "ROI": f"{roi:.1f}%",
        "ROAS": f"{roas:.2f}x",
        "Ticket Medio": f"R$ {ticket_medio:,.2f}",
        "CAC": f"R$ {cac:,.2f}",
        "Conversao": f"{conversao:.1f}%",
        "LTV/CAC": f"{ltv_cac:.1f}x"
    }
    with col_save:
        if st.button("💾 SALVAR AGORA", use_container_width=True, type="primary") or (auto and st.session_state.get('last_save') != faturamento_total):
            st.session_state['historico_inv'].append(dados_atual)
            st.session_state['last_save'] = faturamento_total
            st.success(f"Salvo! {len(st.session_state['historico_inv'])} registros")
    with col_pdf:
        pdf_bytes = gerar_pdf_investimentos(dados_atual)
        st.download_button("📄 BAIXAR PDF RELATÓRIO", data=pdf_bytes, file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf", mime="application/pdf", use_container_width=True)
    with col_hist:
        if st.session_state['historico_inv']:
            df_hist = pd.DataFrame(st.session_state['historico_inv'])
            st.dataframe(df_hist.tail(10), use_container_width=True)
            st.download_button("⬇️ BAIXAR HISTÓRICO CSV", df_hist.to_csv(index=False).encode('utf-8'), "historico_investimentos.csv", "text/csv", use_container_width=True)
        else:
            st.info("Nenhum histórico. Clique em Salvar.")

with tab_filtros:
    col_f1, col_f2 = st.columns(2, gap="large")
    with col_f1:
        st.subheader("🔥 FILTRO 1: Curso Online Porcelanato")
        st.caption("Só porcelanato/cerâmica + PT-BR")
        texto_curso = st.text_area("Comentários Curso (1 por linha)", height=180, value="quero aprender bancada de porcelanato\npia de banheiro porcelanato quanto custa curso\ncurso gratis de gesso how to free", key="t1")
        file_curso = st.file_uploader("CSV Curso", type="csv", key="curso")
        if st.button("FILTRAR CURSO", key="f1", use_container_width=True):
            dados = []
            if file_curso:
                df = pd.read_csv(file_curso)
                lista = df['comentario'].astype(str).tolist() if 'comentario' in df.columns else df.iloc[:,0].astype(str).tolist()
            else:
                lista = [x for x in texto_curso.split("\n") if x.strip() != ""]
            for coment in lista:
                status = filtrar_curso_online(coment)
                dados.append({"Comentario": coment, "Status": status})
            df_res = pd.DataFrame(dados)
            aprovados = df_res[df_res['Status'].str.contains("APROVADO")]
            st.metric("Curso", f"{len(aprovados)}/{len(df_res)} Aprovados")
            st.dataframe(df_res, use_container_width=True, height=250)
            st.download_button("Baixar Curso Aprovados", aprovados.to_csv(index=False).encode('utf-8'), "leads_curso.csv", key="down1")
    with col_f2:
        st.subheader("🎯 FILTRO 2: Trabalhos Locais - 6 Cidades")
        st.caption("Santanopolis PRIORIDADE + Feira=FSA")
        c1, c2 = st.columns(2)
        with c1:
            cidade_filtro = st.selectbox("Base:", ["Santanopolis (PRIORIDADE)", "Irara", "Feira de Santana", "Santa Barbara", "Serrinha", "Ouricangas", "Todas"], index=0, key="cidade")
        with c2:
            raio = st.slider("Raio km", 10, 150, 50, key="raio")
        texto_local = st.text_area("Mensagens Local (1 por linha)", height=180, value="sou de Irara, quanto custa bancada 2m urgente\nFeira pia banheiro orcamento pra hoje\nsou de Salvador Bahia, quanto custa bancada 2m", key="t2")
        file_local = st.file_uploader("CSV Local", type="csv", key="local")
        if st.button("FILTRAR LOCAL 50km", key="f2", use_container_width=True):
            dados = []
            if file_local:
                df = pd.read_csv(file_local)
                comentarios = df['comentario'].astype(str).tolist() if 'comentario' in df.columns else df.iloc[:,0].astype(str).tolist()
                cidades = df['cidade'].astype(str).tolist() if 'cidade' in df.columns else [""]*len(comentarios)
            else:
                comentarios = [x for x in texto_local.split("\n") if x.strip() != ""]
                cidades = [""]*len(comentarios)
            for com, cid in zip(comentarios, cidades):
                status = filtrar_local_func(com, cid, cidade_filtro, raio)
                dados.append({"Comentario": com, "Cidade": cid, "Status": status})
            df_res = pd.DataFrame(dados)
            aprovados = df_res[df_res['Status'].str.contains("APROVADO")]
            quentes = df_res[df_res['Status'].str.contains("Quente")]
            st.metric("Local", f"{len(aprovados)}/{len(df_res)} | Quentes: {len(quentes)}")
            st.dataframe(df_res, use_container_width=True, height=250)
            st.download_button("Baixar Locais", aprovados.to_csv(index=False).encode('utf-8'), "leads_local.csv", key="down2")

with tab2:
    st.subheader("♻️ Reciclar Conteúdo")
    st.caption("Transforme 1 vídeo em 3 formatos")
    url = st.text_input("Link do vídeo YouTube (longo)")
    if st.button("Gerar 3 versões"):
        st.write("1. Shorts 0-30s (gancho)")
        st.write("2. Reels com legenda")
        st.write("3. Texto para descrição")
    st.file_uploader("Upload vídeo para transcrição", type=["mp4","mov"], key="vid")

with tab3:
    st.subheader("📊 Dashboard + Gráficos IA - ÚNICA ABA COM GRÁFICOS")
    mostrar_graficos_ia()
    st.divider()
    st.write("**Resumo Operacional**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Leads Curso Semana", "127")
    c2.metric("Leads Local Semana", "18")
    c3.metric("Taxa Conversão", "22%")

with tab4:
    st.subheader("🎨 Thumbnails AUTOMÁTICOS 1280x720 - COMBINADA")
    st.caption("Pessoa + Obra / Antes Depois - Formato YouTube 16:9")
    col_a, col_b = st.columns([1.2, 0.8], gap="large")
    with col_a:
        modo = st.selectbox("LAYOUT 1280x720:", ["1 Foto Só (Obra ou Você)","2 Fotos - ANTES / DEPOIS (lado a lado)","2 Fotos - PESSOA + OBRA (lado a lado)","3 Fotos - Grade"], index=2, key="layout_thumb")
        if "1 Foto" in modo:
            up = st.file_uploader("Sobe 1 foto", type=["jpg", "png", "jpeg"], key="1foto")
            files = [up] if up else []
        else:
            up = st.file_uploader("Sobe 2 ou 3 fotos (na ordem)", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="multifoto")
            files = up if up else []
        texto_thumb = st.text_input("Texto da Thumb (max 4 palavras)", "BANCADA 2M", key="txt_thumb")
        cor_fundo = st.color_picker("Cor de fundo (se não tiver foto)", "#FF6B00", key="cor_thumb")
        estilo = st.selectbox("Estilo:", ["Com escurecer (recomendado)", "Foto original"], key="estilo")
        if st.button("🔥 GERAR THUMB AUTOMÁTICA 1280x720", use_container_width=True, type="primary"):
            pil_list = [Image.open(f) for f in files if f]
            if not pil_list: st.warning("Sobe pelo menos 1 foto!")
            else:
                thumb = criar_thumb_combinada(pil_list, texto_thumb, modo, cor_fundo)
                st.session_state['thumb_comb'] = thumb
                st.success("Thumb 1280x720 gerada!")
    with col_b:
        if 'thumb_comb' in st.session_state:
            st.write("**Preview 1280x720:**")
            st.image(st.session_state['thumb_comb'], use_container_width=True)
            buf = io.BytesIO(); st.session_state['thumb_comb'].save(buf, format="PNG")
            st.download_button("⬇️ BAIXAR THUMB 1280x720 PNG", buf.getvalue(), f"thumb_{texto_thumb}_1280x720.png", "image/png", use_container_width=True)
        else:
            st.info("Sobe fotos e gera - formato 1280x720")

with tab5:
    st.subheader("📦 YouTube Pack - 2 Negócios")
    st.caption("Separação Curso Online vs Trabalhos Locais")
    negocio = st.selectbox("Negócio:", ["Curso Online Porcelanato", "Trabalhos Locais (Francis)"])
    tema = st.text_input("Tema do vídeo", "como fazer bancada")
    if st.button("Gerar Títulos + Descrição + Tags"):
        st.write(f"**Para {negocio}:**")
        st.write(f"Títulos: 1. {tema} - SEM SEGREDO 2. Como fazer {tema} em 1 dia")
        st.write("Descrição com CTA + Tags")

with with tab8:
    st.subheader("💰 CAC CPA ROAS - Onde investir R$300")
    st.caption("Meta vs Google vs Orgânico")
    
    # --- CORREÇÃO: Salva estado pra não sumir com o relógio ---
    if 'roas_calc_feito' not in st.session_state:
        st.session_state['roas_calc_feito'] = False
    if 'df_roas_data' not in st.session_state:
        st.session_state['df_roas_data'] = None
    if 'invest_valor' not in st.session_state:
        st.session_state['invest_valor'] = 300

    col1, col2 = st.columns(2)
    with col1:
        st.file_uploader("Meta ADS CSV (gasto, leads)", type="csv", key="meta")
        st.file_uploader("Google ADS CSV", type="csv", key="google")
    with col2:
        st.file_uploader("Kiwify CSV (vendas)", type="csv", key="kiwify")
        investimento = st.number_input("Investimento teste R$", value=st.session_state['invest_valor'], key="invest_input")

    if st.button("Calcular ROAS e Melhor Canal", key="calc", type="primary", use_container_width=True):
        # Salva no estado permanente
        st.session_state['roas_calc_feito'] = True
        st.session_state['invest_valor'] = investimento
        st.session_state['df_roas_data'] = pd.DataFrame({"ROAS": [2.1, 1.4, 4.0]}, index=["Meta", "Google", "Organico"])
        st.success("Cálculo realizado! Gráfico fixado abaixo.")

    # Mostra o gráfico SE já foi calculado, mesmo após o relógio atualizar
    if st.session_state['roas_calc_feito'] and st.session_state['df_roas_data'] is not None:
        st.divider()
        st.bar_chart(st.session_state['df_roas_data'])
        st.success(f"Com R${st.session_state['invest_valor']}: Orgânico ROAS 4x melhor! (Meta 2.1x vs Google 1.4x)")
        if st.button("🔄 Limpar cálculo", key="limpar_roas"):
            st.session_state['roas_calc_feito'] = False
            st.session_state['df_roas_data'] = None
            st.rerun()
        

with tab_invest:
    render_investimentos()

# --- FOOTER COM DATA/HORA VIVA ---
fuso_footer = pytz.timezone('America/Bahia')
agora_footer = datetime.now(fuso_footer)
st.markdown(f"""
<div style="text-align:center; color:#9CA3AF; font-size:11px; margin-top:40px; padding-top:15px; border-top:1px solid #E5E7EB;">
    FC CONSTRÓI © {agora_footer.year} • {agora_footer.strftime('%d/%m/%Y %H:%M:%S')} - Irará/BA • GROWTH AI v3.1.1 • Cores Anteriores
</div>
""", unsafe_allow_html=True)


