#!/usr/bin/python

import numpy as np
from keras.models import model_from_json
import cv2
from matplotlib import pyplot as plt
import os
import shutil

archive = open('kids.json','r')
settingsRaioX = archive.read()
archive.close()

classifier = model_from_json(settingsRaioX)
classifier.load_weights('weight_kids.h5')

def validation(dir,images):
    if not os.path.exists('validation-tests'):
        os.makedirs('validation-tests')

    if 'non-child' not in dir:
        number_validations = len(os.listdir('validation-tests/')) + 1

    for image in images:
        filename = dir + image
        oriimg = cv2.imread(filename)
        height, width, depth = oriimg.shape
        newimg = cv2.resize(oriimg,(int(150),int(150)))

        arimg= np.array([newimg])
        # print(arimg.shape)
        arimg = arimg.reshape(arimg.shape[0],150,150,3)
        arimg = arimg.astype('float32')
        arimg /= 255

        previ = classifier.predict(arimg)

        if previ[0][0] > 0.5:
            # print('Metrica: {:.2f} - Original: {} - Classificacao: Nao crianca'.format(previ[0][0],image))
            with open('validation-tests/' + number_validations + '.txt') as file:
                file.write('Metrica: {:.2f} - Classificacao Original: {} - CNN: Nao crianca\n'.format(previ[0][0],image[:-4]))
        else:
            # print('Metrica: {:.2f} - Original: {} - Classificacao: crianca'.format(previ[0][0],image))
            with open('validation-tests/' + number_validations + '.txt') as file:
                file.write('Metrica: {:.2f} - Classificacao Original: {} - CNN: Crianca\n'.format(previ[0][0],image[:-4]))
