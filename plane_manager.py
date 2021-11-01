import pygame
from numpy import frompyfunc
from configuration import PLANE_PATH
from utilities import Loader
from plane_airline_information import PlaneInformation,AirlineInformation
from configuration import FONT, COLOR, PLANE_INFORMATIONS, AIRLINES, PLANE_PATH
from plane import Plane

### plane mamager that can update plane
class PlaneManager:
    __LIMIT = 3
    def __init__(self, plane_size=30, image_path=PLANE_PATH, text_color=COLOR["white"], font=FONT["bebasneue_small"], line_color = COLOR["light_gray"]):
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

        self.__route_color = line_color
        self.__route_width = None
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
            #chaing plane status
            for plane in self.__plane_list:
                if (plane.get_status() != 'Landing' and plane.get_status() != 'Taking-off'):
                    if (plane.get_remain_distance() <20):
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
        # dict for return
        status_dict ={
            'Waiting': [],
            'Circling': [],
            'Taking-off': [],
            'Landing': [],
            'Flying': []            
        }
        #check status
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

    #check is airport empty ?
    def is_empty(self, airport_code=None):
        for plane in self.__plane_list:
            if (plane.get_status() == 'Landing' and plane.get_destination().get_code() ==airport_code):
                return(False)
            if (plane.get_status() == 'Taking-off' and plane.get_origin().get_code() ==airport_code):
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
                if (converter.get_selected_object_code() == plane.get_flight_code()):
                    pygame.draw.line(display, self.__route_color, pixel, airport_pixel, width = 2)
                pixel = (pixel[0]-25,pixel[1]-25)
                direction = plane.get_direction()
                # rotate the plane in the direction of the destination.
                image = pygame.transform.rotate(self.__plane_icon, direction)
                position = plane.get_degree_position()
                pixel_position = converter.degree_to_pixel(degree_postion=position)
                new_hit_box = image.get_rect(center = pixel_position)
                plane.set_hit_box(new_hit_box)
                # draw plane according to current position.
                display.blit(image, new_hit_box)
                # draw text right side of plane
                flight_code_surface = self.__font.render(plane.get_flight_code(), True, self.__text_color)
                route_surface = self.__font.render(f"{plane.get_origin().get_code()} - {plane.get_destination().get_code()}", True, self.__text_color)
                text_x = pixel_position[0] + self.__plane_size/2
                text_y = pixel_position[1] - flight_code_surface.get_size()[1]
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
                return(["Flight Code: "+plane.get_flight_code(),
                "Airline: "+plane.get_airline_information().get_name(),
                "From: "+plane.get_origin().get_code()+" To: "+plane.get_destination().get_code(),
                "Passenger: "+str(plane.get_passenger()),
                "Altitude: "+str(round(plane.get_altitude(),2))+" ft",
                "Speed: "+str(round(plane.get_speed(),2))+" km/h",
                "Status: "+str(plane.get_status())
            ])
        return([""])

    # generate new plane
    def generate_new_plane(self, airport_manager):
        # if (len(self.__plane_list) != self.__LIMIT):
        gen_plane = Plane.generate_random_plane(plane_information=self.__plane_specification_tuple, airline_information=self.__airline_tuple, airport_manager = airport_manager, flight_counter = self.__flight_counter)
        self.__plane_list.append(gen_plane)
