from flask import Flask, render_template, request, jsonify
from db import get_db_connection
from blueprints.alunos import alunos_bp
from blueprints.professores import professores_bp
from blueprints.cursos import cursos_bp
from blueprints.disciplinas import disciplinas_bp
from blueprints.turmas import turmas_bp
from blueprints.matriculas import matriculas_bp

app = Flask(__name__)

app.secret_key = 'uma_chave_muito_secreta'

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(matriculas_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/buscar-alunos')
def buscar_alunos():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    termo = request.args.get('q') # O que o usuário digitou

    querry = ("SELECT id_aluno, nome FROM alunos WHERE nome LIKE %s LIMIT 5")

    cursor.execute(querry, (termo,))

    alunos = cursor.fetchall()

    return jsonify(alunos) # Retorna um JSON para o seu JavaScript

if __name__ == '__main__':
    app.run(debug=True)