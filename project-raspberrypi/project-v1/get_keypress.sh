#!/bin/bash





main () {
	reset_buffer
	get_keypress
}

BUFFER_PATH="/root/buffer"

get_keypress () {
	while true; do {
		get_keypress_once
	} done
}

reset_buffer () {
	touch "$BUFFER_PATH"
	echo "" > "$BUFFER_PATH"
}

get_keypress_once () {
	display_keypress
	read_keypress
	save_keypress
}

save_keypress () {
	sed -i '{
		$ {
			s/$/'"$KEYPRESS"'/
		}
	}' "$BUFFER_PATH"
}

read_keypress () {
	read -sn1 KEYPRESS
}

display_keypress () {	
	echo -en "\rpressed key: $KEYPRESS\r"
}

main
