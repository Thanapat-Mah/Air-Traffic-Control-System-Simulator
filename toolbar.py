import pygame
from color import Color
from font import Font
from button import Button
from button import QuitButton
from button import MultiStateButton
from icon_loader import *

### toolbar at bottom side of screen, provide tool for modify simulation behavior
class Toolbar:
	def __init__(self, screen_size, height, background_color=Color.dark_gray, font=Font.roboto_normal):
		self.__x = 0
		self.__y = screen_size[1] - height	# adjust position to buttom of screen
		self.__width = screen_size[0]
		self.__height = height
		self.__background_color = background_color
		# self.__simulated_datetime = None
		self.__font = font
		# initiate play-pause button
		self.__play_pause_button = MultiStateButton(icon_tuple=load_icons(30, "icon_playing.png", "icon_paused.png"),
			x=200, y=self.__y+10, width=100, height=self.__height-20, text="Multi")
		self.__speed_button = Button(x=350, y=self.__y+10, width=100, height=self.__height-20)
		self.__zoom_button = None
		self.__quit_button = QuitButton(x=self.__width-120, y=self.__y+10, width=100, height=self.__height-20)

	# draw simulated datetime on toolbar
	def draw_datetime(self, display):
		pass

	# draw button on toolbar
	def draw_button(self, display):
		self.__play_pause_button.draw_button(display)
		self.__speed_button.draw_button(display)
		self.__quit_button.draw_button(display)

	# draw all componenets on toolbar
	def draw_toolbar(self, display):
		# draw background
		pygame.draw.rect(display, self.__background_color, (self.__x, self.__y, self.__width, self.__height))
		self.draw_button(display=display)

	# check event on toolbar
	def check_event(self, event):
		self.__quit_button.click(event)
