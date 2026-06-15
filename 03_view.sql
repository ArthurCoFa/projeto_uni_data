-- VIEW
CREATE OR REPLACE VIEW vw_historico_academico AS
	SELECT
		a.nome AS aluno,
		c.nome AS curso,
		d.nome AS disciplina,
		p.nome AS professor,
		m.nota AS nota,
		m.frequencia AS frequencia,
		m.situacao AS situacao,
		CONCAT(t.semestre, '/', t.ano) AS periodo
	FROM matriculas m
		JOIN alunos a ON m.id_aluno = a.id_aluno
		JOIN cursos c ON a.id_curso = c.id_curso
		JOIN turmas t ON m.id_turma = t.id_turma
		JOIN disciplinas d ON t.id_disc = d.id_disc
		JOIN professores p ON t.id_prof =  p.id_prof
	ORDER BY aluno;
        
        
SELECT * FROM vw_historico_academico_2;
	
    

