import pygame
from color import Color

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=Color.dark_gray):
		self.__name = name
		self.__name_background_color = name_background_color
		# keep state in format (index_of_current_state, (state_label, state_value), ...)
		self.__is_play = [1, ("Playing", True), ("Paused", False)]
		self.__speed = [1, ("Speed", 300), ("Speed", 200), ("Speed", 100)]
		self.__zoomed = [1, ("Zoom", True), ("Zoom", False)]
		self.__time = 0
		self.__time_delta_count = 0

	# return current playing state
	def get_state(self, state, current=False):
		state_list = None
		if state == "play_pause":
			state_list = self.__is_play
		elif state == "speed":
			state_list = self.__speed
		elif state == "zoomed":
			state_list = self.__zoomed
		if current:
			return(state_list[0])
		else:
			return(state_list[1:])

	# update current state of one given state
	def update_single_state(self, state_list):
		if state_list[0] == len(state_list) - 1:
			state_list[0] = 0
		else:
			state_list[0] += 1
		return(state_list)

	# update is_play state
	def update_state(self, state):
		state_list = None
		if state == "play_pause":
			self.__is_play = self.update_single_state(self.__is_play)
		elif state == "speed":
			self.__speed = self.update_single_state(self.__speed)
		elif state == "zoomed":
			self.__zoomed = self.update_single_state(self.__zoomed)