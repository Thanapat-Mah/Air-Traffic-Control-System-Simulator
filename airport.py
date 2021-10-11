import pygame
from color import Color
from simulator import Simulator

class Airport :
    zoom_status = "zoom_out"
    first_click_position = None # position when rightclick is be down
    previous_distance = 0 # previous_distance is used to calulate in move method
    def __init__(self):
        self.__CNX = (800, 200, "CNX")
        self.__BKK = (900, 480, "BKK")
        # self.__KKC = (1020, 320, "KKC")
        # self.__HKT = (770, 800, "HKT")
        # self.__HDY = (890, 890, "HDY")
        self.__listCNX = list(self.__CNX)
        self.__listBKK = list(self.__BKK)
        # self.__listKKC = list(self.__KKC)
        # self.__listHKT = list(self.__HKT)
        # self.__listHDY = list(self.__HDY)
        self.__top_left_point = (0,0)

    def zoom_in(self):
        if self.zoom_status != "zoom_in":
            self.zoom_status = "zoom_in"
            self.__listCNX = [640, 400, "CNX"]
            self.__listBKK = [840, 960, "BKK"]
            # self.__listKKC = [1020, 320, "KKC"]
            # self.__listHKT = [770, 800, "HKT"]
            # self.__listHDY = [890, 890, "HDY"]
            
    def zoom_out(self):
        if self.zoom_status != "zoom_out":
            self.zoom_status = "zoom_out"
            self.__listCNX = [800, 200, "CNX"]
            self.__listBKK = [900, 480, "BKK"]
            # self.__listKKC = [1020, 320, "KKC"]
            # self.__listHKT = [770, 800, "HKT"]
            # self.__listHDY = [890, 890, "HDY"]

    def move(self):
        if self.first_click_position is None:
            self.first_click_position = pygame.mouse.get_pos()
        click_list = pygame.mouse.get_pos()
        # convert turple to list
        first_click_position_list = list(self.first_click_position)
        last_click_position_list = list(click_list)
        top_left_point_list = list(self.__top_left_point)
        # calulate distance between positon of first click and last click (current click)
        moving_distance = last_click_position_list[1] - first_click_position_list[1]
        top_left_point_list[1] = top_left_point_list[1] + moving_distance - self.previous_distance
        self.__listCNX[1] = self.__listCNX[1] + moving_distance - self.previous_distance
        self.__listBKK[1] = self.__listBKK[1] + moving_distance - self.previous_distance
        self.previous_distance = moving_distance # store the distance for future calculation.
        if top_left_point_list[1] > 0: #if moving more than top border
            top_left_point_list[1] = 0
            self.__listCNX[1] = 400
            self.__listBKK[1] = 960
        elif top_left_point_list[1] < -750: #if moving more than bottom border
            top_left_point_list[1] = -750
            self.__listCNX[1] = -350
            self.__listBKK[1] = 210
            
        self.__top_left_point = tuple(top_left_point_list)
           

    def check_event(self, event, simulator):
        if simulator.get_state(state = "zoomed", current=True)[1]:
            self.zoom_in()
        else: self.zoom_out()
        if (pygame.mouse.get_pressed()[2] and self.zoom_status == "zoom_in" ):
            self.move()
        if event.type == pygame.MOUSEBUTTONUP:
            self.first_click_position = None
            self.previous_distance = 0

    def draw_airport(self, display):
        pygame.draw.circle(display, (255, 82, 96), (self.__listCNX[0], self.__listCNX[1]), 10)
        pygame.draw.circle(display, (255, 82, 96), (self.__listBKK[0], self.__listBKK[1]), 10)
        # pygame.draw.circle(display, (255, 82, 96), (self.__listKKC[0], self.__listKKC[1]), 10)
        # pygame.draw.circle(display, (255, 82, 96), (self.__listHKT[0], self.__listHKT[1]), 10)
        # pygame.draw.circle(display, (255, 82, 96), (self.__listHDY[0], self.__listHDY[1]), 10)
        