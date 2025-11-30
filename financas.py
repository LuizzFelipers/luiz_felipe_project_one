import pandas as pd
import streamlit as st
import plotly.express as px
import requests
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

st.set_page_config(layout="wide",
                   page_icon="",
                   page_title="Blue Chips Vs Startups",
                   initial_sidebar_state="expanded")

def get_data(data_inicial, data_final,codigo):

    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        dados = response.json()
        
        df = pd.DataFrame(dados)
        df["data"] = pd.to_datetime(df["data"], dayfirst=True)
        df["valor"] = pd.to_numeric(df["valor"])

        return df
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisião: {e}")
        return None
    
def get_etf(ticker, start_date, end_date):
    try:
        etf = yf.download(ticker, start_date, end_date)
        etf["Returns"] = etf["Close"].pct_change()
        etf['Cumulative_Returns'] = (1 + etf['Returns']).cumprod()
    
        return etf
    
    except Exception as e:
        st.error(f"Erro ao Buscar dados do ETF: {ticker}: {e}")
    
        return None
    
ETFS = {
    "BLUE_CHIPS": {
        "BOVA11.SA": "Ibovespa (Brasil)"
    },
    "STARTUPS": {
        "SMAL11.SA":"Small Caps - br"
    }
}


st.sidebar.header("Selecione o Período de Análise")
data_inicio = st.sidebar.date_input("Data Inicial", value=datetime(2015,1,1))
data_fim = st.sidebar.date_input("Data Final", value=datetime(2025,1,1))

data_inicio_str = data_inicio.strftime("%d/%m/%Y")
data_fim_str = data_fim.strftime("%d/%m/%Y")

with st.spinner("Carregando dados do BACEN..."):

    selic = get_data(data_inicial=data_inicio_str, data_final=data_fim_str, codigo=432)
    
    ipca = get_data(data_inicial=data_inicio_str, data_final=data_fim_str, codigo=433)
    
    cambio = get_data(data_inicial=data_inicio_str, data_final=data_fim_str, codigo=1)
    
    pib = get_data(data_inicial=data_inicio_str, data_final=data_fim_str, codigo=4380)

    etf_data = {}
    for category, etfs in ETFS.items():
        for ticker, name in etfs.items():
            etf_data[ticker] = get_etf(ticker, data_inicio, data_fim)


st.header(" Blue Chips Vs Startups")
st.markdown("----------------")
st.write("Qual o Impacto dos principais indicadores Macroeconômicos em Empresas Consolidadas e Empresas em Crescimento")
st.markdown("-------------------")
st.subheader(" Evolução dos Indicadores Macroeconômicos")

if all(df is not None for df in [selic, ipca, cambio, pib]):

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Taxa Selic (%)", "IPCA Mensal (%)", "Câmbio USD/BRL", "PIB (Var. % Anual)"),
        vertical_spacing=0.1
    )

    # SELIC
    fig.add_trace(
        go.Scatter(x=selic['data'], y=selic['valor'], name="Selic", line=dict(color='red')),
        row=1, col=1
    )

    #IPCA
    fig.add_trace(
        go.Scatter(x=ipca['data'], y=ipca['valor'], name="IPCA", line=dict(color='blue')),
        row=1, col=2
    )

    #CÂMBIO
    fig.add_trace(
        go.Scatter(x=cambio['data'], y=cambio['valor'], name="Câmbio", line=dict(color='green')),
        row=2, col=1
    )

    #PIB
    fig.add_trace(
        go.Scatter(x=pib['data'], y=pib['valor'], name="PIB", line=dict(color='orange')),
        row=2, col=2
    )

    fig.update_layout(height=600, showlegend=False, title_text="Indicadores Macroeconômicos - Série Histórica")
    
    st.plotly_chart(fig, use_container_width=True)

if all(etf_data.get(ticker) is not None for ticker in list(ETFS["BLUE_CHIPS"].keys())[:1] + list(ETFS["STARTUPS"].keys())[:1]):
    
    # Gráfico de performance comparativa dos ETFs
    fig_etf = go.Figure()
    
    # Adicionando ETFs Blue Chips
    for ticker, name in ETFS["BLUE_CHIPS"].items():
        if etf_data.get(ticker) is not None:
            fig_etf.add_trace(go.Scatter(
                x=etf_data[ticker].index,
                y=etf_data[ticker]['Cumulative_Returns'] * 100,
                name=f"🏢 {name}",
                line=dict(width=3)
            ))
    
    # Adicionando ETFs Startups
    for ticker, name in ETFS["STARTUPS"].items():
        if etf_data.get(ticker) is not None:
            fig_etf.add_trace(go.Scatter(
                x=etf_data[ticker].index,
                y=etf_data[ticker]['Cumulative_Returns'] * 100,
                name=f"🚀 {name}",
                line=dict(width=3, dash='dash')
            ))
    
    fig_etf.update_layout(
        title='Performance Acumulada dos ETFs - Retorno Percentual',
        xaxis_title='Data',
        yaxis_title='Retorno Acumulado (%)',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_etf, use_container_width=True)