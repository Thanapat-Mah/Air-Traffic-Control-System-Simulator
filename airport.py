import pygame
from configuration import FONT, COLOR, AIRPORTS, ZOOM_SCALE
from simulator import Simulator
from utilities import Converter
class Airport :
    def __init__(self, name, x, y,screen_size):
        converter = Converter()
        self.name = name
        self.degree_postion = converter.degree_to_pixel((x, y),screen_size)
        self.status = True
        self.landed = None
        self.departed = None
        self.code = None

    def switch_status(self):
        pass



class AirportManager :
    def __init__(self, screen_size, airport_color=COLOR["black"], text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        airport_list = [Airport(a[1], a[2], a[3],screen_size) for a in AIRPORTS]
        self.__airport_size = 10
        
        for airport in airport_list:
            print(airport.name)
            print(airport.degree_postion)
        
        self.__airport_tuple = tuple(airport_list)
        self.__airport_color = airport_color
        self.__text_color = text_color
        self.__font = font

    def draw_airport(self, display, map_, simulator):
        top_left_point = map_.get_top_left_point()
        scale = 1
        if simulator.get_state(state = "zoomed", current=True):
            scale = ZOOM_SCALE
        else:
            scale = 1


        # for airport in self.__airport_tuple:
            # degree_position = airport.x, airport.y
            # pixel_position = Converter.degree_to_pixel(degree_position,None, None)
            # pygame.draw.circle(display, self.__airport_color, pixel_position, self.__airport_size)

            # text = self.__font.render(airport.name, True, self.__text_color)
            # display.blit(text, (airport_x + (self.__airport_size * 1.5), airport_y - self.__airport_size ))


        for airport in self.__airport_tuple:
            airport_x = (airport.degree_postion[0]*scale)+top_left_point[0]
            airport_y = (airport.degree_postion[1]*scale)+top_left_point[1]
            pygame.draw.circle(display, self.__airport_color, (airport_x, airport_y), self.__airport_size)

            text = self.__font.render(airport.name, True, self.__text_color)
            display.blit(text, (airport_x + (self.__airport_size * 1.5), airport_y - self.__airport_size ))

    def mock_update_airport(self, plane_manager=None):
        return({
            "Empty": 3,
            "In Use": 2
        })

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