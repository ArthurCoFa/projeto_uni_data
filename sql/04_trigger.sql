-- Arquivo 04 - TRIGGER:
-- Criação da Trigger: trg_calcula_situacao
-- Momento: Antes do UPDATE.
-- Objetivo: Atualizar automaticamente a coluna 'situacao' da tabela 
-- 			 matriculas sempre que a nota E frequencia forem alteradas.

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


-- Primeiro UPDATE na tabela matriculas (Reprovado por Falta).
UPDATE matriculas
SET frequencia = 70, nota = 7.0
WHERE id_mat = 8;

-- Verificação do funcionamento da trigger no primeiro UPDATE.
SELECT * FROM matriculas;


-- Segundo UPDATE na tabela matriculas (Reprovado por Nota).
UPDATE matriculas
SET frequencia = 80, nota = 5.8
WHERE id_mat = 9;

-- Verificação do funcionamento da trigger no segundo UPDATE.
SELECT * FROM matriculas;


-- Terceiro UPDATE na tabela matriculas (Aprovado).
UPDATE matriculas
SET frequencia = 100, nota = 8.2
WHERE id_mat = 10;

-- Verificação do funcionamento da trigger no segundo UPDATE.
SELECT * FROM matriculas;


-- Verificação da trigger com NULL (não pode alterar situação sem nota E frequencia).
UPDATE matriculas
SET frequencia = NULL, nota = NULL
WHERE id_mat = 10;

UPDATE matriculas
SET frequencia = NULL, nota = 8.2
WHERE id_mat = 10;

UPDATE matriculas
SET frequencia = 100, nota = NULL
WHERE id_mat = 10;