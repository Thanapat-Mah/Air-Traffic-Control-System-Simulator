import pygame
import random
from configuration import FONT, COLOR
from utilities import Loader
from configuration import PLANE_INFORMATIONS, AIRLINES, PLANE_PATH
# from configuration import AIRLINES, PLANE_INFORMATIONS

# plane information/specification for each model
class PlaneInformation:
    def __init__(self, model, max_seat, speed, altitude):
        self.model = model
        self.max_seat = max_seat
        self.speed = speed
        self.altitude = altitude

# airline information for each airline
class AirlineInformation:
    def __init__(self, name, code):
        self.__name = name
        self.__code = code
    
    def get_code(self):
        return self.__code

class PlaneManager:
    def __init__(self, image_path=PLANE_PATH, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        loader = Loader()
        self.__plane_icon = loader.load_image(image_path = image_path, size=(100, 100), scale = 1)
        self.__plane_specifictaion_tuple = tuple([
            PlaneInformation(model= info[0], max_seat=info[1], speed=info[2], altitude=info[3]) for info in PLANE_INFORMATIONS
        ])
        self.__plane_list = None 
        self.__airline_tuple = tuple([
            AirlineInformation(name= info[0], code=info[1]) for info in AIRLINES
        ])
        self.__flight_counter = 0
        self.__text_color = None
        self.__font = None

    def mock_update_plane_position(self):
        pass

    def mock_update_plane_status(self):
        return {
            'Flying': 10,
            'Taking-off': 10,
            'Landing': 10,
            'Circling': 10,
            'Waiting': 10
        }

    def mock_is_empty(self, airport_code=None):
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

    def gen_new_plane(self):
        plane1 = Plane.generate_random_plane(plane_information=self.__plane_specifictaion_tuple, airline_information=self.__airline_tuple)
        plane1.print()


class Plane:
    def __init__(self, airline_code, model, passenger):
        self.__flight_code = None
        self.__airline_code = airline_code
        self.__degree_position = None
        self.__model = model
        self.__passenger = passenger
        self.__speed = None
        self.__direction = None
        self.__altitude = None
        self.__origin = None
        self.__route = None
        self.__destination = None
        self.__status = None

    def get_information(self):
        return ({
            
        })

    def generate_random_plane(plane_information, airline_information, airport_manager=None):
        airline_code = airline_information[random.randint(0, len(airline_information)-1)].get_code()
        spec = plane_information[random.randint(0, len(plane_information)-1)]
        model = spec.model
        passenger = random.randint(40, spec.max_seat)

        return Plane(airline_code=airline_code, model=model, passenger=passenger)

    def print(self):
        print(self.__airline_code)
        print(self.__model)
        print(self.__passenger)
		
        

    def update_position(self, time_pass=None):
        pass

pm = PlaneManager()
pm.gen_new_plane()