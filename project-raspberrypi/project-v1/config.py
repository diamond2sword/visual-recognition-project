def get_keypress_checker_path():
	name = get_keypress_checker_name()
	projectPath = get_project_path()
	path = f"{projectPath}/{name}"
	return path

def get_keypress_getter_path():
	name = get_keypress_getter_name()
	projectPath = get_project_path()
	path = f"{projectPath}/{name}"
	return path

def get_keypress_buffer_path():
	name = get_keypress_buffer_name()
	projectPath = get_project_path()
	path = f"{projectPath}/{name}"
	return path

def get_classifier_preview_path():
	projectPath = get_project_path()
	name = get_classifier_preview_name()
	path =f"{projectPath}/{name}"
	return path

def get_class_dict_path():
	projectPath = get_project_path()
	name = get_class_dict_name()
	path = f"{projectPath}/{name}"
	return path

def get_test_dataset_path():
	projectPath = get_project_path()
	name = get_test_dataset_name()
	path = f"{projectPath}/{name}"
	return path

def get_onnx_model_path():
	projectPath = get_project_path()
	name = get_onnx_model_name()
	path = f"{projectPath}/{name}"
	return path

def get_project_path():
	path = sys.path[0]
	return path

def get_keypress_checker_name():
	name = "check_keypress.sh"
	return name

def get_keypress_getter_name():
	name = "get_keypress.sh"
	return name

def get_keypress_buffer_name():
	name = "keypress_buffer.txt"
	return name

def get_classifier_preview_name():
	name = "classifier_preview.py"
	return name

def get_pic_window_name():
	picName = get_pic_name()
	name = f"preview of {picName}"
	return name
	
def get_pic_name():
	name = "test.jpg"
	return name

def get_any_class_name():
	name = "Any"
	return name

def get_class_dict_name():
	name = "classDict.json"
	return name

def get_test_dataset_name():
	name = "test"
	suffix = get_dataset_suffix_name()
	fullName = f"{name}{suffix}"
	return fullName

def get_onnx_model_name():
	name = "model.onnx"
	return name

def get_dataset_suffix_name():
	suffix = "-dataset"
	return suffix

def get_keypress_getter_stop_word():
	word = "stop_keypress_getter"
	return word

def get_test_loader_batch_size():
	batchSize = 200
	return batchSize

def get_pic_size():
	height = 224
	width = 224
	picSize = (height, width)
	return picSize
	
def get_default_preview_time():
	time = 3
	return time

def get_onnx_model_link():
	link = "https://raw.githubusercontent.com/diamond2sword/visual-recognition-project/main/models/model.onnx"
	return link

def get_class_dict_link():
	link = "https://raw.githubusercontent.com/diamond2sword/visual-recognition-project/main/classifiers/plantClassifier/classDict.json"
	return link

import sys
if __name__ == "__main__":
	pass
