# -*- coding: utf-8 -*-
"""
Utility functions for pilgrim
"""

def __defaultopen(file):
	import os, subprocess
	if os.name == "mac":
		return subprocess.call(("open", file))
	if os.name == "nt":
		return subprocess.call(("start", file))
	if os.name == "posix":
		return subprocess.call(("xdg-open", file))
	
	raise NotImplementedError("Unsupported os: %r", os.name)

def show(files):
	import tempfile
	images = []
	for img in files:
		tmp, filename = tempfile.mkstemp(suffix=".png")
		img.save(filename)
		__defaultopen(filename)

def getDecoder(filename):
	from mime import MimeType
	from . import codecs
	filename = filename.lower()
	mime = MimeType.fromName(filename)
	
	if mime == "image/png":
		return codecs.PNG
	
	if filename.endswith(".blp"):
		return codecs.BLP
	
	if filename.endswith(".ftc") or filename.endswith(".ftu"):
		return codecs.FTEX
