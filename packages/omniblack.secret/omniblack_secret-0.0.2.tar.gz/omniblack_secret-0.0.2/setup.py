from setuptools import setup
from importlib import import_module
from sys import path
from os.path import dirname

path.append(dirname(__file__))
ext_mod = import_module('cflags')
ext = ext_mod.ext

setup(ext_modules=[ext])
