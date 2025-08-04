import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide',page_title="Dashboard de desempenho")
st.title("Dashboard de Vendas")

def load_data():

    df = pd.read_excel("base_dados_vendas.xlsx")
    df["Data da Venda"] = pd.to_datetime(df["Data da Venda"])
    df["Mes"] = df["Data da Venda"].dt.month

    return df
    

df = load_data()

st.sidebar.header("Filtros")

colaborador = df['Nome do Funcionário']
funcionario = st.sidebar.selectbox("Funcionário",
                                   options=(colaborador.unique()))


df_filtrado = df[df["Nome do Funcionário"] == funcionario]

tab1,tab2 = st.tabs(["$ Métricas Totais",
                           "Desempenho Individual dos Vendedores"])

def formatar_em_reais(valor: float) -> str:
    """Formata usando string.format()."""
    return "R$ {:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_coluna_em_reais(df: pd.DataFrame, nome_coluna: str) -> pd.DataFrame:
    """
    Formata uma coluna em Reais usando f-string.
    """
    df[nome_coluna] = df[nome_coluna].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    return df

df["Mês-Ano"] = df["Data da Venda"].dt.strftime("%Y-%m")

with tab1:

    col1, col2 = st.columns(2)
    with col1:

        vendas_totais = df["Valor da Venda"].sum()
        st.metric("Vendas Totais",f"{formatar_em_reais(vendas_totais)}")
    
    with col2:
        
        comissao_total = df["Comissão"].sum()
        st.metric("Montante de comissões",formatar_em_reais(comissao_total))
    
    st.subheader("Desempenho dos Planos mais Vendidos")
    df_planos = df.groupby('Tipo de Plano Contratado')['Valor da Venda'].sum().reset_index(name="Valor da Venda")
    st.dataframe(df_planos.assign(**{"Valor da Venda": df_planos["Valor da Venda"].apply(formatar_em_reais)}))

    st.subheader("Média de Preço dos Planos")
    df_media = df.groupby('Tipo de Plano Contratado')["Valor da Venda"].mean().reset_index(name='Preço Médio')
    st.dataframe(df_media.assign(**{"Preço Médio":df_media["Preço Médio"].apply(formatar_em_reais)}))
    fig_planos = px.pie(
        df_planos,
        names='Tipo de Plano Contratado',
        values='Valor da Venda',
        title="Participação percentual na Receita Total",
        labels={"Tipo de Plano Contratado":"Plano",
                "Valor da Venda":"Percentual"},
        hole=0.3

    )
    st.plotly_chart(fig_planos,use_container_width=True)

    fig_receita = px.line(
        df.groupby('Mês-Ano')['Valor da Venda'].sum().reset_index(name="Total Vendido").sort_values(by="Mês-Ano",ascending=True),
        x="Mês-Ano",
        y="Total Vendido",
        title="Evolução da Receita Mensal",
        labels={"Total vendido":"Receita Mensal"}
    )
    st.plotly_chart(fig_receita,use_container_width=True)    

with tab2:
    st.subheader(f"Desempenho de {funcionario}")

    col1, col2 = st.columns(2)

    with col1:
        vendas_vendedor = df_filtrado["Valor da Venda"].sum()
        st.metric('Total Vendido',formatar_em_reais(vendas_vendedor))
        st.markdown('----------------')
    with col2:
        comissao_vendedor = df_filtrado['Comissão'].sum()
        st.metric('Total de Comissão',formatar_em_reais(comissao_vendedor))
        st.markdown('------------------')
    
    fig_vendedor = px.bar(
        df_filtrado.groupby("Tipo de Plano Contratado")["Valor da Venda"].sum().reset_index(name='Valor total'),
        x='Tipo de Plano Contratado',
        y="Valor total",
        title="Total de Vendas por Tipo de Plano",
        color=['Gold',"Premium",'Simples']
    )
    st.plotly_chart(fig_vendedor,use_container_width=True)

    df_filtrado["Mes-Ano"] = df["Mês-Ano"]
    fig_funcionario = px.line(
        df_filtrado.groupby('Mes-Ano')['Valor da Venda'].sum().reset_index(name='Vendas'),
        x='Mes-Ano',
        y='Vendas',
        title='Evolução das Vendas Mensais'
    )
    st.plotly_chart(fig_funcionario,use_container_width=True)