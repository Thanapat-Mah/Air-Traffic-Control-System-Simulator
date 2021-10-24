import pygame
from configuration import FONT, COLOR, AIRPORTS, AIRPORT_PATH, ZOOM_SCALE
from simulator import Simulator
from utilities import Loader, Converter

### airport, store information and mark airport' position on map
class Airport:
    def __init__(self, name, code, x, y):
        self.__name = name
        self.__code = code        
        self.__degree_position = (x, y)
        self.__available = True
        self.__landed = 0
        self.__departed = 0
        self.__hit_box = None

    def get_code(self):
        return(self.__code)

    def get_degree_position(self):
        return(self.__degree_position)

    def get_available(self):
        return(self.__available)

    def set_available(self, new_available):
        self.__available = new_available

    def set_hit_box(self, new_hit_box):
        self.__hit_box = new_hit_box

    # return detail of airport
    def get_detail(self):
        if self.__available:
            status = "Empty"
        else:
            status = "In Use"
        detail_string_list = [
            "Name: {}".format(self.__name),
            "IATA Code: {}".format(self.__code),
            "Status: {}".format(status),
            "Landed: {}".format(self.__landed),
            "Departed: {}".format(self.__departed)
        ]
        return(detail_string_list)

    # check if this airport is clicked, return empty string or airport' IATA code
    def click(self, event):
        if self.__hit_box:
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.__hit_box.collidepoint(x, y):
                        return(self.__code)
        return("")

### airport manager, used to manage and coordinate all airport related task
class AirportManager:
    def __init__(self, airport_size=20, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        self.__airport_size = airport_size     
        self.__airport_icon = Loader.load_image(AIRPORT_PATH, (airport_size, airport_size))        
        airport_list = [Airport(name=a[0], code=a[1], x=a[2], y=a[3]) for a in AIRPORTS]
        self.__airport_tuple = tuple(airport_list)
        self.__text_color = text_color
        self.__font = font

    def get_airport_tuple(self):
        return self.__airport_tuple

    # update status of airport and return all aiport in each status
    def update_airport(self, plane_manager=None):
        status_dict = {
            "Empty": [],
            "In Use": []
        }
        for airport in self.__airport_tuple:
            if airport.get_available():
                status_dict["Empty"].append(airport.get_code())
            else:
                status_dict["In Use"].append(airport.get_code())
        return(status_dict)

    # draw all airport and IATA code
    def draw_all_airport(self, display, converter):
        for airport in self.__airport_tuple:
            # set new hit box
            position = airport.get_degree_position()
            pixel_position = converter.mock_degree_to_pixel(degree_postion=position)
            new_hit_box = self.__airport_icon.get_rect(center = pixel_position)
            airport.set_hit_box(new_hit_box)
            # draw airport
            display.blit(self.__airport_icon, new_hit_box)
            # draw IATA code
            text_surface = self.__font.render(airport.get_code(), True, self.__text_color)
            text_x = pixel_position[0] - text_surface.get_size()[0]/2
            text_y = pixel_position[1] + self.__airport_size/2
            display.blit(text_surface, (text_x, text_y))

    # return selected airport' IATA code
    def check_selection (self, event):
        selected_airport = ""
        for airport in self.__airport_tuple:
            if selected_airport == "":
                selected_airport = airport.click(event)
        return(selected_airport)

    # return selected airports detail
    def get_detail(self, code):
        airport_detail_dict = {}
        for airport in self.__airport_tuple:
            if code == airport.get_code():
                return(airport.get_detail())
        return("")