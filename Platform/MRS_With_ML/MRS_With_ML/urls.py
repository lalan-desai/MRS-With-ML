from django.urls import include, path

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", include("user_authentication.urls")),
    path("dashboard", include("dashboard.urls")),
    path("logout", LogoutView.as_view(template_name='dashboard/logout.html')),
]