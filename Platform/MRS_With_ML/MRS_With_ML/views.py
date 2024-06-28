from django.shortcuts import render, redirect
from django.db import connection
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from dashboard.models import Content,Feedback

def like_content(request, imdbid):
    if request.method == 'POST':
        content = get_object_or_404(Content, imdbid=imdbid)
        user = request.user  # Assuming user is authenticated
        
        try:
            # Attempt to retrieve existing feedback
            feedback = Feedback.objects.get(user=user, content=content)
        except Feedback.DoesNotExist:
            # Create new feedback if it doesn't exist
            feedback = Feedback.objects.create(user=user, content=content, has_liked=True)
        
        # Update the has_liked field and save the feedback
        feedback.has_liked = True
        feedback.save()
        
        return JsonResponse({'status': 'liked'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def dislike_content(request, imdbid):
    if request.method == 'POST':
        content = get_object_or_404(Content, imdbid=imdbid)
        user = request.user  # Assuming user is authenticated
        
        try:
            # Attempt to retrieve existing feedback
            feedback = Feedback.objects.get(user=user, content=content)
        except Feedback.DoesNotExist:
            # Create new feedback if it doesn't exist
            feedback = Feedback.objects.create(user=user, content=content, has_liked=False)
        
        # Update the has_liked field to False (disliked) and save the feedback
        feedback.has_liked = False
        feedback.save()
        
        return JsonResponse({'status': 'disliked'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def getContentFromIMDBID(ID):
    query = f"""
    SELECT *
    FROM mrs.dashboard_content
    WHERE imdbid = '{ID}';
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

# Write your SQL query
query = 'SELECT * FROM dashboard_content'

# Read data into a DataFrame
df = pd.read_sql(query, connection)

df.set_index('imdbid', inplace=True)

df['Plot_Genre'] = df['title'] + ' ' + df['plot'] + ' ' + df['genre'] + ' ' + df['actors']

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(df['Plot_Genre'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(imdb_id, cosine_sim=cosine_sim, df=df):

    idx = df.index.get_loc(imdb_id)

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:8]
    movie_indices = [i[0] for i in sim_scores]

    recommended_movies = df.iloc[movie_indices].copy()

    return pd.DataFrame(recommended_movies)

def content(request, imdbid):
    data = getContentFromIMDBID(imdbid)
    recomendations = get_recommendations(imdb_id=imdbid)
    return render(request, 'MRS_With_ML/content.html', {'content' : data, 'recomendations' : recomendations})