def check_input(question, goodAnswer):
	command = f'/bin/bash -c \'echo -en "\\r{question}\\r"; read -t .1 -sn1 ANSWER; [[ "$ANSWER" == "{goodAnswer}" ]]; result="$?"; (exit $result) && echo "\n $ANSWER"; exit $result\''
	processResult = subprocess.run(
        command, 
        shell=True,
        text=True,
        stderr=subprocess.PIPE,
	)
	if processResult.returncode == 0:
		return True

def stop_keypress_getter():
	keypressBufferPath = get_keypress_buffer_path()
	keypressGetterStopWord = get_keypress_getter_stop_word()
	command = f'echo -n "{keypressGetterStopWord}" > "{keypressBufferPath}"'
	exec_with_bash(command)
	
def is_pressed(testKey):
	keypressBufferPath = get_keypress_buffer_path()
	checkKeypressPath = get_keypress_checker_path()
	command = f'bash "{checkKeypressPath}" "{testKey}" "{keypressBufferPath}"'
	processResult = exec_with_bash(command)
	if processResult.returncode == 0:
		return True

def start_keypress_getter(description=None):
	reset_keypress_buffer()
	exec_keypress_getter_script(description)

def exec_keypress_getter_script(description):
	keypressBufferPath = get_keypress_buffer_path()
	keypressGetterPath = get_keypress_getter_path()
	keypressGetterStopWord = get_keypress_getter_stop_word()
	command = f'x-terminal-emulator -e \'bash "{keypressGetterPath}" "{keypressBufferPath}" "{keypressGetterStopWord}" "{description}"\''
	exec_with_bash(command)
	
def reset_keypress_buffer():
	keypressBufferPath = get_keypress_buffer_path()
	command = f'echo -n "" > "{keypressBufferPath}"'
	exec_with_bash(command)

def exec_with_bash(commandString):
    processResult = subprocess.run(
        commandString, 
        shell=True,
        text=True,
        stderr=subprocess.PIPE, 
        stdout=subprocess.PIPE,
    )
    return processResult

from config import *
from running_time import *
import subprocess
from subprocess import STDOUT
import sys
if __name__ == "__main__":
	stopKey = "k"
	description = f"stopKey = {stopKey}"
	start_keypress_getter(description)
	returncode = None
	while not is_pressed(stopKey):
		mustStop = check_input("stop keypress getter?[y]: ", "y")
		if mustStop:
			break
	stop_keypress_getter()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
