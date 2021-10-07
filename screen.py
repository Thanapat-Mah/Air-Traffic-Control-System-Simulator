import pygame
from color import Color

### screen of program, adjust and display component.
class Screen:
	def __init__(self, fullscreen=False, width=1500, height=750, background_color=Color.dark_gray):
		self.__fullscreen = fullscreen
		# if fullsreen, adjust width and height to fit user's display size
		if fullscreen:
			info_object = pygame.display.Info()
			self.__width = info_object.current_w
			self.__height = info_object.current_h
		else:
			self.__width = width
			self.__height = height
		self.__background_color = background_color
		self.display = pygame.display.set_mode((self.__width, self.__height))

	# return the size of screen in format (width, height)
	def get_size(self):
		return((self.__width, self.__height))

	# refresh plain color background
	def refresh_background(self):
		self.display.fill(self.__background_color)

	# draw name of simulation
	def draw_name(self):
		pass

	# update screen by re-draw every components
	def update_screen(self, map=None, airport=None, sidebar=None, toolbar=None):
		self.refresh_background()
		toolbar.draw_toolbar(self.display)
		sidebar.draw_sidebar(self.display)