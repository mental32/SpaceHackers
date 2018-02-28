##
# -*- coding: utf-8 -*-
##
import pygame

class Player:
	def __init__(self, game, save):
		self.game = game
		self.save = save
		self.loc = (0, 0)
		self.displacement = (0, 0)
		self.speed = 10

		self.ship_type = save.get('ship_type', 'falcon')
		self.image = game.images[self.ship_type]

	def compute_displacement(self):
		self.loc = self.loc[0] + self.displacement[0], self.loc[1] + self.displacement[1]

	def scale(self, *args, **kwargs):
		self.image = pygame.transform.scale(self.image, *args, **kwargs)
		return self.image

	def render(self):
		'''an alias to game.screen.blip(player.image, player.loc)'''
		self.game.screen.blit(self.image, self.loc)
