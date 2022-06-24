
CREATE view vendas(ean,cat,ano,trimestre,mes,dia_mes,
                dia_semana,distrito,concelho,unidades) AS 
    SELECT t.ean,t.cat,
            EXTRACT(YEAR FROM e.instante),
            EXTRACT(QUARTER FROM e.instante),
            EXTRACT(MONTH FROM e.instante),
            EXTRACT(DAY FROM e.instante),
            EXTRACT(DOW FROM e.instante),
            p.distrito,p.concelho,e.unidades
    FROM ponto_de_retalho AS p
    INNER JOIN instalada_em AS i AS i.nome=p.nome
    INNER JOIN evento_reposicao AS e ON (e.num_serie=i.num_serie AND 
                                        e.fabricante LIKE i.fabricante)
    INNER JOIN tem_categoria AS t ON (t.ean=e.ean)
