
from urllib.request import *
import numpy as np
import cv2
import os

def downloadNegativas():
    # link_imagens_negativas = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    link_imagens_negativas = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n02960352'
    urls_imagens_negativas = urlopen(link_imagens_negativas).read().decode()

    if not os.path.exists('negativas'):
        os.makedirs('negativas')

    numero_imagem = 1

    for i in urls_imagens_negativas.splitlines():
        print(i)
        urlretrieve(i, "negativas/" + str(numero_imagem) + ".jpg")
        img = cv2.imread("negativas/" + str(numero_imagem) + ".jpg", cv2.IMREAD_GRAYSCALE)
        img = cv2.imread("negativas/" + str(numero_imagem) + ".jpg")
        imagem_redimensionada = cv2.resize(img, (150, 150))
        cv2.imwrite("negativas/" + str(numero_imagem) + ".jpg", imagem_redimensionada)
        numero_imagem += 1


def removeFalhas():
    for file_type in ['negativas']:
        for img in os.listdir(file_type):
            for feia in os.listdir('feias'):
                try:
                    caminho_imagem = str(file_type) + '/' + str(img)
                    feia = cv2.imread('feias/' + str(feia))
                    pergunta = cv2.imread(caminho_imagem)

                    if feia.shape == pergunta.shape and not(np.bitwise_xor(feia, pergunta).any()):
                        print('Apagando imagem feia!')
                        print(caminho_imagem)
                        os.remove(caminho_imagem)

                except Exception as e:
                    print(str(e))


def geraListaNegativa():
    for file_type in ['negativas']:
        for img in os.listdir(file_type):
            if file_type == 'negativas':
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)

            elif file_type == 'positivas':
                line = file_type + '/' + img + ' 1 0 0 150 150\n'
                with open('info.dat', 'a') as f:
                    f.write(line)

    print("Gerado lista no arquivo: bg.txt\n")


def renomeiaImagens():
    for i, f in enumerate(os.listdir(".")):
        f_new = '{}.jpg'.format(i)
        os.rename(f, f_new)
        print ('{}.'.format(i), f, '->', f_new)


downloadNegativas()
removeFalhas()
# geraListaNegativa()
# renomeiaImagens()
