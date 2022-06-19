from stat import FILE_ATTRIBUTE_READONLY
import numpy as np
import pandas as pd


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
    ivms = []
    for t in tupls:
        ivms += [IVM(t[0],t[1])]
    return ivms


