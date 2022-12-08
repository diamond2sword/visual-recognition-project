

def get_class_dict():
    classDictPath = get_class_dict_path()
    classDictFile = open(classDictPath, "r")
    classDictStr = classDictFile.read()
    classDict = literal_eval(classDictStr)
    return classDict

def get_class_labels(includeAnyClass=False):
    classDict = get_class_dict()
    classLabels = list(classDict.keys())
    if includeAnyClass:
        anyClassName = get_any_class_name()
        classLabels.append(anyClassName)
    classLabels.sort()
    return classLabels

def get_random_class_label(includeAnyClass=False):
    classLabels = get_class_labels(includeAnyClass=includeAnyClass)
    shuffle(classLabels)
    randClassLabel = classLabels.pop(0)
    return randClassLabel


from config import *
from random import shuffle
from ast import literal_eval
