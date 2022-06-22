import psycopg2
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def get_root_categs(dbConn):
    roots = []
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query_file_pre = os.path.join(basedir, 'queries/rootCategs.txt')
    query_file = open(query_file_pre,"r")
    query = query_file.read()
    query_file.close()
    cursor.execute(query)
    for row in cursor.fetchall(): 
        roots += [row[0]]
    return roots

def get_query_data_new_simple_categ(inputs,dbConn):
    input_keys = list(inputs)
    if inputs['new_categ']=='':
        raise Exception("Submissao invalida! Nova Categoria nao tem nome.")
    if 'new_categ_has_mother' not in input_keys:
        data = (inputs['new_categ'],)*2
        query_file_pre = os.path.join(basedir, 'queries/addSimplestCateg.txt')
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
    else:
        if inputs['new_categ_mother']=='':
            raise Exception("Submissao invalida! Nome da Categoria Mae nao inserido")
        data = (inputs['new_categ'],inputs['new_categ'],
        inputs['new_categ_mother'],inputs['new_categ'],)
        query_file_pre = os.path.join(basedir, 'queries/addSimpleCategWithMother.txt')
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
    return query,data

def get_query_data_from_categ_sons(categ_name,sons):
    query = "start transaction; insert into categoria values (%s); insert into super_categoria values (%s); "
    data = (categ_name,)*2
    for son in sons:
        query += "insert into tem_outra values (%s,%s); "
        data += (categ_name,son)
    return query,data

def get_query_data_new_super_categ(inputs,dbConn):
    input_keys = list(inputs)
    if inputs['new_categ']=='':
        raise Exception("Submissao invalida! Nova Categoria nao tem nome.")
    if inputs['new_categ_sons']=='':
        raise Exception("Submissao invalida! Filhos de Super Categoria não foram indicados.")
    query,data = get_query_data_from_categ_sons(inputs['new_categ'],inputs["new_categ_sons"].split(','))
    if inputs['new_categ_mother']!='':
        query += "insert into tem_outra values (%s,%s); "
        data += (inputs['new_categ'],inputs['new_categ_mother']) 
    return query,data

