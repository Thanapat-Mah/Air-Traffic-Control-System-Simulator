import pygame
from styles import Color
from styles import Font
from simulator import Simulator

class Airport :
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.status = True

    
class AirportManager :
    def __init__(self, screen_size):
        airport_list = [
            Airport("CNX", 800, 200),
            Airport("BKK", 900, 480),
            Airport("KKC", 1020, 320),
            Airport("HKT", 770, 800),
            Airport("HDY", 890, 890)
        ]
        self.__airport_size = 10
        for airport in airport_list:
            airport.x = (airport.x/1920)*screen_size[0]
            airport.y = (airport.y/1080)*screen_size[1]
        self.__airport_tuple = tuple(airport_list)

    def draw_airport(self, display, map, simulator):
        top_left_point = map.get_top_left_point()
        scale = 1
        if simulator.get_state(state = "zoomed", current=True):
            scale = 2
        else: 
            scale = 1

        for airport in self.__airport_tuple:
            airport_x = (airport.x*scale)+top_left_point[0]
            airport_y = (airport.y*scale)+top_left_point[1]
            pygame.draw.circle(display, Color.light_gray, (airport_x, airport_y), self.__airport_size*scale)

            text = Font.roboto_normal.render(airport.name, True, Color.dark_gray)
            display.blit(text, (airport_x , airport_y ))

        