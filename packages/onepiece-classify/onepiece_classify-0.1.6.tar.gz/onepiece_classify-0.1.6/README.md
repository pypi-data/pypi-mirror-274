# Machine Learning Project Documentation

## Project Overview
This repository contains programs for classifying images. The images used for this project are images of Onepiece anime characters. There are 18 predicted anime characters. This project is packaged in the form of a python package so that it can be used by the public.

## Installation Guide
### Requirements
It is recommended to run this application within a virtual environment. First thing first is clone the repository

```sh
git clone https://github.com/lombokai/onepiece-classifier.git
```
### Virtual Environment Setup
create a virtual environment

```sh
python3 -m venv <virtual environment name>
```

command line to activate your virtual environment in linux
```sh
source <virtual environment name>/bin/activate
```

command line to activate your virtual environment in windows
```sh
<virtual environment name>\Scripts\activate
```

install package requirements
```sh
pip install -r requirements/main.txt
```

## Usage
### Example Usage
This package provide image to predict in `assets` directory. If you want to try predict an image, run predict.py script with command bellow
```
python3 predict.py <image path>
```

command example if you are working in parent directory of this repo

```sh
python3 predict.py assets/luffy.png
```

try to predict different image with command above

### Run the Application
install onepiece-classify package
```sh
pip install onepiece-classify
```

acces predict method from onepiece-classify pakcage

```python
from onepiece_classify.infer import ImageRecognition
```

instantiate the class with your model path. Download trained model [here](https://drive.google.com/file/d/1M1-1Hs198XDD6Xx-kSWLThv1elZBzJ0j/view?usp=sharing) and make sure you specify model path parameter in the location of downloaded model

```python
predictor = ImageRecognition(<model path>)
```

then you just predict your image with `predict` method
```python
predictor.predict(<your image path>)
```


## Data Description
### Data Sources
Data obtained from Kaggle [here](https://www.kaggle.com/datasets/ibrahimserouis99/one-piece-image-classifie). The data contains a collection of 18 onepiece character images, and is saved in jpg, jpeg and png formats.

## Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)