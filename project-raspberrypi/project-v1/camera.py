

def preview_until(time=None, key=None):
	if time is None:
		time = get_default_preview_time()
	time = Time(until=time)
	camera = VideoCapture(0)
	picWindowName = get_pic_window_name()
	while not time.is_up():
		preview_once_with(camera, picWindowName)
	camera.release()
		
def take_photo():
	camera = VideoCapture(0)
	isCaptured = None
	while not isCaptured:
		isCaptured, picArray = camera.read()
	pic = Image.fromarray(picArray)
	camera.release()
	return pic
	
def preview_once_with(camera, picWindowName):
	isCaptured, pic = camera.read()
	request_to_display(picWindowName, pic)
	update_pic_window()
	
	
def update_pic_window():
	waitKey(1)

class Time:
	def __init__(self, until):
		base = get_time()
		self.end = base + until
	
	def is_up(self):
		current = get_time()
		isUp = current >= self.end
		return isUp


	
from config import *
from printer import *
from cv2 import VideoCapture,  imshow as request_to_display, waitKey
from PIL import Image
from timeit import default_timer as get_time

if __name__ == "__main__":
	preview_until(time=3)
	pic = take_photo()
	print_pic(pic)


