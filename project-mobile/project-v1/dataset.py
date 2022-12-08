

def to_onnx_input(pic):
    testTransform = get_test_transforms()
    pic = testTransform(pic)
    pic = with_dim_added_to(pic)
    pic = with_memory_moved_to_cpu(pic)
    pic = with_no_grad(pic)
    pic = to_numpy_array(pic)
    return pic

def get_random_pic_from_test_dataset():
    picNames = get_test_dataset_pic_names()

    numOfPicsFound = len(picNames)
    if numOfPicsFound == 0:
        raise NoInputPictureFoundError(numOfPicsFound)
    
    picName, picLabel = choice_pic_from(picNames)

    testDatasetPath = get_test_dataset_path()
    picPath = f"{testDatasetPath}/{picLabel}/{picName}"
    pic = open_as_pil_image(picPath)
    return [pic, picLabel]


def get_test_transforms():
    picSize = get_pic_size()
    testTransform = Compose([
        Resize(picSize),
        ToTensor(),
        Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225]
        )
    ])
    return testTransform

def to_numpy_array(pic):
    pic = pic.numpy()
    pic = pic.astype(float32)
    return pic

def with_no_grad(pic):
    pic = pic.detach()
    return pic

def with_memory_moved_to_cpu(pic):
    pic = pic.cpu()
    return pic

def with_dim_added_to(pic):
    pic = pic.unsqueeze(0)
    return pic

def get_test_dataset_pic_names():
    picNames = []
    classLabels = get_class_labels()
    testDatasetPath = get_test_dataset_path()
    for classLabel in classLabels:
        classPath = f"{testDatasetPath}/{classLabel}"
        names = get_file_names_in(classPath)
        for name in names:
            picName = [name, classLabel]
            picNames.append(picName)
    return picNames

def get_file_names_in(path):
    names = listdir(path)
    return names

def choice_pic_from(picNames):
    isPic = False
    picName = None
    testDatasetPath = get_test_dataset_path()
    
    shuffle(picNames)
    while not isPic:
        picName = picNames.pop(0)
        name, label = picName
        picPath = f"{testDatasetPath}/{label}/{name}"
        isPic = is_pic(picPath)
    return picName


def is_pic(picPath):
    isPic = True
    try:
        open_as_pil_image(picPath)
    except:
        isPic = False
    return isPic
       

class NoInputPictureFoundError(Exception):
    def __str__(self):
        testDatasetName = get_test_dataset_name()
        testDatasetPath = get_test_dataset_path()
        randClassLabel = get_random_class_label(includeAnyClass=True)
        return f"There's no picture in {testDatasetName}. Please put a picture in the class folders such as class {randClassLabel}, located in {testDatasetPath}/{randClassLabel}."


from config import *
from class_dict_manager import *
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from numpy import float32
from random import shuffle
from PIL.Image import open as open_as_pil_image
from os import listdir
