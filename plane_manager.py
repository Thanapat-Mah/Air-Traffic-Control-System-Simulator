import pygame
import copy
import math
from numpy import arctan, frompyfunc
from pygame import surface
from configuration import PLANE_PATH
from utilities import Loader
from plane_airline_information import PlaneInformation,AirlineInformation
from configuration import FONT, COLOR, PLANE_INFORMATIONS, AIRLINES, PLANE_PATH, PLNAE_PHASE
from plane import Plane

### plane mamager that can update plane
class PlaneManager:
    __LIMIT = 1
    def __init__(self, plane_size=30, image_path=PLANE_PATH, text_color=COLOR['white'], font=FONT['bebasneue_small'], route_color = COLOR['light_gray'], route_width = 3):
        self.__plane_size = plane_size
        self.__plane_icon = Loader.load_image(image_path = image_path, size=(plane_size, plane_size), scale = 1)
        self.__plane_specification_tuple = tuple([
            PlaneInformation(model= info[0], max_seat=info[1], speed=info[2], altitude=info[3]) for info in PLANE_INFORMATIONS
        ])
        self.__plane_list = []
        self.__airline_tuple = tuple([
            AirlineInformation(code= info[0], name=info[1]) for info in AIRLINES
        ])
        self.__flight_counter = {
            'FD' : 0,
            'TG' : 0
        }
        self.__text_color = text_color
        self.__font = font

        self.__route_color = route_color
        self.__route_width = route_width
        self.__collision_circle_color = None
        self.__collision_circle_width = None

    # get plane list that contain all plane object
    def get_plane_list(self):
        return(self.__plane_list)

    # update all plane position in plane list
    def update_plane_position(self):
        for plane in self.__plane_list:
            plane.update_position()

    # this method will be called by Simulator in update_simulator()
    def update_plane(self, simulated_delta_count, airport_manager):
        for i in range(simulated_delta_count.seconds):
            self.update_plane_position()
            #chaing plane phase
            for plane in self.__plane_list:
                if plane.get_phase() == PLNAE_PHASE['takingoff']:
                        if (plane.get_speed() == 0.8*plane.get_plane_information().get_speed()):
                            airport_manager.count_plane(plane.get_origin().get_code(), 'departed')
                            plane.set_phase(PLNAE_PHASE['climbing'])

                elif plane.get_phase() == PLNAE_PHASE['climbing']:
                    avrage_altitude = (sum(plane.get_plane_information().get_altitude())/2)
                    if (plane.get_altitude() == avrage_altitude):
                        plane.set_phase(PLNAE_PHASE['holding']) ############

                elif plane.get_phase() == PLNAE_PHASE['cruising']:
                    if (plane.get_remain_distance() <= plane.get_starting_descending_point()/1000):
                        plane.set_phase(PLNAE_PHASE['descending'])

                elif plane.get_phase() == PLNAE_PHASE['descending']:
                    if (plane.get_altitude() <= 0):
                        plane.set_phase(PLNAE_PHASE['landing'])

                elif plane.get_phase() == PLNAE_PHASE['landing']:
                    if(plane.get_speed() <= 0):
                        airport_manager.count_plane(plane.get_destination().get_code(), "arrived")
                        plane.set_altitude(0)
                        self.__plane_list.remove(plane)
        # dict for return
        phase_dict ={
            PLNAE_PHASE['holding']: [],
            PLNAE_PHASE['takingoff']: [],
            PLNAE_PHASE['climbing']: [],
            PLNAE_PHASE['cruising']: [],
            PLNAE_PHASE['descending']: [],
            PLNAE_PHASE['landing']: [],
            PLNAE_PHASE['waiting']: []          
        }
        #check phase
        for plane in self.__plane_list:
            if plane.get_phase() ==  PLNAE_PHASE['holding']:
                phase_dict[PLNAE_PHASE['holding']].append(plane.get_flight_code())
            elif plane.get_phase() ==  PLNAE_PHASE['takingoff']:
                phase_dict[PLNAE_PHASE['takingoff']].append(plane.get_flight_code())
            elif plane.get_phase() == PLNAE_PHASE['climbing']:
                phase_dict[PLNAE_PHASE['climbing']].append(plane.get_flight_code())
            elif plane.get_phase() == PLNAE_PHASE['cruising']:
                phase_dict[PLNAE_PHASE['cruising']].append(plane.get_flight_code())
            elif plane.get_phase() == PLNAE_PHASE['descending']:
                phase_dict[PLNAE_PHASE['descending']].append(plane.get_flight_code())
            elif plane.get_phase() == PLNAE_PHASE['landing'] :
                phase_dict[PLNAE_PHASE['landing']].append(plane.get_flight_code())
            elif plane.get_phase() == PLNAE_PHASE['waiting'] :
                phase_dict[PLNAE_PHASE['waiting']].append(plane.get_flight_code())
        return(phase_dict)

    #check is airport empty ?
    def is_empty(self, airport_code=None):
        for plane in self.__plane_list:
            if (plane.get_phase() == PLNAE_PHASE['landing'] and plane.get_destination().get_code() ==airport_code):
                return(False)
            if (plane.get_phase() == PLNAE_PHASE['takingoff'] and plane.get_origin().get_code() ==airport_code):
                return(False)
        return(True)

    #draw plane, route line and side plane detail
    def draw_all_plane(self, display, converter):
        for plane in self.__plane_list:
            if(plane.get_direction() != None):
                # set new hit box
                position = plane.get_degree_position()
                pixel = converter.degree_to_pixel(degree_postion=position)
                # draw route line when is selected
                airport_pixel = converter.degree_to_pixel(degree_postion=plane.get_destination().get_degree_position())

                if converter.get_selected_object_code() == plane.get_flight_code():
                    if plane.get_phase() != PLNAE_PHASE['holding']:
                        pygame.draw.line(display, self.__route_color, pixel, airport_pixel, width = self.__route_width)
                    else: 
                        #pygame.draw.arc(display, self.__route_color, [plane.get_holding_fix_direction()], width = self.__route_width)
                        tmp = copy.deepcopy(plane.get_holding_point())
                        ###test###
                        if (tmp["outboundend"] != None):
                            tmp["fix"] = converter.degree_to_pixel(degree_postion=tmp["fix"])
                            tmp["fix_end"] = converter.degree_to_pixel(degree_postion=tmp["fix_end"])
                            tmp["outbound"] = converter.degree_to_pixel(degree_postion=tmp["outbound"])
                            tmp["outboundend"] = converter.degree_to_pixel(degree_postion=tmp["outboundend"])
                            #pygame.draw.line(display, (255,0,0), tmp["fix"], tmp["fix_end"], width = 2) #red
                            
                            
                            x_mid = (tmp["fix"][0]+tmp["fix_end"][0])/2
                            y_mid = (tmp["fix"][1]+tmp["fix_end"][1])/2
                            mid_1 = (int(x_mid),int(y_mid))
                            r = int(math.dist(tmp["fix"],tmp["fix_end"])/2)
                            degree = plane.get_holding_fix_direction()

                            x_mid = (tmp["outboundend"][0]+tmp["outbound"][0])/2
                            y_mid = (tmp["outboundend"][1]+tmp["outbound"][1])/2
                            mid_2 = (int(x_mid),int(y_mid))
                            # print(tmp["fix"], tmp["fix_end"])
                            # print(mid, r)
                            # print(int(math.dist((mid),(tmp["fix"]))), int(math.dist((mid),(tmp["fix_end"]))))
                            #pygame.draw.circle(display, (255,0,0), mid, r, self.__route_width)
                            #rect = pygame.Rect(tmp["fix"][0], tmp["fix"][1]-r, r, r)
                            
                            #print("y/x",math.degrees(math.atan2(tmp["fix"][1]-mid[1], tmp["fix"][0]-mid[0])))
                            #pygame.draw.line(display, (255,0,0), tmp["fix"], mid, width = self.__route_width) # blue
                            #pygame.draw.rect(display, (255,255,255),(mid_1[0]-r, mid_1[1]-r, 2*r, 2*r), 1)
                            red = (255,0,0)
                            blue = (30,144,255)
                            violet = (222,87,255)
                            green = (20,255,36)
                            white = (255,255,255)
                            pygame.draw.arc(display, white, (mid_1[0]-r, mid_1[1]-r, 2*r, 2*r), math.radians(degree+90-10)+math.pi, math.radians(degree+90+10),self.__route_width)
                            pygame.draw.line(display, white, tmp["fix_end"], tmp["outbound"], width = self.__route_width) # blue
                            pygame.draw.arc(display, white, (mid_2[0]-r, mid_2[1]-r, 2*r, 2*r), math.radians(degree+90-10), math.radians(degree+90+10)+math.pi,self.__route_width)
                            pygame.draw.line(display, white, tmp["outboundend"], tmp["fix"], width = self.__route_width) #light green
                            
                            #pygame.draw.line(display, (222,87,255), tmp["outbound"], tmp["outboundend"], width = 2) #violet





                        ###test###
                direction = plane.get_direction()
                # rotate the plane in the direction of the destination.
                image = pygame.transform.rotate(self.__plane_icon, direction)
                position = plane.get_degree_position()
                pixel_position = converter.degree_to_pixel(degree_postion=position)
                new_hit_box = image.get_rect(center = pixel_position)
                plane.set_hit_box(new_hit_box)
                image = pygame.Surface((2,2))
                image.fill((255,0,0))
                # draw plane according to current position.
                display.blit(image, pixel)
                #display.blit(image, new_hit_box)
                # draw text right side of plane
                flight_code_surface = self.__font.render(plane.get_flight_code(), True, self.__text_color)
                route_surface = self.__font.render(f'{plane.get_origin().get_code()} - {plane.get_destination().get_code()}', True, self.__text_color)
                text_x = pixel_position[0] + self.__plane_size/2
                display.blit(flight_code_surface, (text_x, pixel_position[1]-flight_code_surface.get_size()[1]/2-5))
                display.blit(route_surface, (text_x, pixel_position[1]))

    # return selected plane' airline code
    def check_selection (self, event):
        selected_plane = ''
        for plane in self.__plane_list:
            if selected_plane == '':
                selected_plane = plane.click(event)
        return(selected_plane)

    # return detail of plane
    def get_detail(self, code=None):
        for plane in self.__plane_list:
            if plane.get_flight_code() == code:
                return(['Flight Code: '+plane.get_flight_code(),
                'Airline: '+plane.get_airline_information().get_name(),
                'From: '+plane.get_origin().get_code()+' To: '+plane.get_destination().get_code(),
                'Passenger: '+str(plane.get_passenger()),
                #"{:03d}".format(flight_counter['TG'])
                'Altitude: '+"{:.2f}".format(plane.get_altitude())+' ft',
                # 'Altitude: '+str(round(plane.get_altitude(),2))+' ft',
                'Speed: '+"{:.2f}".format(plane.get_speed())+' km/h',
                'phase: '+str(plane.get_phase())
            ])
        return([''])

    # generate new plane
    def generate_new_plane(self, airport_manager):
        if (len(self.__plane_list) != self.__LIMIT):
            gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specification_tuple, airline_information=self.__airline_tuple, airport_manager = airport_manager, flight_counter = self.__flight_counter)
            self.__plane_list.append(gen_plane)

    def respond_command(self, command): 
        if command[0] == 'generate':
            pass
        elif command[1] == 'takeoff':
            pass
        elif command[1] == 'hold':
            pass
        elif command[1] == 'continue':
            pass
        elif command[1] == 'altitude':
            pass
        else:
            pass

        return
    
    def command_generate(self, model, origin, destination):
        return

    def command_takeoff(self, flight_code):
        return
    
    def command_hold(self, flight_code):
        return

    def command_continue(self, flight_code):
        return

    def command_altitude(self, flight_code, altitude):
        return