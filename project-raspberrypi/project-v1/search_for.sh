#!/bin/bash
(
	main () {
		search_for "$@"
		return 0
	}

	search_for () {
		phrase="$1"; shift
		glob="$1"
		files=$(eval echo $glob)
		for file in $files; {
			lines_matched="$(get_lines_with "$phrase" $file)"
			is_empty $lines_matched && {
				continue
			}
			echo $file
			print_wrapped "$lines_matched" 4
		}
	}

	print_wrapped () {
		str="$1"; shift
		indent=$1
		term_cols=$(tput cols)
		width=$((term_cols - indent))
		wrapped_str=$(echo $str | fold -sw $width | sed -r '{
			s/^/'"$(
				for ((i=0; i<$indent; i++)); {
					echo -n ' ';
				})"'/g
		}')
		echo "$wrapped_str"
	}

	is_empty () {
		! [[ "$@" ]] && {
			return 0
		}
	}

	get_lines_with () {
		phrase="$1"; shift
		file=$1
		lines_matched=$(cat $file 2>/dev/null | sed -rn '{
			/'"$phrase"'/=
		}')
		echo "$lines_matched"
	}

	main "$@"
)
