create function apagar_dependencias_prateleira () returns trigger as $$
    declare prateleira_nro integer;
    declare prateleira_num_serie integer;
    declare prateleira_fabricante varchar(50);
    begin
        SELECT nro into prateleira_nro
        FROM prateleira

        SELECT num_serie into prateleira_num_serie
        FROM prateleira

        SELECT fabricante into prateleira_fabricante
        FROM prateleira
        
        if new.unidades>max_unid then
            raise exception 'O numero de unidades do evento de reposicao é superior ao permitido pelo planograma';
        end if;
        return new;
    end;
    $$ Language plpgsql;

create trigger pre_apagar_prateleira before delete on prateleira
for each row execute procedure apagar_dependencias_prateleira();
