# -*- coding: utf-8 -*-

from struct import unpack

def decodeDXT1(data):
	"""
	Python-only DXT1 decoder; this is slow!
	Better to use _dxt1.decodeDXT1 if you can
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