# -*- coding: utf-8 -*-

def show(img, viewer="eog"):
	import os, tempfile, time, subprocess
	tmp, filename = tempfile.mkstemp(suffix=".png")
	img.save(filename)
	subprocess.Popen([viewer, filename])
	time.sleep(0.2)
	os.remove(filename)
