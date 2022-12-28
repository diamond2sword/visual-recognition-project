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


import config
import printer
import running_time
from PIL import Image
try:
	from cv2 import VideoCapture,  imshow as request_to_display, waitKey
except:
	from camera_mock import VideoCapture, request_to_display, waitKey
if __name__ == "__main__":
	main()
