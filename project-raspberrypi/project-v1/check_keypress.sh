#!/bin/bash

main () {
	is_pressed=$(check_buffer_for_key)
	reset_buffer
	exit $is_pressed
}

TEST_KEY=$1
BUFFER_PATH="$2"

reset_buffer () {
	echo "" > "$BUFFER_PATH"
}

check_buffer_for_key () {
	is_pressed=$(sed -n '{
		/'"$TEST_KEY"'/!{
			q1
		}
	}' "$BUFFER_PATH")
	return $is_pressed
}

main
