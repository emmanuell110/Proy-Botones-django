from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('pedidos.urls')),   # 👈 raíz del sitio = app pedidos
    path('api/', include('api.urls')),   # API para el botón físico
    path('admin/', admin.site.urls),
]