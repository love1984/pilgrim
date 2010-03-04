#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup, Extension

dxtc = Extension('dxtc',
		define_macros = [('MAJOR_VERSION', '1'),
							('MINOR_VERSION', '0')],
		include_dirs = ['/usr/local/include'],
		library_dirs = ['/usr/local/lib'],
		sources = ['decoders/_dxtc.c'])

setup(name = 'image',
		version = '1.0',
		description = 'Python image package',
		author = 'Jerome Leclanche',
		author_email = 'adys.wh@gmail.com',
		url = 'http://docs.python.org/extending/building',
		long_description = "Testing...",
		ext_modules = [dxtc])
