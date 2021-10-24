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
    def __init__(self, plane_size=50, image_path=PLANE_PATH, text_color=COLOR["white"], font=FONT["bebasneue_small"], line_color = COLOR["white"]):
        self.__plane_size = plane_size
        self.__plane_icon = Loader.load_image(image_path = image_path, size=(plane_size, plane_size), scale = 1)
        self.__plane_specifictaion_tuple = tuple([
            PlaneInformation(model= info[0], max_seat=info[1], speed=info[2], altitude=info[3]) for info in PLANE_INFORMATIONS
        ])
        self.__plane_list = []
        self.__airline_tuple = tuple([
            AirlineInformation(code= info[0], name=info[1]) for info in AIRLINES
        ])
        self.__text_color = text_color
        self.__font = font
        self.__line_color = line_color
        self.__flight_counter = {
            'FD' : 0,
            'TG' : 0
        }


    def get_plane_list(self):
        return(self.__plane_list)

    # update all plane position in plane list
    def update_plane_position(self):
        for plane in self.__plane_list:
            plane.update_position()

    # this method will be called by Simulator in update_simulator()
    def update_plane(self, delta_simulated_time, airport_manager):
        for i in range(delta_simulated_time.seconds):
            self.update_plane_position()

            for plane in self.__plane_list:
                if (plane.get_status() != 'Landing' and plane.get_status() != 'Taking-off'):
                    if (plane.get_remain_distance() <10):
                        plane.set_status('Landing')
                    else: plane.set_status('Flying')

                if plane.get_status() == 'Taking-off':
                        if (plane.get_speed() == plane.get_plane_information().get_speed()):
                            airport_manager.count_plane(plane.get_origin().get_code(), "departed")
                            plane.set_status('Flying')

                if plane.get_status() == 'Landing':
                    if(plane.get_speed() == 0):
                        airport_manager.count_plane(plane.get_destination().get_code(), "landed")
                        plane.set_altitude(0)
                        self.__plane_list.remove(plane)

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
        return(status_dict)

    def is_empty(self, airport_code=None):
        for plane in self.__plane_list:
            if (plane.get_status() == 'Landing' and plane.get_destination().get_code() ==airport_code):
                return(False)
            if (plane.get_status() == 'Taking-off' and plane.get_origin().get_code() ==airport_code):
                return(False)
        return(True)

    def draw_plane(self, display, converter):
        for plane in self.__plane_list:
            if(plane.get_direction() != None):
                # set new hit box
                position = plane.get_degree_position()
                pixel = converter.mock_degree_to_pixel(degree_postion=position)
                airport_pixel = converter.mock_degree_to_pixel(degree_postion=plane.get_destination().get_degree_position())
                if (converter.get_selected_object_code() == plane.get_flight_code()):
                    pygame.draw.line(display, self.__line_color, pixel, airport_pixel, width = 2)
                pixel = (pixel[0]-25,pixel[1]-25)
                direction = plane.get_direction()
                image = pygame.transform.rotate(self.__plane_icon, direction)
                position = plane.get_degree_position()
                pixel_position = converter.mock_degree_to_pixel(degree_postion=position)
                new_hit_box = image.get_rect(center = pixel_position)
                plane.set_hit_box(new_hit_box)
                # draw plane
                display.blit(image, new_hit_box)
                # draw text right side of plane
                flight_code_surface = self.__font.render(plane.get_flight_code(), True, self.__text_color)
                origin_surface = self.__font.render(f"FROM: {plane.get_origin().get_code()}", True, self.__text_color)
                destination_surface = self.__font.render(f"TO: {plane.get_destination().get_code()}", True, self.__text_color)
                text_x = pixel_position[0] + self.__plane_size/2
                text_y = pixel_position[1] - origin_surface.get_size()[1]
                display.blit(flight_code_surface, (text_x, text_y))
                text_y += origin_surface.get_size()[1]/2 + 3
                display.blit(origin_surface, (text_x, text_y))
                text_y += origin_surface.get_size()[1]/2 + 3
                display.blit(destination_surface, (text_x, text_y))

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
            if plane.get_flight_code() == code:
                return(["Flight Code: "+plane.get_flight_code(),
                "Airline: "+plane.get_airline_information().get_name(),
                "From: "+plane.get_origin().get_code()+" To: "+plane.get_destination().get_code(),
                "Passenger: "+str(plane.get_passenger()),
                "Altitude: "+str(round(plane.get_altitude(),2))+" ft",
                "Speed: "+str(round(plane.get_speed(),2))+" km/h",
                "Status: "+str(plane.get_status())
            ])
        return([""])

    def generate_new_plane(self, airport_manager):
        if (len(self.__plane_list) != self.__LIMIT):
            gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specifictaion_tuple, airline_information=self.__airline_tuple, airport_manager = airport_manager, flight_counter = self.__flight_counter)
            self.__plane_list.append(gen_plane)

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
            else:
                self.__speed = 0
                self.__altitude = 0
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
