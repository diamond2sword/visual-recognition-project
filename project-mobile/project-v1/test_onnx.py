def main()->int:
    onnx_classify()
    return 0


def onnx_classify():
    pic, picLabel = get_random_pic_from_test_dataset()
    
    pic = center_of(pic)
    print_pic(pic)
    
    model = get_onnx_model()

    inputPic = to_onnx_input(pic)
    inputName = get_input_name_of(model)

    result = exp(model.run(None, {inputName: inputPic}))
    
    classLabels = get_class_labels()
    predictedIndex = int(result.argmax().item())
    print_str(f"true label: {picLabel}")
    print_str(f"predicted label: {classLabels[predictedIndex]}")

def get_input_name_of(onnxModel):
    inputName = onnxModel.get_inputs()[0].name
    return inputName

def get_onnx_model():
    path = get_onnx_model_path()
    model = InferenceSession(path)
    return model

from config import *
from dataset import *
from printer import *
from class_dict_manager import *
from numpy import exp
from onnxruntime import InferenceSession
if __name__ == "__main__":
    main()
