# About this repository
Implementation of Haar-Cascade combined with CNN to detect children in images. CNN was used for facial classification of children in facial frames captured by Haar-Cascade.

# Dependencies
Before running these codes it should be installed:
- Python 2.7
- OpenCV 4.1.1
- Pip
After installing these packages, it's recommended to create a virtual environment. To do that just run the commands below to create and activate virtual environment:
```
$ virtualenv venv
$ source venv/bin/activate
```
Now, with active virtualenv, install dependency packages by running:
```
$ pip install -r requirements.txt
```
## Issues
If there's any issues on recognizing installed packages, try to export PYTHONPATH where your virtualenv is:
```
export PYTHONPATH=/your/path/to/venv/lib/python2.7/site-packages/
```
If exporting PYTHONPATH doesn't solve the problems, try to create __init__.py for the module as shown below:
```
cp /your/path/to/venv/lib/python2.7/site-packages/google/protobuf/__init__.py /your/path/to/venv/lib/python2.7/site-packages/google/
```
