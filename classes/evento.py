import os
import glob
from PIL import Image

import classes.constantes as consts
from classes.detector_face import Detector_Face

class Evento:

    def __init__(self, nome_pasta):
        self.id = 1
        self.nome_ori = nome_pasta
        nome_data = self.nome_ori.split("-")

        self.titulo = nome_data[0].strip()

        dt = nome_data[1].strip().split(" ")
        self.data = "{}:{}:{}".format(dt[2], dt[1], dt[0])

        self.path_ori = consts.DIR_UPL + self.nome_ori

        self.criar_diretorios()
        self.copiar_imagens()
        
        df = Detector_Face()
        df.treinar_evento(self.id)

    def criar_diretorios(self):

        raiz_evento = "{}{}".format(consts.DIR_EVE, self.id)

        if not os.path.exists(raiz_evento):
            os.makedirs(raiz_evento)
            os.makedirs(raiz_evento + "/imagens")
            os.makedirs(raiz_evento + "/imagens_mini")
            os.makedirs(raiz_evento + "/treinamento")

    def copiar_imagens(self):
        lista_imagens = glob.glob(os.path.join(
            "{}{}".format(consts.DIR_UPL, self.nome_ori), "*JPG"))
        largura_max = 300

        for i, arquivo in enumerate(lista_imagens):

            img = Image.open(arquivo)
            porcentagem_larg = (largura_max / float(img.size[0]))
            tamanho_altura = int(
                (float(img.size[1] * float(porcentagem_larg))))
            img = img.resize((largura_max, tamanho_altura), Image.ANTIALIAS)

            img.save("{}{}/imagens_mini/{}.jpg".format(consts.DIR_EVE, self.id, i))