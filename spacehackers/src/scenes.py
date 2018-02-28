##
# -*- coding: utf-8 -*-
##
import time
import string
import random

import pygame

from . import (colours, utils, player)

__all__ = ['scenes']
scenes = {}

def scene(func):
	'''decorator to neatly collect all the scenes'''
	scenes[func.__name__] = func

@scene
def main_menu(game):
	def make_selected_option(text, option, message=''):
		if text.lower() == option:
			return text + ' <- ' + message
		else:
			return text

	next_scene = None
	_string = ''
	nested_selection = False
	new_account = False
	save_option = (game.saves[0]['name'] if game.saves else None)
	save_options = [save['name'] for save in game.saves]
	patterns = [[]]
	option = 'play'
	options = ['play', 'new', 'load', 'exit']
	game.load_image('images/space_background.gif', name='space')
	background = utils.looping_image(game.images['space'])

	for i in range(2):
		for x in range(0, game.width, 282):
			for y in range(0, game.height, 199):
				patterns[-1].append((background.poll(), (x, y)))
		else:
			patterns.append([])

	while game.running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False

			elif event.type == pygame.KEYDOWN:
				if nested_selection:
					if event.key == pygame.K_DOWN:
						save_option = save_options[(save_options.index(save_option) + 1) % len(save_options)]
					elif event.key == pygame.K_UP:
						save_option = save_options[(save_options.index(save_option) - 1)]
					elif event.key == pygame.K_RETURN:
						game.save_file = save_option
					elif event.key == pygame.K_BACKSPACE:
						nested_selection = False
				elif new_account:
					if chr(event.key).lower() in string.ascii_lowercase:
						_string += chr(event.key)
					elif event.key == pygame.K_RETURN:
						game.make_save(_string)
						game.save = _string
						return 'main_game'
					elif event.key == pygame.K_BACKSPACE:
						new_account = False
				else:
					if event.key == pygame.K_DOWN:
						option = options[(options.index(option) + 1) % len(options)]
					elif event.key == pygame.K_UP:
						option = options[(options.index(option) - 1)]

					elif event.key == pygame.K_RETURN:
						if option == 'play':
							return 'main_game'
						elif option == 'load':
							nested_selection = True
						elif option == 'new':
							new_account = True
						else:
							game.running = False
							return None

		game.screen.fill(colours.black)
		if int(time.time()) % 2 == 0:
			for item in patterns[0]:
				game.screen.blit(*item)
		else:
			for item in patterns[1]:
				game.screen.blit(*item)

		game.display_text('SpaceHackers', (190, 40), size=50, colour=colours.white)
		for index, opt in enumerate(options):
			offset = 100 + (50 * index)
			game.display_text(make_selected_option(opt.title(), option), (40, offset), size=20, colour=colours.white)

		if nested_selection:
			for index, save in enumerate(game.saves):
				x, y = game.width // 2 // 2, (200) + (45 * index)
				game.display_text(make_selected_option(save['name'], save_option), (x, y), size=20, colour=colours.white)
			game.display_text('saves (%s found)'%(str(len(game.saves))), (game.width // 2 // 2 + 50, 160), size=30, colour=colours.white)

		elif new_account:
			game.display_text('Name: ', (game.width // 2, game.height // 2 - 50), size=30, colour=colours.white)
			game.display_text(_string, (game.width // 2, game.height // 2), size=30, colour=colours.white)

		pygame.display.update()

@scene
def main_game(game):
	game.load_image('images/falcon.png', name='falcon')
	game.load_image('images/space.jpg', name='space')

	user = player.Player(game, {})
	user.scale((80, 100))

	while game.running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game.running = False
				return None

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					_dis = user.displacement
					user.displacement = _dis[0], -user.speed

				elif event.key == pygame.K_DOWN:
					_dis = user.displacement
					user.displacement = _dis[0], user.speed

				elif event.key == pygame.K_LEFT:
					user.rotate(5)

				elif event.key == pygame.K_RIGHT:
					user.rotate(-5)

				elif event.key == pygame.K_BACKSPACE:
					return None

		game.screen.fill(colours.black)
		game.screen.blit(pygame.transform.scale(game.images['space'], (game.width, game.height)), (0, 0))
		user.render()
		# game.display_text('Hello This is the main game event loop.', (600, 400), size=30, colour=colours.white)
		pygame.display.update()
