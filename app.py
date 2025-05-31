from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from test import procesar_personalidad
from forms import *
from extensions import db
from base_de_datos import *
from recomendacion_hibrida import recomendar_cursos_hibrido

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basedatos.db'
app.secret_key = '1234'

db.init_app(app)

with app.app_context():
    import usuarios_model as model
    db.create_all()
    db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = model.Usuario.query.filter_by(email=email, password=password).first()

        if usuario:
            session['user_id'] = usuario.id
            session['nombre'] = f"{usuario.nombre} {usuario.apellido}"

            # Extraer datos del estudiante desde Neo4j
            conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
            datos_estudiante = obtener_estudiante_por_nombre(conn, session['nombre'])
            conn.cerrar()

            if datos_estudiante:
                session['edad'] = datos_estudiante['edad']
                session['año'] = datos_estudiante['año']
                session['facultad'] = datos_estudiante['facultad']
                session['carrera'] = datos_estudiante['carrera']
                session['intereses_seleccionados'] = datos_estudiante['intereses']
                session['promedio'] = datos_estudiante['promedio']
                session['personalidad'] = datos_estudiante['personalidad']

            if usuario.tipo == 1:
                return redirect(url_for('admin'))
            elif usuario.tipo == 2:
                session['user_id'] = usuario.id
                if not usuario.perfil_completo:
                    return redirect(url_for('formulario'))
                return redirect(url_for('estudiante'))
        else:
            flash('Usuario o password inválido', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Elimina todos los datos de sesión
    return redirect(url_for('login')) 

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['firstName']
        apellido = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('registro.html')

        if model.Usuario.query.filter_by(email=email).first():
            flash('Este correo ya está registrado.', 'error')
            return render_template('registro.html')

        # Obtiene el ID correspondiente al tipo 'Estudiante'
        tipo_estudiante = model.UsuarioTipo.query.filter_by(tipo='Estudiante').first()

        if not tipo_estudiante:
            flash('Error: tipo de usuario "Estudiante" no está definido.', 'error')
            return render_template('registro.html')

        nuevo_usuario = model.Usuario(nombre=nombre, apellido=apellido, email=email, password=password, tipo=tipo_estudiante.id)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Cuenta creada exitosamente. Inicia sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada

@app.route('/admin',  methods=['GET', 'POST'])
@login_requerido
def admin():
    return render_template('admin.html')


@app.route('/estudiante')
@login_requerido
def estudiante():
    return render_template('estudiante.html')

@app.route('/formulario', methods=['GET', 'POST'])
@login_requerido
def formulario():
    if request.method == 'POST':
        print("Llegó un POST al formulario")
        session['edad'] = int(request.form.get('edad'))
        session['año'] = request.form.get('año')
        session['facultad'] = request.form.get('facultad')
        session['carrera'] = request.form.get('carrera')
        session['intereses_seleccionados'] = request.form.getlist('intereses')
        session['promedio'] = float(request.form.get('promedio'))

        flash("Perfil guardado exitosamente", "success")
        return redirect(url_for('test'))

    return render_template("formulario.html", facultades=facultades, intereses= intereses)

@app.route('/test', methods = ['GET', 'POST'])
@login_requerido
def test():
    datos = request.form.to_dict(flat=True)
    return  render_template("test.html", preguntas = preguntas_personalidad,datos_previos = datos)

@app.route('/resultado', methods=['POST'])
@login_requerido
def resultado():
    datos = request.form.to_dict(flat=True)
    session['personalidad'] = procesar_personalidad(datos)
    print(session.get('personalidad'))
    personalidad = session.get('personalidad')
    nombre = session.get('nombre')
    edad = session.get('edad')
    año = session.get('año')
    facultad = session.get('facultad')
    carrera = session.get('carrera')
    intereses_seleccionados = session.get('intereses_seleccionados')
    promedio = session.get('promedio')

    user_id = session['user_id']
    usuario = db.session.get(model.Usuario, user_id)
    usuario.perfil_completo = True
    db.session.commit()

    # Guardar en Neo4j
    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
    crear_estudiante(conn, nombre, edad, año, facultad, carrera, intereses_seleccionados, promedio, personalidad)
    estudiantes = obtener_estudiantes(conn)
    crear_relaciones(conn, estudiantes, k=3)
    conn.cerrar()

    # Redirigir a pantalla de estudiante
    return redirect(url_for('estudiante'))

@app.route('/recomendaciones')
@login_requerido
def recomendaciones():
    nombre = session['nombre']

    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))

    datos_usuario = {
    "edad": session.get('edad'),
    "facultad": session.get('facultad'),
    "carrera": session.get('carrera'),
    "año_academico": session.get('año'),
    "promedio": session.get('promedio'),
    "intereses": session.get('intereses_seleccionados'),
    "personalidad": session.get('personalidad')
    }

    # Obtener cursos recomendados usando el algoritmo híbrido
    cursos = recomendar_cursos_hibrido(conn, nombre)
    return render_template('recomendaciones.html', cursos=cursos, datos_usuario=datos_usuario)

@app.route('/ranking')
@login_requerido
def ranking():
    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
    cursos = obtener_cursos_mejor_valorados(conn, limite=10)
    conn.cerrar()
    return render_template('ranking.html', cursos=cursos)


@app.route('/agregar_curso', methods=['POST', 'GET'])
@login_requerido
def agregar_curso():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']

    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
    crear_curso(conn, nombre, descripcion)
    conn.cerrar()

    return render_template("agregar_curso.html")

if (__name__ == "__main__"):
    app.run(debug=True)