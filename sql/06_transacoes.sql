-- Arquivo 06 - TRANSACOES:
-- Possui 2 cenários de tranações usando BEGIN, COMMIT e ROLLBACK.

-- CENÁRIO 1:
-- Matrícula com rollback por capacidade excedida:


-- Criação da Procedure: inserir_matricula_turma
-- Objetivo: Facilitar o cenário 1 na realização da matrícula 
--           de um aluno em uma turma.
-- Parâmetros:
-- 		in_id_aluno (INT): ID do aluno que será matriculado.
--      in_id_turma (INT): ID da turma de destino.
-- Regras:
-- 		Verifica se a turma possui capacidade antes de inserir a matrícula.
-- 		Realiza ROLLBACK caso a turma esteja lotada.
DELIMITER $$

CREATE PROCEDURE inserir_matricula_turma(
	IN in_id_aluno INT,
    IN in_id_turma INT 
)
BEGIN
	DECLARE vagas_restantes INT DEFAULT 0; 
    -- variável para cálculo de vagas na turma.
    
    -- Inicia o controle de transação garantindo atomicidade.
	START TRANSACTION;
    
		-- Cálculo das vagas restantes na turma.
		SELECT (t.capacidade - COUNT(m.id_mat)) INTO vagas_restantes
		FROM turmas t
		LEFT JOIN matriculas m ON m.id_turma = t.id_turma
		WHERE t.id_turma = in_id_turma
		GROUP BY t.id_turma;
        
        -- Verificação da quantidade de vagas restantes.
		IF vagas_restantes > 0 THEN
			INSERT INTO matriculas(id_aluno, id_turma)
			VALUES (in_id_aluno, in_id_turma);
			COMMIT;
            -- COMMIT do aluno na turma desejada.
            SELECT 'Sucesso na operação' AS status;
		ELSE 
			ROLLBACK;
            -- ROLLBACK não realizando matrícula do aluno na turma desejada.
            SELECT 'ERRO: Turma lotada. Matrícula não realizada.' AS status;
		END IF;
END;

$$ DELIMITER ;

-- Primeira transação na turma com capacidade para 1 aluno.
CALL inserir_matricula_turma(6, 8);

-- Segunda transação com a turma lotada devido à primeira transação.
CALL inserir_matricula_turma(1, 8);

-- Verificação de alunos na turma escolhida.
SELECT * 
FROM matriculas
WHERE id_turma = 8;

-- Propriedade de ATOMICIDADE, CONSISTÊNCIA e DURABILIDADE assegurados, pois:
-- Se a turma possuir capacidade o aluno será inserido, se não possuir o aluno 
-- não será inserido nela (ATOMICIDADE).
-- Regra de capacidade de turma não foi violada (CONSISTÊNCIA).
-- Caso o feche o MYSQL Workbench ou faça outro COMMIT a informação estará lá (DURABILIDADE).


-- CENÁRIO 2:
-- Lançamento de notas em lote.

-- Primeira transaction para lançamentos de notas com COMMIT.
START TRANSACTION;

	UPDATE matriculas
    SET nota = 8.0, frequencia = 70
    WHERE id_mat = 11;
    
    UPDATE matriculas
    SET nota = 5, frequencia = 80
    WHERE id_mat = 12;
    
    UPDATE matriculas
    SET nota = 9, frequencia = 90
    WHERE id_mat = 13;
    
    SELECT id_mat, situacao 
    FROM matriculas
    WHERE id_mat IN(11, 12, 13);

COMMIT;

SELECT * FROM matriculas;

-- Segunda transaction com ROLLBACK e verificação antes e depois do ROLLBACK
START TRANSACTION;

	UPDATE matriculas 
    SET nota = 0, frequencia = 0 
    WHERE id_mat IN (1, 2, 3);

	-- Verificação antes do ROLLBACK
	SELECT id_mat, nota, frequencia, situacao FROM matriculas WHERE id_mat IN (1, 2, 3);

ROLLBACK;

-- Verificação depois do ROLLBACK
SELECT id_mat, nota, frequencia, situacao FROM matriculas WHERE id_mat IN (1, 2, 3);

-- Propriedade de ATOMICIDADE, CONSISTÊNCIA e DURABILIDADE assegurados.