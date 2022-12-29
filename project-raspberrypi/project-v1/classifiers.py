
def main():
	c = Classifier(
		stopTime=5,
		stopTakenPicLimit=5,
		stopKey=None, 
		hasStopProgressbar=True,
		pauseKey=None,
		hasPreview=False,
		picWindowName=None,
		isSummed=True,
		isRealtime=False,
		isRealtimeOutputLabeled=True,
		mustShowSummedClassifyProgress=True,
		isDelayedOutputLabeled=True,
		isSimpleOutputLabeled=True,
	)
	c.main()


class Classifier:
	def main(self)->int:
		self.__run()
		return 0

	######################## ABSTRACTION LEVEL 4 #########################
		
	def __run(self):
		self.__wake_up_camera()
		self.__reset_run_variables()
		self.__start_stop_progressbar()
		self.__start_keypress_getter()
		self.__reset_stop_time()
		while True:
			self.__update_stop_progressbar()
			if self.__check_for_stop():
				break
			self.__get_pictures()
			self.__show_preview()
			if self.__check_pause_key():
				continue
			self.__save_input_pic()
			self.__realtime_classify()
			self.__add_last_probabilities_to_sum()
			self.__change_realtime_output()
			self.__show_realtime_output()
		self.__stop_keypress_getter()
		self.__end_stop_progressbar()
		self.__stop_camera()
		self.__summed_classify()
		self.__change_delayed_output()
		self.__show_delayed_output()
		self.__get_last_output()
		self.__explain_last_output()
	
	def __run_simple(self):
		self.__wake_up_camera()
		self.__reset_run_variables()
		self.__get_pictures()
		self.__show_preview()
		self.__simple_classify()
		self.__change_simple_output()
		self.__show_simple_output()
		self.__get_last_output()
		self.__explain_last_output()
		
	######################## ABSTRACTION LEVEL 3 #########################

	def __explain_last_output(self):
		lastOutput = self.__get_last_output()
		explain.explain(lastOutput)

	def __get_last_output(self):
		pass

	def __get_simple_output(self):
		return self.simpleOutput
	
	def __show_simple_output(self):
		self.__print(self.simpleOutput)
	
	def __change_simple_output(self):
		self.__change_simple_output_to_simple_probabilities()
		self.__change_simple_output_to_labeled_probabilities()
		
	def __simple_classify(self):
		self.simpleProbabilities = self.__classify(self.inputPic)

	def __get_delayed_output(self):
		return self.delayedOutput

	def __show_delayed_output(self):
		self.__print(self.delayedOutput)
	
	def __change_delayed_output(self):
		self.__change_delayed_output_to_summed_probabilities()
		self.__change_delayed_output_to_average_probabilities()
		self.__change_delayed_output_to_labeled_probabilities()
	
	def __summed_classify(self):
		self.__reset_summing_variables()
		self.__start_summed_classify_progressbar()
		for inputPic in self.savedInputPics:
			probabilities = self.__classify(inputPic)
			self.__add_to_sum(probabilities)
			self.__update_summed_classify_progressbar()
		self.__end_summed_classify_progressbar()
	
	def __end_summed_classify_progressbar(self):
		self.summedClassifyProgressbar.close()

	def __update_summed_classify_progressbar(self):
		self.summedClassifyProgressbar.n = self.addCount
		self.summedClassifyProgressbar.refresh()
		
	def __clear_summed_classify_progressbar(self):
		self.summedClassifyProgressbar.clear()
			
	def __start_summed_classify_progressbar(self):
		self.summedClassifyProgressbar = Progressbar(
			desc="CLASSIFYING",
			unit="pics",
			total=len(self.savedInputPics),
			file=sys.stdout
		)
		
	def __get_realtime_output(self):
		return self.realtimeOutput

	def __show_realtime_output(self):
		self.__print_with_respect_to_stop_progressbar(self.realtimeOutput)
		
	def __change_realtime_output(self):
		self.__change_realtime_output_to_last_probabilities()
		self.__change_realtime_output_to_average_probabilities()
		self.__change_realtime_output_to_labeled_probabilities()
		
	def __add_last_probabilities_to_sum(self):
		self.__add_to_sum(self.lastProbabilities)	 

	def __realtime_classify(self):
		self.lastProbabilities = self.__classify(self.inputPic)
		
	def __classify(self, inputPic): 
		scores = self.model.run(None, {self.modelInputName: inputPic})
		probabilities = onnx.get_probability_distribution_of(scores)
		return probabilities
		
	def __show_preview(self):
		request_to_display(self.picWindowName, self.picArray)
		self.__update_pic_window()
		
	def __save_input_pic(self):
		self.savedInputPics.append(self.inputPic)
		
	def __get_pictures(self):
		self.picArray = camera.take_photo_with(self.camera)
		self.pilPic = Image.fromarray(self.picArray)
		self.centeredPic = self.__center_transform(self.pilPic)
		self.inputPic = dataset.to_onnx_input(self.centeredPic)

	def __check_pause_key(self):
		if keypress.is_pressed(self.pauseKey):
			self.isPaused = not self.isPaused
		if self.isPaused:
			return True

	def __check_for_stop(self):
		return self.__check_stop_time() or self.__check_stop_taken_pic_limit() or self.__check_stop_key()

	def __print_with_respect_to_stop_progressbar(self, string):
		self.__clear_stop_progressbar()
		self.__print(string)
		self.__update_stop_progressbar()
		
	def __end_stop_progressbar(self):
		self.__end_stop_time_progressbar()
		self.__end_stop_taken_pic_limit_progressbar()

	def __update_stop_progressbar(self):
		self.__update_stop_time_progressbar()
		self.__update_stop_taken_pic_limit_progressbar()
		
	def __clear_stop_progressbar(self):
		self.__clear_stop_time_progressbar()
		self.__clear_stop_taken_pic_limit_progressbar()
			
	def __start_stop_progressbar(self):
		self.__start_stop_time_progressbar()
		self.__start_stop_taken_pic_limit_progressbar() 
		
	def __reset_stop_time(self):
		self.runningStopTime.reset()

	def __stop_keypress_getter(self):
		keypress.stop_keypress_getter()

	def __start_keypress_getter(self):
		keypress.start_keypress_getter(self.keypressGetterDescription)	 
		 
	def __reset_run_variables(self):
		self.timeProgressBar = None
		self.picArray = None
		self.pilPic = None
		self.centeredPic = None
		self.inputPic = None
		self.savedInputPics = []
		self.isPaused = False
		self.__reset_summing_variables()
		self.lastProbabilities = None
		self.averageProbabilities = None
		self.labeledRealtimeOutput = None
		self.realtimeOutput = None
		self.delayedOutput = None
		self.simpleOutput = None
		self.lastOutput = None
		
	def __stop_camera(self):
		self.camera.release()
		remove_pic_display(self.picWindowName)
		
	def __wake_up_camera(self):
		self.__get_pictures()
		self.__show_preview()

######################## ABSTRACTION LEVEL 2 #########################

	def __change_simple_output_to_labeled_probabilities(self):
		self.simpleOutput = self.__change_to_labeled_probabilities(self.simpleOutput) 

	def __change_simple_output_to_simple_probabilities(self):
		self.simpleOutput = self.simpleProbabilities

	def __change_delayed_output_to_labeled_probabilities(self):
		self.delayedOutput = self.__change_to_labeled_probabilities(self.delayedOutput) 
	
	def __change_delayed_output_to_average_probabilities(self):
		self.delayedOutput = divide_array(self.delayedOutput, len(self.savedInputPics))

	def __change_delayed_output_to_summed_probabilities(self):
		self.delayedOutput = self.sum

	def __add_to_sum(self, probabilities):
		self.sum = add_array(self.sum, probabilities)
		self.addCount += 1

	def __change_realtime_output_to_labeled_probabilities(self):
		self.realtimeOutput = self.__change_to_labeled_probabilities(self.realtimeOutput)
		
	def __change_realtime_output_to_average_probabilities(self):
		self.realtimeOutput = divide_array(self.sum, self.addCount)
		
	def __change_realtime_output_to_last_probabilities(self):
		self.realtimeOutput = self.lastProbabilities

	def __change_to_labeled_probabilities(self, probabilities):
		labeledProbabilities = dict(zip(self.classLabels, probabilities[0][0]))
		labeledProbabilities = sorted(
			labeledProbabilities.items(), 
			key=lambda item: item[1], 
			reverse=True
		)
		return labeledProbabilities

	def __update_pic_window(self):
		waitKey(1)

	def __end_stop_time_progressbar(self):
		self.stopTimeProgressbar.close()

	def __update_stop_time_progressbar(self):
		self.stopTimeProgressbar.n = int(self.runningStopTime.spent())
		self.stopTimeProgressbar.refresh()
		
	def __clear_stop_time_progressbar(self):
		self.stopTimeProgressbar.clear()
			
	def __start_stop_time_progressbar(self):
		self.stopTimeProgressbar = Progressbar(
			desc="TIME",
			unit="secs",
			total=self.stopTime,
			file=sys.stdout,
		)

	def __end_stop_taken_pic_limit_progressbar(self):
		self.stopTakenPicLimitProgressbar.close()

	def __update_stop_taken_pic_limit_progressbar(self):
		self.stopTakenPicLimitProgressbar.n = len(self.savedInputPics) 
		self.stopTakenPicLimitProgressbar.refresh()
	
	def __clear_stop_taken_pic_limit_progressbar(self):
		self.stopTakenPicLimitProgressbar.clear()
			
	def __start_stop_taken_pic_limit_progressbar(self):
		self.stopTakenPicLimitProgressbar = Progressbar(
			desc="PICS TAKEN",
			unit="pics",
			total=self.stopTakenPicLimit,
			file=sys.stdout
		)

	def __check_stop_key(self):
		return keypress.is_pressed(self.stopKey)
		
	def __check_stop_taken_pic_limit(self):
		if len(self.savedInputPics) >= self.stopTakenPicLimit:
			return True

	def __check_stop_time(self):
		if self.runningStopTime.is_up():
			return True
		
	def __reset_summing_variables(self):
		self.sum = 0
		self.addCount = 0

	def __print(self, string):
		print(string)
		
					
	def __return_true(self):
		return True
			
	def __do_nothing(self):
		pass

######################## ABSTRACTION LEVEL 1 #########################
							
	def __init__(
		self,
		stopTime=5,
		stopTakenPicLimit=None,
		stopKey=None, 
		hasStopProgressbar=False,
		pauseKey=None,
		hasPreview=False,
		picWindowName=None,
		isSummed=False,
		isRealtime=False,
		isRealtimeOutputLabeled=True,
		mustShowSummedClassifyProgress=False,
		isDelayedOutputLabeled=True,
		isSimpleOutputLabeled=True,
		mustShowOutput=True,
		mustExplainLastOutput=True,
		):
		
		self.stopTime = stopTime
		self.stopTakenPicLimit = stopTakenPicLimit
		self.stopKey = stopKey
		self.__def_stop_time()
		self.__def_stop_taken_pic_limit()
		self.__def_stop_key()
		
		self.hasStopProgressbar = hasStopProgressbar
		self.__def_stop_progressbar()
		
		self.pauseKey = pauseKey
		self.__def_check_pause_key()
	
		self.__def_keypress_getter()
		self.keypressGetterDescription = f"stopKey = {self.stopKey}, pauseKey = {self.pauseKey}"
	
		self.camera = camera.get_camera()
		self.__def_center_transform()
		
		self.model = onnx.get_onnx_model()
		self.modelInputName = onnx.get_input_name_of(self.model)
		
		self.classLabels = class_dict_manager.get_class_labels()
		
		self.hasPreview = hasPreview
		self.picWindowName = picWindowName
		self.__def_show_preview()

		self.mustShowOutput = mustShowOutput
		
		self.isRealtime = isRealtime
		self.isSummed = isSummed
		self.isRealtimeOutputLabeled = isRealtimeOutputLabeled
		self.__def_realtime_classify()
		self.__def_add_last_probabilities_to_sum()
		self.__def_change_realtime_output()
		self.__def_show_realtime_output()
		self.__def_run()
	
		self.mustShowSummedClassifyProgress = mustShowSummedClassifyProgress
		self.isDelayedOutputLabeled = isDelayedOutputLabeled
		self.__def_summed_classify_progressbar()
		self.__def_summed_classify()
		self.__def_change_delayed_output()
		self.__def_show_delayed_output()
		
		self.__def_simple_classify()
		self.isSimpleOutputLabeled = isSimpleOutputLabeled
		self.__def_change_simple_output()
		self.__def_show_simple_output()

		self.mustExplainLastOutput = mustExplainLastOutput
		self.__def_get_last_output()
		self.__def_explain_last_output()

		self.__reset_run_variables()

	def __def_run(self):
		if not self.isRealtime and not self.isSummed:
			self.__run = self.__run_simple

	def __def_explain_last_output(self):
		if not self.mustExplainLastOutput:
			self.__explain_last_output = self.__do_nothing

	def __def_get_last_output(self):
		if self.isRealtime:
			self.__get_last_output = self.__get_realtime_output
		if self.isSummed and not self.isRealtime:
			self.__get_last_output = self.__get_delayed_output
		if not self.isSummed and not self.isRealtime:
			self.__get_last_output = self.__get_simple_output
			
	def __def_show_simple_output(self):
		if self.isRealtime or self.isSummed or not self.mustShowOutput:
			self.__show_simple_output = self.__do_nothing
	
	def __def_change_simple_output(self):
		if self.isRealtime or self.isSummed:
			self.__change_show_simple_output = self.__do_nothing		
	
	def __def_simple_classify(self):
		if self.isRealtime or self.isSummed:
			self.__simple_classify = self.__do_nothing		

	def __def_show_delayed_output(self):
		if self.isRealtime or not self.mustShowOutput:
			self.__show_delayed_output = self.__do_nothing

	def __def_change_delayed_output(self):
		if self.isRealtime or not self.isSummed:
			self.__change_delayed_output = self.__do_nothing
		if not self.isDelayedOutputLabeled:
			self.__change_delayed_output_to_labeled_probabilities = self.__do_nothing
			
	def __def_summed_classify(self):
		if not self.isSummed or self.isRealtime:
			self.__summed_classify = self.__do_nothing

	def __def_summed_classify_progressbar(self):
		if not self.mustShowSummedClassifyProgress:
			self.__start_summed_classify_progressbar = self.__do_nothing
			self.__clear_summed_classify_progressbar = self.__do_nothing
			self.__update_summed_classify_progressbar = self.__do_nothing
			self.__end_summed_classify_progressbar = self.__do_nothing

	def __def_show_realtime_output(self):	
		if not self.isRealtime or not self.mustShowOutput:
			self.__show_realtime_output = self.__do_nothing

	def __def_change_realtime_output(self):
		if not self.isRealtime:
			self.__change_realtime_output = self.__do_nothing
			self.__change_realtime_output_to_last_probabilities = self.__do_nothing
		if not self.isSummed:
			self.__change_realtime_output_to_average_probabilities = self.__do_nothing
		if not self.isRealtimeOutputLabeled:
			self.__change_realtime_output_to_labeled_probabilities = self.__do_nothing
			
	def __def_add_last_probabilities_to_sum(self):
		if not self.isRealtime or not self.isSummed:
			self.__add_last_probabilities_to_sum = self.__do_nothing

	def __def_realtime_classify(self):
		if not self.isRealtime:
			self.__realtime_classify = self.__do_nothing
		
	def __def_show_preview(self):
		if self.picWindowName is None:
			self.picWindowName = config.get_pic_window_name()
		if not self.hasPreview:
			self.__show_preview = self.__do_nothing
			
	def __def_center_transform(self):
		camPicArray = camera.take_photo_with(self.camera)
		camPilPic = Image.fromarray(camPicArray)
		camPicWidth = min(camPilPic.size)
		picSize = config.get_pic_size()
		self.__center_transform = Sequential(
			CenterCrop(camPicWidth),
			Resize(picSize),
		)
		
	def __def_check_pause_key(self):
		if self.pauseKey is None:
			self.__check_pause_key = self.__do_nothing
		
	def __def_stop_progressbar(self):
		if not self.hasStopProgressbar:
			self.__start_stop_progressbar = self.__do_nothing
			self.__clear_stop_progressbar = self.__do_nothing
			self.__update_stop_progressbar = self.__do_nothing
			self.__end_stop_progressbar = self.__do_nothing
		if self.stopTime is None:
			self.__start_stop_time_progressbar = self.__do_nothing
			self.__clear_stop_time_progressbar = self.__do_nothing
			self.__update_stop_time_progressbar = self.__do_nothing
			self.__end_stop_time_progressbar = self.__do_nothing
		if self.stopTakenPicLimit is None:
			self.__start_stop_taken_pic_limit_progressbar = self.__do_nothing
			self.__clear_stop_taken_pic_limit_progressbar = self.__do_nothing
			self.__update_stop_taken_pic_limit_progressbar = self.__do_nothing
			self.__end_stop_taken_pic_limit_progressbar = self.__do_nothing

			
	def __def_stop_time(self):
		if self.stopTime is None:
			self.__check_stop_time = self.__do_nothing
			self.__reset_stop_time = self.__do_nothing
		else:
			self.runningStopTime = running_time.Time(until=self.stopTime)

	def __def_stop_taken_pic_limit(self):
		if self.stopTakenPicLimit is None:
			self.__check_stop_taken_pic_limit = self.__do_nothing
			
	def __def_stop_key(self):
		if self.stopKey is None:
			self.__check_stop_key = self.__do_nothing

	def __def_keypress_getter(self):
		if self.stopKey is not None:
			return
		if self.pauseKey is not None:
			return
		self.__start_keypress_getter = self.__do_nothing
		self.__stop_keypress_getter = self.__do_nothing


import config
import class_dict_manager
import onnx
import dataset
import camera
import keypress
import running_time
import explain
try:
	from cv2 import imshow as request_to_display, waitKey, destroyWindow as remove_pic_display
except:
	from camera_mock import request_to_display, waitKey, remove_pic_display
from torchvision.transforms import Resize, CenterCrop
from torch.nn import Sequential
from numpy import add as add_array, divide as divide_array
from tqdm import tqdm as Progressbar
from PIL import Image
import sys
if __name__ == "__main__":
	main()
