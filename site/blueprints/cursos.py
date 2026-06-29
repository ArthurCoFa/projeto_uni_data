from flask import Blueprint, render_template, request, redirect, flash
from db import get_db_connection

cursos_bp = Blueprint('cursos', __name__)

@cursos_bp.route('/cursos')
def pagina_cursos():
    busca = request.args.get('busca', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT c.* FROM cursos c WHERE c.id_curso = %s", (busca,))
        else:
            # Busca por Nome
            cursor.execute("SELECT c.* FROM cursos c WHERE c.nome LIKE %s ORDER BY c.id_curso", ('%' + busca + '%',))
    else:
        # Traz todos
        cursor.execute("SELECT c.* FROM cursos c ORDER BY c.id_curso")

    cursos = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('cursos.html', busca=busca, cursos=cursos)

@cursos_bp.route('/adicionar-curso', methods=['POST'])
def adicionar_curso():

    tipos_validos = ['Graduacao', 'Pos-Graduacao']

    # Captura os dados enviados pelo formulário
    nome = request.form['nome']
    
    ch_total = request.form['carga_horaria_total']

    tipo = request.form['tipo']

    if tipo not in tipos_validos:
        return "ERRO: tipo inválido", 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO cursos (nome, ch_total, tipo) VALUES (%s, %s, %s)", (nome, ch_total, tipo))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Curso cadastrado com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/cursos')

@cursos_bp.route('/excluir-curso/<int:id>')
def excluir_curso(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM cursos WHERE id_curso = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Curso excluído com sucesso!")
    return redirect('/cursos')

@cursos_bp.route('/editar-curso/<int:id>', methods=['GET'])
def editar_curso(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (id,))
    curso = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editar_curso.html', curso=curso)

@cursos_bp.route('/atualizar-curso/<int:id>', methods=['POST'])
def atualizar_curso(id):

    nome = request.form['nome']
    
    ch_total = request.form['carga_horaria_total']

    tipo = request.form['tipo']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE cursos SET nome=%s, ch_total=%s, tipo=%s WHERE id_curso=%s", 
                   (nome, ch_total, tipo, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/cursos')