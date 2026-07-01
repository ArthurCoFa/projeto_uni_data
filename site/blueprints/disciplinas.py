from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil

disciplinas_bp = Blueprint('disciplinas', __name__)

TABELA = 'disciplinas'

@disciplinas_bp.route('/disciplinas')
def pagina_disciplinas():

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('disciplinas.pagina_disciplinas', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('disciplinas.pagina_disciplinas', page=total_paginas, busca=busca))
        

    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT d.* FROM disciplinas d WHERE d.id_disc = %s", (busca,))
        else:
            # Busca por Nome
            querry = "SELECT d.* FROM disciplinas d WHERE d.nome LIKE %s ORDER BY d.id_disc " \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, ('%' + busca + '%', PER_PAGE, offset))
    else:
        # Traz todos
        querry = "SELECT d.* FROM disciplinas d ORDER BY d.id_disc LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    disciplinas = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('disciplinas.html', busca=busca, disciplinas=disciplinas, page=page, total_paginas=total_paginas)

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
def atualizar_disciplina(id):

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

@disciplinas_bp.route('/disciplinas/<int:id>/editar-pre-requisitos')
def editar_pre_requisitos(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    querry = "SELECT d.nome AS disciplina, d.id_disc AS id_d FROM disciplinas d JOIN pre_requisitos pr ON d.id_disc = pr.id_pre_req WHERE pr.id_disc = %s"
    cursor.execute(querry, (id,))

    pre_requisitos = cursor.fetchall()

    querry = "SELECT id_disc, nome FROM disciplinas WHERE id_disc = %s"
    cursor.execute(querry, (id,))

    disciplina = cursor.fetchone()

    querry = "SELECT * FROM disciplinas WHERE id_disc != %s AND id_disc NOT IN " \
    "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s)"
    cursor.execute(querry, (id, id,))
    
    disciplinas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('editar_pre_requisitos.html', disciplinas=disciplinas, disciplina=disciplina, pre_requisitos=pre_requisitos)

@disciplinas_bp.route('/disciplinas/<int:id>/adicionar-pre-requisito', methods=['POST'])
def adicionar_pre_requisito(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    id_pre_req = request.form['pre-requisito']

    querry = "INSERT INTO pre_requisitos (id_disc, id_pre_req) " \
    "VALUES (%s, %s)"

    cursor.execute(querry, (id, id_pre_req))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect(url_for('disciplinas.editar_pre_requisitos', id=id))


@disciplinas_bp.route('/disciplinas/<int:id_disc>/excluir-pre-requisito/<int:id_pre_req>')
def excluir_pre_requisito(id_disc, id_pre_req):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM pre_requisitos WHERE id_disc = %s AND id_pre_req = %s", (id_disc, id_pre_req))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina excluída com sucesso!")
    return redirect(url_for('disciplinas.editar_pre_requisitos', id=id_disc))