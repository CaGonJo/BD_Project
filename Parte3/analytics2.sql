SELECT concelho,cat,dia_semana, SUM(unidades) AS TOTQTY
FROM vendas
WHERE distrito='Distrito_0'
GROUP BY
    GROUPING SETS ((concelho, cat, dia_semana), ())