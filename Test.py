from forms import preguntas_personalidad, puntajes  # asegúrate de importar esto

def procesar_personalidad(respuestas):
    conteo = {}

    for key, value in respuestas.items():
        if key.startswith("pregunta_"):
            idx = int(key.split("_")[1])

            # Buscamos el tipo de personalidad asociado a esa respuesta
            efectos = puntajes.get(idx, {}).get(value, {})

            for tipo, puntos in efectos.items():
                conteo[tipo] = conteo.get(tipo, 0) + puntos

    personalidad_final = max(conteo, key=conteo.get, default="Indefinida")

    return personalidad_final