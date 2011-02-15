#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os.path import exists, splitext
from pilgrim.utils import getDecoder, show

usage = "Usage: %s image.{blp,ftc,...}" % (sys.argv[0])

def main():
	try:
		args = sys.argv[1:]
	except IndexError:
		print usage
		exit(1)
	
	files = []
	for f in args:
		if not exists(f):
			print "%r: No such file or directory" % (f)
		
		codec = getDecoder(f)
		if codec:
			print "Converting...", f
			name, _ = splitext(f)
			files.append(codec(f))
		else:
			print "Unknown file format for %s..." % (f)
			print usage
	
	show(files)

if __name__ == "__main__":
	main()
