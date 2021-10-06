import pygame
from button import Button
from color import Color

### sidebar at left of screen, display simulation's infomations
class Sidebar:
	def __init__(self, screen_size, toolbar_height, notch_width=20, notch_color=Color.dark_gray, width=200, background_color=Color.dark_gray):
		self.__x = screen_size[0] - notch_width
		self.__y = 0
		self.__width = width
		self.__height = screen_size[1] - toolbar_height
		self.__is_open = False
		self.__notch_width = notch_width
		self.__notch_color = notch_color
		self.__notch_button = Button(x=self.__x-notch_width-10, y=(self.__height-60)/2, width=40, height=60, text="<|",
			border_size=0, border_radius=10, background_color=notch_color)
		self.__background_color = background_color

	# draw sidebar background, notch and notch button
	def draw_background(self, display):
		pass		

	# draw all components on sidebar
	def draw_sidebar(self, display):
		if self.__is_open:
			current_x = self.__x - self.__width
		else:
			current_x = self.__x
		pygame.draw.rect(display, self.__notch_color, (current_x, self.__y, self.__notch_width, self.__height))
		self.__notch_button.draw_button(display=display)