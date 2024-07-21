from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'user_authentication/login.html'
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.is_superuser:
            return redirect('/admin')
        return redirect('/dashboard')

def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard') 
    else:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            form = RegistrationForm()
            return render(request, "user_authentication/index.html", {'form': form})

