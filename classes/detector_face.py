import os
import glob
import _pickle as cPickle
import dlib
import cv2
import numpy as np
import PIL
from PIL import Image
import base64

import classes.constantes as consts

class Detector_Face:

    def __init__(self):
        self.detector_face = dlib.get_frontal_face_detector()
        self.detector_pontos = dlib.shape_predictor(
            "{}dlib/shape_predictor_68_face_landmarks.dat".format(consts.DIR_REC))
        self.reconhecimento_facial = dlib.face_recognition_model_v1(
            "{}dlib/dlib_face_recognition_resnet_model_v1.dat".format(consts.DIR_REC))

        self.indice = {}
        self.idx = 0
        self.descritores_faciais = None

    def treinar_usuario(self, id_usu):
        for arquivo in glob.glob(os.path.join("{}{}".format(consts.DIR_USU, id_usu), "*.png")):
            imagem = cv2.imread(arquivo)
            
            faces_detectadas = self.detector_face(imagem, 1)
            qtd_faces_detectadas = len(faces_detectadas)

            if qtd_faces_detectadas > 1:
                print("---Há mais de uma face na imagem {}".format(arquivo))
                exit(0)
            elif qtd_faces_detectadas < 1:
                print("---Nenhuma face encontrada no arquivo {}".format(arquivo))
                exit(0)

            for face in faces_detectadas:
                pontos_faciais = self.detector_pontos(imagem, face)

                descritor_facial = self.reconhecimento_facial.compute_face_descriptor(imagem, pontos_faciais)

                lista_descritor_facial = [df for df in descritor_facial]
                np_array_descritor_facial = np.asarray(lista_descritor_facial, dtype=np.float64)
                np_array_descritor_facial = np_array_descritor_facial[np.newaxis, :]

                if self.descritores_faciais is None:
                    self.descritores_faciais = np_array_descritor_facial
                else:
                    self.descritores_faciais = np.concatenate((self.descritores_faciais, np_array_descritor_facial), axis=0)

        np.save("{}{}/treinamento/descritores.npy".format(consts.DIR_USU, id_usu), self.descritores_faciais)

    def treinar_evento(self, id_eve):

        lista_imagens = glob.glob(os.path.join("{}{}/imagens_mini".format(consts.DIR_EVE, id_eve), "*jpg"))
        qtd_imagens = len(lista_imagens)

        for i, arquivo in enumerate(lista_imagens):
            print("---Treinando imagens: {}/{}".format(i+1, qtd_imagens))
            descritores_faciais = None
            print(arquivo)
            idx_imagem = arquivo.split("\\")[1].split(".")[0]

            print(arquivo)

            imagem = cv2.imread(arquivo)
            faces_detectadas = self.detector_face(imagem, 2)

            for face in faces_detectadas:
                pontos_faciais = self.detector_pontos(imagem, face)
                descritor_facial = self.reconhecimento_facial.compute_face_descriptor(imagem, pontos_faciais)

                lista_descritor_facial = [df for df in descritor_facial]
                np_array_descritor_facial = np.asarray(lista_descritor_facial, dtype=np.float64)
                np_array_descritor_facial = np_array_descritor_facial[np.newaxis, :]

                if descritores_faciais is None:
                    descritores_faciais = np_array_descritor_facial
                else:
                    descritores_faciais = np.concatenate((descritores_faciais, np_array_descritor_facial), axis=0)

            np.save("{}{}/treinamento/descritores.{}.npy".format(consts.DIR_EVE, id_eve, idx_imagem), descritores_faciais)

    def buscar_imagens(self, id_usu, id_evento):
        descritores_usu = np.load("{}{}/treinamento/descritores.npy".format(consts.DIR_USU, id_usu))
        lista_descritores = glob.glob(os.path.join("{}{}/treinamento".format(consts.DIR_EVE, id_evento), "*npy"))
        limiar = 0.5
        resultado = []

        for i, descritor in enumerate(lista_descritores):

            descritor_eve = np.load(descritor)

            if descritor_eve.all() == None:
                continue

            for d in descritor_eve:
                distancias = np.linalg.norm(d - descritores_usu, axis=1)
                minimo = np.argmin(distancias)
                distancia_minima = distancias[minimo]

                if distancia_minima <= limiar:
                    idx_foto = descritor.split(".")[1]
                    imagem = "{}{}/imagens_mini/{}.jpg".format(consts.DIR_EVE, id_evento, idx_foto)
                    
                    with open(imagem, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read())
                    resultado.append("{}".format(encoded_string))

        return resultado
                