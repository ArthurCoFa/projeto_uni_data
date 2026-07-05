from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil

turmas_bp = Blueprint('turmas', __name__)

TABELA = 'turmas'

@turmas_bp.route('/turmas')
def pagina_turmas():
    
    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    if busca:
        if busca.isdigit():
            total_registros = contar_registros(TABELA, busca=busca, campo_busca='id_turma')
        else:
            total_registros = contar_registros('disciplinas', busca=busca)
    else:
        total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('turmas.pagina_turmas', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('turmas.pagina_turmas', page=total_paginas, busca=busca))
        
    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_disc, nome FROM disciplinas")
    disciplinas = cursor.fetchall()

    cursor.execute("SELECT id_prof, nome FROM professores")
    professores = cursor.fetchall()

    if busca:
        if busca.isdigit():
            cursor.execute("SELECT t.id_turma, d.nome AS disciplina, p.nome AS professor, " \
            "t.semestre, t.ano, t.capacidade " \
            "FROM turmas t " \
            "JOIN professores p ON p.id_prof = t.id_prof " \
            "JOIN disciplinas d ON d.id_disc = t.id_disc " \
            "WHERE t.id_turma = %s ", (busca,))
        else:
            cursor.execute("SELECT t.id_turma, d.nome AS disciplina, p.nome AS professor, " \
            "t.semestre, t.ano, t.capacidade " \
            "FROM turmas t " \
            "JOIN professores p ON p.id_prof = t.id_prof " \
            "JOIN disciplinas d ON d.id_disc = t.id_disc " \
            "WHERE d.nome LIKE %s ", ('%' + busca + '%',))
    else:
        # Traz todos
        querry = "SELECT t.id_turma, d.nome AS disciplina, p.nome AS professor, " \
        "t.semestre, t.ano, t.capacidade " \
        "FROM turmas t " \
        "JOIN professores p ON p.id_prof = t.id_prof " \
        "JOIN disciplinas d ON d.id_disc = t.id_disc " \
        "ORDER BY t.id_turma LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    turmas = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('turmas.html', busca=busca, turmas=turmas, page=page, 
                           total_paginas=total_paginas, disciplinas=disciplinas, professores = professores)

@turmas_bp.route('/turmas/adicionar-turma', methods=['POST'])
def adicionar_turma():
    
    id_disc = request.form['id_disc']

    id_prof = request.form['id_prof']

    semestre = request.form['semestre']

    ano = request.form['ano']

    capacidade = request.form['capacidade']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO turmas(id_disc, id_prof, semestre, ano, capacidade) " \
        "VALUES (%s, %s, %s, %s, %s)", (id_disc, id_prof, semestre, ano, capacidade))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Turma cadastrada com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/turmas')

@turmas_bp.route('/turmas/excluir-turma/<int:id_turma>')
def excluir_turma(id_turma):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM turmas WHERE id_turma = %s", (id_turma,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Disciplina excluída com sucesso!")
    return redirect('/turmas')

@turmas_bp.route('/turmas/editar-turma/<int:id_turma>', methods=['GET'])
def editar_turma(id_turma):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id_disc, nome FROM disciplinas")
    disciplinas = cursor.fetchall()

    cursor.execute("SELECT id_prof, nome FROM professores")
    professores = cursor.fetchall()

    cursor.execute("SELECT * FROM turmas WHERE id_turma = %s", (id_turma,))
    turma = cursor.fetchone()

    cursor.close()
    conn.close()
    return render_template('editar_turma.html', turma=turma, disciplinas=disciplinas, 
                           professores = professores)

@turmas_bp.route('/turmas/atualizar_turma/<int:id_turma>', methods=['POST'])
def atualizar_disciplina(id_turma):

    id_disc = request.form['id_disc']

    id_prof = request.form['id_prof']

    semestre = request.form['semestre']

    ano = request.form['ano']

    capacidade = request.form['capacidade']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("UPDATE turmas SET id_disc = %s, id_prof = %s, " \
    "semestre = %s, ano = %s, capacidade = %s WHERE id_turma = %s", 
    (id_disc, id_prof, semestre, ano, capacidade, id_turma))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Turma atulualizada com sucesso!")
    return redirect('/turmas')

