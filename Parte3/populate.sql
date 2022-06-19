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
insert into categoria values ('Sandes');
insert into categoria values ('Batatas fritas');

insert into super_categoria values ('Doce');
insert into super_categoria values ('Bebida');
insert into super_categoria values ('Salgado');


insert into categoria_simples values ('Bolo');
insert into categoria_simples values ('Iogurte');
insert into categoria_simples values ('Refrigerante');
insert into categoria_simples values ('Agua');
insert into categoria_simples values ('Bolacha');
insert into categoria_simples values ('Fruta');
insert into categoria_simples values ('Sandes');
insert into categoria_simples values ('Batatas fritas');

insert into tem_outra values ('Doce','Bolo');
insert into tem_outra values ('Doce','Fruta');
insert into tem_outra values ('Bebida','Iogurte');
insert into tem_outra values ('Bebida','Refrigerante');
insert into tem_outra values ('Bebida','Agua');
insert into tem_outra values ('Doce','Bolacha');
insert into tem_outra values ('Salgado','Batatas fritas');
insert into tem_outra values ('Salgado','Sandes');


insert into produto values (1234567890123, 'Bolo de Cafe', 'Bolo');
insert into produto values (1234567890124, 'Bolo de Laranja', 'Bolo');
insert into produto values (1234567890125, 'Waffle', 'Bolo');
insert into produto values (1234567890126, 'Fanta', 'Refrigerante');
insert into produto values (1234567890127, 'Coca-Cola', 'Refrigerante');
insert into produto values (1234567890128, 'Powerade', 'Refrigerante');
insert into produto values (1234567890129, 'RedBull', 'Refrigerante');
insert into produto values (1234567890130, 'Luso', 'Agua');
insert into produto values (1234567890131, 'Vitalis', 'Agua');
insert into produto values (1234567890132, 'Cafe', 'Bebida');
insert into produto values (1234567890133, 'Tuc', 'Bolacha');
insert into produto values (1234567890134, 'Bolacha Maria', 'Bolacha');
insert into produto values (1234567890135, 'Maca', 'Fruta');
insert into produto values (1234567890136, 'Banana', 'Fruta');
insert into produto values (1234567890137, 'Batatas Lays', 'Salgado');
insert into produto values (1234567890138, 'Batatas Pala-Pala', 'Salgado');
insert into produto values (1234567890139, 'Pedras Limao', 'Agua');
insert into produto values (1234567890140, 'Sandes Mista', 'Sandes');
insert into produto values (1234567890141, 'Chips Ahoy', 'Bolacha');
insert into produto values (1234567890142, 'Sandes de atum', 'Sandes');
insert into produto values (1234567890143, 'Hot Dog', 'Sandes');
insert into produto values (1234567890144, 'Rissol de camarao', 'Salgado');
insert into produto values (1234567890145, 'Croquete', 'Salgado');

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

insert into instalada_em values (1201, 'Yamaha', 'Ezequiel');
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

insert into planograma values (1234567890123,1,5601,'McLaren',3,10,'cba')
insert into planograma values (1234567890123,1,3402,'Ferrari',3,10,'123')
insert into planograma values (1234567890123,1,1201,'Yamaha',3,20,'cba')
insert into planograma values (1234567890123,1,2302,'Ducati',3,20,'321')
insert into planograma values (1234567890124,1,5601,'McLaren',3,20,'321')
insert into planograma values (1234567890124,1,2302,'Ducati',3,10,'321')
insert into planograma values (1234567890124,1,3402,'Ferrari',3,5,'123')
insert into planograma values (1234567890124,1,1201,'Yamaha',3,15,'123')
insert into planograma values (1234567890125,1,1201,'Yamaha',3,5,'cba')
insert into planograma values (1234567890125,1,3402,'Ferrari',3,15,'abc')
insert into planograma values (1234567890125,1,2301,'Ducati',3,20,'abc')
insert into planograma values (1234567890125,1,2302,'Ducati',3,10,'abc')
insert into planograma values (1234567890126,2,2302,'Ducati',3,15,'321')
insert into planograma values (1234567890126,3,3402,'Ferrari',3,10,'abc')
insert into planograma values (1234567890127,2,1202,'Yamaha',3,5,'abc')
insert into planograma values (1234567890127,2,2302,'Ducati',3,5,'abc')
insert into planograma values (1234567890128,3,3402,'Ferrari',3,5,'123')
insert into planograma values (1234567890128,2,1202,'Yamaha',3,20,'abc')
insert into planograma values (1234567890129,2,2302,'Ducati',3,10,'321')
insert into planograma values (1234567890129,3,3402,'Ferrari',3,20,'cba')
insert into planograma values (1234567890130,2,3401,'Ferrari',3,20,'abc')
insert into planograma values (1234567890131,2,3402,'Ferrari',3,10,'321')
insert into planograma values (1234567890133,1,3401,'Ferrari',3,10,'abc')
insert into planograma values (1234567890133,2,4501,'KTM',3,15,'cba')
insert into planograma values (1234567890134,2,5601,'McLaren',3,5,'321')
insert into planograma values (1234567890134,2,4501,'KTM',3,10,'321')
insert into planograma values (1234567890135,1,4501,'KTM',3,15,'123')
insert into planograma values (1234567890136,1,4501,'KTM',3,20,'321')
insert into planograma values (1234567890137,3,3401,'Ferrari',3,10,'321')
insert into planograma values (1234567890137,2,1201,'Yamaha',3,20,'cba')
insert into planograma values (1234567890138,3,1201,'Yamaha',3,10,'abc')
insert into planograma values (1234567890138,2,1201,'Yamaha',3,10,'cba')