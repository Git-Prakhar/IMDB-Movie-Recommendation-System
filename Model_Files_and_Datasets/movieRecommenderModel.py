# Libraries.
import pandas as pd
import numpy as np
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Getting the datasets.
movies_df = pd.read_csv("Model_Files_and_Datasets/tmdb_5000_movies.csv")
credits_df = pd.read_csv("Model_Files_and_Datasets/tmdb_5000_credits.csv")

movies_df.rename(columns={'id':'movie_id'}, inplace=True)

# Merging the 2 datasets into a new dataframe.
movies = movies_df.merge(credits_df, on="movie_id")
movies = movies.drop('title_y', axis=1)
movies.rename(columns={'title_x':'title'}, inplace=True)

# Selecting only necessary columns.
movies = movies[["movie_id", "title", "overview", "genres", "keywords", "cast", "crew", "release_date"]]

# Dropping null values (because there are only 3 out of ~5000 rows that are null).
movies.dropna(inplace=True)

# Removing duplicates based on the 'movie_id' column and keeping the first.
movies = movies.drop_duplicates(subset='movie_id', keep='first')

# Converting 'genres', 'keywords', 'cast' and 'crew' columns from string list of dictionaries to list of strings
# with only the names of the genres, keywords, top 3 casts and director (from the crew) respectively.
movies["genres"] = movies["genres"].apply(
    lambda x: [col["name"] for col in ast.literal_eval(x)]
)
movies["keywords"] = movies["keywords"].apply(
    lambda x: [col["name"] for col in ast.literal_eval(x)]
)
movies["cast"] = movies["cast"].apply(
    lambda x: [col["name"] for col in ast.literal_eval(x)[0:3]]
)
movies["crew"] = movies["crew"].apply(
    lambda x: [col["name"] for col in ast.literal_eval(x) if col["job"] == "Director"][:1]
)
movies['release_date'] = movies['release_date'].apply(
    lambda x: str(x[0:4])
)

# Splitting the overview column into a list of words.
movies["overview"] = movies["overview"].apply(lambda x: x.split())

# Removing spaces from the genres, keywords, cast and crew columns.
movies["genres"] = movies["genres"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["keywords"] = movies["keywords"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["cast"] = movies["cast"].apply(lambda x: [i.replace(" ", "") for i in x])
movies["crew"] = movies["crew"].apply(lambda x: [i.replace(" ", "") for i in x])

# Combining the overview, genres, keywords, cast and crew columns into a single 'tag' column.
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)

# Creating the main dataframe with 3 columns: 'movie_id', 'title' and 'tags'.
main_df = movies[["movie_id", "title", "tags", "release_date"]]

# Turning the 'tags' column into a string and in lower caps.
main_df["tags"] = main_df["tags"].apply(lambda x: " ".join(x))
main_df["tags"] = main_df["tags"].apply(lambda x: x.lower())

# Stemming the tags column. (Stemming is the process of reducing a word to its word stem. : 'running' -> 'run')
ps = PorterStemmer()
main_df["tags"] = main_df["tags"].apply(
    lambda x: " ".join([ps.stem(i) for i in x.split()])
)

# Creating a CountVectorizer object with a maximum of 5000 features and removing english stop words.
# Vectorizing the 'tags' column. (Vectorization is the process of converting text data into numerical data.)
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(main_df["tags"]).toarray()

# Calculating the cosine similarity between the vectors.
# (Cosine similarity is a metric used to measure how similar the documents are irrespective of their size.)
similarity = cosine_similarity(vectors)

main_df.drop(main_df[(main_df['title']=='Batman') & (main_df['release_date']=='1966')].index, inplace=True)
main_df["title"] = main_df["title"] + " (" + main_df["release_date"] + ")"

# Function to recommend movies based on the input movie.
def recommend(movie):
    movieIndex = main_df[main_df["title"] == movie].index[0]
    distances = list(enumerate(similarity[movieIndex]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    moviesArr = []
    for i in distances:
        movieArr = {}
        movieArr["title"] = main_df.iloc[i[0]]["title"]
        movieArr["id"] = main_df.iloc[i[0]]["movie_id"].item()
        movieArr['date'] = main_df.iloc[i[0]]['release_date']
        moviesArr.append(movieArr)
    return moviesArr