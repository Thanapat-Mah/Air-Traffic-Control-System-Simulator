import pygame
from color import Color
import datetime

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=Color.dark_gray):
		self.__name = name
		self.__name_background_color = name_background_color
		self.__playing = True
		self.__speed = [200, 50, 1]		# time period, less value more speed, first value is current
		self.__zoomed = False
		self.__running_time_count = 0
		self.__simulated_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)

	# return name of simulator
	def get_name(self):
		return(self.__name)

	# return simulated datetime
	def get_simulated_datetime(self):
		return(self.__simulated_datetime)

	# return simulators states
	def get_state(self, state, current=False):		
		state_list = None
		# calculate all possible state
		if state == "play_pause":
			state_list = [self.__playing, not self.__playing]
		elif state == "speed":
			state_list = self.__speed
		elif state == "zoomed":
			state_list = [self.__zoomed, not self.__zoomed]
		# return only current value
		if current:
			return(state_list[0])
		# return all possible value for specific state
		else:
			return(state_list)

	# update is_play state
	def update_state(self, state):
		state_list = None
		if state == "play_pause":
			self.__playing = not self.__playing
		elif state == "speed":
			self.__speed.append(self.__speed[0])
			self.__speed = self.__speed[1:]
		elif state == "zoomed":
			self.__zoomed = not self.__zoomed

	# count time and calculate simulated datetime
	def tick_time(self):
		if self.__playing:
			self.__running_time_count += 1
			if self.__running_time_count%self.get_state("speed", current=True) == 0:
				self.__simulated_datetime += datetime.timedelta(minutes = 1)
