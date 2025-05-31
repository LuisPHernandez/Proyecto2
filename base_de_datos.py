from neo4j import GraphDatabase

URI = "bolt://localhost"
AUTH = ("neo4j", "lipelupaadair")

class Neo4jConnection:
    def __init__(self, uri, autor):
        self.driver = GraphDatabase.driver(uri, auth=(autor))

    def cerrar(self):
        self.driver.close()

    def correr_query(self, query, parametros=None, mode="list"):
        with self.driver.session() as session:
            result = session.run(query, parametros)

            if mode == "list":
                return list(result)
            elif mode == "single":
                return result.single()
            elif mode == "value":
                record = result.single()
                return record[0] if record else None
            else:
                return result

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

    if (estudiante_1["facultad"] == estudiante_2["facultad"]):
        similitud_de_facultad = 1
    else:
        similitud_de_facultad = 0

    if (estudiante_1["carrera"] == estudiante_2["carrera"]):
        similitud_de_carrera = 1
    else:
        similitud_de_carrera = 0


    if (estudiante_1["personalidad"] == estudiante_2["personalidad"]):
        similitud_de_personalidad = 1
    else:
        similitud_de_personalidad = 0

    return 0.45 * similitud_de_intereses + 0.25 * similitud_de_promedio + 0.15 * similitud_de_personalidad + 0.05 * similitud_de_facultad + 0.10 * similitud_de_carrera 

def crear_relaciones(conn, estudiantes, k=3):
    for a in estudiantes:
        # 1. Borrar relaciones previas
        query_delete = """
        MATCH (a:Estudiante {nombre: $nombre})-[r:SIMILAR_A]->()
        DELETE r
        """
        conn.correr_query(query_delete, {'nombre': a['nombre']})

    # 2. Crear nuevas relaciones como antes
    for i, a in enumerate(estudiantes):
        similitudes = []
        for j, b in enumerate(estudiantes):
            if a["nombre"] != b["nombre"]:
                sim = calcular_similitud(a, b)
                similitudes.append((b["nombre"], sim))

        vecinos_mas_similares = sorted(similitudes, key=lambda x: x[1], reverse=True)[:k]

        for nombre_b, sim in vecinos_mas_similares:
            query = """
            MATCH (a:Estudiante {nombre: $nombre_a}), (b:Estudiante {nombre: $nombre_b})
            MERGE (a)-[r:SIMILAR_A]->(b)
            SET r.similitud = $similitud
            """
            conn.correr_query(query, {
                'nombre_a': a['nombre'],
                'nombre_b': nombre_b,
                'similitud': sim
            })

def estudiantes_con_ratings(conn, estudiantes):
    estudiantes_validos = []

    for est in estudiantes:
        query = """
        MATCH (:Estudiante {nombre: $nombre})-[r:RATED]->(:Curso)
        RETURN COUNT(r) AS cantidad
        """
        record = conn.correr_query(query, {'nombre': est['nombre']}, mode="single")

        if record and record["cantidad"] > 0:
            estudiantes_validos.append(est)

    return estudiantes_validos

def obtener_estudiantes(conn):
    query = """
    MATCH (e:Estudiante)
    RETURN e.nombre AS nombre, e.edad AS edad, e.año_academico AS año, 
           e.facultad AS facultad, e.carrera AS carrera, e.intereses AS intereses,
           e.promedio AS promedio, e.personalidad AS personalidad
    """
    resultado = conn.correr_query(query)
    return [
        {
            "nombre": r["nombre"],
            "edad": r["edad"],
            "año": r["año"],
            "facultad": r["facultad"],
            "carrera": r["carrera"],
            "intereses": r["intereses"],
            "promedio": r["promedio"],
            "personalidad": r["personalidad"]
        }
        for r in resultado if r["nombre"] is not None
    ]

def obtener_estudiante_por_nombre(conn, nombre):
    query = """
    MATCH (e:Estudiante {nombre: $nombre})
    RETURN e.nombre AS nombre, e.edad AS edad, e.año_academico AS año,
           e.facultad AS facultad, e.carrera AS carrera, e.intereses AS intereses,
           e.promedio AS promedio, e.personalidad AS personalidad
    """
    record = conn.correr_query(query, {'nombre': nombre}, mode="single")
    if record:
        return {
            "nombre": record["nombre"],
            "edad": record["edad"],
            "año": record["año"],
            "facultad": record["facultad"],
            "carrera": record["carrera"],
            "intereses": record["intereses"],
            "promedio": record["promedio"],
            "personalidad": record["personalidad"]
        }
    return None

def obtener_cursos_mejor_valorados(conn, limite=10):
    query = """
    MATCH (:Estudiante)-[r:RATED]->(c:Curso)
    RETURN c.nombre AS nombre, AVG(r.rating) AS promedio_rating
    ORDER BY promedio_rating DESC
    LIMIT $limite
    """
    resultados = conn.correr_query(query, {'limite': limite})
    return [
        {
            "nombre": r["nombre"],
            "promedio_rating": round(r["promedio_rating"], 2)
        }
        for r in resultados
    ]

def obtener_cursos_rateados_por_estudiante(conn, nombre_estudiante):
    query = """
    MATCH (e:Estudiante {nombre: $nombre})-[r:RATED]->(c:Curso)
    RETURN c.nombre AS curso, r.rating AS rating
    """
    resultados = conn.correr_query(query, {'nombre': nombre_estudiante})
    return [
        {
            "curso": r["curso"],
            "rating": r["rating"]
        }
        for r in resultados
    ]

def obtener_cursos_no_tomados_por_estudiante(conn, nombre_estudiante):
    query = """
    MATCH (c:Curso)
    WHERE NOT EXISTS {
        MATCH (:Estudiante {nombre: $nombre})-[r:RATED]->(c)
    }
    RETURN c.nombre AS nombre, c.descripcion AS descripcion
    """
    resultados = conn.correr_query(query, {'nombre': nombre_estudiante})
    return [
        {
            "nombre": r["nombre"],
            "descripcion": r["descripcion"]
        }
        for r in resultados
    ]