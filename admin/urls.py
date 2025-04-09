
from django.urls import path


from . import views

urlpatterns = [
    path("", views.home, name="admin_home"),
    path("login", views.signin, name="admin_login"),
    path("logout", views.sign_out, name="admin_logout"),
    path("register", views.admin_create, name="admin_create"),

    path("payments/<str:user_email>", views.view_payments, name="admin_payments"),
    path("requests/<str:user_email>", views.view_requests, name="admin_requests"),
]

