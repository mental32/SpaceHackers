##
# -*- coding: utf-8 -*-
##
import pygame

class Player:
	def __init__(self, game, save):
		self.game = game
		self.save = save
		self.loc = (400, 400)
		self.displacement = (0, 0)
		self.speed = 10

		self.rotating = False
		self.rotating_offset = 0
		self.rotated_offset = 0

		self.ship_type = save.get('ship_type', 'falcon')
		self.surface = game.images[self.ship_type]

	def compute_displacement(self):
		self.loc = self.loc[0] + self.displacement[0], self.loc[1] + self.displacement[1]

	def scale(self, *args, **kwargs):
		self.surface = pygame.transform.scale(self.surface, *args, **kwargs)
		return self.surface

	def rotate(self, degrees):
		self.rotating_offset += degrees
		self.rotating = True

	def render(self):
		'''an alias to game.screen.blip(player.image, player.loc)'''
		if self.rotating:
			surface, rect = self.game.rot_center(self.surface, self.rotated_offset)
			rect.center = self.loc
			self.rotated_offset += self.rotating_offset
		else:
			surface = self.surface
			rect = surface.get_rect()
			rect.center = self.loc

		self.game.screen.blit(surface, rect)
