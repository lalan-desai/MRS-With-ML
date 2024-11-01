from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("initialSelection/", views.initialSelection, name="initialSelection"),
    path("search", views.searchContent, name="search"),

    path("toggleFavorite/", views.toggleFavorite, name="toggleFavorite"),
    path("favoriteList/", views.favoriteList, name="favoriteList")
]