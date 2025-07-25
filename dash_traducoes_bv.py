import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Dashboard de Traduções BV", layout="wide")
st.title("📊 Dashboard de Análise de Traduções BV")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_excel("bv_traducoes_corrigida.xlsx")
    
    # Limpeza e padronização
    df['Tipo de Documento'] = df['Tipo de Documento'].str.lower().str.strip()
    df['TIPO DE TRADUÇÃO'] = df['TIPO DE TRADUÇÃO'].str.lower().str.strip()
    
    # Extrair quantidade numérica
    df['Quantidade'] = df['Qtde. de documentos/laudas'].str.extract('(\d+)').astype(int)
    
    # Calcular tempo de processamento
    df['Data da solicitação'] = pd.to_datetime(df['Data da solicitação'])
    df['Data de finalização'] = pd.to_datetime(df['Data de finalização'])
    df['Tempo de processamento (dias)'] = (df['Data de finalização'] - df['Data da solicitação']).dt.days
    
    # Corrigir valores negativos (erros de digitação)
    df.loc[df['Tempo de processamento (dias)'] < 0, 'Tempo de processamento (dias)'] = 0
    
    df["IDIOMA"] = df['IDIOMA'].str.lower()
    df = df.drop(columns={"Código da Atividade"})

    return df

df = load_data()


# Sidebar com filtros
st.sidebar.header("🔍 Filtros")
tipo_doc = st.sidebar.multiselect(
    "Tipo de Documento",
    options=df['Tipo de Documento'].unique(),
    default=df['Tipo de Documento'].unique()
)

idioma = st.sidebar.multiselect(
    "Idioma",
    options=df['IDIOMA'].unique(),
    default=df['IDIOMA'].unique()
)

tipo_trad = st.sidebar.multiselect(
    "Tipo de Tradução",
    options=df['TIPO DE TRADUÇÃO'].unique(),
    default=df['TIPO DE TRADUÇÃO'].unique()
)

data_range = st.sidebar.date_input(
    "Período das solicitações",
    value=[df['Data da solicitação'].min(), df['Data da solicitação'].max()],
    min_value=df['Data da solicitação'].min(),
    max_value= df["Data da solicitação"].max()
)

# Aplicar filtros
df_filtered = df[
    (df['Tipo de Documento'].isin(tipo_doc)) &
    (df['IDIOMA'].isin(idioma)) &
    (df['TIPO DE TRADUÇÃO'].isin(tipo_trad)) &
    (df['Data da solicitação'] >= pd.to_datetime(data_range[0])) &
    (df['Data da solicitação'] <= pd.to_datetime(data_range[1]))
]

# Métricas principais
st.subheader("📈 Métricas Principais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Traduções", "1.138")
col2.metric("Receita Total", "R$ 92.720,00")
col3.metric("Tempo Médio (dias)", f"{df_filtered['Tempo de processamento (dias)'].mean():.0f}")
col4.metric("Valor Médio", "R$ 81,48")

# Tabs para diferentes visualizações
tab1, tab2, tab3, tab4 = st.tabs(["📋 Dados", "⏱ Tempo", "📊 Distribuição", "💰 Receita"])

with tab1:
    st.subheader("Dados Completos")
    st.dataframe(df_filtered.sort_values('Data da solicitação', ascending=False), 
                height=400,
                column_config={
                    "Data da solicitação": st.column_config.DateColumn("Solicitação"),
                    "Data de finalização": st.column_config.DateColumn("Finalização"),
                    "Valor Total": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f")
                })
    st.markdown("----")
    st.subheader("🔍 Análise Detalhada")

    

    
    st.write("**Top 5 Documentos Mais Frequentes**")
    st.dataframe(df_filtered['Tipo de Documento'].value_counts().head(5).reset_index(),
                hide_index=True,
                column_config={
                    "Tipo de Documento": "Documento",
                    "count": "Quantidade"
            })

with tab2:
    st.subheader("Análise de Tempo de Processamento")
    tempo_dias = df.groupby('Tipo de Documento')['Tempo de processamento (dias)'].mean().round().sort_values(ascending=False).reset_index()
    fig_scatter = px.scatter(
            tempo_dias,
            x='Tipo de Documento',
            y='Tempo de processamento (dias)',
            color='Tipo de Documento',
            width=800,
            height=500,
            hover_data=['Tipo de Documento', 'Tempo de processamento (dias)'],
            title="Tempo de Processamento por Solicitação",
            labels={'Tempo de processamento (dias)': 'Dias', 'Data da solicitação': 'Data de Solicitação'}
        )
    fig_scatter.update_layout(
            autosize=True,
            margin=dict(l=20, r=20, t=40, b=20),
            height=500
        )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("-----")
    st.subheader("🔍Tabela completa:")

    colunas =["Data da solicitação","IDIOMA","TIPO DE TRADUÇÃO","Data de finalização",
                                       "Qtde. de documentos/laudas","Valor unitário","Valor Total","Quantidade"]
    st.dataframe(                      
            tempo_dias,
            hide_index=True,
            column_config = {
                "Tempo de processamento(dias)":"Tempo de Processamento",
                "Tipo de Documento":"Tipo de Documento"
            },
            use_container_width=True
        )
    

with tab3:
    st.subheader("Distribuição das Traduções")
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_filtered['Tipo de Documento'] = df_filtered['Tipo de Documento'].str.lower()
        doc_counts = df_filtered['Tipo de Documento'].value_counts().reset_index()
        fig_pie = px.pie(
            doc_counts,
            names='Tipo de Documento',
            values='count',
            title="Distribuição por Tipo de Documento",
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(
            df_filtered.groupby(['IDIOMA', 'TIPO DE TRADUÇÃO']).size().reset_index(name='Quantidade'),
            x='IDIOMA',
            y='Quantidade',
            color='TIPO DE TRADUÇÃO',
            title="Distribuição por Idioma e Tipo de Tradução",
            barmode='group'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

with tab4:
    st.subheader("Análise de Receita")
       
    receita_mensal = df_filtered.groupby(pd.Grouper(key='Data da solicitação', freq='M'))['Valor Total'].sum().reset_index()
    fig_trend = px.line(
            receita_mensal,
            x='Data da solicitação',
            y='Valor Total',
            title="Receita Mensal (R$)",
            markers=True,
            labels={'Valor Total': 'Receita (R$)', 'Data da solicitação': 'Mês'}
        )
    st.plotly_chart(fig_trend, use_container_width=True)

    receita_por_tipo = df_filtered.groupby('Tipo de Documento')['Valor Total'].sum().reset_index(name="Valor Total")
    fig_receita = px.bar(
            receita_por_tipo,
            x='Tipo de Documento',
            y='Valor Total',
            title="Receita por Tipo de Documento (R$)",
            color='Tipo de Documento',
            labels={'Valor Total': 'Receita (R$)'}
        )
    st.plotly_chart(fig_receita, use_container_width=True)