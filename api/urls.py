from django.urls import path
from . import views

urlpatterns = [
    path("lectura", views.lectura, name="lectura"),
]
