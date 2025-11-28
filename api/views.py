# api/views.py
import json
from collections import deque

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pedidos.models import Pedido   # 👈 importa tu modelo de pedidos

# Guardamos últimas lecturas en memoria para promedios
lecturas = deque(maxlen=3)


@csrf_exempt
def lectura(request):
    """
    Endpoint que recibe JSON del ESP8266 y cambia el estado del último pedido.
    El ESP manda algo como:
    {
      "sensor1": 1|2|3,
      "sensor2": 0,
      "accion": "PENDIENTE" | "LISTO" | "ENTREGADO"
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    accion = data.get("accion")           # "PENDIENTE", "LISTO", "ENTREGADO"
    sensor1 = data.get("sensor1", 0)
    sensor2 = data.get("sensor2", 0)

    # Guardamos la lectura en memoria para el análisis de promedios
    lecturas.append({"sensor1": sensor1, "sensor2": sensor2})

    # Buscamos el último pedido creado
    pedido = Pedido.objects.order_by("-id").first()

    if not pedido:
        # No hay pedidos en la BD
        return JsonResponse(
            {
                "led": "RED",
                "mensaje": "No hay pedidos para actualizar",
            }
        )

    # Cambiar estado según la acción
    if accion == "PENDIENTE":
        pedido.estado = "PENDIENTE"
    elif accion == "LISTO":
        pedido.estado = "LISTO"
    elif accion == "ENTREGADO":
        pedido.estado = "ENTREGADO"
    else:
        # Si llega algo raro, no cambiamos nada
        return JsonResponse(
            {
                "led": "RED",
                "mensaje": f"Acción desconocida: {accion}",
            }
        )

    pedido.save()

    # Calculamos promedios por si el profe te pide análisis de sensores
    prom1 = sum(l["sensor1"] for l in lecturas) / len(lecturas)
    prom2 = sum(l["sensor2"] for l in lecturas) / len(lecturas)

    return JsonResponse(
        {
            "led": "GREEN",  # todo OK → ESP prende LED verde
            "mensaje": f"Pedido {pedido.id} actualizado a {pedido.estado}",
            "accion": accion,
            "promedio_sensor1": prom1,
            "promedio_sensor2": prom2,
        }
    )


def promedios(request):
    """
    Endpoint para consultar los promedios de las últimas lecturas.
    GET /api/promedios
    """
    if not lecturas:
        return JsonResponse(
            {
                "promedio_sensor1": 0,
                "promedio_sensor2": 0,
                "ultimos_sensor1": [],
                "ultimos_sensor2": [],
            }
        )

    prom1 = sum(l["sensor1"] for l in lecturas) / len(lecturas)
    prom2 = sum(l["sensor2"] for l in lecturas) / len(lecturas)

    return JsonResponse(
        {
            "promedio_sensor1": prom1,
            "promedio_sensor2": prom2,
            "ultimos_sensor1": [l["sensor1"] for l in lecturas],
            "ultimos_sensor2": [l["sensor2"] for l in lecturas],
        }
    )
