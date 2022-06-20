create function num_unidades_permitido () returns trigger as $$
    declare max_unid integer;
    begin
        SELECT unidades into max_unid
        FROM planograma
        WHERE planograma.ean=new.ean and plnograma.nro=new.nro and planograma.num_serie=new.num_serie and planograma.fabricante LIKE new.fabricante
        
        if new.unidades>max_unid then
            raise exception 'O numero de unidades do evento de reposicao é superior ao permitido pelo planograma';
        end if;
        return new;
    end;

create trigger verifica_unidades_reposicao before insert on evento_reposicao
for each row execute procedure num_unidades_permitido();


create function cat_prateleira () returns trigger as 
    declare categoria varchar(50);
    begin

        SELECT nome into categoria
        FROM prateleira
        WHERE prateleira.nro=new.nro and prateleira.num_serie=new.num_serie and prateleira.fabricante LIKE new.fabricante

        if new.ean not in   (SELECT ean
                            FROM tem_categoria
                            WHERE tem_categoria.nome=categoria)
        
        then
            raise exception 'Um produto só pode ser reposto numa prateleira que apresente uma das categorias desse produto.';
        end if;
        return new;
    end;

create trigger verifica_planograma before insert on planograma
for each row execute procedure cat_prateleira();