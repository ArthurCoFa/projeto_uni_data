from flask import Blueprint, render_template, request, redirect, flash
from db import get_db_connection

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/professores')
def pagina_professores():
    busca = request.args.get('busca', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT p.*, c.nome AS curso FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso WHERE p.id_prof = %s", (busca,))
        else:
            # Busca por Nome
            cursor.execute("SELECT p.*, c.nome AS curso FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso WHERE p.nome LIKE %s ORDER BY p.id_prof", ('%' + busca + '%',))
    else:
        # Traz todos
        cursor.execute("SELECT p.*, c.nome AS curso FROM professores p LEFT JOIN cursos c ON p.id_curso_coord = c.id_curso ORDER BY p.id_prof")

    professores = cursor.fetchall() # A variável 'alunos' é atualizada aqui!
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('professores.html', professores=professores, busca=busca, cursos=cursos)

@professores_bp.route('/adicionar-professor', methods=['POST'])
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
    cursor.execute("INSERT INTO professores (nome, cpf, email, titulacao, id_curso_coord) VALUES (%s, %s, %s, %s, %s)", (nome, cpf_limpo, email, titulacao, id_curso_coord))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Professor cadastrado com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/professores')

@professores_bp.route('/excluir-professor/<int:id>')
def excluir_professor(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM professores WHERE id_prof = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Professor excluído com sucesso!")
    return redirect('/professores')

@professores_bp.route('/editar-professor/<int:id>', methods=['GET'])
def editar_professor(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM professores WHERE id_prof = %s", (id,))
    professor = cursor.fetchone()

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('editar_professor.html', professor=professor, cursos=cursos)

@professores_bp.route('/atualizar-professor/<int:id>', methods=['POST'])
def atualizar_professor(id):
    nome = request.form['nome']

    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    titulacao = request.form['titulacao']

    id_curso_coord = request.form['id_curso_coord']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE professores SET nome=%s, cpf=%s, email=%s, titulacao=%s, id_curso_coord=%s WHERE id_prof=%s", 
                   (nome, cpf_limpo, email, titulacao, id_curso_coord, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/professores')