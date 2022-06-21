#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras
import os

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
        return render_template("indexIVM.html")
    except Exception as e:
        return str(e) #Renders a page with the error.


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
        query = 'select * from evento_reposicao where num_serie=%s'
        data=(request.form["num_serie"],)
        cursor.execute(query,data)
        return render_template("seeIVMRepEv.html", cursor=cursor, params=request.form)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

@app.route('/replenishment_by_categ')
def see_repl_by_categ():
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
