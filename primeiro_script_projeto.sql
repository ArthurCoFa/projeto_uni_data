CREATE DATABASE teste_uni_data;

USE teste_uni_data;

CREATE TABLE cursos(
	id_curso INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    ch_total INT NOT NULL,
    tipo ENUM('Graduacao', 'Pos-Graduacao')
);

ALTER TABLE cursos
ADD CONSTRAINT 	chk_ch_curso
CHECK(ch_total > 0);

SHOW CREATE TABLE cursos;

CREATE TABLE disciplinas(
	id_disc INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    ch INT NOT NULL,
    creditos INT NOT NULL,
    ementa TEXT,
    CONSTRAINT chk_ch_disc CHECK(ch > 0),
    CONSTRAINT chk_creditos_disc CHECK(creditos > 0)
);

DROP TABLE disciplinas;

SHOW CREATE TABLE disciplinas;

CREATE TABLE pre_requisitos(
	id_disc INT NOT NULL,
    id_pre_req INT NOT NULL,
    CONSTRAINT fk_disc_req FOREIGN KEY (id_disc) REFERENCES disciplinas(id_disc),
    CONSTRAINT fk_disc_req_2 FOREIGN KEY (id_pre_req) REFERENCES disciplinas(id_disc),
    CONSTRAINT chk_no_self_req CHECK(id_disc != id_pre_req)
);

DROP TABLE pre_requisitos;

SHOW CREATE TABLE pre_requisitos;

CREATE TABLE curso_disciplina(
	id_curso INT NOT NULL,
    id_disc INT NOT NULL,
    obrigatoria BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_curso_disc FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    CONSTRAINT fk_disc_curso FOREIGN KEY (id_disc) REFERENCES disciplinas(id_disc)
);

SHOW CREATE TABLE curso_disciplina;

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

DROP TABLE professores;

SHOW CREATE TABLE professores;
   
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

CREATE TABLE matricula(
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

