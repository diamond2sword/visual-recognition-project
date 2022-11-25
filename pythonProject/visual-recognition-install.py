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

picsFolder = "picsFolder"
mkdir(picsFolder)

import torch
from torch import nn,optim
from torchvision import transforms, models ,datasets
import numpy as np
import matplotlib.pyplot as plt
import glob
from mpl_toolkits.axes_grid1 import ImageGrid

model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)