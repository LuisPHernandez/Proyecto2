from forms import preguntas_personalidad

def procesar_personalidad(respuestas):
    conteo = {}
    for key, value in respuestas.items():
        if key.startswith("pregunta_"):
            personalidad = preguntas_personalidad[int(key.split("_")[1])]["respuestas"].get(value)
            if personalidad:
                conteo[personalidad] = conteo.get(personalidad, 0) + 1

    personalidad_final = max(conteo, key=conteo.get, default="Indefinida")

    return {
        "promedio": respuestas.get("promedio"),
        "interes": respuestas.get("interes"),
        "facultad": respuestas.get("facultad"),
        "carrera": respuestas.get("carrera"),
        "personalidad": personalidad_final
    }
