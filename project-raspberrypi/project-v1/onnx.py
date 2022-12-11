def main()->int:
    classify_from_test_dataset()
    classify_from_camera()
    return 0
    
def classify_from_camera(picLabel=None, previewTime=None):
	if picLabel is None:
		picLabel = get_any_class_name()
	preview_until(time=previewTime)
	pic = take_photo()
	pic = center_of(pic)
	probabilities = simple_classify(pic)
	show_output(pic, picLabel, probabilities)

def classify_from_test_dataset(classLabel=None):
	pic, picLabel = get_random_labeled_pic_from_test_dataset(classLabel=classLabel)
	pic = center_of(pic)
	probabilities = simple_classify(pic)
	show_output(pic, picLabel, probabilities)
	
def simple_classify(pic):
	inputPic = to_onnx_input(pic)
	model = get_onnx_model()
	probabilities = get_probabilities_by_running(model, inputPic)
	return probabilities

def show_output(pic, picLabel, probabilities):
	predictedIndex = probabilities.argmax()
	print_pic(pic)
	classLabels = get_class_labels()
	print_str(f"true label: {picLabel}")
	print_str(f"predicted label: {classLabels[predictedIndex]}")
		
def get_probabilities_by_running(model, inputPic):
	inputName = get_input_name_of(model)
	scores = model.run(None, {inputName: inputPic})
	probabilities = get_probability_distribution_of(scores)
	return probabilities


def get_onnx_model():
    path = get_onnx_model_path()
    model = InferenceSession(path)
    return model

def get_probability_distribution_of(scores):
	probabilities = exp(scores)
	return probabilities
	
def get_input_name_of(onnxModel):
    inputName = onnxModel.get_inputs()[0].name
    return inputName

from config import *
from dataset import *
from printer import *
from class_dict_manager import *
from camera import *
from numpy import exp
from onnxruntime import InferenceSession
if __name__ == "__main__":
    main()
