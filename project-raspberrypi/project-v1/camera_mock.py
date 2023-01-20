

class VideoCapture():
	def read(self):
		try:
			pic, picLabel = dataset.get_random_labeled_pic_from_test_dataset()
		except:
			pic, picLabel = self.__get_random_labeled_pic()
		isCaptured = True
		picArray = numpy.asarray(pic)
		return isCaptured, picArray

	def release(self):
		pass

	def __get_random_labeled_pic(self):
		picArray = rand_array(
			low=0,
			high=255,
			size=(224, 224, 3),
			dtype=numpy.uint8
		)
		pic = Image.fromarray(picArray)
		picLabel = class_dict_manager.get_random_class_label()
		return pic, picLabel

	def __init__(self, arg1):
		pass


def request_to_display(picWindowName, pic):
	pass

def remove_pic_display(picWindowName):
	pass

def waitKey(time):
	pass


import dataset
import class_dict_manager
import os
import numpy
from PIL import Image
from numpy.random import randint as rand_array
if __name__ == "__main__":
	pass
