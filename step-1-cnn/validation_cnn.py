#!/usr/bin/python

import numpy as np
from keras.models import model_from_json
import cv2
from matplotlib import pyplot as plt
import os
import shutil

def validation(dir,images,number_validations):
    # load files generated on training
    archive = open('kids.json','r')
    settingsRaioX = archive.read()
    archive.close()

    classifier = model_from_json(settingsRaioX)
    classifier.load_weights('weight_kids.h5')

    if not os.path.exists('validation-tests'):
        os.makedirs('validation-tests')
        os.makedirs('models')

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
            with open('validation-tests/' + str(number_validations) + '.txt','a') as file:
                file.write('Metric: {:.2f} - Original Class: {} - CNN: Negative\n'.format(previ[0][0],image[:-4]))
        else:
            # print('Metrica: {:.2f} - Original: {} - Classificacao: crianca'.format(previ[0][0],image))
            with open('validation-tests/' + str(number_validations) + '.txt','a') as file:
                file.write('Metric: {:.2f} - Original Class: {} - CNN: Positive\n'.format(previ[0][0],image[:-4]))
