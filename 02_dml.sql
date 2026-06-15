INSERT INTO cursos(nome, ch_total, tipo) VALUES 
('Engenharia de Computação', 3600, 'Graduacao'),
('Ciência da Computação', 3400, 'Graduacao'),
('Inteligência Artificial e Machine Learning', 360, 'Pos-Graduacao');

SELECT * FROM cursos;

INSERT INTO disciplinas(nome, ch, creditos) VALUES
('Banco de Dados 1', 60, 4),
('Banco de Dados 2', 60, 4),
('Processamento de Linguagem Natural', 60, 4),
('Sistemas embarcados / Microprocessadores', 90, 6),
('Circuitos Digitais', 90, 6),
('Bootcamp 1', 75, 5),
('Engenharia de Requisitos', 75, 5),
('Estrutura de Dados', 90, 6),
('Programação Orientada a Objeto', 60, 4),
('Lógica de Programação', 60, 4),
('Bootcamp 2', 60, 4);

SELECT * FROM disciplinas;

INSERT INTO pre_requisitos(id_disc, id_pre_req) VALUES
(2, 1),	(11, 6), (9, 10);

-- RN04: Uma disciplina não pode ser pré-requisito dela mesma.
INSERT INTO pre_requisitos(id_disc, id_pre_req) VALUES (1, 1);

SELECT * FROM pre_requisitos;

INSERT INTO curso_disciplina(id_curso, id_disc, obrigatoria) VALUES
(1, 1, TRUE), (1, 2, TRUE), (1, 3, FALSE), (1, 4, TRUE), (1, 5, TRUE), (1, 10, TRUE), (1, 9, TRUE), (1, 6, FALSE),

(2, 1, TRUE), (2, 2, TRUE), (2, 6, TRUE), (2, 11, FALSE), (2, 4, TRUE), (2, 5, FALSE), (2, 7, TRUE),

(3, 3, TRUE), (3, 8, TRUE), (3, 7, TRUE), (3, 9, FALSE), (3, 10, FALSE), (3, 11, FALSE);

SELECT * FROM curso_disciplina;

INSERT INTO professores(nome, cpf, email, titulacao, id_curso_coord) VALUES
('Hudson','12345678912', 'hudson@gmail.com', 'Mestre', 1),
('Ednardo', '98765432100', 'ednardo@gmail.com', 'Doutor', 2),
('Salvador', '11122233344', 'salvador@hotmail.com', 'Pos-Doutor', NULL),
('Vera', '00011122233', 'vera@yahoo.com', 'Mestre', NULL),
('Molina','33388866622', 'molina@gmail.com', 'Mestre', NULL);

SELECT * FROM professores;

INSERT INTO turmas(id_disc, id_prof, semestre, ano, capacidade) VALUES
(2, 3, 1, 2026, 57),
(5, 1, 1, 2026, 52),
(4, 1, 2, 2026, 42),
(8, 4, 1, 2027, 62),
(3, 2, 2, 2026, 46),
(11, 4, 2, 2026, 80),
(6, 1, 2, 2026, 1),
(1, 1, 1, 2027, 1);

SELECT * FROM turmas;

INSERT INTO alunos(nome, cpf, email, dt_nasc, id_curso) VALUES
('Arthur', '12312312312', 'arthur@hotmail.com', '2007-01-22', 1),
('Felipe', '45645645644', 'felipe@gmail.com', '2006-08-16', 2),
('João', '78978978978', 'joao@yahoo.com', '2000-02-07', 3),
('Gabriel', '14714714714', 'gabriel@gmail.com', '2005-06-06', 1),
('Gil', '25825825825', 'gil@hotmail.com', '1990-04-12', 3),
('Gustavo', '36936936936', 'gustavo@gmail.com', '2004-09-30', 2),
('Emanuel', '15915915915', 'emanuel@gmail.com', '2006-09-08', 2),
('Carlos', '35735735735', 'carlos@gmail.com', '2002-07-03', 1),
('Luiz', '00033344499', 'luiz@gmail.com', '1999-01-01', 3),
('Manuela', '99977755533', 'manu@gmail.com', '2007-06-02', 1);

SELECT * FROM alunos;

INSERT INTO matriculas(id_aluno, id_turma) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 3),
(8, 4),
(9, 5),
(10, 5),
(1, 4),
(1, 5),
(4, 3),
(4, 5),
(4, 1),
(5, 5),
(6, 5);

SELECT * FROM matriculas;

-- Verificação da RN 09: Um aluno não pode ter duas matrículas ativas na mesma turma.
INSERT INTO matriculas(id_aluno, id_turma, nota, frequencia)
VALUES (1, 1, 8, 100);

INSERT INTO matriculas(id_aluno, id_turma)
VALUES (6, 5);

INSERT INTO matriculas(id_aluno, id_turma)
VALUES (6, 6), (5, 6);

-- RN12:  Se uma turma for excluída do sistema, todas as matrículas associadas devem ser excluídas automaticamente.
DELETE FROM turmas
WHERE id_turma = 6;