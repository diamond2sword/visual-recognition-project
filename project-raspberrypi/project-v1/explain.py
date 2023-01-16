
def explain(labeledProbabilities):
	print_wrapped(f"I am going to explain the result {labeledProbabilities}")
	for label, probability in labeledProbabilities:
		print_wrapped(f"{round(probability * 100, 2):>8}% {label}") 
	label, probability = labeledProbabilities[0]

def explain_class(classLabel):
	print_wrapped(f"\nExplaining {classLabel}")
	classDict = class_dict_manager.get_class_dict()
	explainDict = classDict[classLabel]["strings"]["explain"]
	for header, descLines in explainDict.items():
		print_wrapped(f"\n{header}")
		for descLine in descLines:
			print_wrapped(descLine, fullIndent=1)

def print_wrapped(string, fullIndent=0):
	while string: 
		string = textwrap.indent(
			string, "\t"*(fullIndent))
		string = textwrap.wrap(
			string, fix_sentence_endings=True,
			drop_whitespace=False,
			replace_whitespace=False)
		print(f"{string.pop(0)}")
		string = " ".join(string)

import textwrap
import class_dict_manager
import random
if __name__ == "__main__":
	classLabels = class_dict_manager.get_class_labels()
	explain_class(random.choice(classLabels))
