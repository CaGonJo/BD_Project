-- Em vez de DELETE usei SELECT * para poder testar sem apagar

WITH plixo AS (
	SELECT nro, num_serie, fabricante
	FROM prateleira
	WHERE nome='Iogurtes'
)


SELECT *
FROM planograma AS p 
WHERE nro IN (SELECT nro FROM plixo) 
AND num_serie IN (SELECT num_serie FROM plixo)
AND fabricante IN (SELECT fabricante FROM plixo)



