import pygame
from image_loader import load_image
class Map:
    zoom_status = "zoom_out"
    def __init__ (self, image_path, screen_size, top_left_point = ((0, 0))):
        self.__width = screen_size[0] 
        self.__height = screen_size[1]
        self.__image = load_image(image_path = image_path, screen_size=(self.__width, self.__height))
        self.__top_left_point = top_left_point

    def zoom_in(self):
        if self.zoom_status != "zoom_in":
            self.zoom_status = "zoom_in"
            self.__width = int(self.__width*2)
            self.__height = int(self.__height*2)
            print("rescale_width, rescale_high: ", self.__width, self.__height)
            self.__top_left_point = ((-self.__width/4, 0))
            print("__top_left_point: ", self.__top_left_point)
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    def zoom_out(self):

        if self.zoom_status != "zoom_out":
            self.zoom_status = "zoom_out"
            self.__width = int(self.__width/2)
            self.__height = int(self.__height/2)
            print("rescale_width, rescale_high: ", self.__width, self.__height)
            self.__top_left_point = ((0, 0))
            print("__top_left_point: ", self.__top_left_point)
            self.__image = pygame.transform.scale(self.__image, ((self.__width, self.__height)))

    def move(self):
        pass

    def get_top_left_point(self):
        pass

    def draw_map(self, display):
        display.blit(self.__image, self.__top_left_point)

    def check_event(self, event):
        
        if pygame.mouse.get_pressed()[2]:
            print("self.__image.get_size(): ",self.__image.get_size())
            self.zoom_in()
        elif pygame.mouse.get_pressed()[0]:
            print("self.__image.get_size(): ",self.__image.get_size())
            self.zoom_out()
