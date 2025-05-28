from flask import Flask, render_template, url_for, request, redirect, flash, session
import flask_sqlalchemy
from test import procesar_personalidad
from forms import *

app = Flask(__name__)

# Configuración para usar SQLite como base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basedatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = flask_sqlalchemy.SQLAlchemy(app)
import usuarios_model as model

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

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

@app.route('/formulario')
def formulario():
    return render_template("formulario_inicial.html", facultades=facultades, intereses= intereses)

@app.route('/test', methods = ['POST'])
def test():
    datos = request.form.to_dict(flat=True)
    return  render_template("test.html", preguntas = preguntas_personalidad,datos_previos = datos)

@app.route('/resultado', methods=['POST'])
def resultado():
    datos = request.form.to_dict(flat=True)
    resultado_final = procesar_personalidad(datos)
    return render_template("resultado.html", resultado=resultado_final)