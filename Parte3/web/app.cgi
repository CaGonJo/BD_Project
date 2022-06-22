#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras
import os

from aux_scripts import *

# SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist195749"
DB_DATABASE=DB_USER
DB_PASSWORD="ola"
DB_CONNECTION_STRING = "host={} dbname={} user={} password={}".format(DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
@app.route('/')
def main_page():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e) #Renders a page with the error.


# Exerc 1 #################################################

@app.route('/get_remove_categ')
def remove_categ_page():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'select nome from categoria'
        cursor.execute(query)
        return render_template("getRemoveCateg.html",cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/get_insert_categ')
def insert_categ_page():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'select nome from categoria'
        cursor.execute(query)
        return render_template("getInsertCateg.html",cursor=cursor,params=request.args)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/insert_simple_categ', methods=["POST"])
def insert_categ():
    dbConn=None
    cursor=None
    try:
        success = 1
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query,data = get_query_data_new_simple_categ(request.form,dbConn)
        cursor.execute(query,data)
        return render_template("success.html")
    except Exception as e:
        success = 0
        return render_template("error.html",msg_err=e)
    finally:
        if success:
            cursor.execute("commit;")
        else: 
            cursor.execute("rollback;")
        cursor.close()
        dbConn.close()

@app.route('/insert_super_categ', methods=["POST"])
def insert_categ():
    dbConn=None
    cursor=None
    try:
        success = 1
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query,data = get_query_data_new_super_categ(request.form,dbConn)
        cursor.execute(query,data)
        return render_template("success.html")
    except Exception as e:
        success = 0
        return render_template("error.html",msg_err=e)
    finally:
        if success:
            cursor.execute("commit;")
        else: 
            cursor.execute("rollback;")
        cursor.close()
        dbConn.close()

@app.route('/remove_categ', methods=["POST"])
def remove_categ():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        data = (request.form['remove_categ_name'],)
        query_file_pre = os.path.join(basedir, "queries/QC2.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        cursor.execute(query,data)
        return render_template("insertCategResult.html", ola=query)
    except Exception as e:
        return render_template("error.html",msg_err=e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


# Exerc 2 #################################################


@app.route('/get_insert_ret')
def get_insert_categ():
    try:
        return render_template("getInsertRet.html")
    except Exception as e:
        return str(e)


@app.route('/get_remove_ret')
def get_remove_categ():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'select tin from retalhista limit 10'
        cursor.execute(query)
        return render_template("getRemoveRet.html",cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/remove_ret', methods=["POST"])
def remove_ret():
    dbConn=None
    cursor=None
    try:
        success=1
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query_file_pre = os.path.join(basedir, "queries/remRet.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        data=(int(request.form["remove_ret_tin"]),)*3
        cursor.execute(query,data)
        return render_template("success.html")
    except Exception as e:
        success = 0
        return render_template("error.html",msg_err=e)
    finally:
        if success:
            cursor.execute("commit;")
        else: 
            cursor.execute("rollback;")
        cursor.close()
        dbConn.close()


@app.route('/insert_ret', methods=["POST"])
def insert_ret():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query_file_pre = os.path.join(basedir, "queries/Q2Insert.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        data=(request.form["insert_ret_tin"],)
        cursor.execute(query,data)
        return render_template("erroSubmition.html", cursor=cursor, params=request.form)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()



# Exerc 3 #################################################

@app.route('/replenishment_events')
def choose_ivm():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query_file_pre = os.path.join(basedir, "queries/getHighReplIVM.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        cursor.execute(query)
        return render_template("replenishmentIVM.html", cursor=cursor, params=request.args)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/see_ivm_repl_evs', methods=["POST"])
def see_ivm_replenishment_events():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query_file_pre = os.path.join(basedir, "queries/QC2.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        data=(request.form["num_serie"],)
        cursor.execute(query,data)
        return render_template("seeRepByCateg.html", cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

# Exerc 4 #################################################

@app.route('/cat_sub_cats')
def choose_super_categ():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = 'select nome from categoria'
        cursor.execute(query)
        return render_template("catSubCatsIVM.html",cursor=cursor,params=request.args)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/see_cat_sub_cats', methods=["POST"])
def see_cat_sub_cats():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query_file_pre = os.path.join(basedir, "queries/QD.txt")
        query_file = open(query_file_pre,"r")
        query = query_file.read()
        query_file.close()
        data=(request.form["categ_name"],)
        cursor.execute(query,data)
        return render_template("seeCatSubCats.html", cursor=cursor, params=request.form)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


CGIHandler().run(app)
