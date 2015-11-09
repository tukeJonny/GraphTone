#!/bin/bash

#make sound
echo "cythoning make_sound process..."
cd make_sound
cp gensound.py gensound.pyx
python setup.py build_ext --inplace 1> /dev/null 2> /dev/null
cd ..

#parse exp
echo "cythoning parseExpresson process..."
cd numerical_formula
cp parseExpression.py parseExpression.pyx
python setup.py build_ext --inplace 1> /dev/null 2> /dev/null
cd ..

#make png
echo "cythoning make_image process..."
cd make_image
cp makeimage.py makeimage.pyx
python setup.py build_ext --inplace 1> /dev/null 2> /dev/null
