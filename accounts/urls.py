from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout", views.sign_out, name="logout"),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login')
]

