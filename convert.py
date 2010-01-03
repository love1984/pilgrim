#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from BLPImagePlugin import BLPImageFile as BLP
from FTEXImagePlugin import FTEXImageFile as FTEX

usage = "Usage: %s image.{blp,ftc,...}" % (sys.argv[0])

def main():
	try:
		args = sys.argv[1:]
	except IndexError:
		print usage
		exit()
	for f in args:
		print "Converting...", f
		flower = f.lower()
		if flower.endswith(".blp"):
			BLP(f).save(f+".png")
		elif flower.endswith(".ftc") or flower.endswith(".ftu"):
			FTEX(f).save(f+".png")
		else:
			print "Unknown file format for %s..." % (f)
			print usage
	exit()

if __name__ == "__main__":
	main()
