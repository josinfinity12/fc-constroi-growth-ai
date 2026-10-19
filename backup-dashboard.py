import streamlit as st
import pandas as pd
import re
import unicodedata

st.set_page_config(page_title=FC Constrói - Growth AI, layout=wide)

def tirar_acento(texto)
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

CIDADES_VALIDAS = [santanopolis, irara, feira de santana, agua fria, serrinha, santa barbara]
PALAVRAS_CURSO = [gaveta, closet, porcelanato, bancada, argamassa]

def classificar_comentario(comentario)
    texto_norm = tirar_acento(comentario.lower())
    
    # 1. PRIORIDADE CURSO (gaveta, closet, bancada)
    if any(p in texto_norm for p in PALAVRAS_CURSO)
        return CURSO_ONLINE, -
    
    # 2. CIDADE VALIDA
    for cidade in CIDADES_VALIDAS
        if cidade in texto_norm
            return ORCAMENTO_LOCAL_VALIDO, cidade
    
    # 3. FORA DA AREA (só se tem faz em  no)
    match = re.search(r(faz emfaz noatendevoces fazem emfazem no)s+([a-zs]+), texto_norm)
    if match
        cidade_fora = match.group(1).strip()
        if len(cidade_fora)  2
            return ORCAMENTO_FORA_DA_AREA, cidade_fora

    if any(p in texto_norm for p in [quanto cobra, quanto custa, orcamento])
        return ORCAMENTO_LOCAL_VALIDO, sem_cidade

    return DUVIDA_GERAL, -
    texto_norm = tirar_acento(comentario.lower())
    # Verifica se tem cidade
    for cidade in CIDADES_VALIDAS
        if cidade in texto_norm
            return ORCAMENTO_LOCAL_VALIDO, cidade
    
    # Se mencionou faz em  atende  no  na + cidade, mas NÃO é das 6
    match = re.search(r(emparafaz emfaz noatendedenona)s+([a-zs]+), texto_norm)
    if match
        cidade_fora = match.group(1).strip()
        if cidade_fora not in [que, qual, quanto, onde, quanto cobra] and len(cidade_fora)  2
            return ORCAMENTO_FORA_DA_AREA, cidade_fora

    if any(p in texto_norm for p in PALAVRAS_CURSO)
        return CURSO_ONLINE, None
    
    # Se é dúvida genérica de orçamento sem cidade
    if any(p in texto_norm for p in [quanto cobra, quanto custa, orcamento])
        return ORCAMENTO_LOCAL_VALIDO, sem_cidade

    return DUVIDA_GERAL, None

# --- DADOS ---
dados_reels = [
    {id_reel 1, data 2026-10-10, tema bancada_com_gaveta, gancho_3s Olha o erro que 90% faz, tempo_video_s 18, tem_legenda_queimada 1, cta_final Comenta BANCA, likes 11000, views 185000, comentarios 412, shares 890},
    {id_reel 5, data 2026-10-18, tema bancada_com_gaveta, gancho_3s Bancada que que cabe tudo, tempo_video_s 14, tem_legenda_queimada 1, cta_final Comenta PROJETO, likes 300, views 3200, comentarios 12, shares 5},
    {id_reel 4, data 2026-10-13, tema colagem_piso_sobre_piso, gancho_3s O segredo da cola, tempo_video_s 15, tem_legenda_queimada 1, cta_final Comenta COLA, likes 1200, views 25000, comentarios 89, shares 120},
    {id_reel 2, data 2026-10-11, tema porcelanato_lixado, gancho_3s Nunca faça assim, tempo_video_s 12, tem_legenda_queimada 0, cta_final Me segue, likes 800, views 12000, comentarios 23, shares 12},
    {id_reel 3, data 2026-10-12, tema reforma_banheiro, gancho_3s Transformei com R$ 200, tempo_video_s 22, tem_legenda_queimada 1, cta_final Quer o passo a passo, likes 450, views 8900, comentarios 18, shares 8},
]
df_reels = pd.DataFrame(dados_reels)

st.title(FC Constrói - Growth AI v1.0)

tab1, tab2, tab3 = st.tabs([🔥 Preditor Viral, ♻️ Reciclagem, 💬 Funil Comentários])

with tab1
    st.dataframe(df_reels, use_container_width=True)
    st.metric(Taxa Viral Atual, 20.0%, delta=Meta 25%)
    st.warning(Hoje 1 a cada 15 viraliza (6.6%). Com preditor vamos pra 1 a cada 4.)

with tab3
    st.subheader(🔥 Funil Kiwify - AO VIVO)
    st.caption(Link Ativo)
    st.title(HiEJZtFsrc=instagram&kw=gaveta_closet)
    st.link_button(Abrir Checkout Kiwify, httpspay.kiwify.com.brHiEJZtFsrc=instagram&kw=gaveta_closet)

    # Comentários simulados para teste
    comentarios_teste = [
        {id 0, comentario como faz gaveta, link gaveta, status pendente},
        {id 1, comentario qual medida de closet, link closet, status pendente},
        {id 2, comentario faz no Rio, link fora_area, status pendente},
        {id 3, comentario faz em Irará, link orcamento, status pendente},
        {id 4, comentario como faz bancada, link bancada, status pendente},
        {id 5, comentario qual porcelanato usou, link porcelanato, status pendente},
    ]
    
    dados_tabela = []
    for c in comentarios_teste
        classificacao, cidade = classificar_comentario(c[comentario])
        dados_tabela.append({
            id c[id],
            comentario c[comentario],
            classificacao classificacao,
            cidade_detectada cidade if cidade else -,
            link c[link],
            status c[status]
        })
    
    df_funil = pd.DataFrame(dados_tabela)
    st.dataframe(df_funil, use_container_width=True)
    st.success(f{len([x for x in dados_tabela if 'CURSO_ONLINE' in x['classificacao']])} comentários com GAVETACLOSETBANCADA viraram leads hoje. Sem responder manual.)

with tab2
    st.subheader(Reciclagem de Conteúdo)
    st.write(Seu tema viral é bancada_com_gaveta. Reutilize o Reel 1.)
