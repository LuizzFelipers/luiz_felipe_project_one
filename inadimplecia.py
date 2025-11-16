import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_icon="💳",
    page_title="Inadimplência",
    initial_sidebar_state="expanded"
)


# Load Data
@st.cache_data
def load_data():
    df = pd.read_excel("analise_risco_inadimplencia.xlsx")
    return df

df = load_data()

#Sidebar
st.sidebar.title("🔎 Filtros")
st.sidebar.markdown("------")

#criiando os filtros
categoria_risco = st.sidebar.multiselect(
    "Categorias de Risco",
    options=df["categoria_risco"].unique(),
    default=df["categoria_risco"].unique()
)

metodos_pagamento = st.sidebar.multiselect(
    "Métodos de Pagamento",
    options=df["metodo_pagamento"].unique(),
    default=df["metodo_pagamento"].unique()
)

df_filtrado = df[
    (df["categoria_risco"].isin(categoria_risco)) &
    (df["metodo_pagamento"].isin(metodos_pagamento))
]

#Analisando o Risco de Inadimplência pelo Score Crédito


#Header e Principais Métricas
st.title("💳Análise de Inadimplência")
st.markdown("------------------")


col1,col2, col3, col4 = st.columns(4)

with col1:
    total_clientes = len(df_filtrado)
    st.metric("🧑 **Total de Clientes**",total_clientes)

with col2:
    taxa_risco_alto = (len(df_filtrado[df_filtrado["categoria_risco"].isin(["Alto Risco", "Risco Crítico",])])/ total_clientes)*100
    st.metric("🚨 **Taxa Risco Alto/Crítico**", f"{taxa_risco_alto:.1f}%")

with col3:
    score_medio = df_filtrado["score_credito"].mean()
    st.metric("➕ **Score Médio**", f"{score_medio:.0f}")

with col4:
    razao_media = df_filtrado["razao_plano_renda"].mean() * 100
    st.metric("➗ **Razão Plano/Renda Média**", f"{razao_media:.1f}%")


st.markdown("-----------------")

tab1, tab2 = st.tabs(["🕵️‍♂️ **Análise Completa**", "✅ **Resumo e Insights**"])

with tab1:
    st.header(" Distribuição de Risco")

    col1, col2 = st.columns(2)

    with col1:

        fig_pizza = px.pie(
            df_filtrado,
            names="categoria_risco",
            title="Distribuição por Categoria de Risco",
            color="categoria_risco",
            color_discrete_map={
                "Baixo Risco": "green",
                "Risco Moderado": "yellow",
                "Alto Risco":"orange",
                "Risco Crítico":"red"
            },
            hole=0.5
        )

        st.plotly_chart(fig_pizza, use_container_width=True)

    with col2:

        contagem_risco = df_filtrado["categoria_risco"].value_counts().reset_index(name="count")

        fig_barras = px.bar(
            contagem_risco,
            x="categoria_risco",
            y="count",
            title="Número de Clienntes por Categoria de Risco",
            color="categoria_risco",
            color_discrete_map={
                "Baixo Risco":"green",
                "Risco Moderado": "yellow",
                "Alto Risco":"orange",
                "Risco Crítico":"red"
            },
            labels={"count":"Quantidade", "categoria_risco":"Catrgoria Risco"}
        )
        st.plotly_chart(fig_barras, use_container_width=True)

    st.markdown("-------------")
    st.header(" Análise por Score de Crédito")

    col1, col2 = st.columns(2)

    with col1:
        # score por categoria
        fig_box = px.box(
            df_filtrado,
            x="categoria_risco",
            y="score_credito",
            title="Distribuição do Score por Categoria de Risco",
            color="categoria_risco",
            color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"score_credito":"Score Crédito", "categoria_risco":"Categoria Risco"}
        )

        st.plotly_chart(fig_box, use_container_width=True)

    with col2:

        fig_hist = px.histogram(
            df_filtrado,
            x="score_credito",
            color="categoria_risco",
            title="Distribuição do Score de Crédito",
            nbins=30,
                    color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"count":"Quantidade", "score_credito":"Score Crédito"}
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("-----------------")

    st.header(" Análise Financeira")

    col1, col2 = st.columns(2)

    with col1:

        fig_razao = px.box(
            df_filtrado,
            x="categoria_risco",
            y="razao_plano_renda",
            title="Razão Plano/Renda por Cateoria de Risco",
            color="categoria_risco",
                    color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"razao_plano_renda":"Razão entre Plano e Renda", "categoria_risco":"Categoria Risco"}
        )

        fig_razao.update_yaxes(tickformat=".2%")
        st.plotly_chart(fig_razao, use_container_width=True)

    with col2:

        #Renda mensal por categoria
        fig_renda = px.box(
            df_filtrado,
            x='categoria_risco',
            y='renda_mensal',
            title='Renda Mensal por Categoria de Risco',
            color='categoria_risco',
            color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"renda_mensal":"Renda Mensal", "categoria_risco":"Categoria Risco"}
        )
        st.plotly_chart(fig_renda, use_container_width=True)

    st.markdown("-----------")
    st.header(" Métodos de Pagamento e Canais de Aquisição")

    col1, col2 = st.columns(2)

    with col1:
        metodo_risco = pd.crosstab(df_filtrado['metodo_pagamento'], df_filtrado['categoria_risco'], normalize='index') * 100
    
        fig_metodo = px.bar(
            metodo_risco.reset_index().melt(id_vars='metodo_pagamento'),
            x='metodo_pagamento',
            y='value',
            color='categoria_risco',
            title='Distribuição de Risco por Método de Pagamento (%)',
            barmode='stack',
            color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"metodo_pagamento":"Método de Pagamento"}
        )
        fig_metodo.update_yaxes(title_text="Percentual (%)")
        st.plotly_chart(fig_metodo, use_container_width=True)


    with col2:
    # Canais de aquisição por risco
        canal_risco = pd.crosstab(df_filtrado['canal_aquisicao'], df_filtrado['categoria_risco'], normalize='index') * 100
        
        fig_canal = px.bar(
            canal_risco.reset_index().melt(id_vars='canal_aquisicao'),
            x='canal_aquisicao',
            y='value',
            color='categoria_risco',
            title='Distribuição de Risco por Canal de Aquisição (%)',
            barmode='stack',
            color_discrete_map={
                'Baixo Risco': 'green',
                'Risco Moderado': 'yellow',
                'Alto Risco': 'orange',
                'Risco Crítico': 'red'
            },
            labels={"canal_aquisicao":"Canal de Aquisição"}
        )
        fig_canal.update_yaxes(title_text="Percentual (%)")
        st.plotly_chart(fig_canal, use_container_width=True)

with tab2:
    st.header("💡 Insights e Recomendações")

# Tabela resumo
    st.subheader("📊 Estatísticas por Categoria de Risco")

    resumo = df_filtrado.groupby('categoria_risco').agg({
        'score_credito': ['mean', 'median', 'std'],
        'razao_plano_renda': ['mean', 'median'],
        'renda_mensal': ['mean', 'median'],
        'customer_id': 'count'
    }).round(2)

    resumo.columns = ['Score Médio', 'Score Mediano', 'Score Desvio', 
                    'Razão Média', 'Razão Mediana', 
                    'Renda Média', 'Renda Mediana', 'Total Clientes']
    st.dataframe(resumo)

    # Insights
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Padrões Identificados")
        st.markdown("""
        - **Score < 550**: Alto risco de inadimplência
        - **Razão > 5%**: Comprometimento financeiro elevado
        - **Renda baixa + plano caro**: Combinação perigosa
        - **Boleto**: Associado a maior risco
        - **Cartão Crédito**: Menor risco relativo
        """)

    with col2:
        st.subheader("🚀 Recomendações")
        st.markdown("""
        - **Aprovação**: Estabelecer score mínimo de 600
        - **Precificação**: Limitar razão plano/renda em 5%
        - **Métodos**: Incentivar cartão crédito/PIX
        - **Segmentação**: Focar canais de melhor perfil
        - **Monitoramento**: Acompanhar clientes com razão > 5%
        """)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("📊 **Dashboard desenvolvido para análise de risco de inadimplência**")