class AirlineInformation:
	def __init__(self, name, code):
		self.name = name
		self.code = code

class PlaneManager:
	def __init__(self):
		self.__airline_tuple = (
			AirlineInformation("Thai AirAsia", "FD"),
			AirlineInformation("Thai bara", "BR")
			)
		self.__flight_counter = {airline.code: 0 for airline in self.__airline_tuple}
		print(self.__flight_counter)

p = PlaneManager()