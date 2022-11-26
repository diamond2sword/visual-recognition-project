import urllib.request
import json
import ast
url = "https://raw.githubusercontent.com/diamond2sword/visual-recognition-project/main/classifiers/showClassifier/classDict.json"
path = "classDict.json"
urllib.request.urlretrieve(url, path)

classDictFile = open("classDict.json", "r")
classDictStr = classDictFile.read()
classDict = ast.literal_eval(classDictStr)

prettifiedDict = json.dumps(classDict, sort_keys = True, indent=4)
print(prettifiedDict)

#prettyClassDict = json.dumps(classDict, sort_keys = True, indent = 4)
#print(json.dumps(prettyClassDict, sort_keys = True, indent = 4))



import gdown
import os
url = "https://drive.google.com/u/0/uc?id=1-uVwlcGBqc5FNohFiocMVxnE_-DtmNfR&export=download"
outputFile = "modelWeight.pt"
if os.path.isfile(outputFile):
    shouldUpdate = 'y' == input("Update modelWeight.pt (y/n):")
    if shouldUpdate:
        gdown.download(url, outputFile)
else: gdown.download(url, outputFile)



def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

mkdir("picsFolder")
mkdir("picsFolder/anyClass")
mkdir("downloadedPictures")



import torch
from torch import nn,optim
from torchvision import transforms, models ,datasets
import numpy as np
import matplotlib.pyplot as plt
import glob
from mpl_toolkits.axes_grid1 import ImageGrid

model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)