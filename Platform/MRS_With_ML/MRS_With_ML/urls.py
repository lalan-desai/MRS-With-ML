from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", include("user_authentication.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("content/<str:imdbid>", views.content, name="content"),
    path("logout", LogoutView.as_view(template_name='dashboard/logout.html')),
    path('content/<str:imdbid>/like/', views.like_content, name='like_content'),
    path('content/<str:imdbid>/dislike/', views.dislike_content, name='dislike_content'),
]