from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS, cross_origin

import os

import classes.constantes as consts
from classes.usuario import Usuario
from classes.evento import Evento
from classes.detector_face import Detector_Face

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/queromever/api/v1.0/usuario", methods=["POST"])
def criar_usuario():
    if not request.json or not 'nome' in request.json:
        abort(400)

    usuario = {
        "nome": request.json["nome"],
        "fotos": request.json["fotos"]
    }

    usu = Usuario(usuario)

    resposta = jsonify({"task": usuario})
    return resposta, 201

@app.route("/queromever/api/v1.0/testar", methods=["POST"])
def testar():
    teste = {
        "testar": request.json["testar"]
    }
    resposta = jsonify(teste)

    return resposta, 201

@app.route("/", methods=["POST"])
def testar():
    resposta = jsonify("teste")

    return resposta, 201
    

@app.route("/queromever/api/v1.0/fotos/<int:id_usu>", methods=["GET"])
def buscar_fotos(id_usu):

    df = Detector_Face()
    resultado = df.buscar_imagens(id_usu, 1)

    resposta = jsonify({"imagens": resultado})
    return resposta

@app.route("/queromever/api/v1.0/eventos", methods=["GET"])
def treinar_eventos():

    for pasta in os.listdir(consts.DIR_UPL):
        eve = Evento(pasta)

    resposta = jsonify({"Foi": "resultado"})
    return resposta

if __name__ == '__main__':
    app.run(debug=True)
