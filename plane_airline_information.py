### plane information/specification for each model
class PlaneInformation:
    def __init__(self, model, max_seat, speed, altitude):
        self.__model = model
        self.__max_seat = max_seat
        self.__speed = speed
        self.__altitude = altitude

    def get_model(self):
        return self.__model

    def get_max_seat(self):
        return self.__max_seat

    def get_speed(self):
        return self.__speed

    def get_altitude(self):
        return self.__altitude

### airline information for each airline
class AirlineInformation:
    def __init__(self, name, code):
        self.__name = name
        self.__code = code

    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code