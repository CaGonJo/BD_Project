SELECT dia_semana,concelho, SUM (unidades) AS TOTQTY
FROM vendas
WHERE ano BETWEEN 2016 and 2022
GROUP BY
    GROUPING SETS ((dia_semana), (concelho), ());