from django.shortcuts import render, redirect
from .models import UserPreferences

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
        except UserPreferences.DoesNotExist:
            # User preferences do not exist, redirect to preferences page
            return redirect('preferences')  # assuming you have a URL named 'preferences' for the preferences page
    else:
        # User is not authenticated, redirect to login page
        return redirect('/login')

    return render(request, 'dashboard/index.html', {'user_info': user_info})
