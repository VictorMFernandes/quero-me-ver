import base64
import os

from PIL import Image

import classes.constantes as consts
from classes.detector_face import Detector_Face

class Usuario:

    def __init__(self, usu_json):
        self.id = 1 #identificar id
        self.nome = usu_json["nome"]
        self.fotos = usu_json["fotos"]
        
        self.criar_diretorios()
        self.salvar_imagens()

        df = Detector_Face()
        df.treinar_usuario(self.id)

    def criar_diretorios(self):

        raiz_usuario = consts.DIR_USU + "{}".format(self.id)
        
        if not os.path.exists(raiz_usuario):
            os.makedirs(raiz_usuario)
            os.makedirs(os.path.join(raiz_usuario, "treinamento"))

    def salvar_imagens(self):
        fotos = [
            self.fotos["normal"],
            self.fotos["sorrindo"],
            #self.fotos["direita"],
            #self.fotos["baixo"],
            #self.fotos["esquerda"]
        ]

        for i, foto in enumerate(fotos):

            arquivo = base64.b64decode(foto.split(",")[1])

            nome_arq = "{}/{}/{}.png".format(consts.DIR_USU, self.id, i)
            with open(nome_arq, 'wb') as f:
                f.write(arquivo)