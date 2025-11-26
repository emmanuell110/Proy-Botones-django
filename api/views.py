from django.http import JsonResponse
import json

# "Memoria" sencilla en variables globales
datos_sensor1 = []  # número de pedidos
datos_sensor2 = []  # tiempo en minutos
UMBRAL_TIEMPO = 15  # 15 minutos


def promedio(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)


def lectura(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        data = {}

    sensor1 = data.get("sensor1", 0)
    sensor2 = data.get("sensor2", 0)

    # Guardar sólo los últimos 3 valores de cada sensor
    datos_sensor1.append(sensor1)
    datos_sensor2.append(sensor2)

    del datos_sensor1[:-3]
    del datos_sensor2[:-3]

    prom1 = promedio(datos_sensor1)
    prom2 = promedio(datos_sensor2)

    led = "GREEN" if prom2 <= UMBRAL_TIEMPO else "RED"

    return JsonResponse({
        "led": led,
        "promedio_pedidos": prom1,
        "promedio_tiempo": prom2,
        "ultimos_sensor1": datos_sensor1,
        "ultimos_sensor2": datos_sensor2,
    })


def promedios(request):
    prom1 = promedio(datos_sensor1)
    prom2 = promedio(datos_sensor2)

    return JsonResponse({
        "promedio_sensor1": prom1,
        "promedio_sensor2": prom2,
        "ultimos_sensor1": datos_sensor1,
        "ultimos_sensor2": datos_sensor2,
    })
