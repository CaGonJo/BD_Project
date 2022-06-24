import numbers
from pickle import TRUE
from posixpath import split
import numpy as np
import random as ra

OG = max(200,10**3)



###########
# CLASSES #
###########

class Produto:

    def __init__(self,ean,descr,cat):
        self.ean = ean
        self.descr = descr
        self.cat = cat

    def __str__(self):
        return "({},\'{}\',\'{}\')".format(self.ean,
        self.descr,self.cat)

    def sqlStr(self):
        return ("insert into produto values "+str(self)+";\n")

class IVM:

    def __init__(self,nserie, fabri):
        self.num_serie = nserie
        self.fabricante = fabri

    def __str__(self):
        return "({},\'{}\')".format(self.num_serie,
        self.fabricante)

    def __eq__(self,other):
        return self.num_serie==other.num_serie and self.fabricante==other.fabricante

    def __lt__(self,other):
        return self.num_serie < other.num_serie

    def sqlStr(self):
        return "insert into IVM values "+str(self)+";\n"

class Prateleira:

    def __init__(self,nro,nserie,fabri,altura,nome,responsavel):
        self.nro = nro
        self.num_serie = nserie
        self.fabricante = fabri
        self.altura = altura
        self.nome = nome
        self.responsavel = responsavel

    def __str__(self):
        return "({},{},\'{}\',{},\'{}\')".format(self.nro,
        self.num_serie,self.fabricante,self.altura, self.nome)

    def sqlStr(self):
        return "insert into prateleira values "+str(self)+";\n"

class Categoria:

    def __init__(self,nome,tipo):
        self.nome = nome
        self.tipo = tipo

    def __str__(self):
        return "(\'{}\')".format(self.nome)

    def __eq__(self,other):
        return self.nome==other.nome

    def __lt__(self,other):
        return self.nome < other.nome

    def sqlStr(self):
        return "insert into {} values ".format(self.tipo)+str(self)+";\n"

class Planograma:

    def __init__(self,ean,nro,nserie,fabri,faces,unidades,loc,respon):
        self.ean = ean
        self.nro = nro
        self.num_serie = nserie
        self.fabricante = fabri
        self.faces = faces
        self.unidades = unidades
        self.loc = loc
        self.responsavel = respon

    def __str__(self):
        return "({},{},{},\'{}\',{},{},\'{}\')".format(self.ean,
        self.nro,self.num_serie,self.fabricante,self.faces, self.unidades, self.loc )

    def sqlStr(self):
        return "insert into planograma values "+str(self)+";\n"

class Retailer:

    def __init__(self,tin,nome):
        self.tin = tin
        self.nome = nome

    def __str__(self):
        return "({},\'{}\')".format(self.tin,self.nome )

    def __eq__(self,other):
        return self.tin==other.tin and self.nome==other.nome

    def __lt__(self,other):
        return self.tin < other.tin

    def sqlStr(self):
        return "insert into retalhista values "+str(self)+";\n"


class Responsavel:

    def __init__(self,categ,tin,nserie,fabri):
        self.nome_cat = categ
        self.tin = tin
        self.num_serie = nserie
        self.fabricante = fabri

    def __str__(self):
        return "(\'{}\',{},{},\'{}\')".format(self.nome_cat,self.tin,
        self.num_serie,self.fabricante)

    def sqlStr(self):
        return "insert into responsavel_por values "+str(self)+";\n"

class Ponto_de_retalho:

    def __init__(self,nome,distr,conc):
        self.nome = nome
        self.distrito = distr
        self.concelho = conc

    def __str__(self):
        return "(\'{}\',\'{}\',\'{}\')".format(self.nome,self.distrito,self.concelho)

    def sqlStr(self):
        return "insert into ponto_de_retalho values "+str(self)+";\n"

class Instalada:

    def __init__(self,nserie,fabri,nome):
        self.num_serie = nserie
        self.fabricante = fabri
        self.nome = nome

    def __str__(self):
        return "({},\'{}\',\'{}\')".format(self.num_serie,self.fabricante,self.nome)

    def sqlStr(self):
        return "insert into instalada_em values "+str(self)+";\n"

class Replenishment_Event:

    def __init__(self,ean,nro,nserie,fabri,
    inst,units,tin):
        self.ean = ean
        self.nro = nro
        self.num_serie = nserie
        self.fabricante = fabri
        self.instante = inst
        self.unidades = units
        self.tin = tin

    def __str__(self):
        return "({},{},{},\'{}\',\'{}\',{},{})".format(self.ean,self.nro,self.num_serie,
        self.fabricante,self.instante,self.unidades,self.tin)

    def sqlStr(self):
        return "insert into evento_reposicao values "+str(self)+";\n"


###########
# FUNCOES #
###########

# GENERAL #

def product_categ_is_good(prat_cat,prod_cat):
    """
    Verifica se o produto pode pertence a prateleira com base na categoria
    """
    if prat_cat==prod_cat:
        return True
    else: 
        sons_categ = get_categ_sub_categs(prat_cat)
        return prod_cat in sons_categ

# GETS #

def get_categ_sub_categs(categ_name):
    subs = []
    keys = (Super_Categs.keys())
    if categ_name in keys:
        subs += Super_Categs[categ_name]
        for el in Super_Categs[categ_name]:
            subs += get_categ_sub_categs(el)
    return subs

def get_product_abrev(categ_name):
    splitName = categ_name.split(" ")
    split_size = len(splitName)
    addStr=''
    i=0
    while i<split_size:
        addStr = addStr+splitName[i] if i==0 else addStr+splitName[i][:(min(5,len(splitName[i])))].capitalize()
        i+=1
    return addStr

def get_categorias(super_categs):
    pyCategs = []
    supers = list(super_categs.keys())
    subs = list(super_categs.values())
    subs_flat = [item for sublist in subs for item in sublist]
    all_categs = list(set(subs_flat+supers))
    for categ in all_categs:
        pyCategs += [
            Categoria(categ,'categoria')
        ]
    return pyCategs, all_categs

def get_categorias_simples(super_categs,categs_str):
    simple_cats = []
    supers = list(super_categs.keys())
    simp_categs_str = [ categ for categ in categs_str if categ not in supers]
    for sc in simp_categs_str:
        simple_cats += [
            Categoria(sc,'categoria_simples')
        ]
    return simple_cats

def get_super_categorias(super_categs):
    super_cats=[]
    for cat in super_categs:
        super_cats+= [
            Categoria(cat,'super_categoria')
        ]
    return super_cats


def get_luckys(prats,refors,ilucky,rlucky,s_categs):
    """
    Serve para ter a certeza que temos retalhistas responsaveis por todas as cat simples
    """
    for r in rlucky:
        print(r.nome,r.tin)
    heights = [10,15,20]
    ivm = 0
    for cat in s_categs:
        for ret in rlucky:
            refor = Responsavel(cat.nome,ret.tin,ilucky[ivm].num_serie,ilucky[ivm].fabricante)
            refors += [refor]
            num_prats = ra.randint(3,4)
            for i in range(num_prats):
                height  = heights[ra.randint(0,2)]
                prats += [
                    Prateleira((i+1),ilucky[ivm].num_serie,
                    ilucky[ivm].fabricante,height,cat.nome,refor)
                ]
            ivm+=1
    
    return prats,refors
    
def in_prod_categs(b):
    return b in PyProdCategsStrings

def get_prateleiras_refors(pre_ivms,categs,pre_retailers,simple_categs,retailers_simple_all=3):
    heights = [10,15,20]
    prats,refors=[],[]
    retailers_lucky = list(np.random.choice(pre_retailers,size=retailers_simple_all,replace=False))
    retailers = list(np.setdiff1d(pre_retailers,retailers_lucky))
    retailers_num = len(retailers)
    ivms_lucky = list(np.random.choice(pre_ivms,
    size=(len(simple_categs)*retailers_simple_all),replace=False))
    ivms = list(np.setdiff1d(pre_ivms,ivms_lucky))
    print(len(retailers),len(pre_retailers),len(retailers_lucky))
    for ivm in ivms:
        num_prats = ra.randint(3,5)
        num_categs=0
        while num_categs==0:
            ivm_categ = categs[ra.randint(0,(len(categs)-1))]
            ivm_sub_categs = list(filter(in_prod_categs,get_categ_sub_categs(ivm_categ.nome)))
            num_categs = len(ivm_sub_categs)
        #Responsible For
        retailer = retailers[ra.randint(0,(retailers_num-1))]
        refor = Responsavel(ivm_categ.nome,retailer.tin,ivm.num_serie,
            ivm.fabricante)
        refors += [refor]
        #Prateleiras
        for i in range(num_prats):
            height  = heights[ra.randint(0,2)]
            categ = ivm_sub_categs[(i%num_categs)]
            if not in_prod_categs(categ):
                print("ERROOOOO")
            prats += [
                Prateleira((i+1),ivm.num_serie,ivm.fabricante,height,categ,refor)
            ]
    return get_luckys(prats,refors,ivms_lucky,retailers_lucky,simple_categs)


def get_replenishment_events(planograms,refors):
    repevs = []
    num_planograms,num_refors = len(planograms), len(refors)
    dates = generate_dates()
    size = len(dates)
    for i in range(size):
        planogram = planograms[(10*(1010+i))%num_planograms] #pick a planogram
        chosen_tin = planogram.responsavel.tin
        unitss = ra.randint(5,planogram.unidades)
        repevs += [
            Replenishment_Event(planogram.ean,planogram.nro,planogram.num_serie,
            planogram.fabricante,dates[i],unitss,chosen_tin)
        ]
    return repevs



def get_planograms(prods,ivms,ptls,categs):
    num_prods, num_prats = len(prods), len(ptls)
    faces = 3
    unidades = [5,10,15,20]
    locs = ['abc','123','cba','321']
    planograms = []
    for i in range(num_prods):
        product = prods[i]
        good_prats = []
        p=(i*373)
        while len(good_prats)<15 and (p-(i*373)<num_prats):
            prateleira = ptls[p%num_prats]
            if prateleira.nome == product.cat:
                good_prats += [prateleira]
            p+=1
        usable_prats = np.random.choice(good_prats, size=round(len(good_prats)*0.6), replace=False)
        for u_plat in usable_prats:
            random1, random2 = ra.randint(0,3),ra.randint(0,3)
            if product.cat != u_plat.nome:
                print("ERRO")
            planograms += [
                Planograma(product.ean, u_plat.nro,
                u_plat.num_serie,u_plat.fabricante,faces,
                unidades[random1],locs[random2],u_plat.responsavel)
            ]
    return planograms


def get_instalada_em(ivms,prets):
    installs = []
    num_ivms = len(ivms)
    num_prets = len(prets)
    for n in range(num_ivms):
        ivm = ivms[n]
        ret = prets[((2*(2073+n))%num_prets)]
        installs += [
            Instalada(ivm.num_serie,ivm.fabricante,ret.nome)
        ]
    return installs


# GENERATES #

def generate_dates():
    dates=[]
    horas = list(range(24))
    meses = list(range(1,13))
    dias = list(range(1,29))
    inst_by_year = (12*28*24)
    years_delta = int(np.ceil(OG/inst_by_year))
    anos = list(range(2020,2020+years_delta))
    for a in anos:
        for m in meses:
            for d in dias:
                for h in horas:
                    dates += [
                        '{}-{}-{} {}:00:00'.format(a,str(m).zfill(2),str(d).zfill(2),str(h).zfill(2))
                    ]
    return dates


def generate_produtos(simple_categs,super_categs):
    produtos = []
    start_ean = 1234567890123
    categ_numb = len(simple_categs)
    prods_per_categ = round((OG*2)/categ_numb)
    numbers_needed = len(str(prods_per_categ))
    prod_categs = simple_categs+list(np.random.choice(super_categs,size=round(len(super_categs)*0.2),replace=False))
    for categ in prod_categs:
        abrev_name = get_product_abrev(categ.nome)
        i=0
        for i in range(prods_per_categ):
            produtos+=[
                Produto(start_ean,abrev_name+'_'+str(i).zfill(numbers_needed),categ.nome)
            ]
            start_ean+=1
    return produtos,prod_categs


def generate_ivms():
    ivms = []
    fabric_ivms = 10
    start = 501234
    range_num = round((1.1*OG)/10)
    numbers_needed = len(str(range_num))
    for i in range(range_num):
        for n in range(fabric_ivms):
            ivms += [
                IVM(start,'Fabr_{}'.format(str(i).zfill(numbers_needed)))
            ]
            start += 1
    return ivms  

def generate_retailers():
    i = 1
    rets = []
    range_num = round(0.1*OG) #Less retailers, so one retailer has more ivms
    numbers_needed = len(str(range_num))
    for i in range(range_num):
        rets += [
            Retailer(i,'Ret_{}'.format(str(i).zfill(numbers_needed)))
        ]
        i += 1
    return rets

def generate_ponto_de_retalho():
    i = 1
    prets = []
    range_num = round(1.3*OG)
    for i in range(range_num):
        c = ra.randint(0,9)
        d = ra.randint(0,9)
        prets += [
            Ponto_de_retalho('PR_{}'.format(str(i).zfill(6)),'Distrito_{}'.format(d),'Concelho_{}'.format(c))
        ]
    return prets


# INSERT STR #


def insert_str_tem_categoria(prods):
    out = ""
    for produto in prods:
        out+="insert into tem_categoria values ({},\'{}\');\n".format(produto.ean,produto.cat)
    return out

def insert_str_super_categ(super_categ):
    out = ""
    super_categs = list(super_categ.keys())
    for categ in super_categs:
        out+="insert into super_categoria values (\'{}\');\n".format(categ)
    return out

def insert_str_tem_outra(super_categ):
    out = ""
    super_categs = list(super_categ.keys())
    for categ in super_categs:
        for simple_categ in super_categ[categ]:
            out+="insert into tem_outra values (\'{}\',\'{}\');\n".format(categ,simple_categ)
    return out

def insert_str_Base(Base_list):
    out = ""
    for sql_object in Base_list:
        out += sql_object.sqlStr()
    return out  



########
# DATA #
########

Super_Categs = {'Doces':['Bolos','Bolachas','Frutas'],
'Bebidas':['Aguas','Iogurtes','Sumos'],
'Salgados':['Fritos','Sandes'],
'Frutas':['Frutas Verao','Frutas Inverno'],
'Iogurtes':['Iogurtes Vegan','Iogurtes Leite'],
'Sumos':['Refrigerantes','Sumos Fruta'],
'Fritos':['Fritos Caseiros','Fritos pacote'],
'Fritos pacote':['Batatas fritas','Tiras milho','Frutos secos'],
'Iogurtes Vegan':['Iogurte Soja','Iogurte Aveia','Iogurte Amendoa']}


#######
# RUN #
#######




PyCategs, Categs_Str = get_categorias(Super_Categs)
PySimpCategs = get_categorias_simples(Super_Categs,Categs_Str)
PySuperCategs = get_super_categorias(Super_Categs)
PyProdutos,PyProdCategs = generate_produtos(PySimpCategs,PySuperCategs)
PyProdCategsStrings = [el.nome for el in PyProdCategs]


PyIVMs = generate_ivms()
print("Done quarter Pys")
PyPtRet = generate_ponto_de_retalho()
PyInstalled = get_instalada_em(PyIVMs,PyPtRet)
print("Done half Pys")
PyRetailers = generate_retailers()
PyPtls, PyReFors = get_prateleiras_refors(PyIVMs,PyCategs,PyRetailers,PySimpCategs)
print("Done 3 quarters Pys")
PyPlanograms = get_planograms(PyProdutos,PyIVMs,PyPtls,PyCategs)
PyRepEvs = get_replenishment_events(PyPlanograms,PyReFors)
print("Done Pys")


file1 = open('populate2.sql', 'w')

#categoria
categ_str = insert_str_Base(PyCategs)
file1.writelines(categ_str)
file1.write("\n\n")

#categoria simples
categ_simples_str = insert_str_Base(PySimpCategs)
file1.writelines(categ_simples_str)
file1.write("\n\n")

#super categoria
categ_super_str = insert_str_Base(PySuperCategs)
file1.writelines(categ_super_str)
file1.write("\n\n")

print("Done Categs")

#tem outra
tem_outra_str = insert_str_tem_outra(Super_Categs)
file1.writelines(tem_outra_str)
file1.write("\n\n")

#produto
produto_str = insert_str_Base(PyProdutos)
file1.writelines(produto_str)
file1.write("\n\n")

print("Done Products")

#tem categoria
tem_categ_str = insert_str_tem_categoria(PyProdutos)
file1.writelines(tem_categ_str)
file1.write("\n\n")

#IVM
new_str = insert_str_Base(PyIVMs)
file1.writelines(new_str)
file1.write("\n\n")

print("Done IVMs")

#ponto de retalho
new_str = insert_str_Base(PyPtRet)
file1.writelines(new_str)
file1.write("\n\n")

#instalada em 
new_str = insert_str_Base(PyInstalled)
file1.writelines(new_str)
file1.write("\n\n")

#prateleira
new_str = insert_str_Base(PyPtls)
file1.writelines(new_str)
file1.write("\n\n")

#planograma
new_str = insert_str_Base(PyPlanograms)
file1.writelines(new_str)
file1.write("\n\n")

print("Done Planogram")


#retalhista
new_str = insert_str_Base(PyRetailers)
file1.writelines(new_str)
file1.write("\n\n")

#responsavel por
new_str = insert_str_Base(PyReFors)
file1.writelines(new_str)
file1.write("\n\n")

#replenishment
new_str = insert_str_Base(PyRepEvs)
file1.writelines(new_str)
file1.write("\n\n")



file1.close()

