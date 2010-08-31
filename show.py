#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from pilgrim.BLPImagePlugin import BLPImageFile as BLP
from pilgrim.FTEXImagePlugin import FTEXImageFile as FTEX
from pilgrim.utils import show

usage = "Usage: %s image.{blp,ftc,...}" % (sys.argv[0])


def main():
	try:
		args = sys.argv[1:]
	except IndexError:
		print usage
		exit()
	for f in args:
		flower = f.lower()
		if flower.endswith(".blp"):
			show(BLP(f))
		elif flower.endswith(".ftc") or flower.endswith(".ftu"):
			show(FTEX(f))
		else:
			print "Unknown file format for %s..." % (f)
			print usage
	exit()

if __name__ == "__main__":
	main()
