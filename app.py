import streamlit as st
import pickle
import pandas as pd
import requests

# def fetch_poster(movie_id):
#     # response = requests.get('https://api.themoviedb.org/3/movie/%7B65%7D'.format(movie_id))
#     response = requests.get('https://api.themoviedb.org/3/movie/{movie_id}', timeout=10)
#
#     data = response.json()
#
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



import requests
import tenacity
@tenacity.retry(wait=tenacity.wait_exponential(max=60), stop=tenacity.stop_after_attempt(5), reraise=True)

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=540b8d1ca82df89ecff8cc48830d1065'

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        data = response.json()
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return None  # Poster path not found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None



# import requests

# def fetch_poster(movie_id):
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d83f3a41c098474a55ec2fef98985a45'
#     try:
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
#         data = response.json()
#         if 'poster_path' in data:
#             return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#         else:
#             return None  # Poster path not found
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching poster: {e}")
#         return None


@st.cache_data
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse=True,key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  #oth item in the row i.e. i is the movie id
        #fetch poster from API
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
'Enter a movie',
movies['title'].values)


# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#     col1, col2, col3 ,col4, col5= st.columns(5)
#
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])



if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        if posters[0] is not None:
            st.image(posters[0])
        else:
            st.write("Poster not available")

    with col2:
        st.text(names[1])
        if posters[1] is not None:
            st.image(posters[1])
        else:
            st.write("Poster not available")

    with col3:
        st.text(names[2])
        if posters[2] is not None:
            st.image(posters[2])
        else:
            st.write("Poster not available")

    with col4:
        st.text(names[3])
        if posters[3] is not None:
            st.image(posters[3])
        else:
            st.write("Poster not available")

    with col5:
        st.text(names[4])
        if posters[4] is not None:
            st.image(posters[4])
        else:
            st.write("Poster not available")

















# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#     cols = st.columns(len(posters))
#     for i, poster_url in enumerate(posters):
#         with cols[i]:
#             if poster_url is not None:
#                 st.image(poster_url, caption=names[i])
#             else:
#                 st.write("Poster not available")
