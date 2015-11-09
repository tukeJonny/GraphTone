#! -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension( "makeimage", ["makeimage.pyx"] ),
    #Extension( "parseExpression", ["parseExpression.pyx"])
]

setup(
    name = "make image",
    cmdclass = { "build_ext" : build_ext },
    ext_modules = ext_modules,
)