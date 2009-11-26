#!/usr/bin/python
# -*- coding: utf-8 -*-

import Image
import ImageFile
from struct import unpack
from cStringIO import StringIO

##
# Independence War 2: Edge Of Chaos - Texture File Format
# Copyright © 2001 Particle Systems Ltd, All Rights Reserved.
# Version 1.0
# 16 October 2001
#
# The textures used for 3D objects in Independence War 2: Edge Of Chaos are in a
# packed custom format called FTEX. This file format uses file extensions FTC and FTU.
#
# * FTC files are compressed textures (using standard texture compression).
# * FTU files are not compressed.
#
# The game will happily use IFF format textures if they are present, but the
# packed textures are used to decrease load times (compressing textures on the fly is
# expensive) and give better image quality, since the mipmaps can be generated offline
# using a slow but effective filter.
#
# This document describes the FTEX file format specification for those users who are
# interested in converting the game’s textures into an editable form, or who want to
# convert their own textures into the game’s optimal format.
#

def pythonDecodeDXT1(data):
	"""
	Python-only DXT1 decoder; this is slow!
	Better to use _dxt1.decodeDXT1 if you can
	(it's used automatically if available by DdsImageFile)
	input: one "row" of data (i.e. will produce 4*width pixels)
	"""
	blocks = len(data) / 8  # number of blocks in row
	out = ['', '', '', '']  # row accumulators
	
	for xb in xrange(blocks):
		# Decode next 8-byte block.
		c0, c1, bits = unpack('<HHI', data[xb*8:xb*8+8])
		
		# color 0, packed 5-6-5
		r0 = (c0 & 0x1f) << 3
		g0 = ((c0 >> 5) & 0x3f) << 2
		b0 = ((c0 >> 11) & 0x1f) << 3
		
		# color 1, packed 5-6-5
		r1 = (c1 & 0x1f) << 3
		g1 = ((c1 >> 5) & 0x3f) << 2
		b1 = ((c1 >> 11) & 0x1f) << 3
		
		# Decode this block into 4x4 pixels
		# Accumulate the results onto our 4 row accumulators
		for yo in xrange(4):
			for xo in xrange(4):
				# get next control op and generate a pixel
				
				control = bits & 3
				bits = bits >> 2
				if control == 0:
					out[yo] += chr(r0) + chr(g0) + chr(b0)
				elif control == 1:
					out[yo] += chr(r1) + chr(g1) + chr(b1)
				elif control == 2:
					if c0 > c1:
						out[yo] += chr((2 * r0 + r1) / 3) + chr((2 * g0 + g1) / 3) + chr((2 * b0 + b1) / 3)
					else:
						out[yo] += chr((r0 + r1) / 2) + chr((g0 + g1) / 2) + chr((b0 + b1) / 2)
				elif control == 3:
					if c0 > c1:
						out[yo] += chr((2 * r1 + r0) / 3) + chr((2 * g1 + g0) / 3) + chr((2 * b1 + b0) / 3)
					else:
						out[yo] += "\0\0\0"
	return tuple(out)

class FTEXImageFile(ImageFile.ImageFile):
	"""
	Texture File Format
	The FTC and FTU texture files both use the same format, called. This
	has the following structure:
	{header}
	{format_directory}
	{data}
	Where:
	{header} = { u32:magic, u32:version, u32:width, u32:height, u32:mipmap_count, u32:format_count }
	
	* The "magic" number is "FTEX".
	* "width" and "height" are the dimensions of the texture.
	* "mipmap_count" is the number of mipmaps in the texture.
	* "format_count" is the number of texture formats (different versions of the same texture) in this file.
	
	{format_directory} = format_count * { u32:format, u32:where }
	
	The format value is 0 for DXT1 compressed textures and 1 for 24-bit RGB uncompressed textures.
	The texture data for a format starts at the position "where" in the file.
	
	Each set of texture data in the file has the following structure:
	{data} = format_count * { u32:mipmap_size, mipmap_size * { u8 } }
	* "mipmap_size" is the number of bytes in that mip level. For compressed textures this is the
	size of the texture data compressed with DXT1. For 24 bit uncompressed textures, this is 3 * width * height.
	Following this are the image bytes for that mipmap level.
	
	Note: All data is stored in little-Endian (Intel) byte order.
	"""
	format = "FTEX"
	format_description = "Texture File Format"
	
	def _open(self):
		header = StringIO(self.fp.read(24))
		magic = header.read(4)
		if magic != "FTEX":
			raise SyntaxError("not a FTEX file")
		version = unpack("i", header.read(4))
		self.size = unpack("ii", header.read(8))
		linesize = (self.size[0] + 3) / 4 * 8
		mipmap_count, format_count = unpack("ii", header.read(8))
		self.mode = "RGB"
		
		self.tile = []
		for i in range(format_count):
			format, where = unpack("ii", self.fp.read(8))
			if format == 0:
				data = []
				self.fp.seek(where)
				size, = unpack("i", self.fp.read(4))
				for yb in xrange((self.size[1] + 3) / 4):
					decoded = pythonDecodeDXT1(self.fp.read(linesize))
					
					for d in decoded:
						# Make sure that if we have a texture size that's not a
						# multiple of 4 that we correctly truncate the returned data
						data.append(d[:self.size[0]*3])
						#assert len(d) == len(d[:self.size[0]*3])
				data = "".join(data[:self.size[1]])
				self.im = Image.core.new(self.mode, self.size)
				return self.fromstring(data)
			elif format == 1: # Uncompressed RGB
				self.tile.append(("raw", (0, 0) + self.size, where+4, (self.mode, 0, 1)))
			else:
				raise ValueError("Invalid texture format (expected 0 or 1, got %i)" % (format))

Image.register_open("FTEX", FTEXImageFile)
Image.register_extension("FTEX", ".ftu") # uncompressed
Image.register_extension("FTEX", ".ftc") # compressed
