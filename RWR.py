import numpy as np

def recomendar_cursos_rwr(conn, nombre_estudiante, alpha=0.3, max_iter=100, tol=1e-6):
    # 1. Obtener nodos y aristas relevantes del subgrafo
    query = """
    MATCH (e:Estudiante)
    OPTIONAL MATCH (e)-[s:SIMILAR_A]->(e2:Estudiante)
    OPTIONAL MATCH (e)-[r:RATED]->(c:Curso)
    RETURN e.nombre AS estudiante, 
           collect(DISTINCT {vecino: e2.nombre, similitud: s.similitud}) AS vecinos, 
           collect(DISTINCT {curso: c.nombre, rating: r.rating}) AS cursos
    """
    resultado = conn.correr_query(query)
    
    # 2. Construcción de índices y nodos
    estudiantes = set()
    cursos = set()
    relaciones_similitud = []
    relaciones_rating = []

    for fila in resultado:
        estudiante = fila['estudiante']
        estudiantes.add(estudiante)

        for sim in fila['vecinos']:
            if sim['vecino']:
                estudiantes.add(sim['vecino'])
                relaciones_similitud.append((estudiante, sim['vecino'], sim['similitud']))

        for rate in fila['cursos']:
            if rate['curso']:
                cursos.add(rate['curso'])
                relaciones_rating.append((estudiante, rate['curso'], rate['rating']))

    nodos = list(estudiantes) + list(cursos)
    idx = {nodo: i for i, nodo in enumerate(nodos)}

    # 3. Matriz de adyacencia
    n = len(nodos)
    A = np.zeros((n, n))

    for e1, e2, peso in relaciones_similitud:
        A[idx[e1], idx[e2]] = peso
        A[idx[e2], idx[e1]] = peso  # Grafo no dirigido

    for estudiante, curso, nota in relaciones_rating:
        nota_normalizada = nota / 10.0 # Notas van de 0 a 10, similitudes de 0 a 1
        A[idx[estudiante], idx[curso]] = nota_normalizada
        A[idx[curso], idx[estudiante]] = nota_normalizada  # Grafo no dirigido

    # 4. Normalizar matriz por columnas (matriz de transición)
    P = A / np.clip(A.sum(axis=0), 1e-10, None)

    # 5. Vector inicial (solo 1 en el nodo del estudiante)
    p = np.zeros(n)
    p[idx[nombre_estudiante]] = 1.0
    r = p.copy()

    # 6. Iteración de RWR
    for _ in range(max_iter):
        p_new = (1 - alpha) * P @ p + alpha * r
        if np.linalg.norm(p_new - p, 1) < tol:
            break
        p = p_new

    # 7. Devolver cursos no tomados por el estudiante ordenados por score
    cursos_tomados = {c for e, c, _ in relaciones_rating if e == nombre_estudiante}
    resultados = []
    for curso in cursos:
        if curso not in cursos_tomados:
            resultados.append((curso, p[idx[curso]]))

    return sorted(resultados, key=lambda x: x[1], reverse=True)
