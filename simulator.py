import pygame
from color import Color

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=Color.dark_gray):
		self.__name = name
		self.__name_background_color = name_background_color
		self.__is_play = [State('Paused', False), State('Playing', True)]
		self.__speed = [State('Fast', 100), State('Normal', 200), State('Slow', 300)]
		self.__zoomed = [State('In', True), State('Out', False)]
		self.__time = 0
		self.__time_delta_count = 0

	# return current playing state (calculated fron is_play)
	def get_is_play(self):
		return(self.__is_play[len(self.__is_play)-1].value)

	# update is_play state
	def update_is_play(self):
		self.__is_play.insert(0, self.__is_play.pop())