import pygame
from pygame.constants import CONTROLLER_BUTTON_RIGHTSTICK
from loader import Loader
from simulator import Simulator
class Map:
    zoom_state = "zoom_out" # for checking state of zoom
    first_click_position = None # position when rightclick is be down
    previous_distance = 0 # previous_distance is used to calulate in move method
    def __init__ (self, image_path, screen_size, top_left_point = ((0, 0))):
        self.__width = screen_size[0] 
        self.__height = screen_size[1]
        loader = Loader()
        self.__image = loader.load_image(image_path = image_path, screen_size=(self.__width, self.__height))
        self.__top_left_point = top_left_point
    
    #zoom map in
    def zoom_in(self):
        if self.zoom_state != "zoom_in":
            self.zoom_state = "zoom_in"
            self.__width = int(self.__width*2)
            self.__height = int(self.__height*2)
            self.__top_left_point = ((-self.__width/4, 0))
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    #zoom map out
    def zoom_out(self):
        if self.zoom_state != "zoom_out":
            self.zoom_state = "zoom_out"
            self.__width = int(self.__width/2)
            self.__height = int(self.__height/2)
            self.__top_left_point = ((0, 0))
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    #move map by holding the mouse
    def move(self):
        if self.first_click_position is None:
            self.first_click_position = pygame.mouse.get_pos()
        last_click_position = pygame.mouse.get_pos()
        # convert turple to list
        top_left_point_list = list(self.__top_left_point)
        # calulate distance between positon of first click and last click (current click)
        moving_distance = last_click_position[1] - self.first_click_position[1]
        top_left_point_list[1] = top_left_point_list[1] + moving_distance - self.previous_distance
        self.previous_distance = moving_distance # store the distance for future calculation.
        if top_left_point_list[1] > 0: #if moving more than top border
            top_left_point_list[1] = 0
        elif top_left_point_list[1] < -900: #if moving more than bottom border
            top_left_point_list[1] = -900
        self.__top_left_point = tuple(top_left_point_list)

    def get_top_left_point(self):
        return self.__top_left_point

    def draw_map(self, display):
        display.blit(self.__image, self.__top_left_point)

    def check_event(self, event, simulator):
        zoom_status = simulator.get_state(state = "zoomed", current=True)[1]
        if zoom_status:
            self.zoom_in()
        else: self.zoom_out()
        if pygame.mouse.get_pressed()[0] and zoom_status:
            self.move()
        if event.type == pygame.MOUSEBUTTONUP:
            self.first_click_position = None
            self.previous_distance = 0
            
            

