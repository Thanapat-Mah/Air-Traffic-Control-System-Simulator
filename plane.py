import pygame
from configuration import FONT, COLOR
from utilities import Loader
# from configuration import AIRLINES, PLANE_INFORMATIONS

# plane information/specification for each model
class PlaneInformation:
    def __init__(self, model, max_seat, speed, altitude):
        self.__model = model
        self.__max_seat = max_seat
        self.speed = speed
        self.altitude = altitude

# airline information for each airline
class AirlineInformation:
    def __init__(self, name, code):
        self.__name = name
        self.__code = code

class PlaneManager:
    def __init__(self, image_path, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        self.__plane_icon = Loader.load_image(image_path = image_path, size=(100, 100))
        self.__plane_specifictaion_tuple = (
            PlaneInformation(model="Airbus A320-200", max_seat=180, speed=863, altitude= tuple(29000, 39000)),
            PlaneInformation(model="Boeing 787-9", max_seat=236, speed=1050, altitude= tuple(35000, 43000))
        )
        self.__plane_list = None 
        self.__airline_tuple = (
            AirlineInformation(name = "Thai AirAsia", code = "FG"),
            AirlineInformation(name = "Thai Airways International", code = "TG")
        )
        self.__flight_counter = 0
        self.__text_color = None
        self.__font = None

    def mock_update_plane_position(self):
        for plane in self.__plane_list:
            print(plane.flightcode)

    def mock_update_plane_status(self):
        return {
            'Flying': 10,
            'Taking-off': 10,
            'Landing': 10,
            'Circling': 10,
            'Waiting': 10
        }

    def mock_is_empty(self, airport_code=None):
        for plane in self.plane_list:
            pass
        return True

    def draw_plane(self):
        pass

    def mock_check_selection (self, event=None):
        return 'TG200'

    def mock_get_detail(self, code=None):
        return ["Flight Code: TG200",
                "Airline: Thai AirAsia",
                "From: CNX To: BKK",
                "Passenger: 83",
                "Altitude: 37,000 ft",
                "Speed: 900 km/h",
                "Status: Flying"
        ]


class Plane:
    def __init__(self):
        self.__flight_code = None
        self.__airline_code = None
        self.__degree_position = None
        self.__model = None
        self.__passenger = None
        self.__speed = None
        self.__direction = None
        self.__altitude = None
        self.__origin = None
        self.__route = None
        self.__destination = None
        self.__status = None

    def get_information(self):
        return ({})

    def generate_random_plane(self, plane_information, airline_information=None, airport_manager=None):
        pass
        

    def update_position(self, time_pass=None):
        pass
