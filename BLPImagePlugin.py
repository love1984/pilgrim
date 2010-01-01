#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import ImageFile
from struct import pack, unpack, error as StructError
from cStringIO import StringIO

from decoders import dxt1, dxt5

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
			palette.append(unpack("<4B", string.read(4)))
		except StructError:
			break
	return palette

class BLPImageFile(ImageFile.ImageFile):
	"""
	Blizzard Mipmap Format
	"""
	format = "BLP"
	format_description = "Blizzard Mipmap Format"
	
	def show(self):
		path = "/home/adys/.cache/%s.png" % "tmpVfBc3s"
		self.save(path)
		import os
		os.popen("eog %s" % path)
	
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
		
		self.mode = "RGB"
		self.tile = []
		if type == 1: # Uncompressed or DirectX compression
			data = []
			self.fp.seek(offsets[0])
			if encoding == 1: # uncompressed
				print lengths[0]
				_data = StringIO(self.fp.read(lengths[0]))
				while True:
					try:
						offset, = unpack("B", _data.read(1))
					except StructError:
						break
					b, g, r, a = palette[offset]
					if b > 5:
						pass
#						print b, g, r, a
					data.append(pack("BBB", r, g, b))
			
			elif encoding == 2: # directx compression
				if alphaEncoding == 0: # DXT1
					linesize = (self.size[0] + 3) / 4 * 8
					for yb in xrange((self.size[1] + 3) / 4):
						if alphaDepth:
							self.mode = "RGBA"
							decoded = dxt1.decodeDXT1(self.fp.read(linesize), alpha=True)
						else:
							decoded = dxt1.decodeDXT1(self.fp.read(linesize))
						for d in decoded:
							data.append(d)
				
				elif alphaEncoding in (1, 7): # DXT3, DXT5
					linesize = (self.size[0] + 3) / 4 * 16
					self.mode = "RGBA"
					for yb in xrange((self.size[1] + 3) / 4):
						decoded = dxt5.decodeDXT5(self.fp.read(linesize))
						for d in decoded:
							data.append(d)
				
				else:
					raise NotImplementedError
				
			data = "".join(data)
			self.im = Image.core.new(self.mode, self.size)
			return self.fromstring(data)
		else:
			raise NotImplementedError

Image.register_open("BLP", BLPImageFile)
Image.register_extension("BLP", ".blp")
