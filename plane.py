import pygame
import random
import math
from numpy import random
from utilities import Calculator

### plane object
class Plane:
    def __init__(self, flight_code, status, airline_information, plane_information, passenger, origin, destination, altitude, speed, degree_position):
        self.__flight_code = flight_code
        self.__airline_information = airline_information
        self.__degree_position = degree_position
        self.__plane_information = plane_information
        self.__passenger = passenger
        self.__speed = speed
        self.__direction = None
        self.__altitude = altitude
        self.__origin = origin
        self.__destination = destination
        self.__status = status
        self.__hit_box = None

    def get_flight_code(self):
        return(self.__flight_code)

    def get_airline_information(self):
        return(self.__airline_information)

    def get_degree_position(self):
        return(self.__degree_position)

    def get_plane_information(self):
        return(self.__plane_information)

    def get_passenger(self):
        return(self.__passenger)

    def get_speed(self):
        return(self.__speed)

    def get_direction(self):
        return(self.__direction)

    def get_altitude(self):
        return(self.__altitude)

    def get_origin(self):
        return(self.__origin)

    def get_destination(self):
        return(self.__destination)

    def get_status(self):
        return(self.__status)

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

    # get remain distance between plane position and destination position
    def get_remain_distance(self):
        origin_position = self.get_origin().get_degree_position()
        destination_position = self.get_destination().get_degree_position()
        current_postion = self.get_degree_position() #current position of plane
        distance_different_current_origin = math.dist(origin_position,current_postion)*111
        distance_different_origin_destination = math.dist(origin_position,destination_position)*111
        return(distance_different_origin_destination-distance_different_current_origin)

    # generate random all information plane
    def generate_random_plane(plane_information, airline_information, airport_manager, flight_counter):
        airport_list = airport_manager.get_airport_tuple()
        origin = random.choice(airport_list)
        destination = random.choice(airport_list)
        while(destination == origin):
            destination = random.choice(airport_list)
        degree_position = origin.get_degree_position()
        airline = random.choice(airline_information)
        airline_code = airline.get_code()
        # start Flight code
        if (airline_code == 'FD'):
            flight_counter.update({'FD': flight_counter['FD'] + 1})
            generate_num = "{:03d}".format(flight_counter['FD'])
        elif (airline_code == 'TG'):
            flight_counter.update({'TG': flight_counter['TG'] + 1})
            generate_num = "{:03d}".format(flight_counter['TG'])
        flight_code = "{}{}".format(airline_code,str(generate_num))
        # end Flight code
        spec = random.choice(plane_information)
        passenger = spec.get_max_seat()
        normal_seat = Calculator.normal_distribution_seat(passenger=passenger)
        altitude = 0
        speed = 0
        status = 'Taking-off'
        return Plane(airline_information=airline, plane_information=spec, passenger=normal_seat, flight_code=flight_code, origin=origin, destination=destination, altitude=altitude, degree_position=degree_position, speed=speed, status=status)

    # update plane position
    def update_position(self):
        #update position for Landing plane
        if (self.__status != "Landing"):
            destination_position = self.__destination.get_degree_position()
            self.__direction = math.degrees(math.atan2(destination_position[0] - self.__degree_position[0],
                    destination_position[1] - self.__degree_position[1]))
        #update position for Taking off plane
        if (self.__status == "Taking-off"):
                average_speed = self.__plane_information.get_speed()
                avrage_altitude = self.__plane_information.get_altitude()
                avrage_altitude = (sum(avrage_altitude)/2)
                self.__speed += average_speed/60 # 15s to max speed
                self.__altitude += avrage_altitude/60
                if self.__speed > average_speed or self.__altitude > avrage_altitude:
                    self.__speed  = average_speed
                    self.__altitude = avrage_altitude
        #update position for landing plane
        if (self.__status == "Landing"):
            if (self.__speed > 0):
                average_speed = self.__plane_information.get_speed()
                avrage_altitude = self.__plane_information.get_altitude()
                avrage_altitude = (sum(avrage_altitude)/2)
                self.__speed =  self.__speed - average_speed/60 if self.__speed - average_speed/60 >= 0 else 0
                self.__altitude = self.__altitude - avrage_altitude/60 if self.__altitude - avrage_altitude/60 >= 0 else 0
        # if plane is close the airport don't update position in map
        if (self.get_remain_distance() >= 1):
            speed = self.__speed/(111*3600)   #unit = degree/second ,111km = 1 degree
            x_speed = speed*math.cos(math.radians(self.__direction))
            y_speed =speed*math.sin(math.radians(self.__direction))
            self.__degree_position = (self.__degree_position[0]+y_speed,self.__degree_position[1]+x_speed)

    # check if this plane is clicked, return empty string or plane' airline code
    def click(self, event):
        if self.__hit_box:     # if this plane have hit_box (is drawed at least one time)
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.__hit_box.collidepoint(x, y):
                        return(self.__flight_code)
        return("")
