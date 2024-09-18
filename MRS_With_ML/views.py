from django.shortcuts import render, redirect
from django.db import connection
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def getContentFromIMDBID(ID):
    query = f"""
    SELECT *
    FROM utjwurwq_MRS.dashboard_content
    WHERE imdbid = '{ID}';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

# Write your SQL query
query = 'SELECT * FROM utjwurwq_MRS.dashboard_content;'

# Read data into a DataFrame
df = pd.read_sql(query, connection)

df.set_index('imdbid', inplace=True)

df['Plot_Genre'] = df['title'] + ' ' + df['genre'] + ' ' + df['actors']

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(df['Plot_Genre'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(imdb_id, cosine_sim=cosine_sim, df=df, num_recommendations=7):
    idx = df.index.get_loc(imdb_id)
    
    # Get cosine similarity scores for the current movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort movies by similarity scores in descending order
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Exclude the current movie (first entry) and select top n recommendations
    sim_scores = sim_scores[1:num_recommendations + 1]
    movie_indices = [i[0] for i in sim_scores]
    
    # Get recommended movies from the dataframe
    recommended_movies = df.iloc[movie_indices].copy()
    
    return recommended_movies

def content(request, imdbid):
    data = getContentFromIMDBID(imdbid)
    recomendations = get_recommendations(imdb_id=imdbid)
    return render(request, 'MRS_With_ML/content.html', {'content' : data, 'recomendations' : recomendations})