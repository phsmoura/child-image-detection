#!/usr/bin/python

import random
import os
import shutil

def update_number_images(image_list,percent):
    total = int(len(image_list) * percent)
    # print('total: {}'.format(total))
    return total

def create_list(num,list_images,final_list):
    k = 0
    while k < num:
        n = random.choice(list_images)
        if n not in final_list:
            final_list.append(n)
            k += 1

def move_to(path,images,x,y):
    for k in images:
        if x == 'child' and y == 'test':
        	shutil.move(path + k, 'images/2-test/child/')
        elif x == 'non-child' and y == 'test':
            shutil.move(path + k, 'images/2-test/non-child/')
        elif x == 'child' and y == 'validation':
            shutil.move(path + k, 'images/3-validation-test/child/')
        else:
            shutil.move(path + k, 'images/3-validation-test/non-child/')

def rebuild_dataset():
    path_test_child = 'images/2-test/child/'
    path_test_non_child = 'images/2-test/non-child/'
    path_validation_child = 'images/3-validation-test/child/'
    path_validation_non_child = 'images/3-validation-test/non-child/'

    path_list = [path_test_child, path_test_non_child, path_validation_child, path_validation_non_child]

    for k in range(len(path_list)):
        images = os.listdir(path_list[k])
        if k % 2 == 0:
            for p in images:
                shutil.move(path_list[k] + p, 'images/1-training/child/')
        else:
            for p in images:
                shutil.move(path_list[k] + p, 'images/1-training/non-child/')
