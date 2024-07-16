from django.urls import include, path

from . import views
from .views import ContentListView, ContentCreateView, ContentUpdateView, ContentDeleteView

urlpatterns = [
    path("", views.index, name='admin'),
    path('/content/', ContentListView.as_view(), name='content-list'),
    path('/content/create/', ContentCreateView.as_view(), name='content-create'),
    path('/content/<str:pk>/update/', ContentUpdateView.as_view(), name='content-update'),
    path('/content/<str:pk>/delete/', ContentDeleteView.as_view(), name='content-delete'),
]