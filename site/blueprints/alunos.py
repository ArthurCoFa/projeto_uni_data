from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil
from datetime import date

alunos_bp = Blueprint('alunos', __name__)

TABELA = 'alunos'

@alunos_bp.route('/alunos')
def pagina_alunos():

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.", "info")
        return redirect(url_for('alunos.pagina_alunos', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.", "info")
        return redirect(url_for('alunos.pagina_alunos', page=total_paginas, busca=busca))

    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    if busca:
        if busca.isdigit():
            querry = "SELECT a.*, c.nome AS curso FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso WHERE a.id_aluno = %s"
            cursor.execute(querry, (busca,))
        else:

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

    cursor.close()
    conn.close()

    return render_template('alunos.html', alunos=alunos, busca=busca, cursos=cursos, page=page, total_paginas=total_paginas)

@alunos_bp.route('/alunos/adicionar-alunos', methods=['POST'])
def adicionar_aluno():

    # Captura os dados enviados pelo formulário
    nome = request.form['nome']

    nascimento = request.form['data_nascimento']

    if date.fromisoformat(nascimento) > date.today():
        flash("Data de nascimento inválida! O aluno não pode ter nascido no futuro.", "danger")
        return redirect(url_for('alunos.pagina_alunos'))

    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    if len(cpf_limpo) != 11:
        flash("CPF inválido, tente novamente", "danger")
        return redirect(url_for('alunos.pagina_alunos'))

    email = request.form['email']

    id_curso = request.form['id_curso']

    if not id_curso or id_curso == "":
        flash("Erro: Curso inválido ou não selecionado na lista!", "danger")
        return redirect(url_for('alunos.pagina_alunos'))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO alunos (nome, dt_nasc, cpf, email, id_curso) VALUES (%s, %s, %s, %s, %s)", 
                   (nome, nascimento, cpf_limpo, email, id_curso))
    
    conn.commit()
    cursor.close()
    conn.close()

    flash("Aluno cadastrado com sucesso!", "success")
    
    # Volta para a tela inicial
    return redirect('/alunos')

@alunos_bp.route('/alunos/excluir-aluno/<int:id_aluno>')
def excluir_aluno(id_aluno):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM alunos WHERE id_aluno = %s", (id_aluno,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Aluno excluído com sucesso!", "success")
    return redirect('/alunos')

@alunos_bp.route('/alunos/editar-aluno/<int:id_aluno>', methods=['GET'])
def editar_aluno(id_aluno):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (id_aluno,))
    aluno = cursor.fetchone()

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('editar_aluno.html', aluno=aluno, cursos=cursos)

@alunos_bp.route('/alunos/editar-aluno/<int:id_aluno>/atualizar', methods=['POST'])
def atualizar_aluno(id_aluno):

    nome = request.form['nome']
    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    dt_nascimento = request.form['data_nascimento']

    id_curso = request.form['id_curso']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET nome=%s, cpf=%s, email=%s, dt_nasc=%s, id_curso=%s WHERE id_aluno=%s", 
                   (nome, cpf_limpo, email, dt_nascimento, id_curso, id_aluno))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!", "success")
    return redirect('/alunos')