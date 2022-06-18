create table categoria (
    nome    varchar(50),
    primary key(nome),
    check(nome in (select nome from super_categoria) or nome in (select nome from categoria_simples))
);

create table categoria_simples (
    nome    varchar(50),
    foreign key(nome) references categoria(nome),
    primary key(nome),
    check(nome not in (select nome from super_categoria))
);

create table super_categoria (
    nome    varchar(50),
    foreign key(nome) references categoria(nome),
    primary key(nome),
    check(nome in (select super_cat from tem_outra))
);

create table tem_outra (
    super_cat  varchar(50),
    cat    varchar(50),
    foreign key(super_cat) references super_categoria(nome),
    foreign key(cat) references categoria(nome),
    primary key(cat),
    check (super_cat NOT LIKE cat)
);

create table produto (
    ean     numeric(13, 0),
    descr   varchar(255),
    cat     varchar(50),
    primary key(ean),
    foreign key(cat) references categoria(nome),
    check (ean in (select ean from tem_categoria))
);

create table tem_categoria (
    foreign key(ean) references produto,
    foreign key(cat) references categoria 
);

create table IVM (
    num_serie   integer,
    fabricante  varchar(50),
    primary key (num_serie, fabricante)
);

create table ponto_de_retalho (
    nome    varchar(50),
    distrito    varchar(50),
    concelho    varchar(50),
    primary key(nome)
);

create table instalada_em (
    num_serie   integer,
    fabricante  varchar(50),
    nome     varchar(50),
    foreign key (num_serie, fabricante) references IVM(num_serie, fabricante),
    foreign key (nome) references ponto_de_retalho(nome),
    primary key (num_serie, fabricante)
);

create table prateleira (
    nro     integer NOT NULL CHECK (nro >= 0),
    num_serie   integer,
    fabricante  varchar(50),
    altura  integer NOT NULL CHECK (altura > 0),
    nome    varchar(50),
    foreign key(nome) references categoria,
    foreign key(num_serie, fabricante) references IVM,
    primary key(nro, num_serie, fabricante)
);

create table planograma (
    ean     numeric(13, 0),
    nro     integer,
    num_serie   integer,
    fabricante  varchar(50),
    faces   integer CHECK (faces > 0),
    unidades    integer NOT NULL CHECK (unidades > 0),
    loc     integer NOT NULL CHECK (loc >= 0),
    foreign key(ean) references produto,
    foreign key(nro, num_serie, fabricante) references prateleira,
    primary key(ean, nro, num_serie, fabricante)
);

create table retalhista (
    tin     integer,
    nome    varchar(50) NOT NULL UNIQUE,
    primary key(tin)
);

create table responsavel_por (
    nome_cat    varchar(50),
    tin     integer,
    num_serie   integer,
    fabricante  varchar(50),
    foreign key(num_serie, fabricante) references IVM,
    foreign key(tin) references retalhista,
    foreign key(nome_cat) references categoria,
    primary key(num_serie, fabricante)
);

create table evento_reposicao(
    ean     numeric(13, 0),
    nro     integer,
    num_serie   integer,
    fabricante  varchar(50),
    instante    integer NOT NULL CHECK (instante >= 0),
    unidades    integer NOT NULL CHECK (unidades > 0),
    tin     integer,
    foreign key(ean, nro, num_serie, fabricante) references planograma,
    foreign key(tin) references retalhista,
    primary key(ean, nro, num_serie, fabricante, instante)
);

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
    $$ Language plpgsql;

create trigger verifica_unidades_reposicao before insert on evento_reposicao
for each row execute procedure num_unidades_permitido();


create function cat_prateleira () returns trigger as $$
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
    $$ Language plpgsql;

create trigger verifica_planograma before insert on planograma
for each row execute procedure cat_prateleira();

----------------------------------------
-- Populate Relations 
----------------------------------------
insert into categoria values ('Bolo');
insert into categoria values ('Iogurte');
insert into categoria values ('Salgado');
insert into categoria values ('Refrigerante');
insert into categoria values ('Agua');
insert into categoria values ('Bolacha');
insert into categoria values ('Fruta');
insert into categoria values ('Doce');
insert into categoria values ('Bebida');

insert into super_categoria values ('Doce');
insert into super_categoria values ('Bebida');

insert into categoria_simples values ('Bolo');
insert into categoria_simples values ('Iogurte');
insert into categoria_simples values ('Salgado');
insert into categoria_simples values ('Refrigerante');
insert into categoria_simples values ('Agua');
insert into categoria_simples values ('Bolacha');
insert into categoria_simples values ('Fruta');

insert into tem_outra values ('Doce','Bolo');
insert into tem_outra values ('Bebida','Iogurte');
insert into tem_outra values ('Bebida','Refrigerante');
insert into tem_outra values ('Bebida','Agua');
insert into tem_outra values ('Doce','Bolacha');


insert into produto values (01234567890123, 'Bolo de Cafe', 'Bolo');
insert into produto values (01234567890128, 'Bolo de Laranja', 'Bolo');
insert into produto values (01234567890123, 'Waffle', 'Bolo');
insert into produto values (01234567890124, 'Fanta', 'Refrigerante');
insert into produto values (01234567890129, 'Coca-Cola', 'Refrigerante');
insert into produto values (01234567890129, 'Powerade', 'Refrigerante');
insert into produto values (01234567890129, 'RedBull', 'Refrigerante');
insert into produto values (01234567890125, 'Luso', 'Agua');
insert into produto values (01234567890130, 'Vitalis', 'Agua');
insert into produto values (01234567890127, 'Cafe', 'Bebida');
insert into produto values (01234567890130, 'Tuc', 'Bolacha');
insert into produto values (01234567890130, 'Bolacha Maria', 'Bolacha');
insert into produto values (01234567890130, 'Maca', 'Fruta');
insert into produto values (01234567890130, 'Banana', 'Fruta');
insert into produto values (01234567890130, 'Batatas Lays', 'Salgado');
insert into produto values (01234567890130, 'Batatas Pala-Pala', 'Salgado');

insert into IVM values (1201, 'Yamaha');
insert into IVM values (1202, 'Yamaha');
insert into IVM values (2301, 'Ducati');
insert into IVM values (2302, 'Ducati');
insert into IVM values (3401, 'Ferrari');
insert into IVM values (3402, 'Ferrari');
insert into IVM values (3403, 'Ferrari');
insert into IVM values (4501, 'KTM');
insert into IVM values (4502, 'KTM');
insert into IVM values (5601, 'Mclaren');
insert into IVM values (5602, 'Mclaren');
insert into IVM values (5603, 'Mclaren');
insert into IVM values (5604, 'Mclaren');

insert into prateleira values (1, 1201, 'Yamaha', 10, 'Bolo');
insert into prateleira values (2, 1201, 'Yamaha', 10, 'Salgado');
insert into prateleira values (1, 2301, 'Ducati', 10, 'Bolo');
insert into prateleira values (2, 2301, 'Ducati', 10, 'Iogurte');
insert into prateleira values (1, 2302, 'Ducati', 10, 'Bolo');
insert into prateleira values (2, 2302, 'Ducati', 10, 'Refrigerante');
insert into prateleira values (1, 3401, 'Ferrari', 10, 'Bolacha');
insert into prateleira values (2, 3401, 'Ferrari', 20, 'Agua');
insert into prateleira values (3, 3401, 'Ferrari', 20, 'Salgado');
insert into prateleira values (1, 3402, 'Ferrari', 10, 'Bolo');
insert into prateleira values (2, 3402, 'Ferrari', 20, 'Agua');
insert into prateleira values (3, 3402, 'Ferrari', 10, 'Refrigerante');
insert into prateleira values (1, 4501, 'KTM', 10, 'Fruta');
insert into prateleira values (2, 4501, 'KTM', 10, 'Bolacha');
insert into prateleira values (3, 4501, 'KTM', 20, 'Salgado');
insert into prateleira values (1, 5601, 'McLaren', 10, 'Bolo');
insert into prateleira values (2, 5601, 'McLaren', 10, 'Bolacha');
insert into prateleira values (1, 1202, 'Yamaha', 10, 'Bolo');
insert into prateleira values (2, 1202, 'Yamaha', 10, 'Refrigerante');
insert into prateleira values (3, 1201, 'Yamaha', 20, 'Salgado');


insert into ponto_de_retalho values ("Ezequiel", "Faro", "Se");
insert into ponto_de_retalho values ("Asdrubal", "Santarem", "Almeirim");
insert into ponto_de_retalho values ("Gertrudes", "Lisboa", "Arroios");
insert into ponto_de_retalho values ("Anibal", "Lisboa", "Lumiar");
insert into ponto_de_retalho values ("Oscar", "Lisboa", "Paco de Arcos");
insert into ponto_de_retalho values ("Ildefonso", "Leiria", "Batalha");
insert into ponto_de_retalho values ("Coralia", "Porto", "Foz");
insert into ponto_de_retalho values ("Vanessa", "Leiria", "Nazare");
insert into ponto_de_retalho values ("Martinho", "Lisboa", "Arroios");
insert into ponto_de_retalho values ("Palmira", "Leiria", "Peniche");
insert into ponto_de_retalho values ("Astride", "Lisboa", "Odivelas");
insert into ponto_de_retalho values ("Piedade", "Lisboa", "Amoreiras");
insert into ponto_de_retalho values ("Rosa", "Leira", "Caldas");

insert into instalada_em values (1201, 'Yamaha', 'Ezequila');
insert into instalada_em values (1202, 'Yamaha', 'Asdrubal');
insert into instalada_em values (2301, 'Ducati', 'Gertrudes');
insert into instalada_em values (2302, 'Ducati', 'Anibal');
insert into instalada_em values (3401, 'Ferrari', 'Oscar');
insert into instalada_em values (3402, 'Ferrari', 'Ildefonso');
insert into instalada_em values (3403, 'Ferrari', 'Coralia');
insert into instalada_em values (4501, 'KTM', 'Vanessa');
insert into instalada_em values (4502, 'KTM', 'Martinho');
insert into instalada_em values (5601, 'Mclaren', 'Palmira');
insert into instalada_em values (5602, 'Mclaren', 'Astride');
insert into instalada_em values (5603, 'Mclaren', 'Piedade');
insert into instalada_em values (5604, 'Mclaren', 'Rosa');

insert into retalhista values (10, "Johnny Boy");
insert into retalhista values (20, "Xalom");
insert into retalhista values (30, "Nunca da push");
insert into retalhista values (40, "Carol");
