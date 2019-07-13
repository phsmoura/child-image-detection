#!/usr/bin/python

from build_dataset import  *
from cnn_training import  *
from validation_cnn import  *
import subprocess

def main(number_validations):
    # building test and validation datasets
    path_child_images = 'images/1-training/child/'
    path_non_child_images = 'images/1-training/non-child/'

    for k in range(0,2):
        if k == 0:
            dataset_type = 'validation'
        else:
            dataset_type = 'test'

        training_child_images = os.listdir(path_child_images)
        training_non_child_images = os.listdir(path_non_child_images)

        num_child_images = update_number_images(training_child_images,0.15)
        num_non_child_images = update_number_images(training_non_child_images,0.15)

        child_list = []
        non_child_list = []

        create_list(num_child_images, training_child_images, child_list)
        create_list(num_non_child_images, training_non_child_images, non_child_list)

        move_to(path_child_images, child_list, 'child', dataset_type)
        move_to(path_non_child_images, non_child_list, 'non-child', dataset_type)

    # training CNN
    images_training = 'images/1-training'
    images_test = 'images/2-test'

    cnn_train(images_training,images_test)

    # cnn validation
    child_dir = 'images/3-validation-test/child/'
    non_child_dir = 'images/3-validation-test/non-child/'

    images_child = os.listdir(child_dir)
    images_non_child = os.listdir(non_child_dir)

    validation(child_dir,images_child,number_validations)
    validation(non_child_dir,images_non_child,number_validations)

    rebuild_dataset()

def error_calculate(count):
    file = 'validation-tests/' + str(count) + '.txt'
    total_images = 712
    e1 = int(subprocess.check_output("grep 'Crianca' " + file + " | grep 'non-child' | wc -l", shell=True))
    e2 = int(subprocess.check_output("grep 'Nao crianca' " + file + " | grep ': child' | wc -l", shell=True))
    total_errors = e1 + e2
    error_percent = total_errors * 100 / total_images

    print("File: {}.txt - Erro: {}%".format(count,error_percent))

if __name__ == '__main__':
    count = 1
    while count <= 30:
        # main(count)
        error_calculate(count)
        count += 1
