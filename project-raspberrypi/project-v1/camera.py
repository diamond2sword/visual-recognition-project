def main():
	preview_until(time=1)
	pic = take_photo()
	printer.print_pic(pic)

def preview_until(time=None, key=None, mustShow=True):
	if time is None:
		time = config.get_default_preview_time()
	runningTime = running_time.Time(until=time)
	camera = get_camera()
	picWindowName = config.get_pic_window_name()
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

def can_access_camera():
	for index in glob("/dev/video?"):
		camera = VideoCapture(index)
		if camera is None or not camera.isOpened():
			continue
		return True
	
def is_in_termux():
	if not os.path.isdir("/data/data/com.termux/files/home/"):
		return False
	return True

class CameraNotFoundError(Exception):
	def __str__(self):
		errorMessage = self.__get_error_message()
		return errorMessage	
	
	def __get_error_message(self):
		return f"Cannot find any camera. If this error occured even though a camera is already plugged in, replug the camera."


import config
import printer
import running_time
import os
from PIL import Image
from glob import glob
if is_in_termux():
	from camera_mock import VideoCapture, request_to_display, waitKey
else:
	from cv2 import VideoCapture, imshow as request_to_display, waitKey
	if not can_access_camera():
		raise CameraNotFoundError()	
if __name__ == "__main__":
	take_photo()

