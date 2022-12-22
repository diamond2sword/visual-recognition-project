#!/bin/bash

main () {
	is_pressed=$(check_buffer_for_key)
	#reset_buffer
	echo $is_pressed
}

TEST_KEY=$1
BUFFER_PATH="$2"

reset_buffer () {
	echo "" > "$BUFFER_PATH"
}

check_buffer_for_key () {
	sed -n '{
		/'"$TEST_KEY"'/{
			q0
		}
		q1
	}' "$BUFFER_PATH"
	is_pressed=$?
	echo $is_pressed
	
}

main
