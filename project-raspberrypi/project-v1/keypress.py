def main():
	exec_while_ignoring_enter_key(test)

def is_pressed(testKey):
	isPressed = exec_keypress_checker_script(testKey)
	reset_keypress_buffer()
	return isPressed

def stop_keypress_getter():
	keypressBufferPath = config.get_keypress_buffer_path()
	keypressGetterStopWord = config.get_keypress_getter_stop_word()
	command = f'echo -n "{keypressGetterStopWord}" > "{keypressBufferPath}"'
	exec_with_bash(command)

def start_keypress_getter(description=None):
	reset_keypress_buffer()
	exec_keypress_getter_script(description)
	
def exec_keypress_getter_script(description):
	keypressBufferPath = config.get_keypress_buffer_path()
	keypressGetterPath = config.get_keypress_getter_path()
	keypressGetterStopWord = config.get_keypress_getter_stop_word()
	command = f'x-terminal-emulator -e \'bash "{keypressGetterPath}" "{keypressBufferPath}" "{keypressGetterStopWord}" "{description}"\''
	exec_with_bash(command)

def exec_keypress_checker_script(testKey):
	keypressBufferPath = config.get_keypress_buffer_path()
	checkKeypressPath = config.get_keypress_checker_path()
	command = f'bash "{checkKeypressPath}" "{testKey}" "{keypressBufferPath}"'
	processResult = exec_with_bash(command)
	if processResult.returncode == 0:
		return True
	
def reset_keypress_buffer():
	keypressBufferPath = config.get_keypress_buffer_path()
	command = f'echo -n "" > "{keypressBufferPath}"'
	exec_with_bash(command)
	
def exec_while_ignoring_enter_key(function):
	exec_with_bash("stty igncr")
	function()
	exec_with_bash("stty -igncr")

def exec_with_bash(commandString):
	processResult = subprocess.run(
		commandString, 
		shell=True,
		text=True,
		stderr=subprocess.PIPE, 
		stdout=subprocess.PIPE,
	)
	return processResult

def check_input(question, goodAnswer):
	command = f'/bin/bash -c \'read -t .1 -sn1 ANSWER; [[ "$ANSWER" == "{goodAnswer}" ]]; result="$?"; (exit $result); echo -en "\\r{question}$ANSWER\\r"; exit $result\''
	processResult = subprocess.run(
		command, 
		shell=True,
		text=True,
		stderr=subprocess.PIPE,
	)
	if processResult.returncode == 0:
		return True

def test():
	mainStopKey = "k"
	remoteStopKey = "y"
	description = f"stopKey = {mainStopKey}"
	start_keypress_getter(description)
	while True:
		mustStop = check_input(f"stop keypress getter?[{remoteStopKey}]: ", remoteStopKey)
		if is_pressed(mainStopKey):
			break
		if mustStop:
			break
	stop_keypress_getter()

import config
import running_time
import subprocess
import sys
if __name__ == "__main__":
	main()	
