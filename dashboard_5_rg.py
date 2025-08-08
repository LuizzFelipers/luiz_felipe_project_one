import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np 
import datetime
import openpyxl

def load_data(arquivo_excel):

    abas_desejadas = ["Emissoes", "Apostilamento"]

    dados = {}
    
    for aba in abas_desejadas:
        try:
            dados[aba] = pd.read_excel(arquivo_excel, sheet_name=aba)
            print(f"Dados da aba ' {aba}' extraídos com sucesso")
        except Exception as e:
            print(f"Erro ao ler a aba ' {aba}': {e}") 
    
    return dados

def formatar_real(valor):

    return f"R$ {valor:,.2f}".replace(',','X').replace('.',',').replace('X','.')

def formatar_para_reais(coluna):
    """
    Formata uma coluna float para o formato de reais brasileiros (R$).
    
    Parâmetros:
    coluna (pd.Series): Coluna do DataFrame contendo valores numéricos
    
    Retorna:
    pd.Series: Coluna formatada como strings no padrão R$ brasileiro
    """
    return coluna.apply(
        lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    )

# GERAL

df_geral = load_data("5_oficio_rg.xlsx")

# ETL DAS EMISSÕES

df_emissoes = df_geral["Emissoes"]

df_emissoes = df_emissoes[["DATA DA SOLICITAÇÃO","VALOR CRC"]]

df_emissoes["Mes"] = df_emissoes["DATA DA SOLICITAÇÃO"].dt.month

mapeamento = {1:"Janeiro",
              2:"Fevereiro",
              3:"Março",
              4:"Abril",
              5:"Maio",
              6:"Junho",
              7:"Julho"}

df_emissoes["Mes"] = df_emissoes["Mes"].replace(mapeamento)

ordem_mensal = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho"]

df_emissoes["Mes"] = pd.Categorical(df_emissoes["Mes"],categories=ordem_mensal,ordered=True)

receita_mensal_emissoes = df_emissoes.groupby('Mes')["VALOR CRC"].sum().reset_index(name="Receita Mensal")

max_mensal = df_emissoes.groupby("Mes")["VALOR CRC"].max().reset_index(name="Maior Valor Mensal")

media_preco_emissoes = df_emissoes["VALOR CRC"].mean()

#CRIANDO O DASHBOARD

st.set_page_config(page_title="Dashboard 5° Oficio RG",layout="wide")
st.title("Dashboard 5° Ofício RG")

tab1, tab2 = st.tabs(["Análise das Emissões","Análise dos Apostilamento"])

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        st.metric("Preço Médio",formatar_real(df_emissoes["VALOR CRC"].mean()))
        st.markdown('------------------')

        fig_receita = px.line(
            receita_mensal_emissoes,
            x='Mes',
            y='Receita Mensal',
            title='Evolução da Receita Mensal'
        )

        st.plotly_chart(fig_receita,use_container_width=True)

    st.markdown('---------------------------')
    with col2:

        st.metric("Receita Total Emissões",formatar_real(df_emissoes["VALOR CRC"].sum()))
        st.markdown('-------------------')

        st.subheader("Tabela das Receitas Mensais")
        receita_mensal_emissoes_df = receita_mensal_emissoes
        receita_mensal_emissoes_df["Receita Mensal"] = formatar_para_reais(receita_mensal_emissoes_df["Receita Mensal"])
        st.dataframe(receita_mensal_emissoes_df)

    col3, col4 = st.columns(2)

    with col3:

        st.metric("**Maior** Preço Registrado", formatar_real(df_emissoes['VALOR CRC'].max()))
        st.markdown('---------------------------------')

        fig_maires_emissoes = px.scatter(
            max_mensal,
            x='Mes',
            y='Maior Valor Mensal',
            title='Maiores Preços Registrados por Mês'
        )
        st.plotly_chart(fig_maires_emissoes,use_container_width=True)

    with col4:

        st.metric("**Menor** Preço Registrado",formatar_real(df_emissoes["VALOR CRC"].min()))
        st.markdown('-----------------')

        st.subheader("Tabela com os Maiores Preços Mensais Registrados")
        max_mensal["Maior Valor Mensal"] = formatar_para_reais(max_mensal["Maior Valor Mensal"])
        st.dataframe(max_mensal)

df_apostilamentos = df_geral["Apostilamento"]

df_apostilamentos["Mes"] = df_apostilamentos["DATA DA FINALIZAÇÃO"].dt.month

maiores_apostilamentos = df_apostilamentos.groupby("Mes")["VALOR"].max().reset_index(name="Maiores Valores")

receita_mensal_apostilamentos = df_apostilamentos.groupby('Mes')["VALOR"].sum().reset_index(name="Receita Mensal")
receita_mensal_apostilamentos["Mes"] = receita_mensal_apostilamentos["Mes"].replace(mapeamento)
receita_mensal_apostilamentos["Mes"] = pd.Categorical(receita_mensal_apostilamentos["Mes"],categories=ordem_mensal,ordered=True)

with tab2:

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Preço Médio Apostilamentos",formatar_real(df_apostilamentos["VALOR"].mean()))
        st.markdown("------------------")

        fig_apostilamento = px.line(
            receita_mensal_apostilamentos,
            x='Mes',
            y='Receita Mensal',
            title="Evolução da Receita Mensal"
            )
        st.plotly_chart(fig_apostilamento,use_container_width=True)
    with col2:
        st.metric("Receita Total Apostilamento",formatar_real(df_apostilamentos["VALOR"].sum()))
        st.markdown("-----------------")

        
        st.subheader("Tabela das Receitas Mensais")
        receita_mensal_apostilamentos["Receita Mensal"] = formatar_para_reais(receita_mensal_apostilamentos["Receita Mensal"])
        st.dataframe(receita_mensal_apostilamentos)

    st.markdown("-----------------------")

    col3, col4 = st.columns(2)

    maiores_apostilamentos["Mes"] = maiores_apostilamentos["Mes"].replace(mapeamento)

    with col3:
        st.metric("**Maior** Preço Registrado",formatar_real(df_apostilamentos["VALOR"].max()))
        st.markdown("-------------------")

        fig_maiores_apostilamentos = px.scatter(
            maiores_apostilamentos,
            x="Mes",
            y="Maiores Valores",
            title="Maiores Preços Registrados por Mês",
            color="Maiores Valores"
        )
        st.plotly_chart(fig_maiores_apostilamentos,use_container_width=True)

        with col4:
            st.metric("**Menor** Preço Registrado",formatar_real(df_apostilamentos["VALOR"].max()))
            st.markdown("--------------")

            st.subheader("Tabela com os Maiores Preços Mensais Registrados")
            maiores_apostilamentos["Maiores Valores"] = formatar_para_reais(maiores_apostilamentos["Maiores Valores"])

            st.dataframe(maiores_apostilamentos)
