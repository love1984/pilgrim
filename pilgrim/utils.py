# -*- coding: utf-8 -*-
"""
Utility functions for pilgrim
"""

def __defaultopen(file):
	import os, subprocess, sys
	
	if os.name == "posix":
		if sys.platform == "darwin":
			cmd = "open"
		
		cmd = "xdg-open"
	
	elif os.name == "nt":
		cmd = "start"
	
	else:
		raise NotImplementedError("Unsupported os: %r", os.name)
	
	return subprocess.call((cmd, file))

def show(files):
	import tempfile
	
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
	
	if mime == "image/vnd.microsoft.icon":
		return codecs.ICO
	
	if filename.endswith(".blp"):
		return codecs.BLP
	
	if filename.endswith(".ftc") or filename.endswith(".ftu"):
		return codecs.FTEX
