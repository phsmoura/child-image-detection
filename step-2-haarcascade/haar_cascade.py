#!/usr/bin/python

import cv2
import os
import subprocess
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
face_cascade_alt = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
face_cascade_alt2 = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')
profile_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_profileface.xml')

BASE = 'natural_images/'

def face_detection(detect,imagem,img,gray,file):
	for (x,y,w,h) in detect:
		# print(x,y,w,h)
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]

		if 'person' in imagem:
			with open (file,'a') as f:
				f.write('Correto\t{}\n'.format(imagem))
		else:
			with open (file,'a') as f:
				f.write('Errado\t{}\n'.format(imagem))

	# cv2.imshow('img',img)
	# cv2.waitKey(27)
	# cv2.destroyAllWindows()

def error_calculation(count):
	total_images = 6899
	total_images_person = 986
	total_images_not_person = total_images - total_images_person
	list_dir = os.listdir('validation-tests')

	for dir in list_dir:
		file = 'validation-tests/{}/{}.txt'.format(dir,count)
		correct = int(subprocess.check_output("grep 'Correto' {} | wc -l".format(file), shell=True))
		wrong = int(subprocess.check_output("grep 'Errado' {} | wc -l".format(file), shell=True))

		non_face_not_detected = total_images_not_person - wrong
		face_not_detected = total_images_person - correct

		success_percent = (correct + non_face_not_detected) * 100 / total_images
		error_percent = (wrong + face_not_detected) * 100 / total_images

		with open('tests-results.txt','a') as f:
		    f.write("{}\t{}\t{}%\t{}\t{}%\n".format(dir,correct,success_percent,wrong,error_percent))

def main(lista_imagens,count):
	for imagem in lista_imagens:
		img = cv2.imread(BASE + imagem)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_default = face_cascade.detectMultiScale(gray, 1.5, 5)
		face_alt = face_cascade_alt.detectMultiScale(gray, 1.5, 5)
		face_alt2 = face_cascade_alt2.detectMultiScale(gray, 1.5, 5)
		profile = profile_cascade.detectMultiScale(gray, 1.5, 5)

		# Erro com numpy ao usar dicionario
		detect_list = [face_default,face_alt,face_alt2]
		cascade_list = ['haarcascade_frontalface_default.xml','haarcascade_frontalface_alt.xml',
		'haarcascade_frontalface_alt2.xml']

		for k in range(len(detect_list)):
			try:
				if not os.path.exists('validation-tests/{}'.format(cascade_list[k])):
					os.makedirs('validation-tests/{}'.format(cascade_list[k][:-4]))
			except OSError:
				pass

			file = 'validation-tests/{}/{}.txt'.format(cascade_list[k][:-4],count)
			face_detection(detect_list[k],imagem,img,gray,file)

		# for (x,y,w,h) in face_default:
		# 	# print(x,y,w,h)
		# 	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		# 	roi_gray = gray[y:y+h, x:x+w]
		# 	roi_color = img[y:y+h, x:x+w]
		#
		# for (x,y,w,h) in face_alt:
		# 	# print(x,y,w,h)
		# 	cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
		# 	roi_gray = gray[y:y+h, x:x+w]
		# 	roi_color = img[y:y+h, x:x+w]
		#
		# for (x,y,w,h) in face_alt2:
		# 	# print(x,y,w,h)
		# 	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
		# 	roi_gray = gray[y:y+h, x:x+w]
		# 	roi_color = img[y:y+h, x:x+w]
		#
		# for (x,y,w,h) in profile:
		# 	cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		# 	roi_gray = gray[y:y+h, x:x+w]
		# 	roi_color = img[y:y+h, x:x+w]

		# cv2.imshow('img',img)
		# cv2.waitKey(27)
		# cv2.destroyAllWindows()

if __name__ == '__main__':
	lista_imagens = os.listdir(BASE)
	count = 1

	if not os.path.exists('validation-tests'):
		os.makedirs('validation-tests')

	if not os.path.exists('tests-results.txt'):
		with open('tests-results.txt','a') as file:
			file.write("Cascata\tAcertos\tAcertos %\tErros\tErros %\n")

	while count <= 100:
		main(lista_imagens,count)
		error_calculation(count)
		count += 1
