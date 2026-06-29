from flask import Flask, render_template
from blueprints.alunos import alunos_bp
from blueprints.professores import professores_bp
from blueprints.cursos import cursos_bp
from blueprints.disciplinas import disciplinas_bp

app = Flask(__name__)

app.secret_key = 'uma_chave_muito_secreta'

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(disciplinas_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)