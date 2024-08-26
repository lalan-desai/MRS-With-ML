from django.urls import include, path

from . import views
from .views import ContentListView, ContentCreateView, ContentUpdateView, ContentDeleteView

urlpatterns = [
    path("", views.index, name='admin'),
    path("/users", views.users, name='users'),
    path('/content/', ContentListView.as_view(), name='content-list'),
    path('/content/create/', ContentCreateView.as_view(), name='content-create'),
    path('/content/<str:pk>/update/', ContentUpdateView.as_view(), name='content-update'),
    path('/content/<str:pk>/delete/', ContentDeleteView.as_view(), name='content-delete'),

    path('/users/delete_user', views.delete_user, name='delete_user'),  
    path('/users/toggle_user_enabled', views.toggle_user_enabled, name='toggle_user_enabled'),
]