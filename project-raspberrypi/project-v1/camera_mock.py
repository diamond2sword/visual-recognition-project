

class VideoCapture:
	def __init__(self, arg1):
		pass

	def read(self):
		isCaptured = True
		picArray = rand_array(
			low=0,
			high=255,
			size=(224, 224, 3),
			dtype=numpy.uint8
		)
		return isCaptured, picArray

	def release(self):
		pass

def request_to_display(picWindowName, pic):
	pass

def remove_pic_display(picWindowName):
	pass

def waitKey(time):
	pass


from numpy.random import randint as rand_array
import numpy
if __name__ == "__main__":
	pass
