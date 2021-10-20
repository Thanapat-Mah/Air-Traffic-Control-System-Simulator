from numpy.random.mtrand import normal, rand
import pygame
import random
import string
from numpy import std, mean, random
from configuration import AIRPORTS, FONT, COLOR
from utilities import Loader
from configuration import PLANE_INFORMATIONS, AIRLINES, PLANE_PATH
from airport import Airport
# from configuration import AIRLINES, PLANE_INFORMATIONS

# plane information/specification for each model
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

# airline information for each airline
class AirlineInformation:
    def __init__(self, name, code):
        self.__name = name
        self.__code = code
    
    def get_name(self):
        return self.__name

    def get_code(self):
        return self.__code

class PlaneManager:
    __LIMIT = 1;
    def __init__(self, image_path=PLANE_PATH, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        loader = Loader()
        self.__plane_icon = loader.load_image(image_path = image_path, size=(50, 50), scale = 1)
        self.__plane_specifictaion_tuple = tuple([
            PlaneInformation(model= info[0], max_seat=info[1], speed=info[2], altitude=info[3]) for info in PLANE_INFORMATIONS
        ])
        self.__plane_list = []
        self.__airline_tuple = tuple([
            AirlineInformation(name= info[0], code=info[1]) for info in AIRLINES
        ])
        self.__flight_counter = 0
        self.__text_color = None
        self.__font = None

    def mock_update_plane_position(self):
        for plane in self.__plane_list:
            plane.update_position()

    def mock_update_plane_status(self):
        return {
            'Flying': 10,
            'Taking-off': 10,
            'Landing': 10,
            'Circling': 10,
            'Waiting': 10
        }

    def mock_is_empty(self, airport_code=None):
        for plane in self.__plane_list:
            """if plane.status == "waiting and plane.origin == airport_code :
                    return True
                if  plane.status == "landing and and plane.destination == airport_code"
                    return True
                if or plane.status = "taking off and plane.origin == airport_code
                    return True
            """
            pass
        return False

    def draw_plane(self,display):
        for plane in self.__plane_list:
            display.blit(self.__plane_icon, (800, 200))
            

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

    def generate_new_plane(self):
        if (len(self.__plane_list) != self.__LIMIT):
            gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specifictaion_tuple, airline_information=self.__airline_tuple)
            self.__plane_list.append(gen_plane)
        
    def get_plane_list(self):
        return self.__plane_list

class Plane:
    def __init__(self, airline_code, model, passenger, origin, destination, altitude, speed, status):
        self.__flight_code = None
        self.__airline_code = airline_code
        self.__degree_position = None
        self.__model = model
        self.__passenger = passenger
        self.__speed = speed
        self.__direction = None
        self.__altitude = altitude
        self.__origin = origin
        self.__route = None
        self.__destination = destination
        self.__status = status

    def get_information(self):
        return ({})

    def generate_random_plane(plane_information, airline_information, airport_manager=AIRPORTS):
        airport_list = tuple([Airport(a[1], a[2], a[3]) for a in AIRPORTS])
        airport_name_list = []
        for airport in airport_list:
            airport.name = airport.name
            airport_name_list.append(airport.name)
        origin = random.choice(airport_name_list)
        destination = random.choice(airport_name_list)
        while(destination == origin):
            destination = random.choice(airport_name_list)
        airline_code = airline_information[random.randint(0, len(airline_information)-1)].get_code()
        spec = plane_information[random.randint(0, len(plane_information)-1)]
        model = spec.get_model()
        passenger = spec.get_max_seat()
        normal_seat = Plane.normal_distribution_seat(passenger=passenger)
        altitude = 0
        speed = 0
        status = 'waiting'
        return Plane(airline_code=airline_code, model=model, passenger=normal_seat, origin=origin, destination=destination, altitude=altitude, speed=speed, status=status)
    
    def normal_distribution_seat(passenger):
        list_seat = []
        count = 1000
        passenger = passenger
        for n in range(count):
            count_seat = random.randint(1,passenger)
            list_seat.append(count_seat)
        mean_seat = mean(list_seat)
        std_seat = std(list_seat)
        normal_seat = int(random.normal(mean_seat, std_seat, 1))
        return normal_seat

    def print_data_plane(self):
        print("self.__airline_code: ",self.__airline_code)
        print("self.__model:, ",self.__model)
        print("self.__origin:, ",self.__origin)
        print("self.__destination:, ",self.__destination)
        print("self.__passenger:, ",self.__passenger)
        print("self.__altitude:, ",self.__altitude)
        print("self.__speed:, ",self.__speed)
        print("self.__status:, ",self.__status)

		
    def update_position(self, time_pass=None):
        pass
