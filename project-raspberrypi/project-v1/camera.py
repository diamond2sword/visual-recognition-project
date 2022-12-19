

def preview_until(time=None, key=None, mustShow=True):
	if time is None:
		time = get_default_preview_time()
	runningTime = Time(until=time)
	camera = get_camera()
	picWindowName = get_pic_window_name()
	while not runningTime.is_up():
		preview_once_with(camera, picWindowName, mustShow=mustShow)
	camera.release()
		
def take_photo():
	camera = VideoCapture(0)
	picArray = take_photo_with(camera)
	pic = Image.fromarray(picArray)
	camera.release()
	return pic
	
def take_photo_with(camera):
	isCaptured = None
	while not isCaptured:
		isCaptured, picArray = camera.read()
	return picArray
	
def preview_once_with(camera, picWindowName, mustShow=True):
    isCaptured, pic = camera.read()
    if mustShow:
        request_to_display(picWindowName, pic)
    update_pic_window()

	
	
def update_pic_window():
	waitKey(1)
	
def get_camera():
	return VideoCapture(0)

class Time:

	def spent(self):
		current = get_time()
		spent = self.until - self.remaining()
		return spent

	def __str__(self):
		return self.remaining()

	def remaining(self):
		current = get_time()
		remaining = self.end - current
		return remaining
	
	def is_up(self):
		current = get_time()
		isUp = current >= self.end
		return isUp
		
	def __init__(self, until):
		self.until = until
		self.reset()
		
	def reset(self):
		now = get_time()
		self.end = now + self.until


	
from config import *
from printer import *
from cv2 import VideoCapture,  imshow as request_to_display, waitKey
from PIL import Image
from timeit import default_timer as get_time

if __name__ == "__main__":
	preview_until(time=3)
	pic = take_photo()
	print_pic(pic)


