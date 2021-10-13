import random

class AirlineInformation:
	def __init__(self, name, code):
		self.name = name
		self.code = code

	def get_code(self):
		return self.code

class PlaneInfo:
	def __init__(self, model, max_seat):
		self.model = model
		self.max_seat = max_seat

class PlaneManager:
	def __init__(self):
		self.__airline_tuple = (
			AirlineInformation("Thai AirAsia", "FD"),
			AirlineInformation("Thai bara", "BR")
			)
		self.plane_spec = (
			PlaneInfo("bara1", 112),
			PlaneInfo("bara pro", 44)
			)
		self.__flight_counter = {airline.code: 0 for airline in self.__airline_tuple}
		print(self.__flight_counter)

	def gen_new_plane(self):
		plane1 = Plane.generate_random_plane(plane_spec=self.plane_spec, airline_tuple=self.__airline_tuple)
		plane1.print()



class Plane:
	def __init__(self, airline, model, seat):
		self.airline = airline
		self.model = model
		self.seat = seat

	def generate_random_plane(plane_spec, airline_tuple):
		airline = airline_tuple[random.randint(0, len(airline_tuple)-1)].get_code()
		spec = plane_spec[random.randint(0, len(plane_spec)-1)]
		model = spec.model
		seat = random.randint(1, spec.max_seat)

		return Plane(airline=airline, model=model, seat=seat)

	def print(self):
		print(self.airline)
		print(self.model)
		print(self.seat)

pm = PlaneManager()
pm.gen_new_plane()