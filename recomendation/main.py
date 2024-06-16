import pickle
import random

import requests
import streamlit as st

from recomendation.funcaoRecomendacao import recomendar

API_KEY = "66b500a682ff9d5442d293c4e75e4f6a"


def fetch_nome(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US")
    data = response.json()
    return data['title']


def fetch_id(nome_filme):
    response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={nome_filme}&language=en-US")
    data = response.json()
    if data['total_results'] > 0:
        return data['results'][0]['id']
    else:
        return None


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def fetch_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    overview = data.get('overview', 'No overview available.')

    streaming_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    streaming_data = requests.get(streaming_url).json()

    regions = ['US', 'BR', 'CA', 'UK']  # Example regions to check
    platforms_list = []
    for region in regions:
        platforms = streaming_data.get('results', {}).get(region, {}).get('flatrate', [])
        if platforms:
            platforms_list = [platform['provider_name'] for platform in platforms]
            break

    if not platforms_list:
        platforms_list = ["Not available on streaming platforms"]

    return overview, platforms_list


lista_filmes_inseridos = ['Avatar', 'Raging Bull']
lista_id_filmes_inseridos = []
lista_recomendacao = []
lista_id_recomendacao = []


for nome_filme in lista_filmes_inseridos:
    # nome_filme = input("Digite o nome do filme: ")
    id_filme = fetch_id(nome_filme)

    # lista_filmes_inseridos.append(nome_filme)
    lista_id_filmes_inseridos.append(id_filme)

    recomendacao, ids = recomendar(nome_filme)
    lista_recomendacao += recomendacao
    lista_id_recomendacao += ids


# remover todas as duplicatas dos ids dos filmes recomendados
lista_id_recomendacao = list(set(lista_id_recomendacao))

# remover todos os ids dos filmes de entrada:
lista_id_recomendacao = [item for item in lista_id_recomendacao if item not in lista_id_filmes_inseridos]

# embaralhar todos os elementos da lista
random.shuffle(lista_id_recomendacao)

# reduzir a lista para os 10 primeiros elementos
if (len(lista_id_recomendacao) > 10):
    lista_id_recomendacao = lista_id_recomendacao[0:10]

# for elem in lista_id_recomendacao:
#    print(fetch_nome(elem))


# FRONT-END
movies = pickle.load(open('recomendation/movie_list.pkl', 'rb'))
movie_list = movies['title'].values

st.header('CineMatch')

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


if st.button('Show Recommendation'):
    # recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)
    for i in range(10):
        with st.expander(fetch_nome(lista_id_recomendacao[i])):
            st.image(fetch_poster(lista_id_recomendacao[i]))
            overview, platforms = fetch_details(lista_id_recomendacao[i])
            st.write(f"**Overview:** {overview}")
            st.write(f"**Available on:** {', '.join(platforms)}")
