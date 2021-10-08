import pygame
from pygame.constants import CONTROLLER_BUTTON_RIGHTSTICK
from image_loader import load_image
from simulator import Simulator
class Map:
    zoom_status = "zoom_out" # status of zoom
    first_click_position = None # position when rightclick is be down
    previous_distance = 0 # previous_distance is used to calulate in move method
    def __init__ (self, image_path, screen_size, top_left_point = ((0, 0))):
        self.__width = screen_size[0] 
        self.__height = screen_size[1]
        self.__image = load_image(image_path = image_path, screen_size=(self.__width, self.__height))
        self.__top_left_point = top_left_point
    
    #zoom map in
    def zoom_in(self):
        if self.zoom_status != "zoom_in":
            self.zoom_status = "zoom_in"
            self.__width = int(self.__width*2)
            self.__height = int(self.__height*2)
            self.__top_left_point = ((-self.__width/4, 0))
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    #zoom map out
    def zoom_out(self):
        if self.zoom_status != "zoom_out":
            self.zoom_status = "zoom_out"
            self.__width = int(self.__width/2)
            self.__height = int(self.__height/2)
            self.__top_left_point = ((0, 0))
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    #move map by holding the mouse
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
        self.previous_distance = moving_distance # store the distance for future calculation.
        if top_left_point_list[1] > 0: #if moving more than top border
            top_left_point_list[1] = 0
        elif top_left_point_list[1] < -750: #if moving more than bottom border
            top_left_point_list[1] = -750
        self.__top_left_point = tuple(top_left_point_list)

    def get_top_left_point(self):
        return self.__top_left_point

    def draw_map(self, display):
        display.blit(self.__image, self.__top_left_point)

    def check_event(self, event, simulator):
        if simulator.get_state(state = "zoomed", current=True)[1]:
            self.zoom_in()
        else: self.zoom_out()
        if (pygame.mouse.get_pressed()[2] and self.zoom_status == "zoom_in" ):
            self.move()
        if event.type == pygame.MOUSEBUTTONUP:
            self.first_click_position = None
            self.previous_distance = 0
            
            

