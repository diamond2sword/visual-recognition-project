classes = ["Mr-Bean", "Kurzgesagt", "TimersRus"]
num_classes = len(classes)
classes.sort() #important

class_dict = {i : classes[i] for i in range(num_classes)}
print(class_dict)



#import needed libraries
import torch
from torch import nn,optim
from torchvision import transforms, models ,datasets
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import glob
from mpl_toolkits.axes_grid1 import ImageGrid


# choose a pretrained model to start with check options here: https://pytorch.org/vision/stable/models.html
model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)

# Freeze parameters of the tarined network
for param in model.parameters():
    param.requires_grad = False

# print the model to check the classifer and change it
print(model.classifier)

# define new classifier and append it to network but remember to have a 29-neuron output layer for our two classes.
model.classifier= nn.Sequential(nn.Dropout(p=0.6, inplace=False),
                                nn.Linear(in_features=1280, out_features=len(classes), bias=True),
                                nn.LogSoftmax(dim=1))

# ## unlock last three blocks before the classifier(last layer).
for p in model.features[-1].parameters():
    p.requires_grad = True

# choose your loss function
criterion = nn.NLLLoss()

#print the classifier now
print(model.classifier)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)




import os

model.load_state_dict(torch.load("modelWeight.pt"))
#turn model to evaluation mode
model.eval()

picsPath = "picsFolder"
picNameList = os.listdir(picsPath)

if len(picNameList) == 0:
    print("please put input picture to folder \"picsFolder/anyClass\"")
else:
    #load some of the test data
    testSet = datasets.ImageFolder(picsPath,transforms.Compose([transforms.ToTensor()]))
    testLoader = torch.utils.data.DataLoader(testSet, batch_size=1,shuffle=True)

    loaderIterator = iter(testLoader)
    for i in range(len(loaderIterator)):
        pictures, labels = next(loaderIterator)
        picture = pictures[0]
        label = labels[0]
        # show choosed image
        t = transforms.ToPILImage()
        plt.imshow(t(picture))
        plt.show()

        # normalize image as in the training data
        t_n=transforms.Normalize([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
        picture = t_n(picture).unsqueeze(0)

        # classify image using our model
        result = torch.exp(model(picture))

        print(f"image number {i}")
        print("---------------------")

        # print real class
        print("label: anyClass")

        # print predicted class
        print("prediction:", class_dict[result.argmax().item()])







