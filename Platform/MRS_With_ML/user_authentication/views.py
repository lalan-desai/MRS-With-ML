from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm

from django.contrib.auth import views as auth_views

def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard') 
    else:
        # If it's a GET request, create a blank form
        form = RegistrationForm()

    return render(request, "user_authentication/index.html", {'form': form})

