SELECT dia_semana,concelho, SUM (unidades) AS TOTQTY,
FROM vendas
WHERE ano BETWEEN 2016 and 2022
GROUP BY
    GROUPING SETS ((dia_semana), (concelho), ());


SELECT concelho,categir,dia_semana, SUM(unidades) AS TOTQTY,
FROM vendas
WHERE distrito LIKE "Distrito_0"
GROUP BY
    GROUPING SETS ((concelho), (categoria), (dia_semana), ())