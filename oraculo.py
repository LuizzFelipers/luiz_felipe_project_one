import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('dados.csv',sep = ';')  


vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(df['Perguntas']) 


def responder_pergunta(pergunta_usuario):
    
    pergunta_vetor = vectorizer.transform([pergunta_usuario])
    
    
    similaridades = cosine_similarity(pergunta_vetor, tfidf_matrix)
    
   
    indice_mais_similar = similaridades.argmax()
    
   
    return df.iloc[indice_mais_similar][' Respostas']


print("Assistente Virtual - Digite 'sair' para encerrar")
while True:
    pergunta = input("\nComo posso te ajudar? ")
    
    if pergunta.lower() == 'sair':
        print("Até logo!")
        break
        
    resposta = responder_pergunta(pergunta)
    print(f"\nResposta: {resposta}")



