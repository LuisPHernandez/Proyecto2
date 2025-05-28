def recomendar_cursos_knn(conn, nombre_estudiante, k=3, nota_minima=7):
    # Query que devuelve los k vecinos más similares del grafo
    query_vecinos = """
    MATCH (e:Estudiante {nombre: $nombre})-[s:SIMILAR_A]->(vecino)
    RETURN vecino.nombre AS nombre_vecino, s.similitud AS similitud
    ORDER BY similitud DESC
    LIMIT $k
    """
    vecinos = conn.correr_query(query_vecinos, {'nombre': nombre_estudiante, 'k': k})

    recomendaciones = {}
    
    # Para cada vecino se devuelven los cursos y ratings de los cursos aún no llevados por el estudiante objetivo
    for vec in vecinos:
        vecino = vec['nombre_vecino']
        sim = vec['similitud']

        query_cursos = """
        MATCH (v:Estudiante {nombre: $vecino})-[r:RATED]->(c:Curso)
        WHERE r.ratinf >= $nota_minima
        AND NOT EXISTS {
            MATCH (:Estudiante {nombre: $nombre})-[r2:RATED]->(c)
        }
        RETURN c.nombre AS curso, r.rating AS rating
        """
        cursos = conn.correr_query(query_cursos, {'vecino': vecino, 'nombre': nombre_estudiante, 'nota_minima': nota_minima})

        # Para cada curso se calcula el puntaje (puntaje más alto = curso más recomendado)
        for cur in cursos:
            nombre_curso = cur['curso']
            rating = cur['rating']
            puntaje = sim * rating

            # Si ya se tiene un puntaje para el curso, se suma el nuevo puntaje (dos puntajes = dos vecinos que les gustó el curso)
            if nombre_curso in recomendaciones:
                recomendaciones[nombre_curso] += puntaje
            else:
                recomendaciones[nombre_curso] = puntaje
    
    # Ordenar por puntaje de manera descendiente
    cursos_ordenados = sorted(recomendaciones.items(), key=lambda x: x[1], reverse=True)
    return cursos_ordenados