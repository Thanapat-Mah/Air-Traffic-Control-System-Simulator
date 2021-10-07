import pygame
from image_loader import load_image
class Map:
    zoom_status = "zoom_out"
    first_click = None
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
        if self.first_click is None:
            self.first_click = pygame.mouse.get_pos()
        click_list = pygame.mouse.get_pos()
        first_click_list = list(self.first_click)
        last_click_list = list(click_list)
        diff =  last_click_list[1] - first_click_list[1]
        #if top left point hit border and have moving order
        if self.__top_left_point[1] > 0 and diff >= 0: 
            diff = 0
        #if top left point hit border and have moving order
        if self.__top_left_point[1] < -750 and diff <= 0: 
            diff = 0
        top_left_point_list = list(self.__top_left_point)
        top_left_point_list[1] += (diff/20)
        self.__top_left_point = tuple(top_left_point_list)

    def get_top_left_point(self):
        return self.__top_left_point

    def draw_map(self, display):
        display.blit(self.__image, self.__top_left_point)

    def check_event(self, event):
        if pygame.mouse.get_pressed()[1]:
            self.zoom_in()
        if (pygame.mouse.get_pressed()[2] and self.zoom_status == "zoom_in" ):
            self.move()
        if event.type == pygame.MOUSEBUTTONUP:
            self.first_click = None
            
            

