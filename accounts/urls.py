from django.urls import path


from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.sign_out, name="logout"),
    path('login/', views.sign_in, name='login')
]

