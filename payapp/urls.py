from django.urls import path


from . import views

urlpatterns = [
        path("make_transfer/<str:transfer_type>", views.make_tranfer, name="transfer"),
        path("payments", views.view_payments, name="payments"),
        path("requests", views.view_requests, name="requests"),
]

