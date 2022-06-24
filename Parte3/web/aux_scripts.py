import psycopg2
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def get_query_data_new_simple_categ(inputs,dbConn):
    input_keys = list(inputs)
    if inputs['new_categ']=='':
        raise Exception("Submissao invalida! Nova Categoria nao tem nome.")
    query = "start transaction; insert into categoria values (%s); insert into categoria_simples values (%s); "
    data = (inputs['new_categ'],)*2
    if 'new_categ_has_mother' in input_keys:
        if inputs['new_categ_mother']=='':
            raise Exception("Submissao invalida! Nome da Categoria Mae nao inserido")
        if not_super_categ(inputs['new_categ_mother'],dbConn):
            query += "insert into super_categoria values (%s); "
            data += (inputs['new_categ_mother'],)  
        query += "insert into tem_outra values (%s,%s); "
        data += (inputs['new_categ_mother'],inputs['new_categ'],)
    return query,data

def get_query_data_from_categ_sons(categ_name,sons):
    query = "start transaction; insert into categoria values (%s); insert into super_categoria values (%s); "
    data = (categ_name,)*2
    for son in sons:
        query += "insert into tem_outra values (%s,%s); "
        data += (categ_name,son)
    return query,data

def not_super_categ(categ_mother,dbConn):
    super_cats = []
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "select * from super_categoria"
    cursor.execute(query)
    for row in cursor.fetchall(): 
        super_cats += [row[0]]
    return categ_mother not in super_cats


def get_query_data_new_super_categ(inputs,dbConn):
    input_keys = list(inputs)
    if inputs['new_categ']=='':
        raise Exception("Submissao invalida! Nova Categoria nao tem nome.")
    if inputs['new_categ_sons']=='':
        raise Exception("Submissao invalida! Filhos de Super Categoria não foram indicados.")
    query,data = get_query_data_from_categ_sons(inputs['new_categ'],inputs["new_categ_sons"].split(','))
    if inputs['new_categ_mother']!='':
        if not_super_categ(inputs['new_categ_mother'],dbConn):
            raise Exception("Submissao invalida! Categoria Mae ({}) nao pode ser Categoria Simples".format(inputs['new_categ_mother']))
        query += "insert into tem_outra values (%s,%s); "
        data += (inputs['new_categ_mother'],inputs['new_categ'])
    return query,data


def get_categ_sub_categs(categ,cursor):
    sub_cats = []
    check_cats = [categ]
    cursor.execute("start transaction;")
    while len(check_cats)!=0:
        query = "select cat from tem_outra where super_cat=%s"
        range_size = len(check_cats)-1 #-1, pq ja adicionamos a primeira na linha de cima
        for i in range(range_size):
            query += " or super_cat=%s"
        query += '; '
        cursor.execute(query,tuple(check_cats))
        check_cats=[]
        for sub in cursor.fetchall(): 
            sub_cats+=[sub[0]]
            check_cats += [sub[0]]
    return sub_cats

def is_categ_simple(categ,cursor):
    cursor.execute("select * from categoria where nome=%s;",(categ,))
    if cursor.fetchall() == []:
        return False
    cursor.execute("select * from tem_outra where super_cat=%s;",(categ,))
    sub_cats = []
    for sub in cursor.fetchall(): 
        sub_cats+=[sub[0]]
    return sub_cats==[]
