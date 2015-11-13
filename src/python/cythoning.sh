#!/bin/bash

directories=("make_sound" "numerical_formula" "make_image" "make_text_for_read")
files=("gensound" "parseExpression" "makeimage" "makeinfo")

for (( r = 0; r < $((${#files[@]})); r++ )); do
	echo "cythoning ${directories[$r]} process..."
	cd ${directories[$r]}
	cp ${files[$r]}.py ${files[$r]}.pyx
	python setup.py build_ext --inplace 1> /dev/null 2> /dev/null
	cd ..
done

