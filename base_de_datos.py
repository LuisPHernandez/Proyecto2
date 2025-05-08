from neo4j import GraphDatabase
import math

URI = "neo4j://localhost"
AUTH = ("neo4j", "lipelupaadair")

class Neo4jConnection:
    def __init__(self, uri, usuario, password):
        self.driver = GraphDatabase.driver(uri, auth=(usuario, password))

    def cerrar(self):
        self.driver.close()

    def correr_query(self, query, parametros=None):
        with self.driver.session() as session:
            return session.run(query, parametros)

def crear_estudiante(conn, nombre, edad, año, facultad, carera, intereses, promedio):
    query = """
    MERGE (s:Estudiante {nombre: $nombre})
    SET s.edad = $edad, s.año_academico = $año, s.facultad = $facultad,
        s.carera = $carera, s.intereses = $intereses, s.promedio = $promedio
    """
    conn.correr_query(query, {
        'nombre': nombre,
        'edad': edad,
        'año': año,
        'facultad': facultad,
        'carera': carera,
        'intereses': intereses,
        'promedio': promedio
    })

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
    MATCH (s:Estudiante {nombre_estudiante: $nombre_estudiante}), (c:Curso {nombre_curso: $nombre_curso})
    MERGE (s)-[r:RATED]->(c)
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

def crear_relaciones(conn, estudiantes):
    for i, a in enumerate(estudiantes):
        for b in estudiantes[i+1:]:
            sim = calcular_similitud(a, b)
            if sim > 0.6:
                query = """
                MATCH (a:Estudiante {nombre: $id_a}), (b:Estudiante {nombre: $id_b})
                MERGE (a)-[r:SIMILAR_A]->(b)
                SET r.similitud = $similitud
                """
                conn.run_query(query, {'id_a': a['nombre'], 'id_b': b['nombre'], 'score': sim})

