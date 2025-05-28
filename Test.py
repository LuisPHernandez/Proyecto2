preguntas_personalidad = [
    {
        "pregunta": "¿Prefieres resolver problemas usando lógica y datos?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Te gusta inventar nuevas ideas o soluciones?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Prefieres seguir un procedimiento probado antes que improvisar?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Disfrutas trabajar en equipo y hablar con muchas personas?",
        "opciones": ["Sí", "No"]
    }
]


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
