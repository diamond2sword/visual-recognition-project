
def explain(labeledProbabilities):
	print_wrapped("\nI am going to explain the result:")
	pprint.pprint(labeledProbabilities)
	print_wrapped("\nProbabilities:")
	for label, probability in labeledProbabilities:
		print_wrapped(f"{round(probability * 100, 2):>8}% {label}") 
	label, probability = labeledProbabilities[0]
	explain_class(label)

def explain_class(classLabel):
	print_wrapped(f"\nExplaining {classLabel}:")
	classDict = class_dict_manager.get_class_dict()
	explainDict = classDict[classLabel]["strings"]["explain"]
	for header, descLines in explainDict.items():
		print_wrapped(f"\n{header}", fullIndent=1)
		for descLine in descLines:
			print_wrapped(descLine, fullIndent=2)

def print_wrapped(string, fullIndent=0):
	terminalCols = os.get_terminal_size().columns
	while string: 
		string = textwrap.indent(
			string, "  "*fullIndent)
		string = textwrap.wrap(
			string, fix_sentence_endings=True,
			drop_whitespace=True,
			replace_whitespace=False,
			width=terminalCols)
		print(f"{string.pop(0)}")
		string = " ".join(string)

import textwrap
import class_dict_manager
import pprint
import random
import os
if __name__ == "__main__":
	classLabels = class_dict_manager.get_class_labels()
	explain_class(random.choice(classLabels))
