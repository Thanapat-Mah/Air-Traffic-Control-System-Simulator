import pygame
from styles import Color
import datetime

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=Color.dark_gray):
		self.__name = name
		self.__name_background_color = name_background_color
		# keep state in format (index_of_current_state, (state_label, state_value), ...)
		self.__is_play = [1, ("Playing", True), ("Paused", False)]
		self.__speed = [1, ("Speed", 200), ("Speed", 50), ("Speed", 1)]
		self.__zoomed = [1, ("Zoom", False), ("Zoom", True)]
		self.__running_time_count = 0
		self.__simulated_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)

	# return name of simulator
	def get_name(self):
		return(self.__name)

	# return simulated datetime
	def get_simulated_datetime(self):
		return(self.__simulated_datetime)

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
			return(state_list[state_list[0]])
		else:
			return(state_list[1:])

	# update current state of one given state
	def update_single_state(self, state_list):
		if state_list[0] == len(state_list) - 1:
			state_list[0] = 1
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
			self.__running_time_count = 0
		elif state == "zoomed":
			self.__zoomed = self.update_single_state(self.__zoomed)

	# count time and calculate simulated datetime
	def tick_time(self):
		if self.__is_play[0] == 1:
			self.__running_time_count += 1
			if self.__running_time_count%self.get_state("speed", current=True)[1] == 0:
				self.__simulated_datetime += datetime.timedelta(minutes = 1)
