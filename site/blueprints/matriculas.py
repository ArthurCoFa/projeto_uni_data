from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil

matriculas_bp = Blueprint('matriculas', __name__)

TABELA = 'matriculas'

@matriculas_bp.route('/matriculas')
def pagina_matriculas():
    
    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('matriculas.pagina_matriculas', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('matriculas.pagina_matriculas', page=total_paginas, busca=busca))
        
    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        querry = "SELECT m.id_mat, m.id_turma, m.id_aluno, m.dt_inscricao, m.nota, " \
        "m.frequencia, m.situacao, a.nome AS aluno, d.nome AS disciplina " \
        "FROM matriculas m JOIN turmas t ON t.id_turma = m.id_turma " \
        "JOIN alunos a ON a.id_aluno = m.id_aluno " \
        "JOIN disciplinas d ON d.id_disc = t.id_disc " \
        "WHERE m.id_mat = %s" \
        "ORDER BY m.id_mat"
        cursor.execute(querry, (busca,))
    else:
        # Traz todos
        querry = "SELECT m.id_mat, m.id_turma, m.id_aluno, m.dt_inscricao, m.nota, " \
        "m.frequencia, m.situacao, a.nome AS aluno, d.nome AS disciplina " \
        "FROM matriculas m JOIN turmas t ON t.id_turma = m.id_turma " \
        "JOIN alunos a ON a.id_aluno = m.id_aluno " \
        "JOIN disciplinas d ON d.id_disc = t.id_disc " \
        "ORDER BY m.id_mat " \
        "LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    matriculas = cursor.fetchall() 
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('matriculas.html', busca=busca, page=page, 
                           total_paginas=total_paginas, matriculas=matriculas)

@matriculas_bp.route('/adicionar-matricula/aluno')
def adicionar_aluno_matricula():

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros('alunos', busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('matriculas.pagina_matriculas', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('matriculas.pagina_matriculas', page=total_paginas, busca=busca))
        
    offset = (page - 1) * PER_PAGE          # Cálculo do pulo
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT a.*, c.nome AS curso FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso WHERE a.id_aluno = %s", (busca,))
        else:
            # Busca por Nome
            querry = "SELECT a.*, c.nome AS curso " \
            "FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso " \
            "WHERE a.nome LIKE %s ORDER BY a.id_aluno " \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, ('%' + busca + '%', PER_PAGE, offset))
    else:
        # Traz todos
        querry = "SELECT a.*, c.nome AS curso " \
        "FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso ORDER BY a.id_aluno " \
        "LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    alunos = cursor.fetchall()
    
    # Volta para a tela inicial
    return render_template('adicionar_matricula.html', alunos=alunos, page=page, total_paginas=total_paginas)

@matriculas_bp.route('/adicionar-matricula/aluno/<int:id_aluno>/turma')
def adicionar_turma_matricula(id_aluno):

    total_registros = 0

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros('turmas', busca=busca, campo_busca='id_turma')

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
    return render_template('adicionar_matricula_turma.html', busca=busca, turmas=turmas, page=page, 
                           total_paginas=total_paginas, disciplinas=disciplinas, 
                           professores = professores, id_aluno=id_aluno)

@matriculas_bp.route('/adicionar-matricula/aluno/<int:id_aluno>/turma/<int:id_turma>')
def adicionar_matricula_final(id_aluno, id_turma):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO matriculas(id_aluno, id_turma) " \
        "VALUES (%s, %s)", (id_aluno, id_turma))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Matricula cadastrada com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/matriculas')