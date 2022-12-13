	
class Classifier:
	def __main(self)->int:
		self.__run()
		return 0
		
	def __run(self):
		self.__reset_variables()
		self.__warm_up_camera()
		self.__start_time_progressbar()
		self.__reset_stop_time()
		while True:
			if self.__check_for_stop():
				return
			if self.__check_pause_key():
				continue
			self.__get_pictures()
			self.__save_input_pic()
			self.__show_preview()
			if not self.__check_classify_key():
				continue
			self.__realtime_classify()
			self.__add_last_probabilities_to_sum()
			self.__clear_time_progressbar()
			self.__show_probabilities()
			self.__update_time_progressbar()
		self.__end_time_progressbar()
		
	def __show_probabilities(self):
		self.__show_last_probabilities()
		self.__show_sum()
		
	def __add_last_probabilities_to_sum(self):
		self.sum = add_array(self.sum, self.lastProbabilities)
		self.addCount += 1
		return self.sum
		
	def __realtime_classify(self):
		scores = self.model.run(None, {self.modelInputName: self.inputPic})
		self.lastProbabilities = exp(scores)	
		
	def __check_classify_key(self):
		if waitKey(1) == self.unicodeOfClassifyKey:
			return True
		
	def __warm_up_camera(self):
		self.__get_pictures()
		self.__show_preview()

	def __show_preview(self):
		request_to_display(self.picWindowName, self.picArray)
		self.__update_pic_window()
		
	def __save_input_pic(self):
		self.savedInputPics.append(self.inputPic)
		
	def __get_pictures(self):
		self.picArray = take_photo_with(self.camera)
		self.pilPic = Image.fromarray(self.picArray)
		self.centeredPic = self.__center_transform(self.pilPic)
		self.inputPic = to_onnx_input(self.centeredPic)

	def __check_pause_key(self):
		if waitKey(1) == self.unicodeOfPauseKey:
			return True
				
	def __check_for_stop(self):
		return self.__check_stop_time() or self.__check_stop_key()
		
	def __show_sum(self):
		averageProbabilities = divide_array(self.sum, self.addCount)
		self.__print(averageProbabilities)
		
	def __show_last_probabilities(self):
		self.__print(self.lastProbabilities)
		
	def __print(self, string):
		self.__clear_time_progressbar()
		print(string)
		self.__update_time_progressbar()
		
	def __end_time_progressbar(self):
		self.timeProgressbar.close()

	def __update_time_progressbar(self):
		self.timeProgressbar.n = int(self.runningStopTime.spent())
		self.timeProgressbar.refresh()
		
	def __clear_time_progressbar(self):
		self.timeProgressbar.clear()
			
	def __start_time_progressbar(self):
		self.timeProgressbar = Progressbar(
			desc="stopTime", 
			total=self.stopTime,
			file=sys.stdout
		)
			
	def __update_pic_window(self):
		waitKey(1)
		
	def __reset_stop_time(self):
		self.runningStopTime.reset()
		
	def __check_stop_key(self):
		if waitKey(1) == self.unicodeOfStopKey:
			return True
			
	def __check_stop_time(self):
		if self.runningStopTime.is_up():
			return True
							
	def __init__(
		self, 
		stopTime=30, 
		stopKey=None, 
		hasPreview=False, 
		picWindowName=None,
		classifyKey=None,
		mustWaitClassifyKey=False,
		pauseKey=None,
		hasTimeProgressbar=False,
		isSummed=True,
		isRealtime=True,
		):
		self.stopTime = stopTime
		self.stopKey = stopKey
		self.__def_stop_time()
		self.__def_stop_key()
		
		self.pauseKey = pauseKey
		self.__def_check_pause_key()
		
		self.camera = get_camera()
		self.__def_center_transform()
		
		self.model = get_onnx_model()
		self.modelInputName = get_input_name_of(self.model)
		
		self.hasPreview = hasPreview
		self.picWindowName = picWindowName
		self.__def_show_preview()
		
		self.classifyKey = classifyKey
		self.mustWaitClassifyKey = mustWaitClassifyKey
		self.__def_check_classify_key()
		
		self.hasTimeProgressbar = hasTimeProgressbar
		self.__def_time_progressbar()
		
		self.isSummed = isSummed
		self.isRealtime = isRealtime
		self.__def_get_pictures()
		self.__def_save_input_pic()
		self.__def_realtime_classify()
		self.__def_add_last_probabilities_to_sum()
		self.__def_show_probabilities()
		self.__def_run()
		
		self.__reset_variables()
	
	def __reset_variables(self):
		self.picArray = None
		self.pilPic = None
		self.centeredPic = None
		self.inputPic = None
		self.savedInputPics = []
		self.sum = 0
		self.addCount = 0
		self.lastProbabilities = None
		self.timeProgressBar = None
		
	def __def_time_progressbar(self):
		if not self.hasTimeProgressbar or self.stopTime is None:
			self.__start_time_progressbar = self.__do_nothing
			self.__clear_time_progressbar = self.__do_nothing
			self.__update_time_progressbar = self.__do_nothing
			self.__end_time_progressbar = self.__do_nothing
		
	def __def_run(self):
		if not self.isRealtime and not self.isSummed:
			self.__run = self.__do_nothing
	
	def __def_show_probabilities(self):
		if not self.isRealtime:
			self.__show_probabilities = self.__do_nothing
		if not self.isSummed:
			self.__show_sum = self.__do_nothing
		
	def __def_add_last_probabilities_to_sum(self):
		if not self.isRealtime or not self.isSummed:
			self.__add_last_probabilities_to_sum = self.__do_nothing
	
	def __def_realtime_classify(self):
		if not self.isRealtime:
			self.__realtime_classify = self.__do_nothing
		
	def __def_check_classify_key(self):
		if self.classifyKey is not None:
			self.unicodeOfClassifyKey = ord(self.classifyKey)
		if not self.mustWaitClassifyKey or self.classifyKey is None:
			self.__check_classify_key = self.__return_true
		
	def __def_show_preview(self):
		if self.picWindowName is None:
			self.picWindowName = get_pic_window_name()
		if not self.hasPreview:
			self.__show_preview = self.__do_nothing
			
	def __def_save_input_pic(self):
		if not self.isSummed or self.isRealtime:
			self.__save_input_pic = self.__do_nothing
			
	def __def_get_pictures(self):
		if not self.isRealtime and not self.isSummed:
			self.__get_pictures = self.__do_nothing
	
	def __def_center_transform(self):
		camPicArray = take_photo_with(self.camera)
		camPilPic = Image.fromarray(camPicArray)
		camPicWidth = min(camPilPic.size)
		picSize = get_pic_size()
		self.__center_transform = Sequential(
		    CenterCrop(camPicWidth),
		    Resize(picSize),
		)
		
	def __def_check_pause_key(self):
		if self.pauseKey is not None:
			self.unicodeOfPauseKey = ord(self.pauseKey)
		if self.pauseKey is None:
			self.__check_pause_key = self.__do_nothing
			
	def __def_stop_time(self):
		if self.stopTime is None:
			self.__check_stop_time = self.__do_nothing
			self.__reset_stop_time = self.__do_nothing
		else:
			self.runningStopTime = Time(until=self.stopTime)
			
	def __def_stop_key(self):
		if self.stopKey is None:
			self.__check_stop_key = self.__do_nothing
		else:
			self.unicodeOfStopKey = ord(self.stopKey)
					
	def __return_true(self):
		return True
			
	def __do_nothing(self):
		pass
		
from config import *
from class_dict_manager import *
from onnx import *
from dataset import *
from cv2 import imshow as request_to_display, waitKey
from torchvision.transforms import Resize, CenterCrop
from torch.nn import Sequential
from camera import *
from numpy import add as add_array, divide as divide_array
from tqdm import tqdm as Progressbar
import sys
if __name__ == "__main__":
	c = Classifier()
