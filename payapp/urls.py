from django.urls import path


from . import views

urlpatterns = [
    path("pay", views.view_make_payment, name="pay"),
    path("request", views.view_make_request, name="request"),

    path("approve", views.approve_request, name="approve"),
    path("deny", views.deny_request, name="deny"),

    path("payments", views.view_payments, name="payments"),
    path("requests", views.view_requests, name="requests"),
]

