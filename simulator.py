import pygame
from configuration import COLOR
from utilities import Converter
import datetime

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, name_background_color=COLOR["dark_gray"]):
		self.__name = name
		self.__name_background_color = name_background_color
		self.__playing = True
		self.__speed = [80, 30, 10]			# time period, less value more speed, first value is current
		self.__zoomed = False		
		self.__running_time_count = 0
		self.__simulated_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)
		self.__plane_status = {}			# overall plane status Ex. Flying: 3, Landing: 2 etc.
		self.__airport_status = {}		# overall airport status Ex. Empty: 3, In Use: 2
		self.__selected_object_code = ""	# IATA code of selected plane or airport object
		self.__selected_object_detail = []

	# return name of simulator
	def get_name(self):
		return(self.__name)

	# return simulated datetime
	def get_simulated_datetime(self):
		return(self.__simulated_datetime)

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
		elif state == "zoomed":
			self.__zoomed = not self.__zoomed

	# count time and calculate simulated datetime
	def tick_time(self):
		if self.__playing:
			self.__running_time_count += 1
			# increase simulated datetime by 1 minutes when reach the time period
			if self.__running_time_count%self.get_state("speed", current=True) == 0:
				self.__simulated_datetime += datetime.timedelta(minutes = 1)

	# update plane and airport to next time step
	def mock_update_simulator(self, airport_manager=None, plane_manager=None):
		self.__plane_status = plane_manager.mock_update_plane_status()		
		self.__airport_status = airport_manager.mock_update_airport()

	# check for clicking event in simulation, including click on plane, airport or status button on sidebar
	def mock_check_selection(self, event=None, airport_manager=None, plane_manager=None, sidebar=None):
		self.__selected_object_detail = plane_manager.mock_get_detail()
		# self.__selected_object_detail = airport_manager.mock_get_detail()
		overall_plane_text = ["test"]
		sidebar.update_information(overall_plane_information=Converter.dict_to_string(self.__plane_status),
			overall_airport_information=Converter.dict_to_string(self.__airport_status),
			selected_object_detail=self.__selected_object_detail)
