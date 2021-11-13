import pygame
import copy
import math
from numpy import arctan, frompyfunc, mod
from pygame import Rect, surface
from configuration import PLANE_PATH, MODEL_GENERATE
from utilities import Converter, Loader
from plane_airline_information import PlaneInformation,AirlineInformation
from configuration import FONT, COLOR, PLANE_INFORMATIONS, AIRLINES, PLANE_PATH, PLNAE_PHASE, FAIL_RESPONSE
from plane import Plane

### plane mamager that can update plane
class PlaneManager:
    __LIMIT = 100
    def __init__(self, plane_size=30, image_path=PLANE_PATH, text_color=COLOR['white'], font=FONT['bebasneue_small'],
        route_color = COLOR['light_gray'], route_width = 2, collision_circle_color=COLOR["transparance_red"],
        collision_circle_radius=30, collision_circle_width=1):
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
        self.__collision_circle_color = collision_circle_color
        self.__collision_circle_radius = collision_circle_radius
        self.__collision_circle_width = collision_circle_width

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
                            plane.set_current_command("")
                            airport_manager.count_plane(plane.get_origin().get_code(), 'departed')
                            plane.set_phase(PLNAE_PHASE['climbing'])

                elif plane.get_phase() == PLNAE_PHASE['climbing']:
                    avrage_altitude = (sum(plane.get_plane_information().get_altitude())/2)
                    if (plane.get_altitude() == avrage_altitude):
                        plane.set_phase(PLNAE_PHASE['cruising'])

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

                elif plane.get_phase() == PLNAE_PHASE['holding']:
                    if(plane.get_current_command() == 'continue' and
                    (plane.get_holding_phase() == "inbound" or plane.get_degree_position() == plane.get_holding_point()["fix"])):
                        plane.set_current_command("")
                        plane.clear_holding()
                        plane.set_phase(PLNAE_PHASE['cruising'])
        # change hold to continue when pause
        if (simulated_delta_count.seconds == 0):
            for plane in self.__plane_list:
                if plane.get_phase() == PLNAE_PHASE['holding']:
                    if(plane.get_current_command() == 'continue' and
                    (plane.get_holding_phase() == "inbound" or plane.get_degree_position() == plane.get_holding_point()["fix"])):
                        plane.set_current_command("")
                        plane.clear_holding()
                        plane.set_phase(PLNAE_PHASE['cruising'])

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
    def draw_all_plane(self, display, converter, collision_detector):
        collision_set = collision_detector.get_collision_set()
        for plane in self.__plane_list:
            if(plane.get_direction() != None and plane.get_phase() != PLNAE_PHASE['waiting']):
                # set new hit box
                position = plane.get_degree_position()
                pixel = converter.degree_to_pixel(degree_position=position)

                # draw red circle when have future collision
                if plane.get_flight_code() in collision_set:
                    radius = self.__collision_circle_radius
                    circle_surface = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)
                    # fill transparence circle
                    pygame.draw.circle(circle_surface, self.__collision_circle_color, (radius, radius), radius)
                    # draw solid border
                    pygame.draw.circle(circle_surface, self.__collision_circle_color[:-1], (radius, radius), radius, width=self.__collision_circle_width)
                    display.blit(circle_surface, (pixel[0]-radius, pixel[1]-radius))

                # draw route line when is selected
                airport_pixel = converter.degree_to_pixel(degree_position=plane.get_destination().get_degree_position())
                # draw if plane object is selected
                if converter.get_selected_object_code() == plane.get_flight_code():
                    if plane.get_phase() != PLNAE_PHASE['holding']:
                        pygame.draw.line(display, self.__route_color, pixel, airport_pixel, width = self.__route_width)
                    else:
                        # draw if plane is flying in holding pattern
                        holding_point = copy.deepcopy(plane.get_holding_point())
                        if (holding_point["outboundend"] != None):
                            for point in holding_point:
                                holding_point[point] = converter.degree_to_pixel(degree_position=holding_point[point])
                                # check for make sure mid point is integer
                                if holding_point[point][0]%2 != 0:
                                    holding_point[point] = ((holding_point[point][0]-1),(holding_point[point][1]))
                                if holding_point[point][1]%2 != 0:
                                    holding_point[point] = ((holding_point[point][0]),(holding_point[point][1]-1))
                            # find mid point
                            mid_fix_fixend = (round((holding_point["fix"][0]+holding_point["fix_end"][0])/2),round((holding_point["fix"][1]+holding_point["fix_end"][1])/2))
                            mid_outbound_outboundend = (round((holding_point["outboundend"][0]+holding_point["outbound"][0])/2),round((holding_point["outboundend"][1]+holding_point["outbound"][1])/2))
                            # find radius
                            radius_fix_fixend = round(math.dist(holding_point["fix"],holding_point["fix_end"])/2)
                            # find new points for drawing calulated by fix point
                            holding_point["fix_end"] = (round(2*(mid_fix_fixend[0])-(holding_point["fix"][0])),round(2*(mid_fix_fixend[1])-(holding_point["fix"][1])))
                            distance_mid_x = (mid_fix_fixend[0])-(mid_outbound_outboundend[0])
                            distance_mid_y = (mid_fix_fixend[1])-(mid_outbound_outboundend[1])
                            holding_point["outboundend"] = (holding_point["fix"][0]-distance_mid_x,holding_point["fix"][1]-distance_mid_y)
                            holding_point["outbound"] = (holding_point["fix_end"][0]-distance_mid_x,holding_point["fix_end"][1]-distance_mid_y)
                            # find degree for drawing arc
                            arc = math.degrees(math.atan2(mid_fix_fixend[1]-holding_point["fix_end"][1],mid_fix_fixend[0]-holding_point["fix_end"][0]))
                            degree = 180-arc
                            # rectangle for drawing arc
                            rect_fix_fixend = (mid_fix_fixend[0]-radius_fix_fixend, mid_fix_fixend[1]-radius_fix_fixend, 2*radius_fix_fixend+1, 2*radius_fix_fixend+1)
                            rect_outbound_outboundend = (mid_outbound_outboundend[0]-radius_fix_fixend, mid_outbound_outboundend[1]-radius_fix_fixend+1, 2*radius_fix_fixend, 2*radius_fix_fixend+1)
                            # drawing holding route
                            pygame.draw.arc(display, self.__route_color, rect_fix_fixend, math.radians(degree), math.radians(degree+180),self.__route_width)
                            pygame.draw.arc(display, self.__route_color, rect_outbound_outboundend, math.radians(degree+180), math.radians(degree),self.__route_width)
                            pygame.draw.line(display,  self.__route_color, holding_point["fix_end"], holding_point["outbound"], width = self.__route_width)
                            pygame.draw.line(display,  self.__route_color, holding_point["outboundend"], holding_point["fix"], width = self.__route_width)
                direction = plane.get_direction()
                # rotate the plane in the direction of the destination.
                image = pygame.transform.rotate(self.__plane_icon, direction)
                position = plane.get_degree_position()
                pixel_position = converter.degree_to_pixel(degree_position=position)
                new_hit_box = image.get_rect(center = pixel_position)
                plane.set_hit_box(new_hit_box)
                # draw plane according to current position.
                display.blit(image, new_hit_box)
                # draw text right side of plane
                flight_code_surface = self.__font.render(plane.get_flight_code(), True, self.__text_color)
                route_surface = self.__font.render(f'{plane.get_origin().get_code()} - {plane.get_destination().get_code()}', True, self.__text_color)
                text_x = pixel_position[0] + self.__plane_size/2
                display.blit(flight_code_surface, (text_x, pixel_position[1]-flight_code_surface.get_size()[1]/2-5))
                display.blit(route_surface, (text_x, pixel_position[1]))

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
                return(['Flight Code: '+plane.get_flight_code(),
                'Airline: '+plane.get_airline_information().get_name(),
                'From: '+plane.get_origin().get_code()+' To: '+plane.get_destination().get_code(),
                'Passenger: '+str(plane.get_passenger()),
                #"{:03d}".format(flight_counter['TG'])
                'Altitude: '+"{:.2f}".format(plane.get_altitude())+' ft',
                # 'Altitude: '+str(round(plane.get_altitude(),2))+' ft',
                'Speed: '+"{:.2f}".format(plane.get_speed())+' km/h',
                'Phase: '+str(plane.get_phase())
            ])
        return([""])

    # generate new plane
    def generate_new_plane(self, airport_manager, model, origin_comm, destination_comm):
        if (len(self.__plane_list) != self.__LIMIT):
            gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specification_tuple, airline_information=self.__airline_tuple, 
                airport_manager = airport_manager, flight_counter = self.__flight_counter, model = model, origin_comm=origin_comm, destination_comm=destination_comm)
            self.__plane_list.append(gen_plane)
            flight_code = gen_plane.get_flight_code()

        return(flight_code)

    # take commands from the console and follow them
    def respond_command(self, console, airport_manager):
        formatted_input = console.pop_formatted_input()
        if(len(formatted_input)) > 0:
            response_message = []
            has_flight = False
            keyword, *parameters = formatted_input  # unpack keyword and parameters
            if keyword == 'generate':
                if parameters[0] == "":
                    flight_code = self.generate_new_plane(airport_manager=airport_manager ,model="", origin_comm="", destination_comm="")
                    response_message.append({"success_response": "Generate {} success.".format(flight_code)})
                else:
                    self.generate_command(parameters=parameters, response_message=response_message, airport_manager=airport_manager)

            elif keyword == 'takeoff':
                for plane in self.__plane_list:
                    if plane.get_flight_code() == parameters[0]:
                        has_flight = True
                        if plane.get_phase() == PLNAE_PHASE['waiting']:
                            plane.set_current_command('takingoff')
                            plane.set_phase(PLNAE_PHASE['takingoff'])
                            response_message.append({"success_response": "{} is {}".format(plane.get_flight_code(), plane.get_phase())})
                        else:
                            response_message.append({"fail_response": FAIL_RESPONSE["can_not_command"]})
                            response_message.append({"fail_response": "{} is now {}".format(plane.get_flight_code(), plane.get_phase())})
                if not has_flight:
                    response_message.append({"fail_response": FAIL_RESPONSE["invalid_flight_code"]})

            elif keyword == 'hold':
                for plane in self.__plane_list:
                    if plane.get_flight_code() == parameters[0]:
                        has_flight = True
                        if plane.get_phase() == PLNAE_PHASE['cruising']:
                            plane.set_current_command('holding')
                            plane.set_phase(PLNAE_PHASE['holding'])
                            plane.initial_holding()
                            response_message.append({"success_response": "{} is {}".format(plane.get_flight_code(), plane.get_phase())})
                        else:
                            response_message.append({"fail_response": FAIL_RESPONSE["can_not_command"]})
                            response_message.append({"fail_response": "{} is now {}".format(plane.get_flight_code(), plane.get_phase())})
                if not has_flight:
                    response_message.append({"fail_response": FAIL_RESPONSE["invalid_flight_code"]})

            elif keyword == 'continue':
                for plane in self.__plane_list:
                    if plane.get_flight_code() == parameters[0]:
                        has_flight = True
                        if plane.get_phase() == PLNAE_PHASE['holding']:
                            plane.set_current_command('continue')
                            response_message.append({"success_response": "{} will continue".format(plane.get_flight_code())})
                        else:
                            response_message.append({"fail_response": FAIL_RESPONSE["can_not_command"]})
                            response_message.append({"fail_response": "{} is now {}".format(plane.get_flight_code(), plane.get_phase())})
                if not has_flight:
                    response_message.append({"fail_response": FAIL_RESPONSE["invalid_flight_code"]})

            elif keyword == 'altitude':
                for plane in self.__plane_list:
                    if plane.get_flight_code() == parameters[0]:
                        if plane.get_phase() == PLNAE_PHASE['cruising']:
                            for plane_model in self.__plane_specification_tuple:
                                if plane.get_plane_information() == plane_model:
                                    altitude = plane_model.get_altitude()
                                    if int(parameters[1]) >= altitude[0] and int(parameters[1]) <= altitude[1]:
                                        plane.set_target_altitude(float(parameters[1]))
                                        response_message.append({"success_response": "{} is at an altitude of {} ft.".format(plane.get_flight_code(), parameters[1])})
                                    else:
                                        response_message.append({"fail_response": FAIL_RESPONSE["invalid_value"]})
                                        response_message.append({"fail_response": "The value must be between {} and {}".format(altitude[0], altitude[1])})
                        else:
                            response_message.append({"fail_response": FAIL_RESPONSE["can_not_command"]})
                            response_message.append({"fail_response": "{} is now {}".format(plane.get_flight_code(), plane.get_phase())})
            # send response to console this way
            console.handle_response(response_message)
    
    # generate new plane from generate command and check parameters of command
    def generate_command(self, parameters, response_message, airport_manager):
        has_airport = False
        has_model = False
        for model in MODEL_GENERATE:
            if model == parameters[0]:
                if parameters[1] == "" and parameters[2] == "":
                    flight_code = self.generate_new_plane(airport_manager=airport_manager ,model=MODEL_GENERATE[model], origin_comm="", destination_comm="")
                    response_message.append({"success_response": "Generate {} success.".format(flight_code)})
                    has_model = 1
                    break
                elif parameters[1] == "" or parameters[2] == "":
                    has_model = False
                else:
                    airport_list = airport_manager.get_airport_tuple()
                    for airport in airport_list:
                        if airport.get_code() == parameters[1] and airport.get_code() == parameters[2]:
                            response_message.append({"fail_response": FAIL_RESPONSE["invalid_value"]})
                            response_message.append({"fail_response": "Origin and destination can't be the same."})
                            has_airport = True
                            break
                        elif airport.get_code() == parameters[1]:
                            for airport_one in airport_list:
                                if airport_one.get_code() == parameters[2]:
                                    flight_code = self.generate_new_plane(airport_manager=airport_manager ,model=MODEL_GENERATE[model], 
                                        origin_comm=parameters[1], destination_comm=parameters[2])
                                    response_message.append({"success_response": "Generate {} success.".format(flight_code)})
                                    has_airport = True
                                    break
                                else:
                                    has_airport = False
        if not has_model and not has_airport:
            response_message.append({"fail_response": FAIL_RESPONSE["invalid_value"]})