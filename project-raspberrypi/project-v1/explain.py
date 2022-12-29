
def explain(labeledProbabilities):
    print(f"I am going to explain the result {labeledProbabilities}")
    for label, probability in labeledProbabilities:
        print(f"{round(probability * 100, 2):>8}% {label}") 
    classDict = class_dict_manager.get_class_dict()
    label, probability = labeledProbabilities[0]
    explainDict = classDict[label]["strings"]["explain"]

    print(f"Explaining {label}")
    for header, description in explainDict.items():
        print(f"\n{header}\n{description}")


import class_dict_manager
if __name__ == "__main__":
    pass
