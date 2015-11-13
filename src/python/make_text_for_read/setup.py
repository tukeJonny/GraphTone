#! -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension( "makeinfo", ["makeinfo.pyx"] ),
]

setup(
    name = "make say command information",
    cmdclass = { "build_ext" : build_ext },
    ext_modules = ext_modules,
)