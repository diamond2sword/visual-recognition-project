#!/bin/bash

main () {
	is_buffer_empty && {
		exit 1
	}
	(reset_buffer)
	! is_key_in_buffer && {
		exit 1
	}
	exit 0
	
}

TEST_KEY=$1
BUFFER_PATH="$2"
BUFFER=$(cat "$BUFFER_PATH")

reset_buffer () {
	echo -n "" > "$BUFFER_PATH"
}

is_key_in_buffer () {
	echo "$BUFFER" | sed -n '{
		/'"$TEST_KEY"'/{
			Q0
		}
		Q1
	}'
	return $?
}

is_buffer_empty () {
	 ! [ "$BUFFER" ] && {
	 	return 0
	 }
}

main
