import pandas as pd
import streamlit as st
import plotly.express as px
import json
import requests


st.set_page_config(layout="wide",
                   page_icon="🚗",
                   page_title=" | Detran Analytics")

st.title("🚨Análise dos Acidentes Registrados no Brasil - **2025**")


# Data Preparetion
df = pd.read_csv("datatran2025.csv",sep=";", encoding="latin-1")

df = df[["data_inversa",
         "dia_semana",
         "horario",
         "uf",
         "br",
         "km",
         "municipio",
         "causa_acidente",
         "tipo_acidente",
         "classificacao_acidente",
         "fase_dia",
         "condicao_metereologica",
         "pessoas",
         "mortos",
         "feridos_graves",
         "latitude",
         "longitude"
         ]]

df = df.dropna()

tab1, tab2 = st.tabs(["Geral", "Específico"])

with tab1:
    st.subheader("Visão Geral")
    st.markdown("-----------------------")
    col1, col2, col3 = st.columns(3)

    with col1:
        qtd_acidentes = len(df)
        st.metric("⚠️ Quantidade de **Acidentes**", qtd_acidentes)

    with col2:
        qtd_mortos = df["mortos"].sum()
        st.metric("💀 Quantidade de **Óbitos**", qtd_mortos)

    with col3:
        qtd_feridos = df["feridos_graves"].sum()
        st.metric("🤒 Quantidade de Feridos **Gravemente**", qtd_feridos)



    st.markdown("--------")

    col4, col5, col6 = st.columns(3)

    with col4:
        fase_dia = df["fase_dia"].value_counts().reset_index(name="Quantidade")

        indice_maior = fase_dia['Quantidade'].idxmax()
        pull_list = [0.1 if i == indice_maior else 0 for i in range(len(fase_dia))]

        fig_fase_dia = px.pie(
            fase_dia,
            names="fase_dia",
            values="Quantidade",
            hole=0.5,
            title="Fase do Dia com mais Acidentes",
            color_discrete_sequence=px.colors.sequential.Reds_r
            )
        fig_fase_dia.update_traces(
        pull=pull_list,
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
    )

        st.plotly_chart(fig_fase_dia,use_container_width=True)

    with col5:
        dia_semana_mais_perigoso = df.groupby("dia_semana")["mortos"].sum().reset_index(name="Quantidade").sort_values(by="Quantidade", ascending=False)
        
        indice_maior = dia_semana_mais_perigoso['Quantidade'].idxmax()
        pull_list = [0.1 if i == indice_maior else 0 for i in range(len(dia_semana_mais_perigoso))]

        
        fig_dia_semana = px.pie(
            dia_semana_mais_perigoso,
            names="dia_semana",
            values="Quantidade",
            hole=0.5,
            title="Dia da Semana com mais Óbitos",
            color_discrete_sequence=px.colors.sequential.Oranges_r
            )
        fig_dia_semana.update_traces(
        pull=pull_list,
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
        )
        st.plotly_chart(fig_dia_semana, use_container_width=True)

    with col6:
        url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
        response = requests.get(url_geojson)
        geojson_brasil = response.json()

        uf_dados = df.groupby("uf")["mortos"].sum().reset_index(name="Quantidade de Mortos").sort_values(by="Quantidade de Mortos", ascending=False)

        fig = px.choropleth(
        uf_dados,
        geojson=geojson_brasil,
        locations='uf',  # Sua coluna com siglas (SP, RJ, MG, etc.)
        featureidkey="properties.sigla",  # Chave que corresponde às siglas no GeoJSON
        color='Quantidade de Mortos',  # Sua coluna numérica para colorir
        hover_name='uf', # Suas outras colunas
        color_continuous_scale='Reds',
        title='Mapa de Acidentes com Óbitos por UF - Brasil'
    )
        fig.update_traces(
        marker_line=dict(width=1, color='red')

    )
        fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        geo=dict(
            bgcolor='black',
            lakecolor='black',
            landcolor='darkgray'
        )
    )
        fig.update_geos(
        visible=False,
        fitbounds="locations",
        subunitcolor="black"
    )
        st.plotly_chart(fig, use_container_width=True)
        
    st.markdown("----------------")

    df["data_inversa"] = pd.to_datetime(df["data_inversa"])
    df['mes_ano'] = df['data_inversa'].dt.strftime('%m-%Y')
    # ou
    df['mes_ano'] = df['data_inversa'].dt.to_period('M').astype(str)

    mes_mortos = df.groupby("mes_ano")["mortos"].sum().reset_index(name="Quantidade de Mortos")

    fig_mes = px.line(
        mes_mortos,
        x="mes_ano",
        y="Quantidade de Mortos",
        title="Quantidade de óbitos por Mês",
        markers=True,
        line_shape='spline',
        text="Quantidade de Mortos",
        labels={"mes_ano":"Mês e Ano"}


    )
    


    fig_mes.update_traces(
        mode="lines+markers+text",
        text=mes_mortos["Quantidade de Mortos"],
        textposition="top center",
        texttemplate="%{text} Óbitos",
        textfont=dict(size=12,color="#FF0000"),
        line=dict(width=3, color='#6E0000'),
        marker=dict(size=12)
    )


    st.plotly_chart(fig_mes,use_container_width=True)
    st.markdown("----------------------")

    qtd_acidentes_mes = df["mes_ano"].value_counts().reset_index(name="Quantidade de acidentes").sort_values(by="mes_ano", ascending=True)

    fig_qtd_acidentes = px.line(
        qtd_acidentes_mes,
        x="mes_ano",
        y="Quantidade de acidentes",
        title="Quantidade de Acidentes por Mês",
        labels={"mes_ano":"Mês e Ano"},
        markers=True,
        line_shape='spline',
        text="Quantidade de acidentes"

    )

    fig_qtd_acidentes.update_traces(
        mode="lines+markers+text",
        text=qtd_acidentes_mes["Quantidade de acidentes"],
        textposition="top center",
        texttemplate="%{text} Registros",
        textfont=dict(size=12,color="#FF7B00"),
        line=dict(width=3, color="#872D00"),
        marker=dict(size=12)
    )
    st.plotly_chart(fig_qtd_acidentes, use_container_width=True)


with tab2:
    st.subheader("🔎 Visão Específica")
    st.markdown("---------------------")

    col1, col2, col3 = st.columns(3)
    
    trecho_letal = df.groupby(["municipio","km","br"])["mortos"].sum().reset_index(name="Quantidade de Mortes").sort_values(by="Quantidade de Mortes", ascending=False)
    
    #mais letal
    
    idx_mais_letal = trecho_letal['Quantidade de Mortes'].idxmax()
    br_mais_letal =  trecho_letal.loc[idx_mais_letal, 'br']
    km_mais_letal =  trecho_letal.loc[idx_mais_letal, 'km']
    municipio_mais_letal =  trecho_letal.loc[idx_mais_letal, 'municipio']
    mortos =  trecho_letal.loc[idx_mais_letal, 'Quantidade de Mortes']
    
    #menos letal

    idx_menos_letal = trecho_letal["Quantidade de Mortes"].idxmin()
    br_menos_letal = trecho_letal.loc[idx_menos_letal, "br"]
    km_menos_letal = trecho_letal.loc[idx_menos_letal, "km"]
    municipio_menos_letal = trecho_letal.loc[idx_menos_letal, "municipio"]
    mortos_menor = trecho_letal.loc[idx_menos_letal, "Quantidade de Mortes"]

    
    with col1:

        qtd_uf = df["uf"].value_counts().reset_index(name="Quantidade")
        uf_maior_acidentes = qtd_uf.loc[qtd_uf['Quantidade'].idxmax(), 'uf']
        valor_maior_acidentes = qtd_uf['Quantidade'].max()
        
        st.metric("🗺️**UF** com maior número de Acidentes", uf_maior_acidentes,delta=f"{valor_maior_acidentes} acidentes")

        qtd_uf = df["uf"].value_counts().reset_index(name="Quantidade")
        uf_menor_acidentes = qtd_uf.loc[qtd_uf['Quantidade'].idxmin(), 'uf']
        valor_menor_acidentes = qtd_uf['Quantidade'].min()
        
        st.metric("🗺️**UF** com menor número de Acidentes", uf_menor_acidentes,delta=f"{valor_menor_acidentes} acidentes" )        

    with col2:

        st.metric("🏙️ Município **mais Letal**", municipio_mais_letal, delta=f"{mortos} óbitos")

        st.metric("🏙️ Município **menos Letal**", municipio_menos_letal, delta=f"{mortos_menor} óbitos" )


    with col3:
        
        st.metric(
            label="🚨 Trecho mais **Letal** do País",
            value=f"BR - {br_mais_letal} | KM {km_mais_letal}",
            delta=f"{mortos} óbitos"
            )
        
        st.metric(
            label="😌 Trecho Menos **Letal**",
            value= f"BR - {br_menos_letal} | KM {km_menos_letal}",
            delta=f"{mortos_menor} óbitos"
        )
        
    

    st.markdown("------------------------")

    df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.time

    def classificar_faixa_horaria(horario):
        hora = horario.hour
        if 5 <= hora < 12:
            return 'Manhã'
        elif 12 <= hora < 18:
            return 'Tarde'
        elif 18 <= hora < 24:
            return 'Noite'
        else:
            return 'Madrugada'

    # Aplicar a classificação
    
    df['faixa_horaria'] = df['horario'].apply(classificar_faixa_horaria)

    horario_qtd_acidentes = df["faixa_horaria"].value_counts().reset_index(name="Qtd acidentes")

    horario_analise = df.groupby("faixa_horaria")["mortos"].sum().reset_index(name="mortos")

    def formatar(valor):
        return f"{valor:,.0f}".replace(",",".")
    
    horario_analise["mortos"] = horario_analise["mortos"].apply(formatar)


    col7, col8 = st.columns(2)

    with col7:
        
        indice_maior = horario_qtd_acidentes['Qtd acidentes'].idxmax()
        pull_list = [0.1 if i == indice_maior else 0 for i in range(len(horario_qtd_acidentes))]
        
        fig_qtd = px.pie(
            horario_qtd_acidentes,
            names="faixa_horaria",
            values="Qtd acidentes",
            title="Quantidade de Acidentes por Faixa Horária",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        fig_qtd.update_traces(
        pull=pull_list,
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
        )

        st.plotly_chart(fig_qtd, use_container_width=True)

    with col8:
        
        horario_analise = horario_analise.sort_values(by="mortos", ascending=False)

        indice_maior = horario_analise['mortos'].idxmax()
        pull_list = [0.1 if i == indice_maior else 0 for i in range(len(horario_analise))]

        fig_mortos = px.pie(
            horario_analise,
            names="faixa_horaria",
            values="mortos",
            title="Faixa de Horário com mais Óbitos",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Purples_r
        )

        fig_mortos.update_traces(
        pull=pull_list,
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
        )
        st.plotly_chart(fig_mortos, use_container_width=True)

    st.markdown("-----------------")

    tipo_acidente = df["tipo_acidente"].value_counts().reset_index(name="Quantidade de registro").sort_values(by="Quantidade de registro", ascending=False).head()
    tipo_acidente_fatal = df.groupby("tipo_acidente")["mortos"].sum().reset_index(name="Quantidade de mortos").sort_values(by="Quantidade de mortos", ascending=False).head()
    condicao_metereologica = df["condicao_metereologica"].value_counts().reset_index(name="Quantidade de Registro")
    causa_acidente = df["causa_acidente"].value_counts().reset_index(name="Quantidade").sort_values(by="Quantidade", ascending=False).head()

    col10, col11 = st.columns(2)

    fig_tipo_acidente = px.bar(
        tipo_acidente,
        x="tipo_acidente",
        y="Quantidade de registro",
        title="Tipo de Acidente mais frequente",
        color="tipo_acidente"
    )

    with col10:
        fig_tipo_acidente = px.bar(
            tipo_acidente,
            x="tipo_acidente",
            y="Quantidade de registro",
            title="Tipo de Acidente mais frequente",
            color="tipo_acidente",
            color_discrete_sequence=px.colors.sequential.Redor_r
            )

        fig_tipo_acidente.update_layout(
            xaxis_title='Mês',
            yaxis_title='Número de Acidentes',
            showlegend=False
        )
        
        st.plotly_chart(fig_tipo_acidente, use_container_width=True)
        
        st.markdown("------------------------")

        fig_condicao_metedeorologiaca = px.scatter(
            condicao_metereologica,
            x="condicao_metereologica",
            y="Quantidade de Registro",
            title="Quantidade de Acidentes por Condições Metereologicas",
            color="condicao_metereologica",
            size_max=15,
            labels={"condicao_metereologica":"Condição Metereológica"}
        )

        st.plotly_chart(fig_condicao_metedeorologiaca,use_container_width=True)

    with col11:
        fig_tipo_fatal = px.bar(
            tipo_acidente_fatal,
            x="tipo_acidente",
            y="Quantidade de mortos",
            title="Tipo de Acidente mais Fatal",
            color="tipo_acidente",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_tipo_fatal.update_layout(
            xaxis_title='Mês',
            yaxis_title='Número de Acidentes',
            showlegend=False
        )
        
        st.plotly_chart(fig_tipo_fatal, use_container_width=True)

        st.markdown("------------------------")

        indice_maior = causa_acidente['Quantidade'].idxmax()
        pull_list = [0.1 if i == indice_maior else 0 for i in range(len(causa_acidente))]

        fig_causa_acidente = px.pie(
            causa_acidente,
            names="causa_acidente",
            values="Quantidade",
            title="Maiores Causas de Acidentes no País",
            hole=0.5,
            labels={"causa_acidente":"Causas de Acidentes"},
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_causa_acidente.update_traces(
        pull=pull_list,
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
        )

        st.plotly_chart(fig_causa_acidente,use_container_width=True)

