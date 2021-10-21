from numpy.random.mtrand import normal, rand
import pygame
import random
import string
import math
from numpy import std, mean, random
from pygame.constants import NOEVENT
from configuration import AIRPORTS, FONT, COLOR, PLANE_INFORMATIONS, AIRLINES, PLANE_PATH
from utilities import Loader, Converter
from airport import Airport
# from configuration import AIRLINES, PLANE_INFORMATIONS

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

### airline information for each airline
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
        self.__plane_icon = Loader.load_image(image_path = image_path, size=(50, 50), scale = 1)
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

    # this method will be called by Simulator in update_simulator()
    def mock_update_plane(self, delta_simulated_time):
        # insert update_plane_position() here
        # update each plane status here
        # format data and return as below
        return {
            'Flying': ["TG001", "FD002"],
            'Taking-off': ["TG002"],
            'Landing': ["FD001"],
            'Circling': [],
            'Waiting': ["TG003"]
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
        return True

    def draw_plane(self, display, size):
        convert = Converter()
        for plane in self.__plane_list:
            pixel = convert.degree_to_pixel(degree_postion=plane.get_degree_position(), screen_size=size)
            display.blit(self.__plane_icon, pixel)

    def draw_plane(self, display, size):
        for plane in self.__plane_list:
            position = plane.get_degree_position()
            pixel = Converter.degree_to_pixel(degree_postion=position, screen_size=size)
            pixel = (pixel[0]-25,pixel[1]-25)
            display.blit(self.__plane_icon, pixel)

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

    def generate_new_plane(self, airport_manager):
        if (len(self.__plane_list) != self.__LIMIT):
            gen_plane = Plane.mock_generate_random_plane(airport_manager = airport_manager)
            self.__plane_list.append(gen_plane)

    def get_plane_list(self):
        return self.__plane_list


class Plane:
    def __init__(self, flight_code, airline_code = None, model= None, passenger= None, origin= None, destination= None, altitude= None, speed= None, status= None, degree_position= None):
        self.__flight_code = flight_code
        self.__airline_code = airline_code
        self.__degree_position = degree_position
        self.__model = model
        self.__passenger = passenger
        self.__speed = speed
        self.__direction = None
        self.__altitude = altitude
        self.__origin = origin
        self.__route = None
        self.__destination = destination
        self.__status = status

    def get_degree_position(self):
        return self.__degree_position

    def get_information(self):
        return {
            'flight_code' : self.__flight_code,
            'airline_code' : self.__airline_code,
            'degree_position' : self.__degree_position,
            'model' : self.__model,
            'passenger' : self.__passenger,
            'speed' : "{} km/h".format(self.__speed),
            'direction' : self.__direction,
            'altitude' : "{} ft".format(self.__altitude),
            'origin' : self.__origin,
            'route' : self.__route,
            'destination' : self.__destination,
            'status' : self.__status

        }

    def mock_generate_random_plane(airport_manager):
        airport_list = airport_manager.get_airport_list()
        fligt_code = "TEST001"
        origin = airport_list[1]
        destination = airport_list[0]
        degree_position = origin.degree_postion
        speed = 0.1
        return Plane(flight_code=fligt_code, origin=origin, destination=destination, degree_position=degree_position, speed=speed)

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
        while(normal_seat < 0):
            normal_seat = int(random.normal(mean_seat, std_seat, 1))
        return normal_seat

    def print_data_plane(self):
        pass
        #print("self.__airline_code: ",self.__airline_code)
        #print("self.__model:, ",self.__model)
        print("self.__flight_code:, ",self.__flight_code)
        print("self.__degree_position:, ",self.__degree_position)
        print("self.__origin:, ",self.__origin)
        print("self.__destination:, ",self.__destination)
        #print("self.__passenger:, ",self.__passenger)
        #print("self.__altitude:, ",self.__altitude)
        #print("self.__speed:, ",self.__speed)
        #print("self.__status:, ",self.__status)


    def update_position(self, time_pass=None):
        degree_position = self.__degree_position
        destination_position = self.__destination.degree_postion
        speed = self.__speed
        dy = destination_position[0] - degree_position[0]
        dx = destination_position[1] - degree_position[1]
        direction = math.atan2(dy,dx)
        direction = math.degrees(direction)
        self.__direction = direction
        x_speed = speed*math.cos(math.radians(direction))
        y_speed =speed*math.sin(math.radians(direction))
        self.__degree_position = (degree_position[0]+y_speed,degree_position[1]+x_speed)

    def get_degree_position(self):
        return self.__degree_position
