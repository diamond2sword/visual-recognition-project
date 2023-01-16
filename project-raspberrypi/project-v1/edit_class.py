
def main():
	classDict = class_dict_manager.get_class_dict()
	modes = {
		"EDIT": edit_class,
		"ADD": add_class,
		"DEL": del_class,
		"ECHO": echo_class,
	}
	run(classDict, modes)


def run(classDict, modes):
	modeNames = list(modes.keys())
	while True:
		modeName = read_sentence(f"mode {modeNames}: ")
		if modeName not in modeNames:
			continue
		modes[modeName](classDict)

def edit_class(classDict):
	className = read_sentence("class name: ")
	if className not in classDict.keys():
		print(f"'{className}' is not a class")
		return	
	ask_recursively_for(classDict, f"['{className}']")

def add_class(classDict):
	className = read_sentence("class name: ")
	if className in classDict.keys():
		print(f"'{className}' is an existing class")
		return	
	classDict[className] = cp(classDict["None"])
	ask_recursively_for(classDict, f"['{className}']")

def del_class(classDict):
	className = read_sentence("class name: ")
	if className not in classDict.keys():
		print(f"'{className}' is not a class")
		return	
	del classDict[className]

def echo_class(classDict):
	key = read_sentence("key [optional]: ")
	cmd = f"print(json.dumps(classDict{key}, indent=4, sort_keys=True))"
	try:
		print(key)
		eval(cmd)
	except:
		print("Invalid classDict key")

def ask_recursively_for(parentDict, key):
	childDict = eval(f"parentDict{key}")
	if type(childDict) == type(dict()):		
		for childName in childDict.keys():
			ask_recursively_for(parentDict, f"{key}['{childName}']")
	mustEdit = read_sentence(f"edit {key} [y]? ") == 'y'
	if not mustEdit:
		return
	exec(f"parentDict{key} = read_paragraph("")")

		
def read_paragraph(question="", endWord="EOF", isInList=True):
	string = ""
	strList = []
	print(f">>> {question}")
	print(endWord)
	while True:
		line = input()
		if line == endWord:
			break
		string += line + r"\n"
		strList.append(line)
	if isInList:
		return cp(strList)
	return string

def read_sentence(question):
	return input(question)

import class_dict_manager
from copy import deepcopy as cp
import json
if __name__ == "__main__":
	main()
