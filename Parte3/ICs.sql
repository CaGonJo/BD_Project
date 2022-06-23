DROP TRIGGER IF EXISTS verifica_unidades_reposicao ON evento_reposicao;
DROP TRIGGER IF EXISTS verifica_planograma ON planograma;
DROP TRIGGER IF EXISTS verifica_categorias_diferentes ON tem_outra;

create or replace function nomes_diferentes () returns trigger as
    $$
    begin
        if new.cat=new.super_cat then
            raise exception 'Uma categoria não se pode conter a si mesma';
        end if;
        return new;
    end; 
    $$ LANGUAGE plpgsql;

create trigger verifica_categorias_diferentes before insert on tem_outra
for each row execute procedure nomes_diferentes();


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
	
        if new.ean not in   (SELECT ean
                            FROM tem_categoria
                            WHERE tem_categoria.nome=categoria)

        then
            raise exception 'Um produto só pode ser reposto numa prateleira que apresente uma das categorias desse produto.';
        end if;
        return new;
    end; 
    $$ LANGUAGE plpgsql;

create trigger verifica_planograma before insert on planograma
for each row execute procedure cat_prateleira();
