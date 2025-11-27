from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'tipo_tamal', 'cantidad', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'tipo_tamal')
    search_fields = ('nombre_cliente', 'telefono')
