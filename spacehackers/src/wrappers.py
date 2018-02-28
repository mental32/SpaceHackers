##
# -*- coding: utf-8 -*-
##
import os
import json

import pygame

from . import utils
from .scenes import *

class Game:
	pygame.init()

	def __init__(self):
		self.width = 1366
		self.height = 768
		self.running = False
		self.images = {}
		self.save_file = None

		utils.make_dir('saves/', overwrite=False)

	@property
	def saves(self):
		return [json.load(open('saves/' + fp)) for fp in os.listdir('saves/') if fp.endswith('.json')]

	def make_save(self, fp):
		json.dump(utils._NEWUSER(fp), open('saves/' + fp + '.json', 'w'))

	def display_text(self, text, position, font='freesansbold.ttf', size=80, colour=None):
		_font = pygame.font.Font(font, size)
		surface = _font.render(text, True, colour or (0, 0, 0))
		rect = surface.get_rect()
		rect.center = position
		self.screen.blit(surface, rect)

	def load_image(self, fp, name=None):
		if fp.endswith('.gif'):
			self.images[name or fp] = [pygame.image.load(img) for img in utils.extract_gif_frames(fp, yield_filenames=True)]
		else:
			self.images[name or fp] = pygame.image.load(fp)

	def rot_center(self, surf, angle):
			"""rotate an image while keeping its center
			sourced from: https://stackoverflow.com/questions/28261163/out-of-memory-when-using-pygame-transform-rotate"""
			image, rect = surf, surf.get_rect()
			rot_image = pygame.transform.rotate(image, angle)
			rot_rect = rot_image.get_rect(center=rect.center)
			return rot_image, rot_rect

	def run(self):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode([self.width, self.height], pygame.FULLSCREEN)
		pygame.display.set_caption('SpaceHackers')

		self.running = True
		next_scene = None
		main_menu = scenes['main_menu']

		while self.running:
			if next_scene is None:
				next_scene = main_menu(self)
			else:
				next_scene = scenes[next_scene](self)
