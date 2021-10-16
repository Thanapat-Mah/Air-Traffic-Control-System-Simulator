import pygame
class PlaneManager:
    def __init__(self, image):
        self.plane_icon = None
        self.plane_specifictaion_tuple = None
        self.plane_list = None
        self.airline_tuple = None
        self.flight_counter = None
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



