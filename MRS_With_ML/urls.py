from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("", include("user_authentication.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("content/<str:imdbid>", views.content, name="content"),
    path("admin", include("admin.urls")),
    path("logout", LogoutView.as_view(template_name='dashboard/logout.html')),

]