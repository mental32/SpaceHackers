##
# -*- coding: utf-8 -*-
##
try:
	import pygame
	import PIL
except ImportError:
	raise ImportError('SpaceHackers needs the following modules: %s, %s'%('pygame', 'pillow'))

from src.wrappers import Game

def main():
	Game().run()

if __name__ == '__main__':
	main()
