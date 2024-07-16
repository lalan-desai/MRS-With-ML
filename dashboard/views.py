from django.shortcuts import render, redirect
from .models import UserPreferences, Favorite,Content
from .forms import InitialSelectionForm
from django.db import connection
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt



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
            content_suggestions = get_top_content(user_preferences.languages, user_preferences.genres, request.user)

            return render(request, 'dashboard/index.html', {
                'user_info': user_info,
                'content_suggestions': content_suggestions,
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

def get_top_content(languages, genres, user):
    content_suggestions = {}

    # Convert languages and genres to lists of strings
    languages_list = languages.strip("[]").replace("'", "").split(", ")
    genres_list = genres.strip("[]").replace("'", "").split(", ")

    # For each genre, get the top 10 content
    for genre in genres_list:
        query = f"""
        SELECT
            c.title,
            c.poster,
            c.genre,
            c.plot,
            c.imdbVotes,
            c.imdbRating,
            c.language,
            c.imdbid,
            CASE WHEN f.id IS NOT NULL THEN TRUE ELSE FALSE END AS is_favorite
        FROM
            mrs.dashboard_content c
        LEFT JOIN
            mrs.dashboard_favorite f
        ON
            c.imdbid = f.content_id AND f.user_id = %s
        WHERE
            ({' OR '.join([f"FIND_IN_SET('{language}', c.language)" for language in languages_list])})
            AND FIND_IN_SET('{genre}', c.genre)
        ORDER BY
             RAND(), c.imdbVotes DESC
        LIMIT 7;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [user.id])
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



@csrf_exempt
def toggleFavorite(request):
    if request.method == 'POST':
        imdbid = request.POST.get('imdbid')
        user = request.user
        
        # Get the content object
        try:
            content = Content.objects.get(imdbid=imdbid)
        except Content.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Content not found'})

        # Check if the content is already a favorite
        favorite, created = Favorite.objects.get_or_create(user=user, content=content)
        
        if created:
            # The favorite was created, meaning it was not already a favorite
            status = 'favorited'
        else:
            # The favorite already exists, so delete it
            favorite.delete()
            status = 'unfavorited'

        return JsonResponse({'status': status})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



def favoriteList(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        # Get the user's favorite content
        favorites = Favorite.objects.filter(user=request.user).select_related('content')

        # Prepare data for the template
        favorite_contents = [{
            'title': fav.content.title,
            'poster': fav.content.poster,
            'genre': fav.content.genre,
            'plot': fav.content.plot,
            'imdbVotes': fav.content.imdbVotes,
            'imdbRating': fav.content.imdbRating,
            'language': fav.content.language,
            'imdbid': fav.content.imdbid,
        } for fav in favorites]

        return render(request, 'dashboard/favorite_list.html', {
            'favorite_contents': favorite_contents
        })
    else:
        # User is not authenticated, redirect to login page
        return redirect('/login')