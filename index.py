import streamlit as st
import pandas as pd
from Model_Files_and_Datasets.movieRecommenderModel import recommend, main_df

# ''' (In the case of using the pickle files)
# import pickle
# moviesDict = pickle.load(open('moviesDict2.pkl', 'rb'))
# similarity = pickle.load(open('similarity2.pkl', 'rb'))
# movies = pd.DataFrame(moviesDict)
# movies['title'] = movies['title'] + ' (' + movies['release_date'] + ')'
# movies.drop(movies[(movies['title']=='Batman') & (movies['release_date']=='1966')].index, inplace=True)
# movies["title"] = movies["title"] + " (" + movies["release_date"] + ")"

# def recommend(movie):
#     movieIndex = movies[movies['title'] == movie].index[0]
#     distances = list(enumerate(similarity[movieIndex]))
#     distances = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
#     moviesArr = []
#     for i in distances:
#         movieArr = {}
#         movieArr["title"] = movies.iloc[i[0]]["title"]
#         movieArr["id"] = movies.iloc[i[0]]["movie_id"].item()
#         movieArr["date"] = movies.iloc[i[0]]["release_date"]
#         moviesArr.append(movieArr)
#     return moviesArr
# '''


movies = main_df.copy()

st.title("Movie Recommender System")
option = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values,
)
if st.button('Recommend'):
    st.write('Recommending movies similar to:', option)
    recommendDict = recommend(option)
    for i in recommendDict:
        st.write(i['title'])
