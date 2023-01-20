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
	link = config.get_onnx_model_link()
	path = config.get_onnx_model_path()
	download_file(link, path)

def download_class_dict():
	link = config.get_class_dict_link()
	path = config.get_class_dict_path()
	download_file(link, path)

def create_dir(path):
	os.makedirs(path, exist_ok=True)

def download_file(link, path):
	print(f"downloading {os.path.basename(path)}...")
	try:
		urlretrieve(link, path, progress_lambda)
		print()
	except Exception:
		print(f"can't download {path}, check internet connection")

def progress_lambda(block_num, block_size, total_size):
	termCols = os.get_terminal_size().columns
	barCols = termCols - 11
	progress = min(block_num * block_size / total_size, 1)
	percent = f"[{f'{progress*100:.2f}':>6}%]"
	nbars = round(progress*barCols)
	bar = f"[{nbars*'#':.<{barCols}}]"
	print(f"{percent}{bar}", end="\r")

import config
import class_dict_manager
import os
from urllib.request import urlretrieve
from gdown import download as download_from_gdrive
if __name__ == "__main__":
	main()

