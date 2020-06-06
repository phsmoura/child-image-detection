#!/usr/bin/python3

import cv2
import os
import numpy as np
from keras.models import model_from_json
from matplotlib import pyplot as plt
import shutil

face_cascade = cv2.CascadeClassifier('../step-2-haarcascade/haarcascades/haarcascade_frontalface_default.xml')
face_cascade_alt = cv2.CascadeClassifier('../step-2-haarcascade/haarcascades/haarcascade_frontalface_alt.xml')
face_cascade_alt2 = cv2.CascadeClassifier('../step-2-haarcascade/haarcascades/haarcascade_frontalface_alt2.xml')
profile_cascade = cv2.CascadeClassifier('../step-2-haarcascade/haarcascades/haarcascade_profileface.xml')

archive= open('model/kids.json','r')
file_json= archive.read()
archive.close()
classifier= model_from_json(file_json)
classifier.load_weights('model/weight_kids.h5')

BASE = 'base-full/'
KID = 'images/kids/'
NOT_KID = 'images/not-kids/'
FACES = 'images/faces/'

lista_imagens = os.listdir(BASE)

def main():
	tem = []
	nao_tem = []

	for imagem in lista_imagens:
		num_rosto = 1
		img = cv2.imread(BASE + imagem)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_default = face_cascade.detectMultiScale(gray, 1.5, 5)
		face_alt = face_cascade_alt.detectMultiScale(gray, 1.5, 5)
		face_alt2 = face_cascade_alt2.detectMultiScale(gray, 1.5, 5)
		profile = profile_cascade.detectMultiScale(gray, 1.5, 5)

		lista_cascades = [face_default,face_alt,face_alt2,profile]

		for k in lista_cascades:
			for (x,y,w,h) in k:
				# print(x,y,w,h)
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				roi_gray = gray[y:y+h, x:x+w]
				roi_color = img[y:y+h, x:x+w]

				# cv2.imshow('img',roi_gray)
				# cv2.waitKey(27)

				arquivo = FACES + imagem + '-rosto' + str(num_rosto) + '.png'
				cv2.imwrite(arquivo, roi_gray)
				num_rosto += 1

				# rede neural no rosto reconhecido pelo haar
				# height, width, depth = roi_gray.shape
				newimg = cv2.resize(cv2.imread(arquivo),(int(150),int(150)))
				arimg= np.array([newimg])
				# print(arimg.shape)
				# print(len(arimg[0]))
				arimg = arimg.reshape(arimg.shape[0] ,150,150,3)
				arimg = arimg.astype('float32')
				arimg /= 255

				previ = classifier.predict(arimg)

				if previ[0][0] < 0.5 and BASE + imagem not in tem:
				    tem.append(BASE + imagem)
				    if BASE + imagem in nao_tem:
				    	nao_tem.remove(BASE + imagem)
				else:
				    if BASE + imagem not in tem and BASE + imagem not in nao_tem:
				    	nao_tem.append(BASE + imagem)

		# cv2.imshow('img',img)
		# cv2.waitKey(27)
		# cv2.destroyAllWindows()

	# print('tem: \n\n{}\n\n'.format(sorted(tem)))
	# print('nao_tem: \n\n{}\n\n'.format(sorted(nao_tem)))

	for k in tem:
		shutil.copy(k, KID)

	for k in nao_tem:
		shutil.copy(k, NOT_KID)

if __name__ == '__main__':
	dirs = ['kids','faces']
	
	if not os.path.exists('images'):
		os.makedirs('images')

	for folder in dirs:
		if not os.path.exists('images/' + folder):
			os.makedirs('images/' + folder)
			
	main()