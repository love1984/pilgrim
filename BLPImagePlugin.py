#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import ImageFile
from struct import pack, unpack
from cStringIO import StringIO

from decoders import dxt1

##
# Blizzard Mipmap Format
#

def getpalette(string):
	"""
	Transform a StringIO object into a palette
	"""
	palette = []
	while True:
		try:
			palette.append(unpack("4B", string.read(4)))
		except Exception:
			break
	return palette

class BLPImageFile(ImageFile.ImageFile):
	"""
	Blizzard Mipmap Format
	"""
	format = "BLP"
	format_description = "Blizzard Mipmap Format"
	
	def _open(self):
		header = StringIO(self.fp.read(20 + 16*4 + 16*4)) # XXX
		magic = header.read(4)
		if magic != "BLP2":
			raise ValueError("not a BLP2 file")
		type, = unpack("i", header.read(4))
		encoding, alphaDepth, alphaEncoding, hasMips = unpack("4b", header.read(4))
		self.size = unpack("ii", header.read(8))
		offsets = unpack("16i", header.read(16*4))
		lengths = unpack("16i", header.read(16*4))
		palette = getpalette(StringIO(self.fp.read(256*4)))
		print "type: %i, encoding: %i, aEncoding: %i, aDepth: %i" % (type, encoding, alphaEncoding, alphaDepth)
		
		linesize = (self.size[0] + 3) / 4 * 8
		self.mode = "RGB"
		self.tile = []
		if type == 1:
			if encoding == 1: # uncompressed
				self.fp.seek(offsets[1])
				data = StringIO(self.fp.read(lengths[1]))
				_data = []
				while True:
					try:
						offset, = unpack("B", data.read(1))
					except Exception:
						break
					r, g, b, a = palette[offset]
					_data.append(pack("iii", r, g, b))
				self.im = Image.core.new(self.mode, self.size)
				return self.fromstring("".join(data))
			elif encoding == 2: # directx compression
				data = []
				self.fp.seek(offsets[1])
				#data.append(dxt1.decodeDXT1(self.fp.read(lengths[1])))
				for yb in xrange((self.size[1] + 3) / 4):
					decoded = dxt1.decodeDXT1(self.fp.read(linesize))
					for d in decoded:
						data.append(d[:self.size[0]*3])
				data = "".join(data[:self.size[1]])
				self.im = Image.core.new(self.mode, self.size)
				return self.fromstring(data)

Image.register_open("BLP", BLPImageFile)
Image.register_extension("BLP", ".blp")
