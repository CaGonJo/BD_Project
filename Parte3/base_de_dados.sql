create table categoria (
    nome    varchar(50),
    primary key(nome)
);

create table categoria_simples (
    nome    varchar(50),
    foreign key(nome) references categoria(nome),
    primary key(nome)
);

create table super_categoria (
    nome    varchar(50),
    foreign key(nome) references categoria(nome),
    primary key(nome)
);

create table tem_outra (
    nome_super_cat  varchar(50),
    nome_cat    varchar(50),
    foreign key(nome_super_cat) references super_categoria(nome),
    foreign key(nome_cat) references categoria(nome),
    primary key(nome_cat)
);

create table produto (
    ean     numeric(13, 0),
    descr   varchar(255),
    cat     varchar(50),
    primary key(ean),
    foreign key(cat) references categoria(nome)
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
    primary key(nome);
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
    foreign key(nome) references(categoria),
    foreign key(num_serie, fabricante) references(IVM),
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
    foreign key(ean) references(produto),
    foreign key(nro, num_serie, fabricante) references(prateleira),
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
    foreign key(num_serie, fabricante) references(IVM),
    foreign key(tin) references(retalhista),
    foreign key(nome_cat) references(categoria),
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
    foreign key(ean, nro, num_serie, fabricante) references(planograma),
    foreign key(tin) references(retalhista),
    primary key(ean, nro, num_serie, fabricante, instante),
);

----------------------------------------
-- Populate Relations 
----------------------------------------
insert into categoria values ('Bolo');
insert into categoria values ('Iogurte');
insert into categoria values ('Salgado');
insert into categoria values ('Refrigerante');
insert into categoria values ('Água');
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
insert into categoria_simples values ('Água');
insert into categoria_simples values ('Bolacha');
insert into categoria_simples values ('Fruta');

insert into produto values (01234567890123, 'Bolo de Café', 'Bolo');
insert into produto values (01234567890124, 'Fanta', 'Refrigerante');
insert into produto values (01234567890125, 'Luso', 'Água');
insert into produto values (01234567890126, 'Café', 'Bebida');

insert into IVM values (1234, 'Repsol');
insert into IVM values (2222, 'Empresa A');
insert into IVM values (33, 'RNL');
insert into IVM values (456, 'Diferencial');
insert into IVM values (1, 'Sinfo');
insert into IVM values (958, 'David Matos');

insert into ponto_de_retalho values ("Ezequiel", "Faro", "Sé");
insert into ponto_de_retalho values ("Ajdrúbal", "Santarém", "Almeirim");
insert into ponto_de_retalho values ("Gertrudes", "Lisboa", "Arroios");

insert into retalhista values (10, "Johnny Boy");
insert into retalhista values (20, "Xalom");
insert into retalhista values (30, "Nunca dá push");
insert into retalhista values (40, "Carol");
