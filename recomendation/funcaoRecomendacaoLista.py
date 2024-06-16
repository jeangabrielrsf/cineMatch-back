import os
import pickle

import pandas as pd

print(os.getcwd())


def recomendar(lista_filmes):
    dicionario = pickle.load(open('recomendation/dicionario_filmes.pkl', 'rb'))
    filmes = pd.DataFrame(dicionario)
    similaridade = pickle.load(open('recomendation/similaridade.pkl', 'rb'))

    distancias_acumuladas = None

    for filme in lista_filmes:
        if filme in filmes['title'].values:
            indice_filme = filmes[filmes['title'] == filme].index[0]
            distancias = similaridade[indice_filme]
            if distancias_acumuladas is None:
                distancias_acumuladas = distancias
            else:
                distancias_acumuladas += distancias
        else:
            print(f"Filme '{filme}' não encontrado na base de dados.")

    if distancias_acumuladas is not None:
        distancias_medias = distancias_acumuladas / len(lista_filmes)
        lista_filmes_recomendados = sorted(list(enumerate(distancias_medias)), reverse=True, key=lambda x: x[1])

        filmes_recomendados = []
        id_filmes = []
        for i in lista_filmes_recomendados:
            id_filme = filmes.iloc[i[0]].movie_id
            titulo_filme = filmes.iloc[i[0]].title
            if titulo_filme not in lista_filmes:
                id_filmes.append(id_filme)
                filmes_recomendados.append(titulo_filme)
            if len(filmes_recomendados) >= 10:
                break

        return filmes_recomendados, id_filmes
    else:
        return [], []

# Exemplo de uso


lista_de_filmes = ["Toy Story", "Shrek"]
recomendacoes, ids = recomendar(lista_de_filmes)
print("Filmes recomendados:", recomendacoes)
print("IDs dos filmes recomendados:", ids)
