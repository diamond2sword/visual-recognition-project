
def main():
	#classify_from_test_dataset()
	classify_from_camera(previewTime=10, mustShowPreview=False)
	
def classify_from_camera(picLabel=None, previewTime=None, mustShowPreview=True):
	if picLabel is None:
		picLabel = config.get_any_class_name()
	camera.preview_until(time=previewTime, mustShow=mustShowPreview)
	pic = camera.take_photo()
	pic = dataset.center_of(pic)
	probabilities = simple_classify(pic)
	show_output(pic, picLabel, probabilities)

def classify_from_test_dataset(classLabel=None):
	pic, picLabel = get_random_labeled_pic_from_test_dataset(classLabel=classLabel)
	pic = center_of(pic)
	probabilities = simple_classify(pic)
	show_output(pic, picLabel, probabilities)
	
def simple_classify(pic):
	inputPic = dataset.to_onnx_input(pic)
	model = get_onnx_model()
	probabilities = get_probabilities_by_running(model, inputPic)
	return probabilities

def show_output(pic, picLabel, probabilities):
	predictedIndex = probabilities.argmax()
	printer.print_pic(pic)
	classLabels = class_dict_manager.get_class_labels()
	printer.print_str(f"true label: {picLabel}")
	printer.print_str(f"predicted label: {classLabels[predictedIndex]}")

def get_probabilities_by_running(model, inputPic):
	inputName = get_input_name_of(model)
	scores = model.run(None, {inputName: inputPic})
	probabilities = get_probability_distribution_of(scores)
	return probabilities


def get_onnx_model():
	path = config.get_onnx_model_path()
	model = InferenceSession(path)
	return model

def get_probability_distribution_of(scores):
	probabilities = exp(scores)
	return probabilities
	
def get_input_name_of(onnxModel):
	inputName = onnxModel.get_inputs()[0].name
	return inputName

import config
import dataset
import printer
import class_dict_manager
import camera
from numpy import exp
from onnxruntime import InferenceSession
if __name__ == "__main__":
	main()
