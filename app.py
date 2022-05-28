import os

import pymongo
from flask import Flask, redirect, render_template, request

MONGODB_URL = os.getenv('MONGODB_URL', 'localhost')

myclient = pymongo.MongoClient(MONGODB_URL)

mydb = myclient["aluno"]
mycol = mydb["teste"]

dados = {}

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/incluir")
def pagina_incluir():
    return render_template('incluir.html')



@app.post("/salvadados")
def salva():
    nome = request.form.get("nome")
    dados["nome"] = nome
    if "_id" in dados:
        dados.pop("_id")
    x = mycol.insert_one(dados)
    return f"<p style='color: red;' >dados inseridos {x.inserted_id}<p><a href='/'>Retornar</a>"


@app.route('/listar')
def listar():
    # procura={}
    #procura["nome"] = "manoel"
    #dados =  mycol.find(procura)
    dados = mycol.find()
    return render_template('listar.html', dados=dados)


@app.route('/apaga/<id>')
def apagar(id):
    apaga = {}
    apaga["nome"] = id
    x = mycol.delete_one(apaga)
    return f"<p>o id {id} foi removido <p><a href='/'>Retornar</a>"
