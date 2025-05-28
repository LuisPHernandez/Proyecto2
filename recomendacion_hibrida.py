from kNN import recomendar_cursos_knn


def curso_ya_tomado(conn, nombre_estudiante, nombre_curso):
    # Query devuelve los cursos que ya fueron tomados, porque ya fueron rateados, por el estudiante objetivo
    query = """
    MATCH (:Estudiante {nombre: $nombre_estudiante})-[r.RATED]->(:Curso {nombre: $nombre_curso})
    RETURN COUNT(r) > 0 AS tomado
    """
    result = conn.correr_query(query, {'nombre_estudiante': nombre_estudiante, 'nombre_curso': nombre_curso})
    return result.single()['tomado']

def recomendar_cursos_hibrido(conn, nombre_estudiante, k=3, n=5, nota_minima=7):
    peso_knn = 1.0
    peso_rwr = 0.6

    # 1. Obtener cursos recomendados por kNN, normalizar y aplicar peso
    cursos_knn_raw = recomendar_cursos_knn(conn, nombre_estudiante, k=k)
    cursos_knn_norm = normalizar_escala_de_similitud(cursos_knn_raw)
    cursos_knn = [(curso, round(puntaje * peso_knn, 2)) for curso, puntaje in cursos_knn_norm]

    # 2. Filtrar cursos que el estudiante objetivo no ha tomado, máximo n
    cursos_filtrados = []
    for curso, puntaje in cursos_knn:
        if not curso_ya_tomado(conn, nombre_estudiante, curso):
            cursos_filtrados.append((curso, puntaje))
        if len(cursos_filtrados) >= n:
            break

    # 3. Si hay suficientes cursos para mostrar en el sistema de recomendaciones, devolverlos
    if len(cursos_filtrados) >= n:
        return cursos_filtrados
    
    # 4. Si aún no hay suficientes, obtener cursos adicionales con RWR, normalizar y aplicar peso
    # TODO implementar función de recomendación por RWR
    cursos_rwr_raw = recomendar_cursos_rwr(conn, nombre_estudiante)
    cursos_rwr_norm = normalizar_escala_de_similitud(cursos_rwr_raw)
    cursos_rwr = [(curso, round(puntaje * peso_rwr, 2)) for curso, puntaje in cursos_rwr_norm]

    # 5. Agregar solo los cursos nuevos
    cursos_ya_recomendados = {c[0] for c in cursos_filtrados}
    for curso, puntaje in cursos_rwr:
        if curso not in cursos_ya_recomendados and not curso_ya_tomado(conn, nombre_estudiante, curso):
            cursos_filtrados.append((curso, puntaje))
        if len(cursos_filtrados) >= n:
            break
    
    # 6. Ordenar cursos y devolverlos
    cursos_ordenados = sorted(cursos_filtrados, key=lambda x: x[1], reverse=True)
    return cursos_ordenados

def normalizar_escala_de_similitud(puntajes, escala=10.0):
    # Si puntajes esta vacía, retorna una lista vacía
    if not puntajes:
        return []
    
    # Encuentra el puntaje máximo y mínimo para normalizar
    valores = [s[1] for s in puntajes]
    min_s, max_s = min(valores), max(valores)
    if min_s == max_s:
        return [(s[0], escala / 2.0) for s in puntajes] # Puntaje medio si todos son iguales
    
    # Devuelve la lista de puntajes normalizada
    return [(s[0], escala * (s[1] - min_s) / (max_s - min_s) for s in puntajes)]