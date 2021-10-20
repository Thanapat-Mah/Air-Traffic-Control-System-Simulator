import pygame
from configuration import MAP_TOP_LEFT_DEGREE, MAP_BOTTOM_RIGHT_DEGREE

class Loader:

    def load_image(self, image_path, size, scale = 1):
        screen_size_scaled = (size[0]*scale, size[1]*scale)
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

class Converter:
    def dict_to_string(dict_data):
        string_list = []
        for key in dict_data:
            string_list.append(str(key)+": "+str(dict_data[key]))
        return(string_list)

    def degree_to_pixel(self, degree_postion, screen):
        screen_size = screen
        #x_pixel = x_slope* x_degree - b_x
        x_slope = screen_size[0]/(MAP_BOTTOM_RIGHT_DEGREE[1]-MAP_TOP_LEFT_DEGREE[1]) # size of screen divided by size of real map
        x_intercept = -x_slope*MAP_TOP_LEFT_DEGREE[1] 
        x_pixel = degree_postion[1]*x_slope +x_intercept
        #y_pixel = y_slope* y_degree - b_x
        y_slope =  screen_size[1]/(MAP_BOTTOM_RIGHT_DEGREE[0]-MAP_TOP_LEFT_DEGREE[0])
        y_intercept = -y_slope*MAP_TOP_LEFT_DEGREE[0]
        y_pixel = degree_postion[0]*y_slope+y_intercept
        return (int(x_pixel), int(y_pixel))