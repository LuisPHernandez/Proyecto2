from flask import Flask, render_template, url_for, request, redirect, flash, session
from functools import wraps
from Test import procesar_personalidad
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

@app.route('/admin')
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
    personalidad = procesar_personalidad(datos)
    nombre = session.get('nombre')
    edad = session.get('edad')
    año = session.get('año')
    facultad = session.get('facultad')
    carrera = session.get('carrera')
    intereses_seleccionados = session.get('intereses_seleccionados')
    promedio = session.get('promedio')

    user_id = session['user_id']
    usuario = model.Usuario.query.get(user_id)
    usuario.perfil_completo = True
    db.session.commit()

    # Guardar en Neo4j
    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))
    crear_estudiante(conn, nombre, edad, año, facultad, carrera, intereses_seleccionados, promedio, personalidad)
    conn.cerrar()

    # Redirigir a pantalla de estudiante
    return redirect(url_for('estudiante'))

@app.route('/recomendaciones')
@login_requerido
def recomendaciones():
    user_id = session['user_id']

    conn = Neo4jConnection(uri="bolt://localhost", autor=("neo4j", "lipelupaadair"))

    # Obtener cursos recomendados usando el algoritmo híbrido
    cursos = recomendar_cursos_hibrido(conn, user_id)


if (__name__ == "__main__"):
    app.run(debug=True)