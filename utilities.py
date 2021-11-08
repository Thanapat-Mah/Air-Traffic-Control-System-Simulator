import pygame
from configuration import MAP_TOP_LEFT_DEGREE, MAP_BOTTOM_RIGHT_DEGREE, ZOOM_SCALE
from numpy import std, mean, random


class Loader:

    def load_image(image_path, size, scale = 1):
        screen_size_scaled = (int(size[0]*scale), int(size[1]*scale))
        image_loaded = pygame.image.load(image_path)
        return pygame.transform.scale(image_loaded, screen_size_scaled)

    def adjust_size(self, icon, height_limit):
        width, height = icon.get_size()
        scale = height_limit/height
        return(pygame.transform.scale(icon, (int(width*scale), int(height*scale))))

    # load icons used in button
    def load_icons(self, height_limit, *name):
        icons_tuple = tuple(self.adjust_size(pygame.image.load(n), height_limit) for n in name)
        return(icons_tuple)

### convert degree postion to pixel position
class Converter:
    def __init__(self, screen_size, map_, simulator):
        self.__screen_size = screen_size
        self.__top_left_point = map_.get_top_left_point()
        self.__selected_object_code = simulator.get_selected_object_code()
        # check state when zoomed
        if simulator.get_state(state = "is_zoom", current=True):
            self.__scale = ZOOM_SCALE
        else:
            self.__scale = 1

    def degree_to_pixel(self, degree_position):
        # x_pixel = x_slope* x_degree - b_x
        x_slope = self.__screen_size[0]/(MAP_BOTTOM_RIGHT_DEGREE[1]-MAP_TOP_LEFT_DEGREE[1]) # size of screen divided by size of real map
        x_intercept = -x_slope*MAP_TOP_LEFT_DEGREE[1] 
        x_pixel = degree_position[1] * x_slope + x_intercept
        x_int = int(x_pixel)

        # y_pixel = y_slope* y_degree - b_x
        y_slope =  self.__screen_size[1]/(MAP_BOTTOM_RIGHT_DEGREE[0]-MAP_TOP_LEFT_DEGREE[0])
        y_intercept = -y_slope*MAP_TOP_LEFT_DEGREE[0]
        y_pixel = degree_position[0]*y_slope+y_intercept
        y_int = int(y_pixel)

        # Calculate pixel after check state scale is 1 or 2 
        object_x = (x_int*self.__scale)+self.__top_left_point[0]
        object_y = (y_int*self.__scale)+self.__top_left_point[1]
        return (round(object_x), round(object_y))

    def get_selected_object_code(self):
        return self.__selected_object_code
        
    def get_scale(self):
        return self.__scale

class Calculator:
    #Calculate normal distribution of passenger
    def normal_distribution_seat(passenger):
        list_seat = []
        count = 1000
        for n in range(count):
            count_seat = random.randint(1,passenger)
            list_seat.append(count_seat)
        mean_seat = mean(list_seat)
        std_seat = std(list_seat)
        normal_passenger = int(random.normal(mean_seat, std_seat, 1))
        while(normal_passenger < 0):
            normal_passenger = int(random.normal(mean_seat, std_seat, 1))
        return normal_passenger