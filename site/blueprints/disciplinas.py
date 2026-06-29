from flask import Blueprint, render_template, request, redirect, flash
from db import get_db_connection

disciplinas_bp = Blueprint('disciplinas', __name__)

@disciplinas_bp.route('/disciplinas')
def pagina_disciplinas():
    busca = request.args.get('busca', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT d.* FROM disciplinas d WHERE d.id_disc = %s", (busca,))
        else:
            # Busca por Nome
            cursor.execute("SELECT d.* FROM disciplinas d WHERE d.nome LIKE %s ORDER BY d.id_disc", ('%' + busca + '%',))
    else:
        # Traz todos
        cursor.execute("SELECT d.* FROM disciplinas d ORDER BY d.id_disc")

    disciplinas = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('disciplinas.html', busca=busca, disciplinas=disciplinas)

@disciplinas_bp.route('/adicionar-disciplina', methods=['POST'])
def adicionar_disciplina():

    # Captura os dados enviados pelo formulário
    nome = request.form['nome']
    
    ch = request.form['carga_horaria']

    creditos = request.form['creditos']

    ementa = request.form['ementa']

    if ementa == '':
        ementa = None
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO disciplinas (nome, ch, creditos, ementa) VALUES (%s, %s, %s, %s)", (nome, ch, creditos, ementa))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Disciplinas cadastrada com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/disciplinas')

@disciplinas_bp.route('/excluir-disciplina/<int:id>')
def excluir_disciplina(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM disciplinas WHERE id_disc = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina excluída com sucesso!")
    return redirect('/disciplinas')

@disciplinas_bp.route('/editar-disciplina/<int:id>', methods=['GET'])
def editar_disciplina(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM disciplinas WHERE id_disc = %s", (id,))
    disciplina = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editar_disciplina.html', disciplina=disciplina)

@disciplinas_bp.route('/atualizar-disciplina/<int:id>', methods=['POST'])
def atualizar_dsiciplina(id):

    nome = request.form['nome']
    
    ch = request.form['carga_horaria']

    creditos = request.form['creditos']

    ementa = request.form['ementa']

    if ementa == '':
        ementa = None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE disciplinas SET nome=%s, ch=%s, creditos=%s, ementa=%s WHERE id_disc=%s", 
                   (nome, ch, creditos, ementa, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/disciplinas')