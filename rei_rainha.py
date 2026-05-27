import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------
st.set_page_config(
    page_title=" | Rei e Rainha da Pipoca",
    page_icon="🍿",
    layout="wide"
)

st.title("🍿 Ranking Rei e Rainha da Pipoca")
st.markdown("---")

# ------------------------------
# CARREGAR OU CRIAR OS DADOS
# ------------------------------
ARQUIVO_CSV = "dados_pipoca.csv"


def load_data():
    return pd.read_excel("rei_rainha.xlsx")

df = load_data()

# ------------------------------
# FUNÇÃO PARA EXIBIR RANKING (TABELA + GRÁFICO)
# ------------------------------
def exibir_ranking(df_filtrado, titulo):
    if df_filtrado.empty:
        st.warning("Nenhum dado disponível para esta turma.")
        return

    # Ordenar por bilhetes vendidos (decrescente)
    df_rank = df_filtrado.sort_values("Bilhetes vendidos", ascending=False).reset_index(drop=True)
    df_rank.insert(0, "Posição", range(1, len(df_rank) + 1))

    # Tabela
    st.subheader(f"📊 {titulo}")
    st.dataframe(df_rank, use_container_width=True, hide_index=True)

    # Gráfico de barras (top 10 ou todos)
    st.subheader("📈 Visualização das pontuações")
    top_n = min(10, len(df_rank))
    df_top = df_rank.head(top_n)
    
    fig = px.bar(
        df_top,
        x="Bilhetes vendidos",
        y="Nome do Aluno",
        orientation="h",
        color="Tipo",
        text="Bilhetes vendidos",
        title=f"Top {top_n} - {titulo}",
        labels={"Bilhetes vendidos": "Bilhetes Vendidos", "Nome do Aluno": "Aluno"},
        color_discrete_map={"Rei": "#2c3e50", "Rainha": "#e74c3c"}
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=500)
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# CONSTRUÇÃO DAS ABAS
# ------------------------------

turmas_title = ["📌 Ranking Geral","👶 Creche", "🧸 Pré I", "🎈 Pré II", "🎓 1º Ano", "🎓 2º Ano", "🎓 3º Ano", "🎓 4º Ano"]

tabs = st.tabs(turmas_title)

turmas = df["Turma"].unique()
turmas = [turma for turma in turmas if turma != "Geral"]
# Aba Geral
with tabs[0]:
    exibir_ranking(df, "Ranking Geral (Todas as Turmas)")

# Aba para cada turma
for i, turma in enumerate(turmas, start=1):
    with tabs[i]:
        df_turma = df[df["Turma"] == turma]
        exibir_ranking(df_turma, f"Ranking da Turma {turma}")