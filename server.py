from flask import Flask, request, jsonify
import os

app = Flask(__name__)

datos_sensor1 = []  # número de pedidos
datos_sensor2 = []  # tiempo en minutos

UMBRAL_TIEMPO = 15  # 15 min

def promedio(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

@app.route('/lectura', methods=['POST'])
def lectura():
    global datos_sensor1, datos_sensor2

    data = request.get_json()
    sensor1 = data.get('sensor1', 0)
    sensor2 = data.get('sensor2', 0)

    datos_sensor1.append(sensor1)
    datos_sensor2.append(sensor2)

    datos_sensor1 = datos_sensor1[-3:]
    datos_sensor2 = datos_sensor2[-3:]

    prom1 = promedio(datos_sensor1)
    prom2 = promedio(datos2)

    if prom2 <= UMBRAL_TIEMPO:
        led = "GREEN"
    else:
        led = "RED"

    return jsonify({
        "led": led,
        "promedio_pedidos": prom1,
        "promedio_tiempo": prom2
    })

@app.route('/promedios', methods=['GET'])
def promedios():
    return jsonify({
        "promedio_sensor1": promedio(datos_sensor1),
        "promedio_sensor2": promedio(datos_sensor2),
        "ultimos_sensor1": datos_sensor1,
        "ultimos_sensor2": datos_sensor2
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
