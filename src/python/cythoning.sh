#!/bin/bash

directories=("make_sound" "numerical_formula" "make_image")
files=("gensound" "parseExpression" "makeimage")

for r in {0..2}; do
	echo "cythoning ${directories[$r]} process..."
	cd ${directories[$r]}
	cp ${files[$r]}.py ${files[$r]}.pyx
	python setup.py build_ext --inplace 1> /dev/null 2> /dev/null
	cd ..
done
