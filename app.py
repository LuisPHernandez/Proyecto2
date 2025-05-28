from flask import Flask, render_template, url_for, request, redirect, flash, session
import flask_sqlalchemy

app = Flask(__name__)

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