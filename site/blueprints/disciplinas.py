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

@disciplinas_bp.route('/disciplinas/adicionar-disciplina', methods=['POST'])
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

@disciplinas_bp.route('/disciplinas/excluir-disciplina/<int:id_disc>')
def excluir_disciplina(id_disc):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM disciplinas WHERE id_disc = %s", (id_disc,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina excluída com sucesso!")
    return redirect('/disciplinas')

@disciplinas_bp.route('/disciplinas/editar-disciplina/<int:id_disc>', methods=['GET'])
def editar_disciplina(id_disc):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM disciplinas WHERE id_disc = %s", (id_disc,))
    disciplina = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editar_disciplina.html', disciplina=disciplina)

@disciplinas_bp.route('/disciplinas/atualizar-disciplina/<int:id_disc>', methods=['POST'])
def atualizar_disciplina(id_disc):

    nome = request.form['nome']
    
    ch = request.form['carga_horaria']

    creditos = request.form['creditos']

    ementa = request.form['ementa']

    if ementa == '':
        ementa = None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE disciplinas SET nome=%s, ch=%s, creditos=%s, ementa=%s WHERE id_disc=%s", 
                   (nome, ch, creditos, ementa, id_disc))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/disciplinas')

@disciplinas_bp.route('/disciplinas/editar-disciplina/<int:id_disc>/editar-pre-requisitos')
def editar_pre_requisitos(id_disc):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    if busca:
        if str(busca).isdigit():
            querry = "SELECT COUNT(*) AS total FROM disciplinas WHERE id_disc != %s AND id_disc NOT IN " \
            "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s) " \
            "AND disciplinas.id_disc = %s"
            cursor.execute(querry, (id_disc, id_disc, busca))
        else:
           querry = "SELECT COUNT(*) AS total FROM disciplinas d WHERE id_disc != %s " \
           "AND id_disc NOT IN " \
           "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s) " \
           "AND d.nome LIKE %s " \
           "GROUP BY d.id_disc"
           cursor.execute(querry, (id_disc, id_disc, '%' + busca + '%',))
    else:
        querry = "SELECT COUNT(*) AS total FROM disciplinas WHERE id_disc != %s AND id_disc NOT IN " \
        "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s)"
        cursor.execute(querry, (id_disc, id_disc,))

    resultado = cursor.fetchall()

    total_registros = resultado[0]['total'] if resultado else 0

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    offset = (page - 1) * PER_PAGE         # Cálculo do pulo

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('disciplinas.pagina_disciplinas', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('disciplinas.pagina_disciplinas', page=total_paginas, busca=busca))

    querry = "SELECT d.nome AS disciplina, d.id_disc AS id_d FROM disciplinas d " \
    "JOIN pre_requisitos pr ON d.id_disc = pr.id_pre_req WHERE pr.id_disc = %s"
    cursor.execute(querry, (id_disc,))

    pre_requisitos = cursor.fetchall()

    querry = "SELECT id_disc, nome FROM disciplinas WHERE id_disc = %s"
    cursor.execute(querry, (id_disc,))

    disciplina = cursor.fetchone()

    if busca:
        if busca.isdigit():
            querry = "SELECT * FROM disciplinas WHERE id_disc != %s AND id_disc NOT IN " \
            "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s) " \
            "AND disciplinas.id_disc = %s" \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, (id_disc, id_disc, busca, PER_PAGE, offset,))
        else:
            querry = "SELECT * FROM disciplinas WHERE id_disc != %s AND id_disc NOT IN " \
            "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s) " \
            "AND disciplinas.nome LIKE %s" \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, (id_disc, id_disc, '%' + busca + '%', PER_PAGE, offset))
    else:
        querry = "SELECT * FROM disciplinas d WHERE id_disc != %s AND id_disc NOT IN " \
        "(SELECT id_pre_req FROM pre_requisitos WHERE id_disc = %s)" \
        "LIMIT %s OFFSET %s"
        cursor.execute(querry, (id_disc, id_disc, PER_PAGE, offset))
    
    disciplinas_adicionaveis = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('editar_pre_requisitos.html', disciplinas_adicionaveis=disciplinas_adicionaveis, 
                           disciplina=disciplina, pre_requisitos=pre_requisitos, id_disc=id_disc,
                           page=page, total_paginas=total_paginas)

@disciplinas_bp.route('/disciplinas/editar-disciplina/<int:id_disc>/editar-pre-requisitos/adicionar-pre-requisito/<int:id_pre_req>', 
                      methods=['POST'])
def adicionar_pre_requisito(id_disc, id_pre_req):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    querry = "INSERT INTO pre_requisitos (id_disc, id_pre_req) " \
    "VALUES (%s, %s)"

    cursor.execute(querry, (id_disc, id_pre_req))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect(url_for('disciplinas.editar_pre_requisitos', id_disc=id_disc))


@disciplinas_bp.route('/disciplinas/editar-disciplina/<int:id_disc>/editar-pre-requisito/excluir-pre-requisito/<int:id_pre_req>')
def excluir_pre_requisito(id_disc, id_pre_req):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM pre_requisitos WHERE id_disc = %s AND id_pre_req = %s", (id_disc, id_pre_req))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina excluída com sucesso!")
    return redirect(url_for('disciplinas.editar_pre_requisitos', id_disc=id_disc))