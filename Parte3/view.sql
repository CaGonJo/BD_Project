
create view vendas(ean,cat,ano,trimestre,mes,dia_mes,
                dia_semana,distrito,concelho,unidades) as 
    select t.ean,t.cat,
            EXTRACT(YEAR from e.instante),
            EXTRACT(QUARTER from e.instante),
            EXTRACT(MONTH from e.instante),
            EXTRACT(DAY from e.instante),
            EXTRACT(DOW from e.instante),
            p.distrito,p.concelho,e.unidades
    from ponto_de_retalho as p
    INNER JOIN instalada_em as i on i.nome=p.nome
    INNER JOIN evento_reposicao as e on (e.num_serie=i.num_serie and 
                                        e.fabricante LIKE i.fabricante)
    INNER JOIN tem_categoria as t on (t.ean=e.ean)
