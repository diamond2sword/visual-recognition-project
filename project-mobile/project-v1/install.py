
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
    testDatasetPath = get_test_dataset_path()
    classLabels = get_class_labels(includeAnyClass=True)
    for classLabel in classLabels:
        classPath = f"{testDatasetPath}/{classLabel}"
        create_dir(classPath)

def create_test_dataset_dir():
    path = get_test_dataset_path()
    create_dir(path)


def download_onnx_model():
    linkID = get_onnx_model_gdrive_link_id()
    path = get_onnx_model_path()
    download_from_gdrive(id=linkID, output=path, quiet=False)

def download_class_dict():
    link = get_class_dict_link()
    path = get_class_dict_path()
    urlretrieve(link, path)

def create_dir(path):
    makedirs(path, exist_ok=True)


from config import *
from class_dict_manager import *
from os import makedirs
from urllib.request import urlretrieve
from gdown import download as download_from_gdrive
if __name__ == "__main__":
    main()
