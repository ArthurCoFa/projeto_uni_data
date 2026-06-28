from flask import Blueprint, render_template, request, redirect, flash
from db import get_db_connection

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/alunos')
def pagina_alunos():
    busca = request.args.get('busca', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cursos")

    cursos = cursor.fetchall()

    if busca:
        if busca.isdigit():
            # Busca por ID
            cursor.execute("SELECT a.*, c.nome AS curso FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso WHERE a.id_aluno = %s", (busca,))
        else:
            # Busca por Nome
            cursor.execute("SELECT a.*, c.nome AS curso FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso WHERE a.nome LIKE %s ORDER BY a.id_aluno", ('%' + busca + '%',))
    else:
        # Traz todos
        cursor.execute("SELECT a.*, c.nome AS curso FROM alunos a JOIN cursos c ON a.id_curso = c.id_curso ORDER BY a.id_aluno")

    alunos = cursor.fetchall() # A variável 'alunos' é atualizada aqui!
    cursor.close()
    conn.close()
    
    # O segredo é que o render_template precisa enviar essa variável atualizada
    return render_template('alunos.html', alunos=alunos, busca=busca, cursos=cursos)

@alunos_bp.route('/adicionar-alunos', methods=['POST'])
def adicionar_aluno():
    # Captura os dados enviados pelo formulário
    nome = request.form['nome']

    nascimento = request.form['data_nascimento']

    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    id_curso = request.form['id_curso'] # Pega o valor do select

    if len(cpf_limpo) != 11:
        # Aqui você poderia usar o sistema de 'flash' do Flask 
        # para mostrar uma mensagem de erro na tela
        return "Erro: CPF inválido! Deve conter 11 números.", 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o INSERT
    cursor.execute("INSERT INTO alunos (nome, dt_nasc, cpf, email, id_curso) VALUES (%s, %s, %s, %s, %s)", (nome, nascimento, cpf_limpo, email, id_curso))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Aluno cadastrado com sucesso!")
    
    # Volta para a tela inicial
    return redirect('/alunos')

@alunos_bp.route('/excluir-aluno/<int:id>')
def excluir_aluno(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Executa o delete usando o ID recebido na URL
    cursor.execute("DELETE FROM alunos WHERE id_aluno = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Aluno excluído com sucesso!")
    return redirect('/alunos')

@alunos_bp.route('/editar-aluno/<int:id>', methods=['GET'])
def editar_aluno(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM alunos WHERE id_aluno = %s", (id,))
    aluno = cursor.fetchone()

    cursor.execute("SELECT * FROM cursos")
    cursos = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('editar_aluno.html', aluno=aluno, cursos=cursos)

@alunos_bp.route('/atualizar-aluno/<int:id>', methods=['POST'])
def atualizar_aluno(id):
    nome = request.form['nome']
    cpf_form = request.form['cpf']

    cpf_limpo = "".join(filter(str.isdigit, cpf_form))

    email = request.form['email']

    dt_nascimento = request.form['data_nascimento']

    id_curso = request.form['id_curso']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET nome=%s, cpf=%s, email=%s, dt_nasc=%s, id_curso=%s WHERE id_aluno=%s", 
                   (nome, cpf_limpo, email, dt_nascimento, id_curso, id))
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Dados atualizados com sucesso!")
    return redirect('/alunos')