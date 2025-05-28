from flask import Flask, render_template, url_for, request, redirect, flash, session
import flask_sqlalchemy
from Test import procesar_personalidad

app = Flask(__name__)

# Datos para formularios
facultades = {
    "Ingeniería": ["Biomédica", "Ciencias de la Computación", "Industrial", "Mecánica"],
    "Ciencias Sociales": ["Antropología", "Arqueología", "Psicología"],
    "Ciencias y Humanidades": ["Biología", "Bioquímica", "Física"],
    "Educación": ["Educación Musical", "Educación Primaria", "Educación Inclusiva"]
}

intereses = [
    "Tecnología", "Salud", "Educación", "Investigación", "Arte", "Ciencias Naturales", "Psicología", "Historia"
]

# Preguntas de personalidad
preguntas_personalidad = [
    {
        "pregunta": "¿Prefieres resolver problemas usando lógica y datos?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Te gusta inventar nuevas ideas o soluciones?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Prefieres seguir un procedimiento probado antes que improvisar?",
        "opciones": ["Sí", "No"]
    },
    {
        "pregunta": "¿Disfrutas trabajar en equipo y hablar con muchas personas?",
        "opciones": ["Sí", "No"]
    }
]

puntajes = {
    0: {"Sí": {"Analítico": 2}, "No": {"Sociable": 1, "Creativo": 1}},
    1: {"Sí": {"Creativo": 2}, "No": {"Práctico": 1}},
    2: {"Sí": {"Práctico": 2}, "No": {"Creativo": 1}},
    3: {"Sí": {"Sociable": 2}, "No": {"Analítico": 1}}
}

# Inicializar la base de datos
db = flask_sqlalchemy.SQLAlchemy(app)
import usuarios_model as model

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/formulario')
def formulario():
    return render_template("formularioInicial.html",facultades=facultades, intereses= intereses)

@app.route('/test', methods = ['POST'])
def test():
    datos = request.form.to_dict(flat=True)
    return  render_template("test.html", preguntas = preguntas_personalidad,datos_previos = datos)

@app.route('/resultado', methods=['POST'])
def resultado():
    datos = request.form.to_dict(flat=True)
    resultado_final = procesar_personalidad(datos)
    return render_template("resultado.html", resultado=resultado_final)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = model.Usuario.query.filter_by(username=username, password=password).first()

        if usuario != None:

            if usuario.tipo == 1:
                return redirect(url_for('admin'))
            elif usuario.tipo == 2:
                return redirect(url_for('estudiante'))
        else:
            flash('Usuario o password inválido', 'error')

    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/estudiante')
def maestro():
    return render_template('estudiante.html')

if (__name__ == "__main__"):
    app.run(debug=True)