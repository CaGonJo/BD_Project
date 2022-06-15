--Qual o nome do retalhista (ou retalhistas) responsáveis pela reposição do maior número de categorias? 

--Qual o nome do ou dos retalhistas que são responsáveis por todas as categorias simples?

SELECT r.nome
FROM retalhista as r NATURAL JOIN responsavel_por as rp
WHERE tin = ALL (
    SELECT tin
    FROM rp
    WHERE nome_cat IN categoria_simples.nome
)

--Quais os produtos (ean) que nunca foram repostos?

SELECT ean
FROM produto
WHERE produto.ean NOT IN planograma.ean

-- Quais os produtos (ean) que foram repostos sempre pelo mesmo retalhista?

SELECT ean
FROM (
    SELECT ean, COUNT(DISTINCT(tin)) as contagem
    FROM evento_reposicao
)
WHERE contagem == 1
