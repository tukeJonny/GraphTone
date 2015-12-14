#! -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension( "parseExpression", ["parseExpression.pyx"] ),
    Extension( "add_multiplication", ["add_multiplication.pyx"])
]

setup(
    name = "parseExpression",
    cmdclass = { "build_ext" : build_ext },
    ext_modules = ext_modules,
)