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
    foreign key(cat) references categoria(nome)
);

create table tem_categoria (
    ean     numeric(13, 0),
    cat     varchar(50),
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
    instante    timestamp NOT NULL, --CHECK (instante >= 0),
    unidades    integer NOT NULL CHECK (unidades > 0),
    tin     integer,
    foreign key(ean, nro, num_serie, fabricante) references planograma,
    foreign key(tin) references retalhista,
    primary key(ean, nro, num_serie, fabricante, instante)
);





