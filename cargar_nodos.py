import random
from base_de_datos import *

random.seed(42)

facultades = {
    "Ingeniería": ["Biomédica", "Biotecnología Industrial", "Ciencia de la Administración", "Ciencias de Alimentos", "Ciencias de Alimentos Industrial", "Civil", "Ciencias de la Computación", "Electrónica", "Industrial", "Mecánica", "Mecánica Industrial", "Mecatrónica", "Química", "Química Industrial"],
    "Ciencias Sociales": ["Antropología", "Arqueología", "Psicología", "Relaciones Internacionales"],
    "Ciencias y Humanidades": ["Biología", "Bioquímica", "Física", "Matemática Aplicada", "Nutrición", "Química", "Química Farmacéutica"],
    "Educación": ["Educación Musical", "Educación Primaria", "Educación Inclusiva"],
    "Bridge Business School": ["Administración de Empresas", "International Marketing and Business Analytics", "Comunicación Estratégica"],
    "Escuela de Arquitectura": ["Arquitectura"]
}

cursos_base = {
    "Programación Orientada a Objetos": "Aprende a programar usando clases, objetos y principios de diseño de software.",
    "Emprendimiento e Innovación": "Desarrolla ideas de negocio innovadoras y aprende cómo llevarlas al mercado.",
    "Sistemas y Tecnologías Web": "Explora cómo funcionan los sitios web y crea aplicaciones web modernas.",
    "Science of Happiness": "Estudia qué nos hace felices desde una perspectiva científica y práctica.",
    "Cálculo 3": "Analiza funciones multivariables y aprende sobre integrales múltiples y campos vectoriales.",
    "Diseño e Innovación": "Aplica procesos creativos para resolver problemas mediante el diseño centrado en el usuario.",
    "Materiales": "Conoce las propiedades físicas y químicas de los materiales usados en ingeniería y diseño.",
    "Guatemala en el Contexto Mundial": "Analiza el papel histórico, político y económico de Guatemala en el mundo actual.",
    "Investigación y Pensamiento Científico": "Aprende a formular preguntas de investigación y evaluar evidencia con pensamiento crítico.",
    "Anthropology, Culture and Business": "Estudia cómo la cultura influye en los negocios y en el comportamiento humano.",
    "Ecología para Todos": "Explora las bases de la ecología y su importancia para la sostenibilidad del planeta.",
    "Comunicación Efectiva": "Mejora tus habilidades para comunicarte con claridad y persuasión en diversos contextos.",
    "Estadística 2": "Aprende métodos estadísticos avanzados como regresión y análisis de varianza.",
    "Bioética": "Reflexiona sobre dilemas éticos relacionados con la biología, la medicina y la tecnología.",
    "Emoción Laboral": "Comprende el papel de las emociones en el entorno laboral y cómo gestionarlas eficazmente.",
    "Retos Ambientales": "Analiza los principales problemas ambientales y posibles soluciones desde diversas disciplinas."
}


intereses = ["Tecnología", "Salud", "Educación", "Investigación", "Arte", "Ciencias Naturales", "Psicología", "Historia"]
personalidades = ["Analítico", "Creativo", "Práctico", "Sociable"]

nombres_base = ["Ana", "Luis", "Carlos", "María", "Sofía", "José", "Elena", "Mario", "Laura", "Pablo",
                "Isabel", "Daniel", "Andrea", "Javier", "Camila", "David", "Paola", "Héctor", "Renata", "Tomás",
                "Pedro", "Sebastian", "Derek", "Adair", "Daniela", "Diego", "Andrea", "Sandra", "Joel", "Donaldo",
                "Adair", "Harry", "Marcelo", "Fátima", "Lionel", "Cristiano", "Christian", "Emilio", "Alessandra",
                "Esteban", "Matias", "Fabián", "Ronald", "Arturo", "Danilo", "Santiago", "Sabrina", "Olivia", "Lanna"]
apellidos_base = ["Pérez", "García", "Rodríguez", "López", "Martínez", "Sánchez", "Díaz", "Ramírez", "Morales", "Castillo",
                "Hernández", "Figueroa", "Samayoa", "Machón", "Petersen", "Quan", "España", "Toledo", "Nerio", "Leal", 
                "Monroy", "Maldonado", "Cuevas", "Coronado", "Schoenbeck", "Aparicio", "Donado", "Flores", "Godoy",
                "Schnoor", "Alvarez", "Fuentes", "Barillas", "Barrios", "Arzú", "Aguirre", "Aguiluz", "Siguenza",
                "Pineda", "Guzmán", "Castillo", "Castrillo", "Kong", "Porras", "Orellana", "Collia", "Arriola", "Messi"]

estudiantes = []
cursos = []

for i in range(100):
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

for i in range(16):
    nombre = list(cursos_base.keys())[i]
    descripcion = list(cursos_base.values())[i]

    curso = {
        "nombre": nombre,
        "descripcion": descripcion
    }
    cursos.append(curso)

def cargar_estudiantes(conn, estudiantes):
    query = """
    UNWIND $estudiantes AS est
    MERGE (e:Estudiante {nombre: est.nombre})
    SET e.edad = est.edad,
        e.año_academico = est.año,
        e.facultad = est.facultad,
        e.carrera = est.carrera,
        e.intereses = est.intereses,
        e.promedio = est.promedio,
        e.personalidad = est.personalidad
    """
    conn.correr_query(query, {"estudiantes": estudiantes})

def cargar_cursos(conn, cursos):
    query = """
    UNWIND $cursos AS cur
    MERGE (c:Curso {nombre: cur.nombre})
    SET c.descripcion = cur.descripcion
    """
    conn.correr_query(query, {"cursos": cursos})

def asignar_ratings_a_estudiantes(conn, estudiantes, cursos):
    for estudiante in estudiantes:
        num_cursos = random.randint(0, 4)
        cursos_elegidos = random.sample(cursos, k=num_cursos)

        for curso in cursos_elegidos:
            rating = round(random.uniform(5.5, 10), 1)
            agregar_rating(conn, estudiante["nombre"], curso["nombre"], rating)

conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
cargar_estudiantes(conn, estudiantes)
cargar_cursos(conn, cursos)
asignar_ratings_a_estudiantes(conn, estudiantes, cursos)
crear_relaciones(conn, estudiantes)