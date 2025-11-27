# api/views.py
import json
from collections import deque
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 👈 IMPORTANTE

# memoria simple de lecturas (ejemplo)
lecturas = deque(maxlen=3)

@csrf_exempt                     # 👈 DESACTIVA CSRF SOLO AQUÍ
def lectura(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        sensor1 = data.get("sensor1", 0)
        sensor2 = data.get("sensor2", 0)

        lecturas.append({"sensor1": sensor1, "sensor2": sensor2})

        prom1 = sum(l["sensor1"] for l in lecturas) / len(lecturas)
        prom2 = sum(l["sensor2"] for l in lecturas) / len(lecturas)

        # Lógica para decidir color del LED (ajústala a tu gusto)
        if prom1 <= 5:   # por ejemplo: pocos pedidos → todo relax
            led = "GREEN"
        else:            # muchos pedidos → saturación
            led = "RED"

        return JsonResponse(
            {
                "led": led,
                "promedio_sensor1": prom1,
                "promedio_sensor2": prom2,
            }
        )

    return JsonResponse({"error": "Método no permitido"}, status=405)


def promedios(request):
    # si ya la tenías hecha, déjala igual;
    # solo asegúrate de que sea GET
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
