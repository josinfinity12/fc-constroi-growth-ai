# scripts/investimentos.py
import pandas as pd
import streamlit as st

def calcular_metricas(faturamento_curso, faturamento_obra, outros, gasto_trafego, custo_material, custo_ferramentas, taxas):
    faturamento_total = faturamento_curso + faturamento_obra + outros
    custo_total = gasto_trafego + custo_material + custo_ferramentas + taxas
    
    lucro_bruto = faturamento_total - custo_material
    lucro_liquido = faturamento_total - custo_total
    
    margem_bruta = (lucro_bruto / faturamento_total * 100) if faturamento_total else 0
    margem_liquida = (lucro_liquido / faturamento_total * 100) if faturamento_total else 0
    roi = (lucro_liquido / custo_total * 100) if custo_total else 0
    roas = (faturamento_total / gasto_trafego) if gasto_trafego else 0
    
    return {
        "faturamento_total": faturamento_total,
        "custo_total": custo_total,
        "lucro_bruto": lucro_bruto,
        "lucro_liquido": lucro_liquido,
        "margem_bruta": margem_bruta,
        "margem_liquida": margem_liquida,
        "roi": roi,
        "roas": roas
    }

def render_aba_investimentos():
    st.subheader("📈 INVESTIMENTOS - Controle Financeiro Completo")
    st.caption("Os 10 parâmetros mais usados por quem vende curso + obra")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 💸 Entradas")
        faturamento_curso = st.number_input("Faturamento Curso (Kiwify) R$", value=8500.0, step=100.0, key="fat_curso_inv")
        faturamento_obra = st.number_input("Faturamento Obras Locais R$", value=6200.0, step=100.0, key="fat_obra_inv")
        outros = st.number_input("Outros (YouTube, parceria) R$", value=0.0, key="outros_inv")
    with c2:
        st.markdown("#### 💳 Custos / Investimentos")
        gasto_trafego = st.number_input("Tráfego Pago (Meta/Google) R$", value=1200.0, step=50.0, key="traf_inv")
        custo_material = st.number_input("Material / Porcelanato / Insumos R$", value=2800.0, step=100.0, key="mat_inv")
        custo_ferramentas = st.number_input("Ferramentas / Aluguel / Gasolina R$", value=450.0, key="ferr_inv")
        taxas = st.number_input("Taxas Kiwify + Impostos (15%) R$", value=faturamento_curso*0.15, key="taxas_inv")
    with c3:
        m = calcular_metricas(faturamento_curso, faturamento_obra, outros, gasto_trafego, custo_material, custo_ferramentas, taxas)
        st.markdown("#### 📊 Resultados CHAVE")
        st.metric("Faturamento Total", f"R$ {m['faturamento_total']:,.2f}")
        st.metric("Lucro Bruto", f"R$ {m['lucro_bruto']:,.2f}", f"{m['margem_bruta']:.1f}% margem")
        st.metric("Lucro Líquido (Ganância)", f"R$ {m['lucro_liquido']:,.2f}", f"{m['margem_liquida']:.1f}% margem")
        st.metric("ROI", f"{m['roi']:.1f}%")
        st.metric("ROAS", f"{m['roas']:.2f}x")

    st.divider()
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        df_fonte = pd.DataFrame({"Valor": [faturamento_curso, faturamento_obra, outros]}, index=["Curso", "Obras", "Outros"])
        st.bar_chart(df_fonte)
    with col_graf2:
        df_custo = pd.DataFrame({"Valor": [m['custo_total'], m['lucro_liquido']]}, index=["Custos", "Lucro Liquido"])
        st.bar_chart(df_custo)

    st.markdown("#### 🎯 CAC, Ticket, LTV")
    cc1, cc2, cc3, cc4 = st.columns(4)
    vendas = cc1.number_input("Vendas fechadas", value=8, min_value=1, key="vendas_inv")
    leads = cc2.number_input("Leads no mês", value=45, key="leads_inv")
    ticket_medio = m['faturamento_total'] / vendas if vendas else 0
    cac = (gasto_trafego / vendas) if vendas else 0
    conversao = (vendas / leads * 100) if leads else 0
    ltv = ticket_medio * 1.8
    ltv_cac = (ltv / cac) if cac else 0

    cc1.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
    cc2.metric("CAC", f"R$ {cac:,.2f}")
    cc3.metric("Conversão", f"{conversao:.1f}%")
    cc4.metric("LTV/CAC", f"{ltv_cac:.1f}x")
    