import pandas as pd

def calcular_metricas_pagas(df_ads, df_kiwify, plataforma="Meta"):
    custo_total = float(df_ads['custo'].sum()) if 'custo' in df_ads.columns else 0
    cliques = int(df_ads['cliques'].sum()) if 'cliques' in df_ads.columns else 1
    vendas_origem = df_kiwify[df_kiwify['origem'].str.lower() == plataforma.lower()] if 'origem' in df_kiwify.columns else df_kiwify
    faturamento = float(vendas_origem['valor'].sum()) if 'valor' in vendas_origem.columns else 0
    num_vendas = len(vendas_origem)
    clientes_unicos = int(vendas_origem['email'].nunique()) if 'email' in vendas_origem.columns else num_vendas
    cpc = custo_total / cliques if cliques > 0 else 0
    cpa = custo_total / num_vendas if num_vendas > 0 else 0
    cac = custo_total / clientes_unicos if clientes_unicos > 0 else 0
    roas = faturamento / custo_total if custo_total > 0 else 0
    ticket = faturamento / num_vendas if num_vendas > 0 else 0
    return {"plataforma": plataforma, "custo_total": round(custo_total,2), "cliques": cliques, "vendas": num_vendas, "faturamento": round(faturamento,2), "CPC": round(cpc,2), "CPA": round(cpa,2), "CAC": round(cac,2), "ROAS": round(roas,2), "TICKET_MEDIO": round(ticket,2)}

def calcular_metricas_organicas(df_org, df_kiwify_org):
    views = int(df_org['views'].sum()) if 'views' in df_org.columns else 0
    comentarios = int(df_org['comentarios'].sum()) if 'comentarios' in df_org.columns else 0
    coment_bancada = int(df_org['coment_bancada'].sum()) if 'coment_bancada' in df_org.columns else 0
    faturamento_org = float(df_kiwify_org['valor'].sum()) if 'valor' in df_kiwify_org.columns else 0
    vendas_org = len(df_kiwify_org)
    eng = (comentarios / views * 100) if views > 0 else 0
    conv = (vendas_org / coment_bancada * 100) if coment_bancada > 0 else 0
    return {"plataforma": "ORGANICO", "custo_total": 0.0, "views": views, "coment_bancada": coment_bancada, "vendas": vendas_org, "faturamento": round(faturamento_org,2), "CPC": 0.0, "CPA": 0.0, "CAC": 0.0, "ROAS": 999.0, "ENG%": round(eng,2), "CONV_COMENT%": round(conv,2)}

def gerar_recomendacao(df_comp):
    df_sorted = df_comp.sort_values(by="ROAS", ascending=False)
    melhor = df_sorted.iloc[0]
    pior = df_sorted.iloc[-1]
    recs = []
    for _, row in df_sorted.iterrows():
        if row['plataforma'] == 'ORGANICO':
            recs.append(f"ORGANICO: ROAS infinito (R${row['faturamento']} sem custo). DOBRA posts.")
        elif row['ROAS'] >= 3:
            recs.append(f"{row['plataforma'].upper()}: ROAS {row['ROAS']} EXCELENTE. AUMENTA +50%.")
        elif row['ROAS'] >= 2:
            recs.append(f"{row['plataforma'].upper()}: ROAS {row['ROAS']} BOM. Mantém.")
        else:
            recs.append(f"{row['plataforma'].upper()}: ROAS {row['ROAS']} PREJUIZO. PAUSA 70%.")
    recs.append(f"DECISAO: Tira R$300 de {pior['plataforma']} e investe em {melhor['plataforma']}.")
    return "\n\n".join(recs)