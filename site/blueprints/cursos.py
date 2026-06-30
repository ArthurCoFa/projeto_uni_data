from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil

cursos_bp = Blueprint('cursos', __name__)

TABELA = 'cursos'

@cursos_bp.route('/cursos')
def pagina_cursos():

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('cursos.pagina_cursos', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('cursos.pagina_cursos', page=total_paginas, busca=busca))

    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        if busca.isdigit():
            # Busca por ID
            querry = "SELECT c.* FROM cursos c WHERE c.id_curso = %s"
            cursor.execute(querry, (busca,))
        else:
            # Busca por Nome
            querry = "SELECT c.* FROM cursos c WHERE c.nome LIKE %s ORDER BY c.id_curso " \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, ('%' + busca + '%', PER_PAGE, offset))
    else:
        # Traz todos
        querry = "SELECT c.* FROM cursos c ORDER BY c.id_curso " \
        "LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    cursos = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('cursos.html', busca=busca, cursos=cursos, page=page, total_paginas=total_paginas)

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

@cursos_bp.route('/cursos/<int:id>/editar-disciplinas-curso', methods=['GET'])
def editar_disciplinas_curso(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    querry = "SELECT nome, id_curso FROM cursos WHERE id_curso = %s"
    cursor.execute(querry, (id,))
    curso = cursor.fetchone()

    querry = "SELECT c.nome AS curso, d.nome AS disciplina, dc.obrigatoria, d.id_disc, c.id_curso " \
    "FROM disciplinas d JOIN curso_disciplina dc ON d.id_disc = dc.id_disc " \
    "JOIN cursos c ON c.id_curso = dc.id_curso " \
    "WHERE c.id_curso = %s " \
    "ORDER BY dc.obrigatoria DESC, d.nome ASC "

    cursor.execute(querry, (id,))
    disciplinas_curso = cursor.fetchall()

    querry = "SELECT d.id_disc, d.nome AS disciplina " \
    "FROM disciplinas d " \
    "WHERE NOT EXISTS (SELECT 1 " \
    "FROM curso_disciplina cd " \
    "WHERE cd.id_disc = d.id_disc AND cd.id_curso = %s);"

    cursor.execute(querry, (id,))
    todas_disciplinas = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('editar_disciplinas_curso.html', disciplinas_curso=disciplinas_curso, curso=curso, todas_disciplinas=todas_disciplinas)

@cursos_bp.route("/curso/<int:curso_id>/editar-obrigatoriedade/<int:disc_id>/alternar")
def alternar_obrigatoriedade_disciplina(curso_id, disc_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE curso_disciplina SET obrigatoria = NOT obrigatoria WHERE id_curso = %s AND id_disc = %s", 
                   (curso_id, disc_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect(url_for('cursos.editar_disciplinas_curso', id=curso_id))

@cursos_bp.route("/curso/<int:curso_id>/editar-obrigatoriedade/<int:disc_id>/excluir")
def excluir_disciplina_curso(curso_id, disc_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM curso_disciplina WHERE id_curso = %s AND id_disc = %s", 
                   (curso_id, disc_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect(url_for('cursos.editar_disciplinas_curso', id=curso_id))

@cursos_bp.route("/cursos/<int:curso_id>/adicionar-disciplina-curso", methods=['POST'])
def adicionar_disciplina_curso(curso_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    disciplina_id = request.form.get('disciplina_id')
    obrigatoria = 1 if request.form.get('obrigatoria') else 0
    
    querry = "INSERT INTO curso_disciplina (id_curso, id_disc, obrigatoria) " \
    "VALUES (%s, %s, %s)"
    
    cursor.execute(querry, (curso_id, disciplina_id, obrigatoria))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina adicionada com sucesso!")
    return redirect(url_for('cursos.editar_disciplinas_curso', id=curso_id))
