--Qual o nome do retalhista (ou retalhistas) responsáveis pela reposição do maior número de categorias?
WITH t as (
    SELECT nome, contagem
    FROM retalhista AS r NATURAL JOIN (
        SELECT tin, COUNT(DISTINCT nome_cat) as contagem
        FROM responsavel_por
        GROUP BY tin
    ) AS rp
)
SELECT t.nome
FROM t
WHERE t.contagem = (
    SELECT MAX(t.contagem)
    FROM t
    );

--Qual o nome do ou dos retalhistas que são responsáveis por todas as categorias simples?

WITH t as (
    SELECT nome, contagem
    FROM retalhista NATURAL JOIN (
        SELECT tin, COUNT(DISTINCT rp.nome_cat) as contagem
        FROM responsavel_por as rp, categoria_simples as cs
        WHERE rp.nome_cat in cs.nome
        GROUP BY tin
    )
)

SELECT r.nome
FROM retalhista as r
WHERE (
    SELECT COUNT(DISTINCT nome) 
    FROM categoria_simples) = (

    SELECT contagem 
    FROM t
    WHERE r.nome=t.nome);
--Quais os produtos (ean) que nunca foram repostos?

SELECT ean
FROM produto
WHERE ean NOT IN (SELECT ean FROM planograma);

-- Quais os produtos (ean) que foram repostos sempre pelo mesmo retalhista?
SELECT ean
FROM (
            SELECT ean, COUNT(DISTINCT(tin)) as contagem
            FROM evento_reposicao
            GROUP BY ean
) as t
WHERE t.contagem = 1;
