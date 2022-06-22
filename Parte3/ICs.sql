DROP TRIGGER IF EXISTS verifica_unidades_reposicao ON evento_reposicao;
DROP TRIGGER IF EXISTS verifica_planograma ON planograma;



create or replace function num_unidades_permitido () returns trigger as
    $$ declare max_unid integer;
    begin
        SELECT unidades into max_unid
        FROM planograma
        WHERE planograma.ean=new.ean and planograma.nro=new.nro and planograma.num_serie=new.num_serie and planograma.fabricante=new.fabricante;
        
        if new.unidades>max_unid then
            raise exception 'O numero de unidades do evento de reposicao é superior ao permitido pelo planograma';
        end if;
        return new;
    end; 
    $$ LANGUAGE plpgsql;

create trigger verifica_unidades_reposicao before insert on evento_reposicao
for each row execute procedure num_unidades_permitido();


create or replace function cat_prateleira () returns trigger as 
    $$ declare categoria varchar(50);
    begin
        SELECT nome into categoria
        FROM prateleira
        WHERE prateleira.nro=new.nro and prateleira.num_serie=new.num_serie and prateleira.fabricante=new.fabricante;
	
        WITH RECURSIVE t1 AS (
	    SELECT  super_cat
	    FROM tem_outra
	    WHERE cat=categoria

	    UNION ALL

	    SELECT t2.super_cat
	    FROM t1
	    JOIN tem_outra AS t2
	    ON t2.cat=t1.super_cat)


        if new.ean not in   (SELECT ean
                            FROM tem_categoria
                            WHERE tem_categoria.nome in (SELECT * FROM t1))

        
        then
            raise exception 'Um produto só pode ser reposto numa prateleira que apresente uma das categorias desse produto.';
        end if;
        return new;
    end; 
    $$ LANGUAGE plpgsql;

create trigger verifica_planograma before insert on planograma
for each row execute procedure cat_prateleira();
