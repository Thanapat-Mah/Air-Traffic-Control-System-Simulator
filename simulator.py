import datetime

### simulator data and state, keep track of state and time
class Simulator:
	def __init__(self, name, time_step=1, spawn_period=260):
		self.__name = name
		self.__is_play = True
		self.__time_period = [50, 10, 1]		# time period, less value more speed, first value is current
		self.__is_zoom = False		
		self.__running_time_count = 0
		self.__simulated_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0)	# simulated datetime
		self.__simulated_time_step = datetime.timedelta(seconds=time_step)	# time step per 1 time tick
		self.__simulated_delta_count = datetime.timedelta(seconds=0)		# time since last plane/airport update
		self.__spawn_period = datetime.timedelta(seconds=spawn_period)		# time period for spawn new plane
		self.__spawn_delta_count = datetime.timedelta(seconds=0)			# time since last spawn
		self.__plane_information = {}			# plane information from PlaneManager
		self.__airport_information = {}			# airport information from AirportManager
		self.__selected_object_code = ""		# IATA code of selected plane or airport object
		self.__selected_object_detail = []		# details of selected object

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
		if state == "is_play":
			state_list = [self.__is_play, not self.__is_play]
		elif state == "time_period":
			state_list = self.__time_period
		elif state == "is_zoom":
			state_list = [self.__is_zoom, not self.__is_zoom]
		# return only current value
		if current:
			return(state_list[0])
		# return all possible value for specific state
		else:
			return(state_list)

	# update specific state
	def update_state(self, state):
		if state == "is_play":
			self.__is_play = not self.__is_play
		elif state == "time_period":
			self.__time_period.append(self.__time_period[0])
			self.__time_period = self.__time_period[1:]
			self.__running_time_count = 0
		elif state == "is_zoom":
			self.__is_zoom = not self.__is_zoom

	# count time and calculate simulated datetime
	def tick_time(self):
		if self.__is_play:
			self.__running_time_count += 1
			# increase simulated datetime by 1 minutes when reach the time period in time_period
			if self.__running_time_count%self.get_state("time_period", current = True) == 0:
				self.__simulated_datetime += self.__simulated_time_step
				self.__spawn_delta_count += self.__simulated_time_step
				self.__simulated_delta_count += self.__simulated_time_step

	# update plane and airport to next time step, also update information shown on sidebar
	def update_simulator(self, airport_manager, plane_manager, sidebar, collision_detector, console):
		# tick time
		self.tick_time()
		# get selected object detail
		selected_detail = []
		selected_detail.append(plane_manager.get_detail(code=self.__selected_object_code))
		selected_detail.append(airport_manager.get_detail(code=self.__selected_object_code))
		for detail in selected_detail:
			if detail != "":
				self.__selected_object_detail = detail
		# spawn plane when reach time period
		if self.__spawn_delta_count == self.__spawn_period:
			plane_manager.generate_new_plane(airport_manager=airport_manager, model="", origin_comm="", destination_comm="")
			self.__spawn_delta_count = datetime.timedelta(seconds = 0)
		# update plane and get plane information
		self.__plane_information = plane_manager.update_plane(simulated_delta_count=self.__simulated_delta_count, airport_manager=airport_manager)		
		self.__simulated_delta_count = datetime.timedelta(seconds = 0)
		# update airport and get airport information
		self.__airport_information = airport_manager.update_airport(plane_manager=plane_manager)
		# check for future potentail collision between each plane
		collision_detector.check_collision(plane_manager=plane_manager, console=console)
		# update all information on sidebar
		sidebar.update_information(plane_information=self.__plane_information,
			airport_information=self.__airport_information,
			selected_object_detail=self.__selected_object_detail)

	# check for clicking event in simulation, including click on plane, airport or status button on sidebar
	def check_selection(self, event, airport_manager, plane_manager, sidebar):
		selected_candidate = []
		selected_candidate.append(plane_manager.check_selection(event))
		selected_candidate.append(airport_manager.check_selection(event))
		selected_candidate.append(sidebar.check_selection(event))
		for code in selected_candidate:
			if code != "":
				self.__selected_object_code = code