# Child Image Detection

This project was developed as an undergraduate thesis and the goal was an implementation of Haar-Cascade combined with CNN (Convolutional Neural Network) to detect children in images. CNN was used for facial classification of children in facial frames captured by Haar-Cascade.

See [Deteccao_de_criancas_em_imagens.pdf](https://github.com/phsmoura/child-image-detection/blob/master/Deteccao_de_criancas_em_imagens.pdf) to read the undergraduate thesis. All related work and concepts involving this project were explained in this document, just be aware that, aside the abstract, it was written in portuguese (PT_BR).

## Getting Started

This project was developed on an Ubuntu 20.04 LTS, but it's recommended to read the documentation of each package required to install before running the python scripts.

Install git if not present and clone this repository.

```bash
$ apt install git
$ git clone https://github.com/phsmoura/child-image-detection
```

### Prerequisites

This project requires these packages to be installed before running it:
- **Python 3**:

```bash
$ sudo apt-get install python3
```

- **Pip3**:

```bash
$ sudo apt install python3-pip
```

- **Virtualenv**:

There are some ways to install it, see [PYPI](https://virtualenv.pypa.io/en/latest/installation.html) for official documentation. If python version is **3.5+**, then it's safe to run the following command:

```bash
$ pipx install virtualenv
```

### Configuring development environment

Set a development environment with virtualenv:

```bash
$ virtualenv venv
$ source venv/bin/activate
```

Install dependency packages running the command:

```bash
$ pip3 install -r requirements.txt
```

## Running the code

This repository has 4 subdirectories and 3 steps to get it running on real cases. In fact, one of the steps is optional. The subdirectories are:
- **dataset**: here are the images that will be used to train CNN
- **step-1-cnn**: scripts to train CNN and generate models of each training
- **step-2-haarcascade**: this is an optional step and has the script to detect human faces using haar-cascade algorithm
- **step-3-final**: combined haar-cascade with CNN, this script is used in real cases

### About the Dataset

Dataset in this repository has a total of 4.755 images to carry out the training of the convolutional network, of this total 2.587 are adult face images and 2.168 are children face images. These images were extracted from 2 different datasets that are avaliable on:

- [Large Age-Gap Face Verification](http://www.ivl.disco.unimib.it/activities/large-age-gap-face-verification/)
- [KinfaceW](https://www.kinfacew.com/datasets.html)

After downloading and manualy classifing children and nonchildren, all images were scaled to a scale of 150x150 pixels and converted to gray scale. This step is necessary because the convolutional network only accepts fixed-size entries, in this case, 22,500 (150 ∗ 150) entries. In addition, the conversion to grayscale was done to decrease the number of entries. In this way, a single luminance channel (gray scale) is provided for the network.

### Execute CNN Training

After pre-processing images to build the dataset, the convolutional network can carry out the training stage. Training consists of supervised learning, using 90% of the images and the other 10% for cross-validation tests. Execute the following command to run the training, because it randonly creates the training and cross-validation images the training will be executed 100 times and to create 100 models, therefore the best model can be choosen by the success rate.

```bash
$ cd step-1-cnn
$ python main.py
```

The number of trainings can be changed at **line 79** of _"main.py"_ file. The success rate of each training is automatic calculated and registered in the file _"tests-results.txt"_.

With the training finished, the models can be found in the _"models"_ folder, the numbers folders found in this folder _"models"_ correspond to the test column in the file _"tests-results.txt"_ and inside them 2 files: _"kids.json"_ and _"weight_kids.h5"_.

### Test Haar-Cascade facial detection

This is an optional step and it was created just to see how accurate haar-cascade is, because haarcascades _".xml"_ files comes with OpenCV instalation. Empirical tests were performed with 3 types of cascades _"(haarcascade_frontalface_default.xml, haarcascade_frontalface_alt.xml, haarcascade_frontalface_alt2.xml)"_ to detect frontal face. For each cascade in the Haar-Cascade, a percentage of performance was achieved, with two of the cascades having 97% of right facial detection and one of them 98%.

For that study the following dataset were used:
- [Natural-images](https://www.kaggle.com/prasunroy/natural-images)

To reproduce this study, download this dataset, move it inside _"step-2-haarcascade"_ directory with the name _"natural_images"_ and run _"main.py"_ of this step.

```bash
$ cd step-2-haarcascade
$ python main.py
```

### CNN and Haar-Cascade combined in a real dataset

In this step, the combined algorithms are used in images containing scenes and not just faces of people. That is why **haar-cascade** is used, it aims to identify the faces of people in images, whether or not they belong to a child. With the faces identified by the **Haar-Cascade**, it is possible to use the convolutional neural network (**CNN**) to classify the faces as children or not. Identifying just one child is enough to separate that scene image into a directory containing only scenes with children, otherwise the image that don't have children is discarded. This directory can be found in _"step-3-final/kids"_.

Before running the script, copy the best model from _"step-1-cnn/models/<number of the model>/"_ to _"step-3-final"_:

```bash
$ cp -a step-1-cnn/models/<number of the model> step-3-final/model
```

Also create a directory called _"base-full"_ and put all desired imagens to find kids.

```bash
$ mkdir step-3-final/base-full
```

As done in the previous steps, run _"main.py"_ script.

```bash
$ cd step-3-final
$ python main.py
```

## Built With

* [OpenCV](https://docs.opencv.org/master/) - Open source computer vision and machine learning software library.
* [TensorFlow](https://www.tensorflow.org/guide) - End-to-End open source platform for machine learning 

## Authors

* **Pedro Moura** - [GitHub](https://github.com/phsmoura)
* **Vinicius Calil** - [GitHub](https://github.com/vcalil)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/phsmoura/child-image-detection/LICENSE.md) file for details

## Acknowledgments

This project was mentored by:
* **Guilherme Wachs** - [GitHub](https://github.com/lopespt)
