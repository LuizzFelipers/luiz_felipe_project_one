import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Oráculo",
    page_icon="🔮"
)

st.title("🔮 Oráculo")

df = pd.read_csv('dados.csv', sep=';')

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Perguntas'])

def responder_pergunta(pergunta_usuario):
    pergunta_vetor = vectorizer.transform([pergunta_usuario])
    similaridades = cosine_similarity(pergunta_vetor, tfidf_matrix)
    indice_mais_similar = similaridades.argmax()
    return df.iloc[indice_mais_similar][' Respostas']

pergunta = st.text_input("Digite sua pergunta:", placeholder="Ex: Horário de Funcionamento")

if pergunta:
    resposta = responder_pergunta(pergunta)
    st.write(resposta)




