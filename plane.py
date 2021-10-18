import pygame
from configuration import FONT, COLOR
# from configuration import AIRLINES, PLANE_INFORMATIONS

# plane information/specification for each model
class PlaneInformation:
    def __init__(self, model, max_seat, speed, altitude):
        self.model = model
        self.max_seat = max_seat
        self.speed = speed
        self.altitude = altitude

# airline information for each airline
class AirlineInformation:
    def __init__(self, name, code):
        self.name = name
        self.code = code

class PlaneManager:
    def __init__(self, image, text_color=COLOR["black"], font=FONT["bebasneue_normal"]):
        self.plane_icon = None
        self.plane_specifictaion_tuple = None
        self.plane_list = []
        self.airline_tuple = None
        self.flight_counter = 0
        self.text_color = None
        self.font = None

    def mock_update_plane_position(self):
        pass

    def mock_update_plane_status(self):
        return {
            'Flying': 10,
            'Taking-off': 10,
            'Landing': 10,
            'Circling': 10,
            'Waiting': 10
        }

    def mock_is_empty(self, airport_code=None):
        return True

    def draw_plane(self):
        pass

    def mock_check_selection (self, event=None):
        return 'TG200'

    def mock_get_detail(self, code=None):
        return ["Flight Code: TG200",
                "Airline: Thai AirAsia",
                "From: CNX To: BKK",
                "Passenger: 83",
                "Altitude: 37,000 ft",
                "Speed: 900 km/h",
                "Status: Flying"
        ]


class Plane:
    def __init__(self):
        self.flight_code = None
        self.airline_code = None
        self.degree_position = None
        self.model = None
        self.passenger = None
        self.speed = None
        self.direction = None
        self.altitude = None
        self.origin = None
        self.route = None
        self.destination = None
        self.status = None

    def get_information(self):
        return ({})

    def generate_random_plane(self, plane_information=None, airline_information=None, airport_manager=None):
        pass

    def update_position(self, time_pass=None):
        pass
