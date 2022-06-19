from stat import FILE_ATTRIBUTE_READONLY
import numpy as np
import random as ra


###########
# CLASSES #
###########

class Produto:

    def __init__(self,ean,descr,cat):
        self.ean = ean
        self.descr = descr
        self.cat = cat

class IVM:

    def __init__(self,nserie, fabri):
        self.num_serie = nserie
        self.fabricante = fabri

class Prateleira:

    def __init__(self,nro,nserie,fabri,altura,nome):
        self.nro = nro
        self.num_serie = nserie
        self.fabricante = fabri
        self.altura = altura
        self.nome = nome

class Categoria:

    def __init__(self,nome):
        self.nome = nome

class Planograma:

    def __init__(self,ean,nro,nserie,fabri,faces,unidades,loc):
        self.ean = ean
        self.nro = nro
        self.num_serie = nserie
        self.fabricante = fabri
        self.faces = faces
        self.unidades = unidades
        self.loc = loc

    def __str__(self):
        return "({},{},{},\'{}\',{},{},\'{}\')".format(self.ean,
        self.nro,self.num_serie,self.fabricante,self.faces, self.unidades, self.loc )

    def sqlPrint(self):
        print("insert into planograma values "+str(self))



###########
# FUNCOES #
###########


def get_produto_list_from_sql_tuples(tupls):
    products = []
    for t in tupls:
        products += [Produto(t[0],t[1],t[2])]
    return products

def get_ivm_list_from_sql_tuples(tupls):
    ivms = []
    for t in tupls:
        ivms += [IVM(t[0],t[1])]
    return ivms

def get_prateleira_list_from_sql_tuples(tupls):
    ptls = []
    for t in tupls:
        ptls += [Prateleira(t[0],t[1],t[2],t[3],t[4])]
    return ptls

def get_categ_list_from_sql_tuples(tupls):
    categs = []
    for t in tupls:
        categs += [Categoria(t[0])]
    return categs


def get_planograms(prods,ivms,ptls,categs):
    faces = 3
    unidades = [5,10,15,20]
    locs = ['abc','123','cba','321']
    planograms = []
    for product in prods:
        good_prats = []
        for prateleira in ptls:
            if prateleira.nome == product.cat:
                good_prats += [prateleira]
        usable_prats = np.random.choice(good_prats, size=round(len(good_prats)*0.6), replace=False)
        for u_plat in usable_prats:
            random1, random2 = ra.randint(0,3),ra.randint(0,3)
            planograms += [
                Planograma(product.ean, u_plat.nro,
                u_plat.num_serie,u_plat.fabricante,faces,
                unidades[random1],locs[random2])
            ]
    return planograms
        



########
# DATA #
########


Produtos = [(1234567890123, 'Bolo de Cafe', 'Bolo'),
(1234567890124, 'Bolo de Laranja', 'Bolo'),
(1234567890125, 'Waffle', 'Bolo'),
(1234567890126, 'Fanta', 'Refrigerante'),
(1234567890127, 'Coca-Cola', 'Refrigerante'),
(1234567890128, 'Powerade', 'Refrigerante'),
(1234567890129, 'RedBull', 'Refrigerante'),
(1234567890130, 'Luso', 'Agua'),
(1234567890131, 'Vitalis', 'Agua'),
(1234567890132, 'Cafe', 'Bebida'),
(1234567890133, 'Tuc', 'Bolacha'),
(1234567890134, 'Bolacha Maria', 'Bolacha'),
(1234567890135, 'Maca', 'Fruta'),
(1234567890136, 'Banana', 'Fruta'),
(1234567890137, 'Batatas Lays', 'Salgado'),
(1234567890138, 'Batatas Pala-Pala', 'Salgado')]


IVMs = [(1201, 'Yamaha'),
(1202, 'Yamaha'),
(2301, 'Ducati'),
(2302, 'Ducati'),
(3401, 'Ferrari'),
(3402, 'Ferrari'),
(3403, 'Ferrari'),
(4501, 'KTM'),
(4502, 'KTM'),
(5601, 'Mclaren'),
(5602, 'Mclaren'),
(5603, 'Mclaren'),
(5604, 'Mclaren')]


Ptls = [(1, 1201, 'Yamaha', 10, 'Bolo'),
(2, 1201, 'Yamaha', 10, 'Salgado'),
(1, 2301, 'Ducati', 10, 'Bolo'),
(2, 2301, 'Ducati', 10, 'Iogurte'),
(1, 2302, 'Ducati', 10, 'Bolo'),
(2, 2302, 'Ducati', 10, 'Refrigerante'),
(1, 3401, 'Ferrari', 10, 'Bolacha'),
(2, 3401, 'Ferrari', 20, 'Agua'),
(3, 3401, 'Ferrari', 20, 'Salgado'),
(1, 3402, 'Ferrari', 10, 'Bolo'),
(2, 3402, 'Ferrari', 20, 'Agua'),
(3, 3402, 'Ferrari', 10, 'Refrigerante'),
(1, 4501, 'KTM', 10, 'Fruta'),
(2, 4501, 'KTM', 10, 'Bolacha'),
(3, 4501, 'KTM', 20, 'Salgado'),
(1, 5601, 'McLaren', 10, 'Bolo'),
(2, 5601, 'McLaren', 10, 'Bolacha'),
(1, 1202, 'Yamaha', 10, 'Bolo'),
(2, 1202, 'Yamaha', 10, 'Refrigerante'),
(3, 1201, 'Yamaha', 20, 'Salgado')]


Categs= [('Bolo'),
('Iogurte'),
('Salgado'),
('Refrigerante'),
('Agua'),
('Bolacha'),
('Fruta'),
('Doce'),
('Bebida')]



#######
# RUN #
#######

PyCategs = get_categ_list_from_sql_tuples(Categs)
PyIVMs = get_ivm_list_from_sql_tuples(IVMs)
PyPtls = get_prateleira_list_from_sql_tuples(Ptls)
PyProdutos = get_produto_list_from_sql_tuples(Produtos)

PyPlanograms = get_planograms(PyProdutos,PyIVMs,PyPtls,PyCategs)

for plano in PyPlanograms:
    plano.sqlPrint()