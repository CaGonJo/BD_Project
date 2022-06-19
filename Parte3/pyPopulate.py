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

    def __str__(self):
        return "({},{},\'{}\',{},\'{}\')".format(self.nro,
        self.num_serie,self.fabricante,self.altura, self.nome)

    def sqlPrint(self):
        print("insert into prateleira values "+str(self))

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

class Retailer:

    def __init__(self,tin,nome):
        self.tin = tin
        self.nome = nome


class Responsavel:

    def __init__(self,categ,tin,nserie,fabri):
        self.nome_cat = categ
        self.tin = tin
        self.num_serie = nserie
        self.fabricante = fabri




###########
# FUNCOES #
###########

# GETS #

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

def get_retailer_list_from_sql_tuples(tupls):
    rets = []
    for t in tupls:
        rets += [Retailer(t[0],t[1])]
    return rets

def get_prateleiras_refors(ivms,super_categs,simple_categs,retailers):
    heights = [10,15,20]
    prats,refors=[],[]
    retailers_num = len(retailers)
    for ivm in ivms:
        num_prats = ra.randint(3,5)
        ivm_categ = super_categs.keys[ra.randint(0,2)]
        ivm_sub_categs = super_categs[ivm_categ]
        num_categs = len(ivm_sub_categs)
        for i in range(num_prats):
            height  = heights[ra.randint(0,2)]
            categ = ivm_sub_categs[(i%num_categs)]
            prats += [
                Prateleira((i+1),ivm.num_serie,ivm.fabricante,height,categ)
            ]
        retailer = retailers[ra.randint(0,(retailers_num-1))]
        refors += [
            Responsavel(ivm_categ,retailer.tin,ivm.num_serie,
            ivm.fabricante)
        ]
    return prats, refors



def get_tem_categoria(prods):
    for produto in prods:
        print("insert into tem_categoria values ({},\'{}\')".format(produto.ean,produto.cat))

def get_produtos(prods):
    for produto in prods:
        print("insert into produto values ({},\'{}\',\'{}\')".format(product.ean,product.descr,product.categ))

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


# GENERATES #

SuperMercados = ['Pingo Doce','Continente','Lidl','Aldi','PorSi',
'Dia','Mercadona','Carefour']
Frutas = ['Manga','Limao','Maracuja','Laranja','Ananas','Banana',
    'Maca','Abacaxi','Cenoura','Cereja','Morango','Frutos Vermelhos','Framboesa']

def generate_salgados(start_ean):
    #Fritos
    fritos=[]
    Marcas = ['Lays','Ruffles','Pala-pala','Pringles'] + SuperMercados
    Sabores = ['Presunto','Camponesa','Ketchup','Queijo','Tradicionais',
    'Picantes','Pimentos','']
    Pesos = ['150g','250g','400g','500g']
    for m in Marcas:
        for s in Sabores:
            for p in Pesos:
                fritos += [
                    Produto(start_ean,'Batatas {} {} {}'.format(m,s,p),'Fritos')
                ]
                start_ean+=1

    #Sandes
    sandes = []
    Tipos = ['Croissant','Pao de Mafra','Pao Integral','Pao Centeio',
    'Pao Trigo','Baguete','Pao de Forma','Pao com Sementes','Brioche']
    Condimentos = ['Manteiga','Fiambre','Queijo','Atun','Salmao',
    'Milho','Azeitonas','Doce de Morango','Marmelada','Doce de Laranja','Goiabada']
    for t in Tipos:
        for c in Condimentos:
            sandes = [
                Produto(start_ean,'{} com {}'.format(t,c),'Sandes')
            ]
            start_ean+=1
    return fritos + sandes

def generate_bebidas(start_ean):
    #Aguas
    aguas = []
    Marcas = ['Vitalis','Pedras','Luso','Penacova','Vimeiro',
    'Frize']+SuperMercados
    Sabor = ['Natural']+Frutas
    Gas = ['Com Gas', 'Sem Gas']
    Quantidade = ['0.33cl','0.5cl','0.75cl']
    for m in Marcas:
        for s in Sabor:
            for g in Gas:
                for q in Quantidade:
                    aguas += [
                        Produto(start_ean,'Agua {} {} {} {}'.format(m,s,g,q),
                        'Agua')
                    ]
                    start_ean += 1
    #Iogurtes
    iog = []
    Marcas = ['Danone','Nestle','Alpro','Mimosa','Vigor']+SuperMercados
    Sabor = Frutas + ['Bolacha','Acucarado','Natural']
    for m in Marcas:
        for s in Sabor:
            for q in Quantidade:
                iog += [
                    Produto(start_ean,'Iogurte {} {} {}'.format(m,s,q),'Iogurte')
                ]
                start_ean += 1
    #Rerigerantes
    refri = []
    Marcas = SuperMercados+['Powerade','Gatorade','Redbull','Lipton','Nestea',
    'Sumol','B!','Brisa','Compal']
    for m in Marcas:
        for f in Frutas:
            for q in Quantidade:
                refri += [
                    Produto(start_ean,'{} {} {}'.format(m,f,q),'Refrigerante')
                ]
                start_ean += 1
    refri += [Produto(start_ean,'Coca-Cola','Refrigerante')]    #mega rare
    return iog+refri+aguas


def generate_doces(start_ean):
    #Bolos
    bolos = []



def generate_products():
    
        



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
(1234567890137, 'Batatas Lays', 'Batatas fritas'),
(1234567890138, 'Batatas Pala-Pala', 'Batatas fritas'),
(1234567890139, 'Pedras Limao', 'Agua'),
(1234567890140, 'Sandes Mista', 'Sandes'),
(1234567890141, 'Chips Ahoy', 'Bolacha'),
(1234567890142, 'Sandes de atum', 'Sandes'),
(1234567890143, 'Hot Dog', 'Sandes'),
]


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


Categs= [('Bolo'),
('Iogurte'),
('Salgado'),
('Refrigerante'),
('Agua'),
('Bolacha'),
('Fruta'),
('Doce'),
('Bebida'),
('Sandes'),
('Batatas fritas')]

Super_Categs = {'Doce':['Bolo','Bolacha','Fruta'],
'Bebida':['Agua','Iogurte','Refrigerante'],
'Salgado':['Fritos','Sandes']}

Simple_Categs = {
    'Bolo':'Doce',
    'Bolacha':'Doce',
    'Fruta':'Doce',
    'Agua':'Bebida',
    'Iogurte':'Bebida',
    'Refrigerante':'Bebida',
    'Fritos':'Salgado',
    'Sandes':'Salgado'
}


#######
# RUN #
#######

PyCategs = get_categ_list_from_sql_tuples(Categs)
PyIVMs = get_ivm_list_from_sql_tuples(IVMs)
PyProdutos = get_produto_list_from_sql_tuples(Produtos)
PyRetailers = get_retailer_list_from_sql_tuples(Retailers)

PyPtls, PyReFors = get_prateleiras_refors(PyIVMs,Super_Categs,Simple_Categs,PyRetailers)
PyPlanograms = get_planograms(PyProdutos,PyIVMs,PyPtls,PyCategs)

for plano in PyPlanograms:
    plano.sqlPrint()