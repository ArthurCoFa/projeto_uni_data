DELIMITER $$
CREATE TRIGGER trg_calcula_situacao
BEFORE UPDATE ON matriculas
FOR EACH ROW
BEGIN

	IF NEW.nota IS NOT NULL AND NEW.frequencia IS NOT NULL THEN
		IF NEW.frequencia < 75 THEN
			SET NEW.situacao = 'Reprovado por falta';
		ELSEIF NEW.frequencia >= 75 AND NEW.nota < 6 THEN
			SET NEW.situacao = 'Reprovado por Nota';
		ELSE
			SET NEW.situacao = 'Aprovado';
		END IF;
	ELSE
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Algum dos valores é nulo.';
	END IF;
    
END;
$$ DELIMITER ;

-- Primeiro UPDATE
UPDATE matriculas
SET frequencia = 70, nota = 7.0
WHERE id_mat = 8;

SELECT * FROM matriculas;

-- Segundo UPDATE
UPDATE matriculas
SET frequencia = 80, nota = 5.8
WHERE id_mat = 9;

SELECT * FROM matriculas;

-- Terceiro UPDATE
UPDATE matriculas
SET frequencia = 100, nota = 8.2
WHERE id_mat = 10;

SELECT * FROM matriculas;

-- Testes com NULL
UPDATE matriculas
SET frequencia = NULL, nota = NULL
WHERE id_mat = 10;

UPDATE matriculas
SET frequencia = NULL, nota = 8.2
WHERE id_mat = 10;

UPDATE matriculas
SET frequencia = 100, nota = NULL
WHERE id_mat = 10;