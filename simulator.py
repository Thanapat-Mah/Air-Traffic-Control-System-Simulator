import pygame
from configuration import COLOR
from utilities import Converter
import datetime

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=COLOR["dark_gray"], time_step=1, update_period_ratio=1):
		self.__name = name
		self.__name_background_color = name_background_color
		self.__playing = True
		self.__speed = [8, 3, 1]				# time period, less value more speed, first value is current
		self.__zoomed = False		
		self.__running_time_count = 0
		self.__simulated_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)				# simulated datetime
		self.__simulated_time_step = datetime.timedelta(seconds=time_step)				# time step per 1 time tick
		self.__update_period = datetime.timedelta(seconds=time_step*update_period_ratio)# update plane/airport every time period
		self.__delta_simulated_time = datetime.timedelta(seconds=0)						# time since last plane/airport update
		self.__plane_information = {}			# overall plane status Ex. Flying: 3, Landing: 2 etc.
		self.__airport_information = {}			# airport information from AirportManager
		self.__selected_object_code = ""		# IATA code of selected plane or airport object
		self.__selected_object_detail = []

	# return name of simulator
	def get_name(self):
		return(self.__name)

	# return simulated datetime
	def get_simulated_datetime(self):
		return(self.__simulated_datetime)

	# return selected object code
	def get_selected_object_code(self):
		return(self.__selected_object_code)

	# return simulators states
	def get_state(self, state, current=False):		
		state_list = [None]
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

	# update specific state
	def update_state(self, state):
		if state == "play_pause":
			self.__playing = not self.__playing
		elif state == "speed":
			self.__speed.append(self.__speed[0])
			self.__speed = self.__speed[1:]
			self.__running_time_count = 0
		elif state == "zoomed":
			self.__zoomed = not self.__zoomed

	# count time and calculate simulated datetime
	def tick_time(self):
		if self.__playing:
			self.__running_time_count += 1
			# increase simulated datetime by 1 minutes when reach the time period in speed
			if self.__running_time_count%self.get_state("speed", current = True) == 0:
				self.__simulated_datetime += self.__simulated_time_step
				self.__delta_simulated_time += self.__simulated_time_step

	# update plane and airport to next time step, also update information shown on sidebar
	def update_simulator(self, airport_manager, plane_manager, sidebar):
		# tick time
		self.tick_time()
		# get selected object detail
		selected_detail = []
		selected_detail.append(plane_manager.get_detail(code=self.__selected_object_code))
		selected_detail.append(airport_manager.get_detail(code=self.__selected_object_code))
		for detail in selected_detail:
			if detail != "":
				self.__selected_object_detail = detail
		# update plane and get plane information when reach update period
		if self.__delta_simulated_time == self.__update_period:
			self.__plane_information = plane_manager.update_plane(self.__delta_simulated_time, airport_manager=airport_manager)
			self.__delta_simulated_time = datetime.timedelta(seconds = 0)
		else:
			self.__plane_information = plane_manager.update_plane(datetime.timedelta(seconds = 0), airport_manager=airport_manager)		
		# update airport and get airport information
		self.__airport_information = airport_manager.update_airport(plane_manager=plane_manager)
		# update all information on sidebar
		sidebar.update_information(plane_information=self.__plane_information,
			airport_information=self.__airport_information,
			selected_object_detail=self.__selected_object_detail)

	# check for clicking event in simulation, including click on plane, airport or status button on sidebar
	def check_selection(self, event=None, airport_manager=None, plane_manager=None, sidebar=None):
		selected_candidate = []
		selected_candidate.append(plane_manager.check_selection(event))
		selected_candidate.append(airport_manager.check_selection(event))
		selected_candidate.append(sidebar.check_selection(event))
		for code in selected_candidate:
			if code != "":
				self.__selected_object_code = code