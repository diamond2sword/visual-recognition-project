def check_keypress(testKey):
	bufferPath = get_buffer_path()
	checkKeypressPath = get_keypress_checker_path()
	command = f"bash {checkKeypressPath} {testKey} {bufferPath}"
	exec_with_bash(command)

def get_keypress():
	bufferPath = get_buffer_path()
	getKeypressPath = get_keypress_getter_path()
	command = f"x-terminal-emulator -e \"bash {getKeypressPath} {bufferPath}\""
	exec_with_bash(command)

def exec_with_bash(commandString):
    exitOutput = subprocess.check_output(
        commandString, 
        shell=True,
        text=True
    )
    if exitOutput == 0:
        return True
    return exitOutput

from config import *
import subprocess
import sys
if __name__ == "__main__":
	get_keypress()
	exitOutput = None
	while not exitOutput:
		exitOutput = check_keypress(input("testKey: "))
