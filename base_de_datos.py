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
    conn.run_query(query, {
        'nombre': nombre,
        'descripcion': descripcion
    })