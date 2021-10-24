from numpy.random.mtrand import normal, rand
import pygame
import random
import string
import math
from numpy import std, mean, random, subtract
from pygame import surface
from pygame.constants import NOEVENT
from configuration import AIRPORTS, FONT, COLOR, PLANE_INFORMATIONS, AIRLINES, PLANE_PATH, ZOOM_SCALE
from utilities import Calculator, Loader, Converter, NewConverter
from airport import Airport
from plane_airline_information import PlaneInformation, AirlineInformation

### plane mamager that can update plane
class PlaneManager:
    __LIMIT = 2
    def __init__(self, image_path=PLANE_PATH, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        self.__plane_icon = Loader.load_image(image_path = image_path, size=(50, 50), scale = 1)
        self.__plane_specifictaion_tuple = tuple([
            PlaneInformation(model= info[0], max_seat=info[1], speed=info[2], altitude=info[3]) for info in PLANE_INFORMATIONS
        ])
        self.__plane_list = []
        self.__airline_tuple = tuple([
            AirlineInformation(code= info[0], name=info[1]) for info in AIRLINES
        ])
        self.__flight_counter = 0
        self.__text_color = None
        self.__font = None

    def get_plane_list(self):
        return self.__plane_list

    # update all plane position in plane list
    def update_plane_position(self):
        for plane in self.__plane_list:
            plane.update_position(plane_specifictaion_tuple = self.__plane_specifictaion_tuple)

    # this method will be called by Simulator in update_simulator()
    def update_plane(self):
        self.update_plane_position()
        for plane in self.__plane_list:
            if (plane.get_status() != 'Landing' and plane.get_status() != 'Taking-off'):
                if (plane.get_remain_distance() <2):
                    plane.set_status('Landing')
                else: plane.set_status('Flying')

            if plane.get_status() == 'Taking-off': # if (plane.get_model() == plane_info.get_model() and plane.get_speed() == plane_info.get_speed()):
                for plane_info in self.__plane_specifictaion_tuple:
                    if (plane.get_model() == plane_info.get_model() and plane.get_speed() == plane_info.get_speed()):
                        plane.set_status('Flying')

            if plane.get_status() == 'Landing':
                if(plane.get_speed() == 0):
                    plane.set_altitude(0)
                    self.__plane_list.remove(plane)
                
        self.__flight_counter = len(self.__plane_list)
        status_dict ={
            'Flying': [],
            'Taking-off': [],
            'Landing': [],
            'Circling': [],
            'Waiting': []
        }
        for plane in self.__plane_list:
            if plane.get_status() == 'Flying':
                status_dict['Flying'].append(plane.get_flight_code())
            elif plane.get_status() == 'Taking-off':
                status_dict['Taking-off'].append(plane.get_flight_code())
            elif plane.get_status() == 'Landing':
                status_dict['Landing'].append(plane.get_flight_code())
            elif plane.get_status() == 'Circling':
                status_dict['Circling'].append(plane.get_flight_code())
            elif plane.get_status() == 'Waiting' :
                status_dict['Waiting'].append(plane.get_flight_code())
        return status_dict

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

    def draw_plane(self, display, converter):
        for plane in self.__plane_list:
            if(plane.get_direction() != None):
                position = plane.get_degree_position()
                pixel = converter.mock_degree_to_pixel(degree_postion=position)
                pixel = (pixel[0]-25,pixel[1]-25)
                direction = plane.get_direction() - 45 
                image = pygame.transform.rotate(self.__plane_icon, direction)
                new_rect = image.get_rect(center = (pixel[0]+25, pixel[1]+25))
                plane.set_hit_box(new_rect)
                display.blit(image, new_rect)

    # return selected plane' airline code
    def check_selection (self, event):
        selected_plane = ""
        for plane in self.__plane_list:
            if selected_plane == "":
                selected_plane = plane.click(event)
        return(selected_plane)

    # return detail of plane
    def get_detail(self, code=None):
        for plane in self.__plane_list:
            airline_name = ""
            if plane.get_flight_code() == code:
                for airline in self.__airline_tuple:
                    if plane.get_airline_code() == airline.get_code():
                        airline_name = airline.get_name()
                return ["Flight Code: "+plane.get_flight_code(),
                "Airline: "+airline_name,
                "From: "+plane.get_origin().get_code()+" To: "+plane.get_destination().get_code(),
                "Passenger: "+str(plane.get_passenger()),
                "Altitude: "+str(plane.get_altitude())+" ft",
                "Speed: "+str(round(plane.get_speed(),2))+" km/h",
                "Status: "+str(plane.get_status())
            ]
        else : return([""])

        {
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

    def generate_new_plane(self, airport_manager):
        if (len(self.__plane_list) != self.__LIMIT):
            num = 1 #not finished yet
            gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specifictaion_tuple, airline_information=self.__airline_tuple, airport_manager = airport_manager, num=num)
            self.__plane_list.append(gen_plane)

### plane object
class Plane:
    def __init__(self, flight_code, status, airline_code, model, passenger, origin, destination, altitude, speed, degree_position):
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
        self.__hit_box = None

    def get_flight_code(self):
        return self.__flight_code

    def get_airline_code(self):
        return self.__airline_code

    def get_degree_position(self):
        return self.__degree_position

    def get_model(self):
        return self.__model

    def get_passenger(self):
        return self.__passenger

    def get_speed(self):
        return self.__speed

    def get_direction(self):
        return self.__direction

    def get_altitude(self):
        return self.__altitude

    def get_origin(self):
        return self.__origin

    def get_destination(self):
        return self.__destination

    def get_status(self):
        return self.__status

    def set_degree_position(self, degree_position):
        self.__degree_position = degree_position
    
    def set_speed(self, speed):
        self.__speed = speed

    def set_direction(self,direction):
        self.__direction = direction

    def set_altitude(self, altitude):
        self.__altitude = altitude

    def set_status(self,status):
        self.__status = status

    def set_hit_box(self, new_hit_box):
        self.__hit_box = new_hit_box

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
    def get_remain_distance(self):
        origin_position = self.get_origin().get_degree_position()
        destination_position = self.get_destination().get_degree_position()
        current_postion = self.get_degree_position() #current position of plane
        distance_different_current_origin = math.dist(origin_position,current_postion)*111
        distance_different_origin_destination = math.dist(origin_position,destination_position)*111
        return distance_different_origin_destination-distance_different_current_origin

    def generate_random_plane(plane_information, airline_information, airport_manager, num):
        airport_list = airport_manager.get_airport_list()
        origin = random.choice(airport_list)
        destination = random.choice(airport_list)
        while(destination == origin):
            destination = random.choice(airport_list)
        degree_position = origin.get_degree_position()
        airline = random.choice(airline_information)
        airline_code = airline.get_code()
        airline_name = airline.get_name()
        generate_num = "{:03d}".format(num)
        flight_code = "{}{}".format(airline_code,str(generate_num)) #not finished yet
        spec = random.choice(plane_information)
        model = spec.get_model()
        passenger = spec.get_max_seat()
        normal_seat = Calculator.normal_distribution_seat(passenger=passenger)
        altitude = 0
        speed = 0
        status = 'Taking-off'
        #start calculate direction
        # direction_origin = origin.get_pixel_position()
        # direction_destination = destination.get_pixel_position()
        # sub_direction = subtract(direction_destination, direction_origin)
        # degree = (math.atan2(sub_direction[1],sub_direction[0])/math.pi*180)*-1
        # direction = degree
        #end calculate direction

        return Plane(airline_code=airline_code, model=model, passenger=normal_seat, flight_code=flight_code, origin=origin, destination=destination, altitude=altitude, degree_position=degree_position, speed=speed, status=status)

    # update plane position 
    def update_position(self,plane_specifictaion_tuple):
        #update position for flying and taking off plane
        # find plane direction 
        if (self.__status != "Landing"):
            destination_position = self.__destination.get_degree_position()
            self.__direction = math.degrees(math.atan2(destination_position[0] - self.__degree_position[0],
                    destination_position[1] - self.__degree_position[1]))
        if (self.__status == "Taking-off"):
            for plane_spec in plane_specifictaion_tuple:
                if self.__model == plane_spec.get_model():
                    average_speed = plane_spec.get_speed()
                    avrage_altitude = plane_spec.get_altitude()
                    avrage_altitude = (sum(avrage_altitude)/2)
                    self.__speed += average_speed/15 # 15s to max speed
                    self.__altitude += avrage_altitude/10
                    if self.__speed > average_speed or self.__altitude > avrage_altitude:
                        self.__speed  = average_speed
                        self.__altitude = avrage_altitude
        #update position for landing plane
        if (self.__status == "Landing"):
            if (self.__speed > 0):
                for plane_spec in plane_specifictaion_tuple:
                    if self.__model == plane_spec.get_model():
                        average_speed = plane_spec.get_speed()
                        avrage_altitude = plane_spec.get_altitude()
                        avrage_altitude = (sum(avrage_altitude)/2)
                        self.__speed -= average_speed/10 if self.__speed != 0 else 0
                        self.__altitude -= avrage_altitude/10 if self.__altitude != 0 else 0
            else: 
                self.__speed = 0
                self.__altitude = 0
        # if close the airport
        if (self.get_remain_distance() > 0.1):
            speed = self.__speed/(111*3600)   #unit = degree/second ,111km = 1 degree
            x_speed = speed*math.cos(math.radians(self.__direction))
            y_speed =speed*math.sin(math.radians(self.__direction))
            self.__degree_position = (self.__degree_position[0]+y_speed,self.__degree_position[1]+x_speed)
        
    def print_data_plane(self):
        #print("self.__airline_code: ",self.__airline_code)
        #print("self.__model:, ",self.__model)
        #print("self.__flight_code:, ",self.__flight_code)
        #print("self.__degree_position:, ",self.__degree_position)
        #print("self.__origin:, ",self.__origin)
        #print("self.__destination:, ",self.__destination)
        #print("self.__passenger:, ",self.__passenger)
        print("self.__altitude:, ",self.__altitude)
        print("self.__speed:, ",self.__speed)
        #print("self.__status:, ",self.__status)
        #print("self.__direction", self.__direction)

    def get_remain_distance(self):
        origin_position = self.get_origin().get_degree_position()
        destination_position = self.get_destination().get_degree_position()
        current_postion = self.get_degree_position() #current position of plane
        distance_different_current_origin = math.dist(origin_position,current_postion)*111
        distance_different_origin_destination = math.dist(origin_position,destination_position)*111
        return distance_different_origin_destination-distance_different_current_origin

    # check if this plane is clicked, return empty string or plane' airline code
    def click(self, event):        
        if self.__hit_box:     # if this plane have hit_box (is drawed at least one time)
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.__hit_box.collidepoint(x, y):
                        return(str(self.__flight_code))
        return("")
