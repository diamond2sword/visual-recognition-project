

def get_num_of_classes():
	classLabels = get_class_labels()
	return len(classLabels)

def get_class_dict():
	classDictPath = config.get_class_dict_path()
	classDictFile = open(classDictPath, "r")
	classDictStr = classDictFile.read()
	classDict = literal_eval(classDictStr)
	return classDict

def get_class_labels(includeAnyClass=False):
	classDict = get_class_dict()
	classLabels = list(classDict.keys())
	if includeAnyClass:
		anyClassName = config.get_any_class_name()
		classLabels.append(anyClassName)
	classLabels.sort()
	return classLabels

def get_random_class_label(includeAnyClass=False):
	classLabels = get_class_labels(includeAnyClass=includeAnyClass)
	shuffle(classLabels)
	randClassLabel = classLabels.pop(0)
	return randClassLabel

import config
from random import shuffle
from ast import literal_eval
if __name__ == "__main__":
	pass
