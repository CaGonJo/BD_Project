#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

import psycopg2
import psycopg2.extras

# SGBD configs
DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist195749"
DB_DATABASE=DB_USER
DB_PASSWORD="ola"
DB_CONNECTION_STRING = "host={} dbname={} user={} password={}".format(DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


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
    try:
        return render_template("replenishmentIVM.html", params=request.args)
    except Exception as e:
        return str(e)

@app.route('/seeIVMReplEv', methods=["POST"])
def see_ivm_replenishment_events():
    dbConn=None
    cursor=None
    try:
        dbConn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        ivm_num_serie=int(request.form["num_serie"])
        query = 'select * from evento_reposicao where num_serie={}'.format(ivm_num_serie)
        cursor.execute(query)
        return render_template("seeIVMRepEv.html", cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()

# Exerc 4 #################################################

@app.route('/replenishment_events')
def choose_ivm():
    try:
        return render_template("replenishmentIVM.html", params=request.args)
    except Exception as e:
        return str(e)


CGIHandler().run(app)
