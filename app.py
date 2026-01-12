import pickle
import streamlit as st
import requests
import gdown
import os


@st.cache_resource
def load_pickle_files():

    movie_file = "movie_list.pkl"
    sim_file = "similarity.pkl"

    if not os.path.exists(movie_file):
        gdown.download(
            id="1Lh9cEopyWpNCcoilduEgiu6y_5YTSxyr",
            output=movie_file,
            quiet=False
        )

    if not os.path.exists(sim_file):
        gdown.download(
            id="1L6koy5JukBaq53nc1qWekz_1-MJuf6Gn",
            output=sim_file,
            quiet=False
        )

    movies = pickle.load(open(movie_file, "rb"))
    sim = pickle.load(open(sim_file, "rb"))

    return movies, sim

movies, sim = load_pickle_files()

def fetch_poster(movie_id):
    api_key="77ca019044b03eaa11428ee82d739169"
    url="https://api.themoviedb.org/3/movie/{}?api_key=77ca019044b03eaa11428ee82d739169&language=en-US".format(movie_id)
    data =requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="http://image.tmdb.org/t/p/w500/"+ poster_path
    return full_path

def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distances=sorted(list(enumerate(sim[index])), reverse=True,key=lambda x:x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name,recommended_movies_poster

st.header("Movie recommendation system using ML.")

#movies=pickle.load(open("pickle files\movie_list.pkl",'rb'))
#sim=pickle.load(open("pickle files\similarity.pkl",'rb'))

movie_list=movies['title'].values
selected_mov=st.selectbox(
    'select movie to get recommendation',
    movie_list
)


if st.button('Show Recommendation'):
    recommended_movies_name,recommended_movies_poster=recommend(selected_mov)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])