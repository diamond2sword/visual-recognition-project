#!/bin/bash

temp_path="/root/Desktop/project"
repo_path="/root/visual-recognition-project/project-raspberrypi/project-v1"
git_path="/root/visual-recognition-project/git.sh"

x-terminal-emulator -e '{
	#!/bin/bash
	cp -vf $(ls -d  '"$temp_path"'/* | sed -n "/^.*[py|sh]$/p" | tr "\n" " ") '"$repo_path"'
	diff '"$temp_path"' '"$repo_path"'
	'"$git_path"' GIT_PUSH
	read 
}'

