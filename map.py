import pygame
from utilities import Loader
from configuration import ZOOM_SCALE

class Map:
    __zoom_state = "zoom_out" # for checking state of zoom
    __first_click_position = None # position when rightclick is be down
    __previous_distance = 0 # __previous_distance is used to calulate in move method
    def __init__ (self, image_path, screen_size, top_left_point = ((0, 0))):
        self.__width = screen_size[0]
        self.__height = screen_size[1]
        loader = Loader()
        self._source_image = loader.load_image(image_path = image_path, size=(self.__width, self.__height), scale=ZOOM_SCALE) 
        self.__image = pygame.transform.scale( self._source_image, (self.__width, self.__height))
        self.__top_left_point = top_left_point
    
    #zoom map in
    def zoom_in(self):
        if self.__zoom_state != "zoom_in":
            self.__zoom_state = "zoom_in"
            self.__top_left_point = ((int(-self.__width*(ZOOM_SCALE-1)/2), 0))
            self.__image = pygame.transform.scale(self._source_image, ((int(self.__width*ZOOM_SCALE), int(self.__height*ZOOM_SCALE))))

    #zoom map out
    def zoom_out(self):
        if self.__zoom_state != "zoom_out":
            self.__zoom_state = "zoom_out"
            self.__top_left_point = ((0, 0))
            self.__image = pygame.transform.scale( self._source_image, (self.__width, self.__height))

    #move map by holding the mouse
    def move(self):
        if self.__first_click_position is None:
            self.__first_click_position = pygame.mouse.get_pos()
        last_click_position = pygame.mouse.get_pos()
        # convert turple to list
        top_left_point_list = list(self.__top_left_point)
        # calulate distance between positon of first click and last click (current click)
        moving_distance = last_click_position[1] - self.__first_click_position[1]
        top_left_point_list[1] = top_left_point_list[1] + moving_distance - self.__previous_distance
        self.__previous_distance = moving_distance # store the distance for future calculation.
        border_bottom = -self.__height
        if top_left_point_list[1] > 0: #if moving more than top border
            top_left_point_list[1] = 0
        elif top_left_point_list[1] < border_bottom: #if moving more than bottom border
            top_left_point_list[1] = border_bottom
        self.__top_left_point = tuple(top_left_point_list)
    def get_top_left_point(self):
        return self.__top_left_point

    def draw_map(self, display):
        display.blit(self.__image, self.__top_left_point)

    def check_event(self, event, simulator):
        zoom_status = simulator.get_state(state = "zoomed", current=True)
        if zoom_status:
            self.zoom_in()
        else: self.zoom_out()
        if pygame.mouse.get_pressed()[0] and zoom_status:
            self.move()
        if event.type == pygame.MOUSEBUTTONUP:
            self.__first_click_position = None
            self.__previous_distance = 0
            
            

