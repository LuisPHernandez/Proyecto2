import random
from base_de_datos import *

facultades = {
    "Ingeniería": ["Biomédica", "Biotecnología Industrial", "Ciencia de la Administración", "Ciencias de Alimentos", "Ciencias de Alimentos Industrial", "Civil", "Ciencias de la Computación", "Electrónica", "Industrial", "Mecánica", "Mecánica Industrial", "Mecatrónica", "Química", "Química Industrial"],
    "Ciencias Sociales": ["Antropología", "Arqueología", "Psicología", "Relaciones Internacionales"],
    "Ciencias y Humanidades": ["Biología", "Bioquímica", "Física", "Matemática Aplicada", "Nutrición", "Química", "Química Farmacéutica"],
    "Educación": ["Educación Musical", "Educación Primaria", "Educación Inclusiva"],
    "Bridge Business School": ["Administración de Empresas", "International Marketing and Business Analytics", "Comunicación Estratégica"],
    "Escuela de Arquitectura": ["Arquitectura"]
}

intereses = ["Tecnología", "Salud", "Educación", "Investigación", "Arte", "Ciencias Naturales", "Psicología", "Historia"]
personalidades = ["Analítico", "Creativo", "Práctico", "Sociable"]

nombres_base = ["Ana", "Luis", "Carlos", "María", "Sofía", "José", "Elena", "Mario", "Laura", "Pablo",
                "Isabel", "Daniel", "Andrea", "Javier", "Camila", "David", "Paola", "Héctor", "Renata", "Tomás"]
apellidos_base = ["Pérez", "García", "Rodríguez", "López", "Martínez", "Sánchez", "Díaz", "Ramírez", "Morales", "Castillo"]

estudiantes = []

for i in range(30):
    nombre = f"{random.choice(nombres_base)} {random.choice(apellidos_base)}"
    edad = random.randint(18, 24)
    año = random.randint(1, 5)
    facultad = random.choice(list(facultades.keys()))
    carrera = random.choice(facultades[facultad])
    intereses_estudiante = random.sample(intereses, k=random.randint(2, 4))
    promedio = round(random.uniform(70, 95), 2)
    personalidad = random.choice(personalidades)

    estudiante = {
        "nombre": nombre,
        "edad": edad,
        "año": año,
        "facultad": facultad,
        "carrera": carrera,
        "intereses": intereses_estudiante,
        "promedio": promedio,
        "personalidad": personalidad
    }
    estudiantes.append(estudiante)

def cargar_estudiantes(conn, estudiantes):
    query = """
    UNWIND $estudiantes AS est
    MERGE (e:Estudiante {nombre: est.nombre})
    SET e.edad = est.edad,
        e.anio = est.año,
        e.facultad = est.facultad,
        e.carrera = est.carrera,
        e.intereses = est.intereses,
        e.promedio = est.promedio,
        e.personalidad = est.personalidad
    """
    conn.correr_query(query, {"estudiantes": estudiantes})

def cargar_cursos(tx, cursos):
    for curso in cursos:
        tx.run(
            "MERGE (c:Curso {nombre: $nombre}) "
            "SET c.descripcion = $descripcion",
            nombre=curso["nombre"],
            descripcion=curso["descripcion"]
        )

conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
cargar_estudiantes(conn, estudiantes)