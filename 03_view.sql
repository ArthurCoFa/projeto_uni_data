-- Arquivo 03 - VIEW:
-- Criação da VIEW: vw_historico_academico
-- Descição: Pesquisa os dados de todos os alunos para facilitar consultas.
-- Informações da pesquisa: nome do aluno, curso, professor e da disciplina, 
-- periodo da disciplina, nota, frequencia e situação.

CREATE OR REPLACE VIEW vw_historico_academico AS
	SELECT
		a.nome AS aluno,
		c.nome AS curso,
		d.nome AS disciplina,
        CONCAT(t.semestre, '/', t.ano) AS periodo,
		p.nome AS professor,
		m.nota AS nota,
		m.frequencia AS frequencia,
		m.situacao AS situacao
	FROM matriculas m
		JOIN alunos a ON m.id_aluno = a.id_aluno
		JOIN cursos c ON a.id_curso = c.id_curso
		JOIN turmas t ON m.id_turma = t.id_turma
		JOIN disciplinas d ON t.id_disc = d.id_disc
		JOIN professores p ON t.id_prof =  p.id_prof
	ORDER BY aluno;
        
        
SELECT * FROM vw_historico_academico;