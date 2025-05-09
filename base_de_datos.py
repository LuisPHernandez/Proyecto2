from neo4j import GraphDatabase
import math

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

def crear_estudiante(conn, nombre, edad, año, facultad, carrera, intereses, promedio):
    query = """
    MERGE (e:Estudiante {nombre: $nombre})
    SET e.edad = $edad, e.año_academico = $año, e.facultad = $facultad,
        e.carrera = $carrera, e.intereses = $intereses, e.promedio = $promedio
    """
    conn.correr_query(query, {
        'nombre': nombre,
        'edad': edad,
        'año': año,
        'facultad': facultad,
        'carrera': carrera,
        'intereses': intereses,
        'promedio': promedio
    })

    return {
        "nombre": nombre,
        "edad": edad,
        "año": año,
        "facultad": facultad,
        "carrera": carrera,
        "intereses": intereses,
        "promedio": promedio
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

def crear_relaciones(conn, estudiantes):
    for i, a in enumerate(estudiantes):
        for b in estudiantes[i+1:]:
            sim = calcular_similitud(a, b)
            if sim > 0.5:
                query = """
                MATCH (a:Estudiante {nombre: $nombre_a}), (b:Estudiante {nombre: $nombre_b})
                MERGE (a)-[r:SIMILAR_A]->(b)
                MERGE (b)-[r2:SIMILAR_A]->(a)
                SET r.similitud = $similitud, r2.similitud = $similitud
                """
                conn.correr_query(query, {'nombre_a': a['nombre'], 'nombre_b': b['nombre'], 'similitud': sim})

# Conectarse a Neo4j
conn = Neo4jConnection(URI, AUTH)

# Estudiantes ejemplo
e1 = crear_estudiante(conn, "Luis Pedro Hernandez", 20, 2, "Ingenieria", "Ingenieria en sistemas", ["IA", "Robotica", "Numeros"], 97)
e2 = crear_estudiante(conn, "Luis Pedro Figueroa", 20, 2, "Ingenieria", "Ingenieria en sistemas", ["Numeros", "IA", "Arte"], 84)
e3 = crear_estudiante(conn, "Adair Velasquez", 19, 2, "Ingenieria", "Ingenieria en sistemas", ["Economia", "IA"], 90)
e4 = crear_estudiante(conn, "Joel Nerio", 18, 2, "Ingenieria", "Ingenieria en sistemas", ["Circuitos", "Economia", "Diseño"], 90)

estudiantes = [e1, e2, e3, e4]

# Relaciones de estudiantes
crear_relaciones(conn, estudiantes)

# Cursos ejemplo
c1 = crear_curso(conn, "Calculo III", "Matemáticas")
c2 = crear_curso(conn, "Estadistica II", "Estadística")

# Ratings de estudiantes a cursos
agregar_rating(conn, "Luis Pedro Hernandez", "Calculo III", 9)
agregar_rating(conn, "Luis Pedro Figueroa", "Calculo III", 7)
agregar_rating(conn, "Joel Nerio", "Estadistica II", 8)

# Cerrar conexión
conn.cerrar()