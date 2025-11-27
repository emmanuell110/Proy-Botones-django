from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm

def lista_pedidos(request):
    # Crear pedido nuevo
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
    else:
        form = PedidoForm()

    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {
        'form': form,
        'pedidos': pedidos,
    })


def cambiar_estado(request, pk, estado):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.estado = estado
    pedido.save()
    return redirect('lista_pedidos')
