from numpy.lib.function_base import select
import pygame
import random
import math
from numpy import random
from utilities import Calculator
from configuration import ROC, PLNAE_PHASE, ACCELERATE, ROT

### flight, store information, generate random plane, mark plane position on map
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
        v_plane = 0.8*self.__plane_information.get_speed() * 1000/3600 #m/s
        avrage_altitude = (sum(self.__plane_information.get_altitude())/2)
        t_descending = avrage_altitude/ROC
        t_landing = v_plane/6
        self.__starting_descending_point = v_plane * t_descending + ((v_plane*t_landing)+0.5*(-6)*((t_landing)**2))
        self.__holding_state = ""
        self.__holding_fix_direction = None 
        #self.__holding_fix_degree_position = None # fix point
        #self.__holding_fix_end_degree_position = None # end of fix end line
        #self.__holding_outbound_degree_position = None # end of outbound line
        #self.__holding_outbound_end_degree_position = None # end of outbound end line
        self.__holding_point = {"fix": None,
                        "fix_end":None,
                        "outbound": None,
                        "outboundend": None}

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

    def get_starting_descending_point(self):
        return(self.__starting_descending_point)

    def get_holding_point(self):
        return(self.__holding_point)

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
        # origin = airport_list[1]
        # destination = airport_list[2]
        while(destination == origin):
            destination = random.choice(airport_list)
        degree_position = origin.get_degree_position()
        airline = random.choice(airline_information)
        airline_code = airline.get_code()
        # start generate Flight code
        if (airline_code == 'FD'):
            flight_counter.update({'FD': flight_counter['FD'] + 1})
            generate_num = "{:03d}".format(flight_counter['FD'])
        elif (airline_code == 'TG'):
            flight_counter.update({'TG': flight_counter['TG'] + 1})
            generate_num = "{:03d}".format(flight_counter['TG'])
        flight_code = "{}{}".format(airline_code,str(generate_num))
        # end generate Flight code
        plane_info = random.choice(plane_information)
        passenger = plane_info.get_max_seat()
        normal_passenger = Calculator.normal_distribution_seat(passenger=passenger)
        altitude = 0
        speed = 0
        status = 'Waiting'
        return (Plane(airline_information=airline, plane_information=plane_info, passenger=normal_passenger, flight_code=flight_code, origin=origin, destination=destination, altitude=altitude, degree_position=degree_position, speed=speed, status=status))

    # update plane position
    def update_position(self):
        #update position for Landing plane
        if (self.__status != PLNAE_PHASE["landing"] and self.__status != PLNAE_PHASE["holding"]):
            self.find_direction()

        #update position for Taking off plane
        if (self.__status == PLNAE_PHASE["takingoff"]):
            self.taking_off()

        elif (self.__status == PLNAE_PHASE["climbing"]):
            self.climbing()
        
        elif (self.__status == PLNAE_PHASE["descending"]):
            self.descending()

        #update position for landing plane
        elif (self.__status == PLNAE_PHASE["landing"]):
            self.landing()

        elif (self.__status == PLNAE_PHASE["holding"]):
            self.holding()
    
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

    def find_direction(self):
        destination_position = self.__destination.get_degree_position()
        self.__direction = math.degrees(math.atan2(destination_position[0] - self.__degree_position[0],
        destination_position[1] - self.__degree_position[1]))

    def waiting(self):
        pass

    #movment for taking off plane
    def taking_off(self):
        average_speed = self.__plane_information.get_speed()
        self.__speed += ACCELERATE*3600/1000 
        if self.__speed > 0.8*average_speed:
            self.__speed  = 0.8*average_speed

    #movment for climing plane
    def climbing(self):
        avrage_altitude = self.__plane_information.get_altitude()
        avrage_altitude = (sum(avrage_altitude)/2)
        self.__altitude += ROC
        if self.__altitude > avrage_altitude:
            self.__altitude = avrage_altitude

    #movment for descending plane
    def descending(self):
        self.__altitude -= ROC
        if self.__altitude < 0:
            self.__altitude = 0

    #movment for landing plane
    def landing(self):
        self.__speed -= ACCELERATE*3600/1000
        if self.__speed < 0: 
            self.__speed  = 0

    def holding(self):
        if self.__holding_state == "":
            if  self.__holding_fix_direction == None and  self.__holding_point["fix"] == None:
                self.__holding_fix_direction = self.__direction
                #self.__holding_fix_degree_position = self.__degree_position ##correct
                self.__holding_point["fix"]=(self.__degree_position)
            if (self.__holding_point["fix_end"] == None):
                radius = ((self.__speed/3600) / (math.pi/(180/ROT))) /111 # (degree position)
                x_radius =2*radius*math.cos(math.radians(90+self.__holding_fix_direction))
                y_radius =2*radius*math.sin(math.radians(90+self.__holding_fix_direction))
                # self.__holding_fix_end_degree_position = (self.__holding_point["fix"][0]+y_radius,
                #                                             self.__holding_point["fix"][1]+x_radius)
                self.__holding_point["fix_end"]=(self.__holding_point["fix"][0]+y_radius,
                                                            self.__holding_point["fix"][1]+x_radius)
            if (self.__holding_point["outbound"] == None):
                leg_distance = self.__speed/(111*3600)*90 # (degree position)
                x_leg_distance = leg_distance*math.cos(math.radians(self.__holding_fix_direction+180))
                y_leg_distance =leg_distance*math.sin(math.radians(self.__holding_fix_direction+180))
                # self.__holding_outbound_degree_position = (self.__holding_point["fix_end"][0]+y_leg_distance,
                #                                             self.__holding_point["fix_end"][1]+x_leg_distance)
                self.__holding_point["outbound"]=(self.__holding_point["fix_end"][0]+y_leg_distance,
                                                            self.__holding_point["fix_end"][1]+x_leg_distance)
            if (self.__holding_point["outboundend"] == None):
                radius = ((self.__speed/3600) / (math.pi/(180/ROT))) /111 # (degree position)
                x_radius = 2*radius*math.cos(math.radians(self.__holding_fix_direction+270))
                y_radius =2*radius*math.sin(math.radians(self.__holding_fix_direction+270))
                # self.__holding_outbound_end_degree_position = (self.__holding_point["outbound"][0]+y_radius,
                #                                             self.__holding_point["outbound"][1]+x_radius)
                self.__holding_point["outboundend"]=(self.__holding_point["outbound"][0]+y_radius,
                                                        self.__holding_point["outbound"][1]+x_radius)
            self.__holding_state = "fix end"

        if self.__holding_state == "fix end":
            if self.__direction - self.__holding_fix_direction < 180:       
                self.__direction += ROT
            else :
                self.__holding_state = "outbound"




        if self.__holding_state == "outbound":
            self.__holding_point["fix_end"]
            leg_distance = self.__speed/(111*3600)*90
            if (leg_distance - math.dist(self.__degree_position,  self.__holding_point["fix_end"]))*111 <= 0.5:
                self.__holding_state = "outbound end"


        if self.__holding_state == "outbound end":
            if self.__direction - self.__holding_fix_direction < 360:              
                    self.__direction += ROT
            else: 
                self.__holding_state = "inbound"
        
        if self.__holding_state == "inbound":
            if math.dist( self.__holding_point["fix"], self.__degree_position)*111 <= 1:
                self.__holding_state = ""
                self.__direction = self.__holding_fix_direction
                self.__degree_position =  self.__holding_point["fix"]
            