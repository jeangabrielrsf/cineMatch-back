import pickle

import pandas as pd


def recomendar(filme):
    dicionario = pickle.load(open('recomendation/dicionario_filmes.pkl', 'rb'))
    filmes = pd.DataFrame(dicionario)
    similaridade = pickle.load(open('recomendation/similaridade.pkl', 'rb'))

    indice_filme = filmes[filmes['title'] == filme].index[0]
    distancias = similaridade[indice_filme]
    lista_filmes = sorted(list(enumerate(distancias)), reverse=True, key=lambda x: x[1])[1:11]

    filmes_recomendados = []
    id_filmes = []
    for i in lista_filmes:
        id_filme = filmes.iloc[i[0]].movie_id
        id_filmes.append(id_filme)
        filmes_recomendados.append(filmes.iloc[i[0]].title)

    return filmes_recomendados, id_filmes
