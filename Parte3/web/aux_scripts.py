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

def get_query_data_new_categ(inputs,dbConn):
    input_keys = list(inputs)
    query=''
    if 'new_categ' not in input_keys:
        raise Exception("Submissao invalida! Nova Categoria nao tem nome.")
    categ_name = inputs['new_categ']
    if 'new_categ_is_root' in input_keys:            # Categoria Raiz
        root_categs = get_root_categs(dbConn)
        for root in root_categs:
            query+="insert into tem_outra values (%s,'"+str(root)+"'); "
        query = """
        start transaction;
        insert into categoria values (%s);
        insert into super_categoria values (%s);
        """ + query + """
        """
        data = (categ_name,)*(2+len(root_categs)) 
    elif 'new_categ_has_mother' not in input_keys:           # Uma das Cat Raiz
        query = """
        start transaction;
        insert into categoria values (%s);
        insert into categoria_simples values (%s);
        """
        data = (categ_name,)*2
    else:                               # Nova Cat Simples que não é Raiz
        query = """
        start transaction;
        insert into categoria values (%s);
        insert into categoria_simples values (%s);
        insert into tem_outra values (%s,%s);
        """
        if 'new_categ_mother' not in input_keys:
            raise Exception("Submissao invalida")
        data = (categ_name,categ_name,inputs['new_categ_mother'],categ_name)
    return query,data,0