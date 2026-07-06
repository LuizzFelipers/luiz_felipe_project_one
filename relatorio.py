import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np

#Gerar dados fictícios

#Fluxo de caixa diário (entradas e saídas)
np.random.seed(42)
datas = pd.date_range(start='2026-01-01', periods=30, freq='D')
# Fluxo de caixa diário (entradas e saídas)
entradas = np.random.uniform(50, 150, size=30).round(2)
saidas = np.random.uniform(30, 120, size=30).round(2)
saldo_diario = np.cumsum(entradas - saidas) + 500  # saldo inicial 50k

df_caixa = pd.DataFrame({
    'data': datas,
    'entradas': entradas,
    'saidas': saidas,
    'saldo_final': saldo_diario
})

# Gerar dados fictícios de inadimplência
clientes = ['Fulano', 'Ciclano', 'Beltrano', 'Ciclana', 'Beltrana']
inadimplentes = pd.DataFrame({
    'cliente': np.random.choice(clientes, size=8, replace=True),
    'valor_aberto': np.random.uniform(1000, 8000, size=8).round(2),
    'dias_atraso': np.random.randint(5, 90, size=8)
}).drop_duplicates(subset='cliente').reset_index(drop=True)

#Taxa de inadimplência
total_receber = 150000
total_inadimplencia = inadimplentes['valor_aberto'].sum()
taxa_inadimplencia = (total_inadimplencia / total_receber) * 100
qtd_inadimplentes = inadimplentes['cliente'].nunique()

def formatar(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

prox_pagamentos = pd.DataFrame({
    'tipo': ['Folha', 'Fornecedor X', 'Fornecedor Y', 'Folha', 'Fornecedor Z'],
    'descricao': ['Salário mensal', 'Matéria-prima', 'Manutenção', '13º salário', 'Serviços'],
    'valor': [450, 220, 850, 450, 125],
    'vencimento': pd.date_range(start='2026-01-10', periods=5, freq='7D')
})


st.set_page_config(page_title="Relatório Financeiro", 
                   layout="wide", 
                   page_icon=":bar_chart:"
                   )

st.title("Relatório Financeiro")

col1, col2, col3, col4 = st.columns(4)





with col1:
    st.metric(label="💰 Saldo Final do Dia", value=formatar(df_caixa['saldo_final'].iloc[-1]),
              delta=f"R$ {df_caixa['saldo_final'].iloc[-1] - df_caixa['saldo_final'].iloc[-2]:,.2f} vs dia anterior")

with col2:
    st.metric("Inadimplência(%)", f"{taxa_inadimplencia:.1f}%", delta=f"{taxa_inadimplencia - 12:.1f}%")

with col3:
    st.metric("Clientes Inadimplentes", f"{qtd_inadimplentes}", delta=f"{qtd_inadimplentes - 15}")
    
with col4:
    total_prox = prox_pagamentos['valor'].sum()

    st.metric(label="📅 Próximos Pagamentos (7 dias)", value=formatar(total_prox),
              delta=f"{len(prox_pagamentos)} títulos")

st.markdown("-------")

st.subheader("📊 Evolução Diária do Fluxo de Caixa")

df_melt = df_caixa.melt(id_vars='data', value_vars=['entradas', 'saidas'],
                        var_name='tipo', value_name='valor')
fig_caixa = px.bar(df_melt, x='data', y='valor', color='tipo',
                    barmode='group', title='Entradas vs Saídas Diárias',
                    labels={'valor': 'R$', 'data': 'Data'},
                    color_discrete_map={'entradas': '#2ecc71', 'saidas': '#e74c3c'})
    # Adicionar linha de saldo (eixo secundário)
fig_caixa.add_scatter(x=df_caixa['data'], y=df_caixa['saldo_final'],
                        mode='lines+markers', name='Saldo Final',
                        yaxis='y2', line=dict(color='#3498db', width=2))
fig_caixa.update_layout(
        yaxis2=dict(title='Saldo (R$)', overlaying='y', side='right'),
        legend=dict(orientation='h', y=1.02),
        height=450
    )
st.plotly_chart(fig_caixa, use_container_width=True)

st.markdown("-------")
st.subheader("🔴 Clientes Inadimplentes")
if not inadimplentes.empty:
    st.dataframe(
            inadimplentes.style.format({'valor_aberto': 'R$ {:,.2f}'}),
            use_container_width=True
        )
else:
    st.success("Nenhum cliente inadimplente no momento!")

st.markdown("-------")
st.subheader("📆 Próximos Pagamentos")
st.dataframe(
        prox_pagamentos.style.format({'valor': 'R$ {:,.2f}'}),
        use_container_width=True
)

with st.sidebar:
    st.header("⚙️ Filtros")
    data_inicio = st.date_input("Data inicial", value=datas.min())
    data_fim = st.date_input("Data final", value=datas.max())
    if data_inicio and data_fim:
        mask = (df_caixa['data'] >= pd.to_datetime(data_inicio)) & (df_caixa['data'] <= pd.to_datetime(data_fim))
        df_filtrado = df_caixa.loc[mask]
        st.metric("Saldo no período", f"R$ {df_filtrado['saldo_final'].iloc[-1]:,.2f}" if not df_filtrado.empty else "0,00")