import pygame
from configuration import FONT, COLOR, AIRPORTS, ZOOM_SCALE
from simulator import Simulator
from utilities import Converter

class Airport :
    def __init__(self, name, code, x, y, screen_size):
        self.__name = name
        self.__code = code
        self.__pixel_position = Converter.degree_to_pixel((x, y), screen_size)
        self.__degree_position = (x, y)
        self.__status = True
        self.__landed = None
        self.__departed = None

    # return pixel position of airport
    def get_pixel_position(self):
        return self.__pixel_position

    # return degree position of airport
    def get_degree_position(self):
        return self.__degree_position

    # return name of airport
    def get_name(self):
        return self.__name

    def get_code(self):
        return(self.__code)

    def get_status(self):
        return(self.__status)

    # switch status of airport
    def switch_status(self):
        self.__status = not self.__status

class AirportManager :
    def __init__(self, screen_size, airport_color=COLOR["black"], text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        airport_list = [Airport(a[0], a[1], a[2], a[3],screen_size) for a in AIRPORTS]
        self.__airport_size = 10
        self.__airport_tuple = tuple(airport_list)
        self.__airport_color = airport_color
        self.__text_color = text_color
        self.__font = font

    # Display the airport on the map.
    def draw_airport(self, display, map_, simulator, size):
        # top_left_point = map_.get_top_left_point()
        # scale = 1
        # if simulator.get_state(state = "zoomed", current=True):
        #     scale = ZOOM_SCALE
        # else:
        #     scale = 1
        for airport in self.__airport_tuple:
            position = airport.get_degree_position()
            pixel = Converter.degree_to_pixel(position, size, map_=map_, simulator=simulator)
            # airport_x = airport.get_pixel_position()[0]
            # airport_y = airport.get_pixel_position()[1]
            pygame.draw.circle(display, self.__airport_color, (pixel[0], pixel[1]), self.__airport_size)

            text = self.__font.render(airport.get_name(), True, self.__text_color)
            display.blit(text, (pixel[0] + (self.__airport_size * 1.5), pixel[1] - self.__airport_size ))

    # this method will be called by Simulator in update_simulator()
    def update_airport(self, plane_manager=None):
        status_dict = {
            "Empty": [],
            "In Use": []
        }
        for airport in self.__airport_tuple:
            if airport.get_status():
                status_dict["Empty"].append(airport.get_code())
            else:
                status_dict["In Use"].append(airport.get_code())
        # update each airport status here
        # format data and return as below
        return(status_dict)

    def mock_check_selection(self, event=None):
        return("BKK")

    def mock_get_detail(self, code=None):
        return([
            "Name: Suvarnabhumi Airport",
            "IATA Code: BKK",
            "Status: In Use",
            "Landed: 0",
            "Departed: 3"
        ])
    def get_airport_list(self):
        return self.__airport_tuple
