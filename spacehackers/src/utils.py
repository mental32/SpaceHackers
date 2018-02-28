##
# -*- coding: utf-8 -*-
##
import os
import time

from PIL import Image

def _NEWUSER(name):
	return {
		'name': name,
		'created_at': int(time.time())
	}

def extract_gif_frames(gif, outfolder='images/animated/', yield_filenames=False):
	frame = Image.open(gif)
	files = []
	nframes = 0

	while frame:
		fp = '%s/%s-%s.gif' %(outfolder, os.path.basename(gif), nframes)
		files.append(fp)
		frame.save(fp, 'GIF')
		nframes += 1
		if yield_filenames:
			yield fp
		try:
			frame.seek(nframes)
		except EOFError:
			break
	return files

class looping_image:
	def __init__(self, images):
		if not isinstance(images, list):
			self.images = [images]
		else:
			self.images = images

		self.poller = self.poll_next_image()

	def poll_next_image(self):
		yield self.images[0]
		for images in self.images:
			yield images

	def poll(self):
		try:
			return next(self.poller)
		except StopIteration:
			self.poller = self.poll_next_image()
			return next(self.poller)
