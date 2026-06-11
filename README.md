# Projeto de Banco de Dados para uma Universidade

Este projeto é uma implementação de um sistema de Banco de Dados para uma universidade fictícia no MYSQL para a matéria de Banco de Dados 2.

---

## Funcionalidades
* Consultas: Pesquisas nas tabelas com consultas complexas utlizando JOINs, GROUP BY, HAVING e subconsultas com NOT EXISTS.
* Transações: Controle de transações para matrícula e lançamento de notas, garantindo atomicidade através de COMMITs e ROLLBACKs.
* Automação: O uso de Triggers permite a atualização automática da situação acadêmica do aluno.

---

## Pré-Requisitos
Para executar esse programa, certifique-se que tenha instalado:
* MySQL Server (8.0+).
* MySQL Workbench (ou software de preferência).

---

## Como Usar
Para configurar e executar o projeto, siga a ordem de importação/execução dos arquivos abaixo em seu SGBD: </br>
1 - **`01_ddl.sql`**: Define a estrutura das tabelas e relacionamentos. </br>
2 - **`02_dml.sql`**: Popula o banco com dados de teste. </br>
3 - **`03_view.sql`**: Cria a view necessárias para uma das consultas (queries). </br> 
4 - **`04_trigger.sql`**: Instala as automações (triggers) do sistema. </br> 
5 - **`05_queries.sql`**: Contém as consultas de relatório solicitadas. </br>
6 - **`06_transacoes.sql`**: Scripts das transações (ACID) demonstrando controle de matrículas. </br>
7 - **`07_evidencias.pdf`**: Arquivo contendo os prints de comprovação de execução e testes. </br>
8 - **`08_diagrama_er.pdf`**: Modelo Entidade-Relacionamento do banco de dados. </br>

>**NOTA**: É necessário rodar os arquivos de 1 a 4 na ordem correta, pois isso garante que todas as dependências (tabelas, views, triggers) existam antes da execução das queries e transações.
