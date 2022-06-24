--Qual o nome do retalhista (ou retalhistas) responsáveis pela reposição do maior número de categorias?
SELECT t2.nome
FROM (retalhista AS r INNER JOIN responsavel_por AS rp ON r.tin = rp.tin) AS t2
GROUP BY t2.nome
HAVING COUNT(DISTINCT t2.nome_cat) = (SELECT MAX(contagem)
                                      FROM (SELECT COUNT(DISTINCT nome_cat) AS contagem
                                            FROM responsavel_por) as t1);

--Qual o nome do ou dos retalhistas que são responsáveis por todas as categorias simples?
SELECT t1.nome
FROM (retalhista AS r INNER JOIN (SELECT tin, nome_cat 
                                  FROM responsavel_por
                                  WHERE nome_cat IN (SELECT nome
                                                     FROM categoria_simples)) AS rp 
      ON r.tin = rp.tin) AS t1
GROUP BY t1.nome
HAVING COUNT(DISTINCT t1.nome_cat) = (SELECT COUNT(nome) FROM categoria_simples);
--Quais os produtos (ean) que nunca foram repostos?

SELECT ean
FROM produto
WHERE ean NOT IN (SELECT ean FROM evento_reposicao);

-- Quais os produtos (ean) que foram repostos sempre pelo mesmo retalhista?
SELECT ean
FROM (
            SELECT ean, COUNT(DISTINCT(tin)) as contagem
            FROM evento_reposicao
            GROUP BY ean
) as t
WHERE t.contagem = 1;
