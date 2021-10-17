### constant value
# pygame.font.Font object in specific font and size
import pygame
pygame.font.init()
FONT = {
	"roboto_normal": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24),
	"roboto_small": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 16),
	"bebasneue_normal": pygame.font.Font('assets/fonts/BebasNeue-Regular.ttf', 22)
}
# roboto_normal = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24)
# bebasneue_normal = pygame.font.Font('assets/fonts/BebasNeue-Regular.ttf', 22)
# RGB code for every color used in program
COLOR = {
	"black": (28, 28, 28),
	"dark_gray": (57, 62, 70),
	"light_gray": (194, 194, 194),
	"white": (255, 255, 255),
	"pink": (255, 82, 96)
}
MAP_PATH = "assets/images/map_full_size.png"
MAP_TOP_LEFT_DEGREE = (21.924045, 85.992727)		# decimal degree position of top left corner of map image
MAP_BOTTOM_RIGHT_DEGREE = (5.121690, 117.554380)	# decimal degree position of bottom right corner of map image
ICON_PATH = {
	"pause": "assets/icons/icon_paused.png",
	"play": "assets/icons/icon_playing.png",
	"speed1": "assets/icons/icon_speed_1.png",
	"speed2": "assets/icons/icon_speed_2.png",
	"speed3": "assets/icons/icon_speed_3.png",
	"zoom_in": "assets/icons/icon_zoom_in.png",
	"zoom_out": "assets/icons/icon_zoom_out.png"
}



### simulations data setting
# airport name, IATA code and location
AIRPORTS = (
	("Chiang Mai International Airport", "CNX", 800, 200),
	("Suvarnabhumi Airport", "BKK", 905, 488),
	("Khon Kaen Airport", "KKC", 1020, 320),
	("Phuket International Airport", "HKT", 770, 800),
	("Hat Yai International Airport", "HDY", 890, 890)
	# ("Chiang Mai International Airport", "CNX", 18.767750, 98.964000),
    # ("Suvarnabhumi Airport", "BKK", 13.690000, 100.750111),
    # ("Khon Kaen Airport", "KKC", 16.465417, 102.787361),
    # ("Phuket International Airport", "HKT", 8.110722, 98.306944),
    # ("Hat Yai International Airport", "HDY", 6.936417, 100.393389)
)
# airline IATA code and full name
AIRLINES = (
	("FD", "Thai AirAsia"),
	("TG", "Thai Airways International")
)
PLANE_INFORMATIONS = (
	("Airbus A320-200", 180, 863, (29000, 39000)),
	("Boeing 787-9", 236, 1050, (35000, 43000))
)
ZOOM_SCALE = 2		# map zoom scaling
