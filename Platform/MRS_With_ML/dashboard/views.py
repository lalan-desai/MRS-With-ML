from django.shortcuts import render, redirect
from .models import UserPreferences
from .forms import InitialSelectionForm


import pymongo
import pandas as pd
from pymongo import MongoClient

client = MongoClient()

db = client.movie_database

collection = db.movies

df = pd.DataFrame(list(collection.find().limit(100)))

df['imdbRating'].replace('N/A', 0, inplace=True)
df['imdbVotes'].replace('N/A', 0, inplace=True)

df['imdbRating'].replace('NaN', 0, inplace=True)
df['imdbVotes'].replace('NaN', 0, inplace=True)



df.head()



# Function to recommend top 10 movies for each genre and preferred languages
def recommend_movies_by_genre_and_language(genre, languages):
    # Filter dataframe for the given genre and preferred languages
    genre_df = df[df['Genre'].str.contains(genre) & df['Language'].apply(lambda x: any(lang in x for lang in languages))]

    # Sort by imdbVotes and imdbRating in descending order
    sorted_df = genre_df.sort_values(by=['imdbVotes', 'imdbRating'], ascending=False)

    # Select top 10 movies
    top_movies = sorted_df.head(10)
    
    return top_movies

def index(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Check if user has provided preferences once
        try:
            user_preferences = UserPreferences.objects.get(user=request.user)
            # User preferences already exist
            user_info = {
                'username': request.user.username,
                'email': request.user.email,
                'languages': user_preferences.languages,
                'genres': user_preferences.genres,
            }

            recommendations = {}
            for genre in user_preferences.genres:
                recommendations[genre] = recommend_movies_by_genre_and_language(genre, user_preferences.languages)

            # Print recommendations
            for genre, movies in recommendations.items():
                print(f"\nTop 10 Movies in {genre} for Preferred Languages:\n")
                print(movies)


           
                        
            return render(request, 'dashboard/index.html', {'user_info': user_info})
    
        except UserPreferences.DoesNotExist:
            # User preferences do not exist, redirect to preferences page
            return redirect('dashboard/initialSelection')  # assuming you have a URL named 'preferences' for the preferences page
    else:
        # User is not authenticated, redirect to login page
        return redirect('/login')


def initialSelection(request):
    if request.user.is_authenticated:
        # Check if user has provided preferences once
        try:
            user_preferences = UserPreferences.objects.get(user=request.user)
            # User preferences already exist
            user_info = {
                'username': request.user.username,
                'email': request.user.email,
                'languages': user_preferences.languages,
                'genres': user_preferences.genres,
            }
            
            return redirect('/dashboard')
    
        except UserPreferences.DoesNotExist:
            if(request.method == 'GET'):

                isf = InitialSelectionForm()
                return render(request, 'initialSelection/index.html', {'form' : isf})
            
            else:
                form = InitialSelectionForm(request.POST)
                if form.is_valid():
                    instance = UserPreferences(
                    user=request.user,
                    languages=form.cleaned_data['languages'],
                    genres=form.cleaned_data['genres'],
                )
                instance.save()  # Save the instance to the database

                # Redirect to the dashboard or any other page after saving preferences
                return redirect('/dashboard')
                
            
    else:
        # User is not authenticated, redirect to login page
        return redirect('/login')
    


