from neo4j import GraphDatabase

URI = "bolt://localhost"
AUTH = ("neo4j", "lipelupaadair")

class Neo4jConnection:
    def __init__(self, uri, autor):
        self.driver = GraphDatabase.driver(uri, auth=(autor))

    def cerrar(self):
        self.driver.close()

    def correr_query(self, query, parametros=None):
        with self.driver.session() as session:
            return session.run(query, parametros)

def crear_estudiante(conn, nombre, edad, año, facultad, carrera, intereses, promedio, personalidad):
    query = """
    MERGE (e:Estudiante {nombre: $nombre})
    SET e.edad = $edad, e.año_academico = $año, e.facultad = $facultad,
        e.carrera = $carrera, e.intereses = $intereses, e.promedio = $promedio, e.personalidad = $personalidad
    """
    conn.correr_query(query, {
        'nombre': nombre,
        'edad': edad,
        'año': año,
        'facultad': facultad,
        'carrera': carrera,
        'intereses': intereses,
        'promedio': promedio,
        'personalidad': personalidad
    })

    return {
        "nombre": nombre,
        "edad": edad,
        "año": año,
        "facultad": facultad,
        "carrera": carrera,
        "intereses": intereses,
        "promedio": promedio,
        "personalidad": personalidad
    }

def crear_curso(conn, nombre, descripcion):
    query = """
    MERGE (c:Curso {nombre: $nombre})
    SET c.descripcion = $descripcion
    """
    conn.correr_query(query, {
        'nombre': nombre,
        'descripcion': descripcion
    })

def agregar_rating(conn, nombre_estudiante, nombre_curso, rating):
    query = """
    MATCH (e:Estudiante {nombre: $nombre_estudiante}), (c:Curso {nombre: $nombre_curso})
    MERGE (e)-[r:RATED]->(c)
    SET r.rating = $rating
    """
    conn.correr_query(query, {'nombre_estudiante': nombre_estudiante, 'nombre_curso': nombre_curso, 'rating': rating})

def calcular_similitud(estudiante_1, estudiante_2):
    intereses_compartidos = len(set(estudiante_1["intereses"]).intersection(estudiante_2["intereses"]))
    intereses_totales = len(set(estudiante_1["intereses"]).union(estudiante_2["intereses"]))
    similitud_de_intereses = intereses_compartidos / intereses_totales if intereses_totales > 0 else 0

    diferencia_de_promedio = abs(estudiante_1["promedio"] - estudiante_2["promedio"])
    similitud_de_promedio = 1 - (diferencia_de_promedio / 100)

    return 0.6 * similitud_de_intereses + 0.4 * similitud_de_promedio

def crear_relaciones(conn, estudiantes, k=3):
    # Filtrar estudiantes para que solo se tenga relación con estudiantes que han tomado un curso previamente
    estudiantes_filtrados = estudiantes_con_ratings(conn, estudiantes)  

    # Obtener todos los valores de similitud entre cada estudiante y todos los demás
    for i, a in enumerate(estudiantes_filtrados):
        similitudes = []
        for j, b in enumerate(estudiantes_filtrados):
            if a["nombre"] != b["nombre"]:
                sim = calcular_similitud(a,b)
                similitudes.append((b["nombre"], sim))

        # Obtener los k vecinos más similares
        vecinos_mas_similares = sorted(similitudes, key=lambda x: x[1], reverse=True)[:k]

        for nombre_b, sim in vecinos_mas_similares:
            query = """
            MATCH (a:Estudiante {nombre: $nombre_a}), (b:Estudiante {nombre: $nombre_b})
            MERGE (a)-[r:SIMILAR_A]->(b)
            SET r.similitud = $similitud
            """
            conn.correr_query(query, {'nombre_a': a['nombre'], 'nombre_b': nombre_b, 'similitud': sim})

def estudiantes_con_ratings(conn, estudiantes):
    estudiantes_validos = []

    # Revisar todos los estudiantes para que tengan más de 0 ratings
    for est in estudiantes:
        query = """
        MACTH (:Estudiante {nombre: $nombre})-[r:RATED]->(:Curso)
        RETURN COUNT(r) AS cantidad
        """
        result = conn.correr_query(query, {'nombre': est['nombre']})
        if result.single()['cantidad'] > 0:
            estudiantes_validos.append(est)

    # Devolver solo estudiantes que hayan rateado un curso en el pasado
    return estudiantes_validos