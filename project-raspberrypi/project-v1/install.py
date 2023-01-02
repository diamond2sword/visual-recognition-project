def main()->int:
	download_files()
	create_files()
	return 0


def create_files():
	create_test_dataset_dir()
	create_test_dataset_class_dirs()

def download_files():
	download_class_dict()
	download_onnx_model()


def create_test_dataset_class_dirs():
	testDatasetPath = config.get_test_dataset_path()
	classLabels = class_dict_manager.get_class_labels(includeAnyClass=True)
	for classLabel in classLabels:
		classPath = f"{testDatasetPath}/{classLabel}"
		create_dir(classPath)

def create_test_dataset_dir():
	path = config.get_test_dataset_path()
	create_dir(path)


def download_onnx_model():
	linkID = config.get_onnx_model_gdrive_link_id()
	path = config.get_onnx_model_path()
	download_from_gdrive(id=linkID, output=path, quiet=False)

def download_class_dict():
	link = config.get_class_dict_link()
	path = config.get_class_dict_path()
	urlretrieve(link, path)

def create_dir(path):
	makedirs(path, exist_ok=True)


import config
import class_dict_manager
from os import makedirs
from urllib.request import urlretrieve
from gdown import download as download_from_gdrive
if __name__ == "__main__":
	main()

