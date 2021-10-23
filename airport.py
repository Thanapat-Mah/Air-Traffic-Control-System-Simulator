import pygame
from configuration import FONT, COLOR, AIRPORTS, AIRPORT_PATH, ZOOM_SCALE
from simulator import Simulator
from utilities import Loader, Converter

### airport, store information and mark airport' position on map
class Airport:
    def __init__(self, name, code, x, y, screen_size, text_color=COLOR["black"], font=FONT["bebasneue_normal"], airport_size=20):
        self.__name = name
        self.__code = code
        self.__text_color = text_color
        self.__font = font
        self.__airport_image = Loader.load_image(AIRPORT_PATH, (airport_size, airport_size))
        self.__airport_size = airport_size
        self.__pixel_position = Converter.degree_to_pixel((x, y), screen_size)
        self.__degree_position = (x, y)
        self.__status = True
        self.__landed = 0
        self.__departed = 0

    def switch_status(self):
        pass
    
    def get_name(self):
        return self.__name

    def get_pixel_position(self):
        return self.__pixel_position

    # return degree position of airport
    def get_degree_position(self):
        return(self.__degree_position)

    def get_code(self):
        return(self.__code)

    def get_status(self):
        return(self.__status)

    def set_status(self, new_status):
        self.__status = new_status

    # return detail of airport
    def get_detail(self):
        if self.__status:
            status = "Empty"
        else:
            status = "In Use"
        detail_dict = {
            "Name": self.__name,
            "IATA Code": self.__code,
            "Status": status,
            "Landed": self.__landed,
            "Departed": self.__departed
        }
        return(Converter.dict_to_string(detail_dict))

    # draw image and IATA code of airport
    def draw_airport(self, display, top_left_point, scale):
        # calculate center pixel position of airport
        airport_x = (self.__pixel_position[0]*scale)+top_left_point[0]
        airport_y = (self.__pixel_position[1]*scale)+top_left_point[1]
        # draw image
        image_x = airport_x - 0.5 * self.__airport_size
        image_y = airport_y - 0.5 * self.__airport_size
        display.blit(self.__airport_image, (image_x, image_y))
        # draw IATA code at right side of image
        text_surface = self.__font.render(self.__code, True, self.__text_color)
        text_x = image_x + 1.5 * self.__airport_size
        text_y = image_y + (self.__airport_size - text_surface.get_size()[1])/2
        display.blit(text_surface, (text_x, text_y+3))

    # check if this airport is clicked, return empty string or airport' IATA code
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                hit_box = self.__airport_image.get_rect(center=(self.__pixel_position[0], self.__pixel_position[1]))
                if hit_box.collidepoint(x, y):
                    return(self.__code)
        return("")

### airport manager, used to manage and coordinate all airport related task
class AirportManager:
    def __init__(self, screen_size):
        airport_list = [Airport(name=a[0], code=a[1], x=a[2], y=a[3], screen_size=screen_size) for a in AIRPORTS]
        self.__airport_tuple = tuple(airport_list)

    def get_airport_list(self):
        return self.__airport_tuple

    # update status of airport and return all aiport in each status
    def update_airport(self, plane_manager=None):
        status_dict = {
            "Empty": [],
            "In Use": []
        }
        for airport in self.__airport_tuple:
            if airport.get_status():
                status_dict["Empty"].append(airport.get_code())
            else:
                status_dict["In Use"].append(airport.get_code())
        return(status_dict)

    # draw all airport and IATA code
    def draw_all_airport(self, display, map_, simulator):
        top_left_point = map_.get_top_left_point()
        scale = 1
        if simulator.get_state(state = "zoomed", current=True):
            scale = ZOOM_SCALE
        else:
            scale = 1
        for airport in self.__airport_tuple:
            airport.draw_airport(display=display, top_left_point=top_left_point, scale=scale) 

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

    def get_airport_list(self):
        return self.__airport_tuple
