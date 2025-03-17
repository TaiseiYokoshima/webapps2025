from django.urls import path
from .views import convert

urlpatterns = [
    path('<str:source>/<str:target>/<str:amount>', convert, name='convert'),
]
