#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os.path import exists, splitext
from pilgrim.utils import getDecoder

usage = "Usage: %s image.{blp,ftc,...}" % (sys.argv[0])

def main():
	try:
		args = sys.argv[1:]
	except IndexError:
		print usage
		exit(1)
	
	for f in args:
		if not exists(f):
			print "%r: No such file or directory" % (f)
		
		codec = getDecoder(f)
		if codec:
			print "Converting...", f
			name, = splitext(f)
			return codec(f).save(name + ".png")
		else:
			print "Unknown file format for %s..." % (f)
			print usage

if __name__ == "__main__":
	main()
