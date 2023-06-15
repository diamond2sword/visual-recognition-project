#!/bin/bash

main () {
	fix_indents
	run $1
	return 0
}

run () {
	[[ "$1" ]] && {
		python3 ./$1
	}
}

fix_indents () {
	two_spc='  '
	./replace_str.sh '*.py' "$two_spc$two_spc" '\t'
	./replace_str.sh '*.sh' "$two_spc$two_spc" '\t'
}

main "$@"
