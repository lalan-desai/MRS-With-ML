from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import CustomLoginView
urlpatterns = [
    path("", views.index, name="index"),
     path('login/', views.CustomLoginView.as_view(), name='login'),
]
