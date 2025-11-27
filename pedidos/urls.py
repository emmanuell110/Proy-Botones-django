from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('estado/<int:pk>/<str:estado>/', views.cambiar_estado, name='cambiar_estado'),
]
