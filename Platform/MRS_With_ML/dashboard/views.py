from django.shortcuts import render, redirect
from .models import UserPreferences, Feedback, Content
from .forms import InitialSelectionForm
from django.db import connection
import json
from django.http import JsonResponse





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
            
            # Get top 10 content for each genre based on user preferences
            content_suggestions = get_top_content(user_preferences.languages, user_preferences.genres)

            # Get feedback for the current user
            user_feedback = Feedback.objects.filter(user=request.user)
            feedback_data = {feedback.content.imdbid: feedback.has_liked for feedback in user_feedback}
            
            return render(request, 'dashboard/index.html', {
                'user_info': user_info, 
                'content_suggestions': content_suggestions,
                'feedback_data': feedback_data
            })
    
        except UserPreferences.DoesNotExist:
            # User preferences do not exist, redirect to preferences page
            return redirect('initialSelection')  # assuming you have a URL named 'preferences' for the preferences page
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
            if request.method == 'GET':
                isf = InitialSelectionForm()
                return render(request, 'initialSelection/index.html', {'form': isf})
            
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

def get_top_content(languages, genres):
    content_suggestions = {}

    # Convert languages and genres to lists of strings
    languages_list = languages.strip("[]").replace("'", "").split(", ")
    genres_list = genres.strip("[]").replace("'", "").split(", ")

    # For each genre, get the top 10 content
    for genre in genres_list:
        query = f"""
        SELECT title, poster, genre, plot, imdbVotes,imdbRating, language, imdbid
        FROM mrs.dashboard_content
        WHERE ({' OR '.join([f"FIND_IN_SET('{language}', language)" for language in languages_list])})
          AND FIND_IN_SET('{genre}', genre)
        ORDER BY imdbVotes DESC
        LIMIT 7;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            content_suggestions[genre] = results
    
    return content_suggestions



def searchContent(request):
    searchQuery = request.GET.get('query', '')
    results = []
    query = """
        SELECT imdbid, title, year
        FROM mrs.dashboard_content
        WHERE title LIKE %s
        ORDER BY imdbVotes DESC
        LIMIT 5;
        """
    with connection.cursor() as cursor:
        cursor.execute(query, [f"%{searchQuery}%"])
        results = cursor.fetchall()
        
    return JsonResponse(results, safe=False)