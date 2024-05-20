#!/usr/bin/env python
from setuptools import Extension, setup, find_packages
import sys
''' Used for installing the package with pip. For development purposes use the other script setup_dev.py
'''
name = "gasparse"
macros = [("RELEASE_BUILD",None)]
setup(  name=name, 
        version="0.0.6a", # Should have used git tag for the version
        packages=find_packages(exclude=("tests",)),
        ext_modules=[Extension(name,["src/gasparse.c","src/multivector_object.c","src/multivector_types.c","src/multivector_large.c","src/multivector_gen.c","src/common.c"],\
        extra_compile_args = ["-O3", "-mpopcnt"],define_macros=macros)],
        # extra_compile_args = ["-O0", "-mpopcnt","-g3"],define_macros=macros)], # comment out when debugging
        description="A python library written entirely in C for Geometric Algebras to deal with sparse multivector arrays",
        long_description = open('docs/source/README.rst').read(),
        license='MIT',
        author="Anon 6666",
        author_email="completelyanonymous6666@gmail.com",
        python_requires=">=3.7"
)
