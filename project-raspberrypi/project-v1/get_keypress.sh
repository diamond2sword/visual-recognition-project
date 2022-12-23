#!/bin/bash

main () {
	display_description
	get_keypress
}

init () {
	def_must_stop_keypress_getter
	def_display_description
}

BUFFER_PATH="$1"; shift
STOP_WORD="$1"; shift
DESCRIPTION=("$@")


get_keypress () {
	while true; do {
		get_keypress_once
		must_stop_keypress_getter && {
			exit
		}
	} done
}

def_display_description () {
	! [ "$DESCRIPTION" ] && {
		display_description () { :; }
	}
}

def_must_stop_keypress_getter () {
	! [ "$STOP_WORD" ] && {
		must_stop_keypress_getter () { :; }
	}
}

get_keypress_once () {
	display_keypress
	read_keypress
	save_keypress
}

display_description () {
	echo "$DESCRIPTION"
}

must_stop_keypress_getter () {
	get_current_buffer
	is_buffer_empty && {
		return 1
	}
	! is_stop_word_in_buffer && {
		return 1
	}
	return 0
}

save_keypress () {
	echo -n "$KEYPRESS" >> "$BUFFER_PATH"
}

read_keypress () {
	read -t .1 -sn1 KEYPRESS
}

display_keypress () {
	echo -en "\rpressed key: $KEYPRESS\r"
}

is_stop_word_in_buffer () {
	echo "$BUFFER" | sed -n '{
		/'"$STOP_WORD"'/{
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

get_current_buffer () {
	BUFFER=$(cat "$BUFFER_PATH")
}

init
main
