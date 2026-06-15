DELIMITER $$
CREATE PROCEDURE inserir_matricula_turma(
	IN in_id_aluno INT,
    IN in_id_turma INT 
)
BEGIN
	DECLARE vagas_restantes INT DEFAULT 0;
    
	START TRANSACTION;
		SELECT (t.capacidade - COUNT(m.id_mat)) INTO vagas_restantes
		FROM turmas t
		LEFT JOIN matriculas m ON m.id_turma = t.id_turma
		WHERE t.id_turma = in_id_turma
		GROUP BY t.id_turma;
        
		IF vagas_restantes > 0 THEN
			INSERT INTO matriculas(id_aluno, id_turma)
			VALUES (in_id_aluno, in_id_turma);
			COMMIT;
            SELECT 'Sucesso na operação' AS status;
		ELSE 
			ROLLBACK;
            SELECT 'ERRO: Turma lotada. Matrícula não realizada.' AS status;
		END IF;
END;
$$ DELIMITER ;

-- Teste primeira transação			
CALL inserir_matricula_turma(6, 8);

CALL inserir_matricula_turma(1, 8);

-- SEGUNDA TRANSAÇÃO
START TRANSACTION;

	UPDATE matriculas
    SET nota = 8.0, frequencia = 70
    WHERE id_mat = 3;
    
    UPDATE matriculas
    SET nota = 5, frequencia = 80
    WHERE id_mat = 2;
    
    UPDATE matriculas
    SET nota = 9, frequencia = 90
    WHERE id_mat = 1;
    
    SELECT id_mat, situacao 
    FROM matriculas
    WHERE id_mat IN(1, 2, 3);

COMMIT;

-- ROLLBACK
START TRANSACTION;

	UPDATE matriculas SET nota = 0, frequencia = 0 WHERE id_mat IN (1, 2, 3);

	SELECT id_mat, nota, frequencia, situacao FROM matriculas WHERE id_mat IN (1, 2, 3);

ROLLBACK;

SELECT id_mat, nota, frequencia, situacao FROM matriculas WHERE id_mat IN (1, 2, 3);