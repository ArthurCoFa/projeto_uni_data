-- Arquivo 01 - DDL: 
-- Possui o CREATE DATABASE e os CREATE TABLE com todas as constraints

CREATE DATABASE uni_data; -- Criação do Banco de Dados da universidade

USE uni_data; -- Utilização do Banco de Dados criado

/* 
Tabela cursos: Representa os cursos que a universidade possui com nome do curso,
carga horária total (ch_total), tipo de curso é graduação ou pós-graduação 
*/

CREATE TABLE cursos(
	id_curso INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    ch_total INT NOT NULL,
    tipo ENUM('Graduacao', 'Pos-Graduacao') NOT NULL,
    CONSTRAINT chk_ch_curso CHECK(ch_total > 0)
);

/*
Tabela disciplinas: Representa as disciplinas que são ofertadas por cada curso,
contendo nome da disciplina, carga horária, créditos, ementa(opcional).
*/

CREATE TABLE disciplinas(
	id_disc INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    ch INT NOT NULL,
    creditos INT NOT NULL,
    ementa TEXT DEFAULT NULL,
    CONSTRAINT chk_ch_disc CHECK(ch > 0),
    CONSTRAINT chk_creditos_disc CHECK(creditos > 0)
);

/*
Tabela pré-requisitos: Representa disciplinas que possuem pré-requisitos.
*/

CREATE TABLE pre_requisitos(
	id_disc INT NOT NULL,
    id_pre_req INT NOT NULL,
    CONSTRAINT fk_disc_req FOREIGN KEY (id_disc) REFERENCES disciplinas(id_disc),
    CONSTRAINT fk_disc_req_2 FOREIGN KEY (id_pre_req) REFERENCES disciplinas(id_disc),
    CONSTRAINT chk_no_self_req CHECK(id_disc != id_pre_req)
);

/*
Tabela curso_disciplina: Representa o relacionamento entre as disciplinas dentro do curso,
definindo se a disciplina é obrigatória ou opcional.
*/

CREATE TABLE curso_disciplina(
	id_curso INT NOT NULL,
    id_disc INT NOT NULL,
    obrigatoria BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_curso_disc FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    CONSTRAINT fk_disc_curso FOREIGN KEY (id_disc) REFERENCES disciplinas(id_disc)
);

/*
Tabela professores: Representa os professores que possuem cpf, email, titulação (mestre, doutor ou pós-doutor)
e se é coordenador de algum curso(id_curso_coord).
*/

CREATE TABLE professores (
	id_prof INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    cpf CHAR(11) NOT NULL,
	email VARCHAR(150) NOT NULL,
	titulacao ENUM ('Mestre','Doutor','Pos-Doutor') NOT NULL,
	id_curso_coord INT DEFAULT NULL,
    CONSTRAINT fk_prof_curso FOREIGN KEY (id_curso_coord) REFERENCES cursos(id_curso),
    CONSTRAINT uq_cpf_prof UNIQUE(cpf),
    CONSTRAINT uq_email_prof UNIQUE(email)
);

/*
Tabela turmas: Representa a turma com a disciplina ofertada por ela possuindo disciplina, professor, 
semestre (1 ou 2), ano e capacidade.
*/
   
CREATE TABLE turmas (
    id_turma INT PRIMARY KEY AUTO_INCREMENT,
    id_disc INT NOT NULL,
    id_prof INT NOT NULL,
    semestre TINYINT NOT NULL,
    ano YEAR NOT NULL,
    capacidade INT NOT NULL,
    CONSTRAINT fk_id_disc FOREIGN KEY (id_disc) REFERENCES disciplinas (id_disc),
    CONSTRAINT fk_id_prof FOREIGN KEY (id_prof) REFERENCES professores (id_prof),
    CONSTRAINT chk_semestre CHECK(semestre IN(1,2)),
    CONSTRAINT chk_ano CHECK(ano >= 2000),
    CONSTRAINT chk_capacidade CHECK(capacidade > 0)
);

/*
Tabela alunos: Representa os alunos que podem ser matriculados e qual o seu curso escolhido.
*/

CREATE TABLE alunos (
	id_aluno INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(120) NOT NULL,
    cpf CHAR(11) NOT NULL,
    email VARCHAR(150) NOT NULL,
    dt_nasc DATE NOT NULL,
    id_curso INT NOT NULL,
    CONSTRAINT uq_cpf_aluno UNIQUE(cpf),
    CONSTRAINT uq_email_aluno UNIQUE(email),
	CONSTRAINT fk_id_curso FOREIGN KEY (id_curso) REFERENCES cursos (id_curso)
);

/*
Tabela matrículas: Representa as matrículas de alunos nas turmas com suas notas, frequências 
e situção de aprovação, reprovação ou em curso.
*/

CREATE TABLE matriculas(
	id_mat INT PRIMARY KEY AUTO_INCREMENT,
    id_aluno INT NOT NULL,
    id_turma INT NOT NULL,
    dt_inscricao DATE NOT NULL DEFAULT (curdate()),
    nota DECIMAL(4,1) DEFAULT NULL,
    frequencia DECIMAL(5,2) DEFAULT NULL,
    situacao ENUM('Em Curso', 'Aprovado', 'Reprovado por Nota', 'Reprovado por Falta') DEFAULT 'Em Curso',
    CONSTRAINT fk_turma_matricula FOREIGN KEY (id_turma) REFERENCES turmas(id_turma) ON DELETE CASCADE,
    CONSTRAINT fk_aluno_matricula FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    CONSTRAINT uq_aluno_turma UNIQUE (id_aluno, id_turma),
    CONSTRAINT chk_nota CHECK(nota BETWEEN 0 AND 10),
    CONSTRAINT chk_frequencia CHECK(frequencia BETWEEN 0 AND 100)
);

/* Como curiosidade é possível analizar a criação de tabelas com:

	SHOW CREATE TABLE nome_da_tabela;
*/
