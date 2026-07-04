# Projeto de site para uma Universidade

## IMPORTANTE ANTES DE LER!!!
## Esta é uma continuação da branch "main", por isso é necessário seguir os passos dela para configuração correta dos arquivos do Banco de Dados.

Essa branch "feature-site-python" é uma extensão da branch "main" e tem como objetivo a implementação de um Backend em Python(Flask) para o Sistema de Gestão Acadêmica, conectando o usuário ao Banco de Dados permitindo operações de CRUD.

---

## Funcionalidades
* Gestão: Cadastro e edição completo de alunos, disciplinas, professores, turmas e matrículas.
* Busca Inteligente: Sistema de Pesquisa para listas grandes.
* Paginação: Lista organizada para garantir performance e boa usabilidade.

---

## Pré-Requisitos
Para executar esse programa, certifique-se que tenha instalado:
* Python.
* MySQL Server (8.0+).
* Bibliotecas flask e math.

---

## Como Usar

### 1. Clonar o repositório ou baixar o zip
- Caso queira clonar, abra o "git bash" com o botão direito na pasta ou espaço desejado no seu computador e escreva e execute cada linha separadamente: 

        git clone https://github.com/ArthurCoFa/projeto_uni_data.git

        cd projeto_uni_data

        git checkout feature-site-python

- Caso deseje baixar o zip, no repositório e na branch "feature-site-python" clique no botão verde escrito "Code" e clique na opção "Download ZIP" e baixe para o local desejado. 

### 2. Configuração do Banco de Dados
>**NOTA**: É necessário ter executado os arquivos do Banco através dos passos na branch "main", porém caso não tenha feito isso é possível configurar com os arquivos na pasta "SQL" na executando eles em ordem númerica.

Com o banco configurado abra o arquivo "db.py" e modifique os dados de configuração do Banco de acordo com o sua configuração (provavelmente a única mudança será a senha do seu banco, pois o usuário e o database serão iguais).

        return mysql.connector.connect{
        'host': 'localhost',
        'user': 'seu_usuario',
        'password': 'sua_senha',
        'database': 'nome_do_seu_banco'
        }

### 3. Execução
Com os passos anteriores realizados execute o arquivo "app.py" no local desejado (terminal ou IDE de preferência) e abra o link http://127.0.0.1:5000/ no navegador para acessar o sistema.