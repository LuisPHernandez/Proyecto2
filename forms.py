# Datos para formularios
facultades = {
    "Ingeniería": ["Biomédica", "Biotecnología Industrial", "Ciencia de la Administración", "Ciencias de Alimentos", "Ciencias de Alimentos Industrial", "Civil", "Ciencias de la Computación", "Electrónica", "Industrial", "Mecánica", "Mecánica Industrial", "Mecatrónica", "Química", "Química Industrial"],
    "Ciencias Sociales": ["Antropología", "Arqueología", "Psicología", "Relaciones Internacionales"],
    "Ciencias y Humanidades": ["Biología", "Bioquímica", "Física", "Matemática Aplicada", "Nutrición", "Química", "Química Farmacéutica"],
    "Educación": ["Educación Musical", "Educación Primaria", "Educación Inclusiva"],
    "Bridge Business School": ["Administración de Empresas", "International Marketing and Business Analytics", "Comunicación Estratégica"],
    "Escuela de Arquitectura": ["Arquitectura"]
}

intereses = [
    "Tecnología", "Salud", "Educación", "Investigación", "Arte", "Ciencias Naturales", "Psicología", "Historia"
]

# Preguntas de personalidad
preguntas_personalidad = [
    {
        "pregunta": "¿Prefieres resolver problemas usando lógica y datos?",
        "respuestas": {"Sí": "Analítico", "No": "Sociable"}
    },
    {
        "pregunta": "¿Te gusta inventar nuevas ideas o soluciones?",
        "respuestas": {"Sí": "Creativo", "No": "Práctico"}
    },
    {
        "pregunta": "¿Prefieres seguir un procedimiento probado antes que improvisar?",
        "respuestas": {"Sí": "Práctico", "No": "Creativo"}
    },
    {
        "pregunta": "¿Disfrutas trabajar en equipo y hablar con muchas personas?",
        "respuestas": {"Sí": "Sociable", "No": "Analítico"}
    }
]

puntajes = {
    0: {"Sí": {"Analítico": 2}, "No": {"Sociable": 1, "Creativo": 1}},
    1: {"Sí": {"Creativo": 2}, "No": {"Práctico": 1}},
    2: {"Sí": {"Práctico": 2}, "No": {"Creativo": 1}},
    3: {"Sí": {"Sociable": 2}, "No": {"Analítico": 1}}
}