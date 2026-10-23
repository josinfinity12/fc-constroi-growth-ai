# 🏗️ FC CONSTRÓI • GROWTH AI v3.8 NACIONAL - BRASIL TODO
> PUXA INSTA + GERA THUMB 1280x720 AUTOMÁTICO + CURSO ONLINE NACIONAL
> Baseado no v3.3.8 (9 abas + SUPABASE KIWIFY + LOOP VIRAL) -> v3.8 NACIONAL (CURSO BRASIL TODO + 6 CIDADES SERVIÇO LOCAL)

**FIX v3.8 NACIONAL:** Curso Online Academia FC Constrói = **NACIONAL - BRASIL TODO**. As 6 cidades (Santanópolis, Irará, Feira de Santana, Santa Bárbara, Serrinha, Ouriçangas) são **APENAS para SERVIÇO LOCAL** de instalação.

**🔗 App no ar 24h:**  
https://josinfinity12-fc-constroi-growth-ai-dashboard-47vlqz.streamlit.app

---

### 🔥 9 ABAS COMPLETAS - v3.8 NACIONAL

| Aba | O que faz |
|---|---|
| **🔥 FILTROS (Cursos+Local)** | **FIX v3.8:** Filtra Curso NACIONAL Brasil Todo vs Serviço Local em 6 cidades (Santanópolis, Irará, Feira, Santa Bárbara, Serrinha, Ouriçangas) + NACIONAL - Brasil Todo + Filtro Viral Top3 Loop + Score Gancho |
| **♻️ Reciclar Conteúdo** | Transforma TOP3 (gaveta 48k, pia 32k, base 300kg) em 9 conteúdos novos (3x3) + yt-dlp + legenda Insta/TikTok + CTA |
| **📊 Dashboard + Gráficos IA** | FIXO NACIONAL: Views 108k, Vendas Kiwify R$3.477 NACIONAL, ROAS/CAC travados + Plotly Top3 + Crescimento gaveta + Funil Comentário->DM->Kiwify NACIONAL |
| **🖼️ Thumbnails IA [AUTO ONLINE]** | **ESTRELA v3.3.8 mantida:** PUXA @fc_constroi ONLINE + GERA 1280x720 AUTO 1 clique. Upload temporal (BytesIO RAM, não salva disco) + COMBO pessoa+obra + 3 variações + Memória fixa + DALL·E V2 |
| **🎬 YouTube Pack** | Gera Pack completo: Título SEO com Score, Descrição com Kiwify + Timestamp, Tags, Horário ideal + Upload automático API + Copiar 1 clique |
| **💰 CAC CPA ROAS** | Calculadora fixa: Investimento, Vendas, Ticket R$497, CAC, ROAS, Lucro - NACIONAL |
| **💹 INVESTIMENTOS** | Controle: Meta Ads Gaveta R$150 (48k views), YouTube Pia, TikTok Base + Auto Save |
| **💚 VENDAS Kiwify NACIONAL [FIX v3.8]** | **Tracking REAL Supabase NACIONAL:** `vendas_kiwify` agora salva `cidade = "nacional"` + `cidade_origem_lead` + `abrangencia = "NACIONAL - BRASIL TODO"` + `extrair_filtros_sck_nacional()` + `salvar_venda_kiwify_teste()` NACIONAL + `buscar_vendas_reais_supabase()` |
| **🤖 Insta Auto + Loop Viral [NOVO]** | Loop infinito 07h Gaveta / 12h Base / 19h Pia só TOP3 NACIONAL + 5 plataformas: Instagram, Facebook, TikTok, YouTube Shorts, Kwai |

---

### 🚀 NOVO v3.8 NACIONAL - BRASIL TODO

```python
# FIX v3.8 NACIONAL - BRASIL TODO
CURSO_ONLINE_ABRANGENCIA = "NACIONAL - BRASIL TODO"
CIDADE_CURSO_ONLINE_FIXA = "nacional"
ABRANGENCIA_CURSO = "NACIONAL - BRASIL TODO - Academia FC Constrói"

def extrair_filtros_sck_nacional(sck_full: str):
    # Mantem original intacta, mas retorna cidade = nacional para venda curso online
    plat, cid_origem, inter, traffic = extrair_filtros_sck(sck_full)
    return plat, "nacional", cid_origem, inter, traffic

def salvar_venda_kiwify_teste(sck_teste, email_teste):
    # FIX: Salva sempre como NACIONAL
    payload = {
        "cidade": "nacional",
        "cidade_origem_lead": cid_origem,  # guarda origem sem perder dado
        "abrangencia": "NACIONAL - BRASIL TODO - Academia FC Constrói"
    }
    

