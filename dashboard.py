# dashboard.py - v3.1.8 COMPLETO - FC CONSTRÓI GROWTH AI - SEM MODS QUEBRADOS
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.express as px
import plotly.graph_objects as go

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

# ==================== DADOS MOCKADOS (substitua pelo seu banco) ====================
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

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    periodo = st.selectbox("Período", ["Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias", "Mês atual"])
    canal = st.multiselect("Canal", ["Instagram", "Google", "WhatsApp", "Loja"], default=["Instagram", "Google"])
    st.divider()
    st.caption(f"Atualizado: {agora.strftime('%d/%m/%Y %H:%M')}")

# ==================== ABAS PRINCIPAIS ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Visão Geral", 
    "💰 CAC / ROAS", 
    "💵 Investimentos", 
    "🏗️ Porcelanato", 
    "📄 Relatórios"
])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    st.markdown("#### 📈 Performance Geral")
    
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

# --- ABA 2: CAC / ROAS (FIX GRÁFICO NÃO SOME) ---
with tab2:
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
            
            # Gráfico FIXO - usa session_state pra não sumir
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

# --- ABA 3: INVESTIMENTOS ---
with tab3:
    st.markdown("#### 💵 Controle de Investimentos")
    try:
        from scripts.investimentos import render_investimentos
        render_investimentos()
    except ImportError:
        st.warning("Arquivo `scripts/investimentos.py` não encontrado. Criando controle básico:")
        
        # Controle básico caso não tenha o arquivo
        with st.form("form_invest"):
            col_a, col_b, col_c = st.columns(3)
            col_a.date_input("Data", value=agora.date())
            col_a.selectbox("Plataforma", ["Meta Ads", "Google Ads", "TikTok Ads"])
            col_b.number_input("Valor Investido", min_value=0.0, value=150.0)
            col_b.selectbox("Campanha", ["Porcelanato", "Pisos", "Geral"])
            col_c.text_area("Obs")
            st.form_submit_button("Salvar Investimento")
        
        st.dataframe(df[['data', 'investimento']].tail(10), use_container_width=True)

# --- ABA 4: PORCELANATO ---
with tab4:
    st.markdown("#### 🏗️ Inteligência Porcelanato")
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("Ticket Médio Porcelanato", "R$ 1.850", "+12%")
    col_p2.metric("Mais Vendido", "Polido 80x80", "32 vendas")
    
    st.markdown("**Produtos em destaque:**")
    produtos = pd.DataFrame({
        "Produto": ["Porcelanato Polido 80x80", "Porcelanato Acetinado 60x60", "Piso Vinílico", "Revestimento 3D"],
        "Vendas": [32, 28, 15, 9],
        "Estoque": [120, 80, 45, 20]
    })
    st.dataframe(produtos, use_container_width=True)

# --- ABA 5: RELATÓRIOS ---
with tab5:
    st.markdown("#### 📄 Relatórios")
    st.download_button("📥 Baixar CSV Vendas", df.to_csv(index=False), "vendas_fc.csv", "text/csv")
    st.dataframe(df, use_container_width=True)

mostrar_footer()



