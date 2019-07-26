#!/usr/bin/python

from build_dataset import  *
from cnn_training import  *
from validation_cnn import  *
import subprocess
import os
import shutil

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

        num_child_images = update_number_images(training_child_images,0.1)
        num_non_child_images = update_number_images(training_non_child_images,0.1)

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

    # copy result files
    os.makedirs('models/' + str(number_validations))
    shutil.move('kids.json', 'models/' + str(number_validations))
    shutil.move('weight_kids.h5', 'models/' + str(number_validations))

    rebuild_dataset()

def error_calculate(count):
    file = 'validation-tests/' + str(count) + '.txt'
    total_images = 474
    e1 = int(subprocess.check_output("grep 'Crianca' " + file + " | grep 'non-child' | wc -l", shell=True))
    e2 = int(subprocess.check_output("grep 'Nao crianca' " + file + " | grep ': child' | wc -l", shell=True))

    total_errors = e1 + e2
    total_success = total_images - total_errors
    success_percent = total_success * 100 / total_images
    error_percent = total_errors * 100 / total_images

    with open('tests-results.txt','a') as file:
        file.write("{}\t{}\t{}%\t{}\t{}%\n".format(count,total_success,success_percent,total_errors,error_percent))

    total = [total_success,total_errors]

    return total

if __name__ == '__main__':
    count = 1
    sum_success,sum_error = 0,0
    n = 100
    success_array = []
    error_array = []
    dp_suc,dp_err = 0,0

    with open('tests-results.txt','a') as file:
        file.write("Teste\tAcertos\tAcerto %\tErros\tErro %\n")

    while count <= n:
        main(count)
        total = error_calculate(count)
        success_array.append(total[0])
        error_array.append(total[1])
        count += 1

    for k in range(n):
        sum_success += success_array[k]
        sum_error += error_array[k]

    average_success = sum_success / n
    average_error = sum_error / n

    for k in range(n):
        dp_suc += (success_array[k] - average_success)**2
        dp_err += (error_array[k] - average_error)**2

    dp1 = (dp_suc / n)**(0.5)
    dp2 = (dp_err / n)**(0.5)

    with open('tests-results.txt','a') as file:
        file.write("\nMedia suc:\t{}\nMedia err:\t{}\nDesvio padrao suc:\t{:.2f}\nDesvio padrao err:\t{:.2f}\n"
        .format(average_success,average_error,dp1,dp2))
