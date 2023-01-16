#!/bin/bash

main() {
	run "$@"
}

run () {
	glob="$1"; shift
	str1="$1"; shift
	str2="$1"
	for path in $(eval echo $glob); {
		echo "$path"
		sed -i "s/$str1/$str2/g" $path
	}
}

main "$@"
