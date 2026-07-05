from flask import Blueprint, render_template, request, redirect, flash, url_for
from db import get_db_connection, contar_registros, PER_PAGE
from math import ceil

professores_bp = Blueprint('professores', __name__)

TABELA = 'professores'

@professores_bp.route('/professores')
def pagina_professores():

    busca = request.args.get('busca', '')

    page = int(request.args.get('page', 1))  # Pega a página, padrão é 1

    total_registros = contar_registros(TABELA, busca=busca)

    total_paginas = ceil(total_registros / PER_PAGE) if total_registros > 0 else 1

    if page < 1: 
        flash("Você foi redirecionado para a primeira página disponível.")
        return redirect(url_for('professores.pagina_professores', page=1, busca=busca))
    elif page > total_paginas: 
        flash("Você foi redirecionado para a última página disponível.")
        return redirect(url_for('professores.pagina_professores', page=total_paginas, busca=busca))

    offset = (page - 1) * PER_PAGE          # Cálculo do pulo

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    if busca:
        if busca.isdigit():
            # Busca por ID
            querry = "SELECT p.*, c.nome AS curso " \
            "FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso " \
            "WHERE p.id_prof = %s"
            cursor.execute(querry, (busca,))
        else:
            # Busca por Nome
            querry = "SELECT p.*, c.nome AS curso " \
            "FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso " \
            "WHERE p.nome LIKE %s ORDER BY p.id_prof " \
            "LIMIT %s OFFSET %s"
            cursor.execute(querry, ('%' + busca + '%', PER_PAGE, offset))
    else:
        # Traz todos
        querry = "SELECT p.*, c.nome AS curso " \
        "FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso ORDER BY p.id_prof " \
        "LIMIT %s OFFSET %s"
        cursor.execute(querry, (PER_PAGE, offset))

    professores = cursor.fetchall() # A variável 'alunos' é atualizada aqui!
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('professores.html', professores=professores, busca=busca, 
                           cursos=cursos, page=page, total_paginas=total_paginas)

@professores_bp.route('/professores/adicionar-professor', methods=['POST'])
def adicionar_professor():
    # Captura os dados enviados pelo formulário
    nome = request.form['nome']

    titulacao = request.form['titulacao']
    titulacoes_validas = ['Mestre', 'Doutor', 'Pos-doutor']

    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    id_curso_coord = request.form['id_curso_coord'] # Pega o valor do select

    if titulacao not in titulacoes_validas:
        return "Erro: titulação inválida", 400
    
    if id_curso_coord == '0':
        id_curso_coord = None

    if len(cpf_limpo) != 11:
        # Aqui você poderia usar o sistema de 'flash' do Flask 
        # para mostrar uma mensagem de erro na tela
        return "Erro: CPF inválido! Deve conter 11 números.", 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO professores (nome, cpf, email, titulacao, id_curso_coord) " \
    "VALUES (%s, %s, %s, %s, %s)", (nome, cpf_limpo, email, titulacao, id_curso_coord))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Professor cadastrado com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/professores')

@professores_bp.route('/professores/excluir-professor/<int:id_prof>')
def excluir_professor(id_prof):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM professores WHERE id_prof = %s", (id_prof,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Professor excluído com sucesso!")
    return redirect('/professores')

@professores_bp.route('/professores/editar-professor/<int:id_prof>', methods=['GET'])
def editar_professor(id_prof):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM professores WHERE id_prof = %s", (id_prof,))
    professor = cursor.fetchone()

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('editar_professor.html', professor=professor, cursos=cursos)

@professores_bp.route('/professores/atualizar-professor/<int:id_prof>', methods=['POST'])
def atualizar_professor(id_prof):
    nome = request.form['nome']

    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    titulacao = request.form['titulacao']

    id_curso_coord = request.form['id_curso_coord']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE professores SET nome=%s, cpf=%s, email=%s, titulacao=%s, id_curso_coord=%s " \
                   "WHERE id_prof=%s", 
                   (nome, cpf_limpo, email, titulacao, id_curso_coord, id_prof))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/professores')