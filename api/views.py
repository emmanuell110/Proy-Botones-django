# api/views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pedidos.models import Pedido   # 👈 importa tu modelo

@csrf_exempt
def lectura(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    accion = data.get("accion")  # "PENDIENTE", "LISTO", "ENTREGADO"
    sensor1 = data.get("sensor1", 0)
    sensor2 = data.get("sensor2", 0)

    # Buscar el último pedido creado
    pedido = Pedido.objects.order_by('-fecha_creacion').first()

    if not pedido:
        # No hay pedidos en la BD
        return JsonResponse({
            "led": "RED",
            "mensaje": "No hay pedidos para actualizar",
        })

    # Cambiar estado según la acción
    if accion == "PENDIENTE":
        pedido.estado = "PENDIENTE"
    elif accion == "LISTO":
        pedido.estado = "LISTO"
    elif accion == "ENTREGADO":
        pedido.estado = "ENTREGADO"
    else:
        # Si llega algo raro, no cambiamos nada
        return JsonResponse({
            "led": "RED",
            "mensaje": f"Acción desconocida: {accion}",
        })

    pedido.save()

    # Aquí podrías seguir usando los sensores para promedios, si quieres
    return JsonResponse({
        "led": "GREEN",
        "mensaje": f"Pedido {pedido.id} actualizado a {pedido.estado}",
        "accion": accion,
        "sensor1": sensor1,
        "sensor2": sensor2,
    })
