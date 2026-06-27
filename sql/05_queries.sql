-- Arquivo 05 - QUERIES:
-- Queries de 1 a 10 que fazem consultas específicas no Banco de Dados, 
-- solicitadas no projeto.



-- QUERRY 1: 
-- Todos os alunos com nome do curso e total de disciplinas cursadas. 
SELECT 
	a.nome AS aluno,
	c.nome AS curso,
    COUNT(id_disc) AS disciplinas
FROM
	alunos a 
    JOIN 
    cursos c ON c.id_curso = a.id_curso
    JOIN
	matriculas m ON m.id_aluno = a.id_aluno
    JOIN 
    turmas t ON t.id_turma = m.id_turma
GROUP BY a.id_aluno;



-- QUERRY 2:
-- Professores com mais de 2 turmas ativas no ano corrente. 
SELECT
	p.nome AS professor,
	COUNT(t.id_turma) AS turmas
FROM
	professores p
	JOIN
	turmas t ON p.id_prof = t.id_prof
WHERE ano = YEAR(NOW())
GROUP BY p.id_prof
HAVING COUNT(id_turma) > 2;



-- QUERRY 3:
-- Taxa de aprovação por disciplina (%). 
SELECT
	d.nome AS disciplina,
	ROUND(SUM(CASE WHEN m.situacao = 'Aprovado' THEN 1 ELSE 0 END) * 100 / COUNT(*), 2) AS taxa_aprovacao
FROM
	matriculas m
    JOIN
    turmas t ON t.id_turma = m.id_turma
    RIGHT JOIN 
    disciplinas d ON d.id_disc = t.id_disc
GROUP BY d.id_disc;



-- QUERRY 4:
-- Alunos com nota acima da média da sua disciplina

-- Usando Common Table Expression (CTE).
WITH media_por_disciplina AS (
	SELECT 
		t.id_disc, 
        AVG(m.nota) AS media_disciplina
	FROM 
		matriculas m
        JOIN turmas t ON m.id_turma = t.id_turma
	GROUP BY t.id_disc
)
SELECT
	d.nome AS disciplina,
	a.nome AS aluno,
    m.nota,
    md.media_disciplina
FROM
	matriculas m 
    JOIN
	alunos a ON a.id_aluno = m.id_aluno
    JOIN
    turmas t ON t.id_turma = m.id_turma
    JOIN 
    disciplinas d ON d.id_disc = t.id_disc
    JOIN 
	media_por_disciplina md ON md.id_disc = d.id_disc
WHERE m.nota > md.media_disciplina;



-- Querry 4:
-- Usando Subquerry. 
SELECT 
	d.nome AS disciplina,
    a.nome AS aluno,
    m.nota
FROM
	matriculas m 
    JOIN
	alunos a ON a.id_aluno = m.id_aluno
    JOIN
    turmas t ON t.id_turma = m.id_turma
    JOIN 
    disciplinas d ON d.id_disc = t.id_disc
WHERE m.nota > (
	SELECT AVG(m2.nota)
    FROM matriculas m2
    JOIN turmas t2 ON t2.id_turma = m2.id_turma
    WHERE t2.id_disc = t.id_disc
);



-- QUERRY 5:
-- Disciplinas sem nenhuma matrícula ativa.
SELECT
	d.nome AS disciplina
FROM 
	disciplinas d 
    LEFT JOIN 
    turmas t ON t.id_disc = d.id_disc
    LEFT JOIN
    matriculas m ON m.id_turma = t.id_turma
WHERE m.id_mat IS NULL;




-- QUERRY 6:
-- Ranking de alunos por média ponderada (créditos).
SELECT 
	a.nome AS aluno,
    ROUND(SUM(m.nota * d.creditos) / SUM(d.creditos), 2) AS media_ponderada
FROM
	alunos a
    JOIN
    matriculas m ON m.id_aluno = a.id_aluno
    JOIN
	turmas t ON t.id_turma = m.id_turma
    JOIN
    disciplinas d ON d.id_disc = t.id_disc
GROUP BY a.id_aluno
ORDER BY media_ponderada DESC;



-- QUERRY 7:
-- Disciplinas e seus pré-requisitos via Self JOIN.
SELECT 
	d.nome AS disciplina,
    pr.nome AS pre_requisito
FROM 
	disciplinas d
    JOIN
    pre_requisitos p ON p.id_disc = d.id_disc
    JOIN
    disciplinas pr ON pr.id_disc = p.id_pre_req;
    
    
    
-- QUERRY 8:
-- Cursos com média de nota dos alunos abaixo de 7,0. 
SELECT 
	c.nome AS curso,
    AVG(m.nota) AS media
FROM
	disciplinas d
    JOIN 
    turmas t ON t.id_disc = d.id_disc
    JOIN
    matriculas m ON m.id_turma = t.id_turma
    JOIN
    alunos a ON a.id_aluno = m.id_aluno
    JOIN
    cursos c ON c.id_curso = a.id_curso
GROUP BY c.id_curso
HAVING AVG(m.nota) < 7;



-- QUERRY 9:
-- Histórico completo de um aluno específico via view
SELECT * FROM vw_historico_academico
WHERE aluno = 'Arthur';




-- QUERRY 10:
-- Professores que nunca reprovaram nenhum aluno
SELECT 
    p.nome AS professor
FROM 
    professores p
WHERE NOT EXISTS (
    SELECT 1 
    FROM turmas t
    JOIN matriculas m ON t.id_turma = m.id_turma
    WHERE t.id_prof = p.id_prof
      AND m.situacao IN('Reprovado por Nota', 'Reprovado por Falta')
);