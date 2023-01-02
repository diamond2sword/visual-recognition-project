
def to_onnx_input(pic):
	pic = normalized(pic)
	pic = with_dim_added_to(pic)
	pic = with_memory_moved_to_cpu(pic)
	pic = with_no_grad(pic)
	pic = to_numpy_array(pic)
	return pic

def get_random_labeled_pic_from_test_dataset(classLabel=None):
	labeledPicNames = get_labeled_pic_names_from_test_dataset()
	if classLabel is not None:
		labeledPicNames = get_labeled_pic_names_from_class(classLabel)
		
	numOfPicsFound = len(labeledPicNames)
	if numOfPicsFound == 0:
		raise NoInputPictureFoundError(classLabel)
	
	picName, picLabel = choice_pic_from(labeledPicNames)

	testDatasetPath = config.get_test_dataset_path()
	picPath = f"{testDatasetPath}/{picLabel}/{picName}"
	pic = open_as_pil_image(picPath)
	return [pic, picLabel]


def to_numpy_array(pic):
	pic = pic.numpy()
	pic = pic.astype(float32)
	return pic

def with_no_grad(pic):
	pic = pic.detach()
	return pic

def with_memory_moved_to_cpu(pic):
	pic = pic.cpu()
	return pic

def with_dim_added_to(pic):
	pic = pic.unsqueeze(0)
	return pic

def normalized(pic):
	normalizeTransform = Compose([
		ToTensor(),
		Normalize(
			[0.485, 0.456, 0.406],
			[0.229, 0.224, 0.225]
		)
	]) 
	pic = normalizeTransform(pic)
	return pic
   
def center_of(pic):
	width, height = pic.size
	width = min(width, height)
	picSize = config.get_pic_size()
	centerTransform = Sequential(
		CenterCrop(width),
		Resize(picSize),
	)
	pic = centerTransform(pic)
	return pic

	

def get_labeled_pic_names_from_test_dataset():
	classLabels = class_dict_manager.get_class_labels(includeAnyClass=True)
	labeledPicNames = []
	for classLabel in classLabels:
		classPicNames = get_labeled_pic_names_from_class(classLabel)
		labeledPicNames.extend(classPicNames)
	return labeledPicNames
	
def get_labeled_pic_names_from_class(classLabel):
	classLabels = class_dict_manager.get_class_labels(includeAnyClass=True)
	if classLabel not in classLabels:
		raise InvalidClassLabelError(classLabel)
	testDatasetPath = config.get_test_dataset_path()
	classPath = f"{testDatasetPath}/{classLabel}"
	picNames = get_file_names_in(classPath)
	classPicNames = map(lambda picName: [picName, classLabel], picNames)
	return classPicNames
	
	
def get_file_names_in(path):
	fileNames = listdir(path)
	return fileNames

def choice_pic_from(picNames):
	isPic = False
	picName = None
	testDatasetPath = config.get_test_dataset_path()
	
	shuffle(picNames)
	while not isPic:
		picName = picNames.pop(0)
		name, label = picName
		picPath = f"{testDatasetPath}/{label}/{name}"
		isPic = is_pic(picPath)
	return picName


def is_pic(picPath):
	isPic = True
	try:
		open_as_pil_image(picPath)
	except Exception as e:
		print(e)
		isPic = False
	return isPic


class InvalidClassLabelError(Exception):
	def __str__(self):
		errorMessage = self.__get_error_message()
		return errorMessage 
		
	def __get_error_message(self):
		classLabels = class_dict_manager.get_class_labels(includeAnyClass=True)
		testDatasetName = config.get_test_dataset_name()
		testDatasetPath = config.get_test_dataset_path()
		return f"Class \"{self.classLabel}\" does not belong to the {testDatasetName} classes, located in {testDatasetPath}: {classLabels}"
		
	def __init__(self, classLabel):
		self.classLabel = classLabel
		
   	

class NoInputPictureFoundError(Exception):
	def __str__(self):
		errorMessage = self.__get_error_message()
		return errorMessage		
		
	def __get_error_message(self):
		testDatasetName = config.get_test_dataset_name()
		testDatasetPath = config.get_test_dataset_path()
		classLabel = self.classLabel
		emphasisPhrase = "class"
		if self.classLabel is None:
			classLabel = class_dict_manager.get_random_class_label(includeAnyClass=True)
			emphasisPhrase = "class folders such as class"
		return f"There's no picture in {testDatasetName}. Please put a picture in {emphasisPhrase} {classLabel}, located in {testDatasetPath}/{classLabel}."
	
	def __init__(self, classLabel):
		self.classLabel = classLabel
			  

import config
import class_dict_manager
from torchvision.transforms import Compose, Resize, ToTensor, Normalize, CenterCrop
from torch.nn import Sequential
from numpy import float32
from random import shuffle
from PIL.Image import open as open_as_pil_image
from os import listdir
if __name__ == "__main__":
    pass
