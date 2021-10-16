### constant value
# pygame.font.Font object in specific font and size
import pygame
pygame.font.init()
FONT = {
	"roboto_normal": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24),
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
# airport IATA code and location
AIRPORTS = (
	("CNX", 800, 200),
	("BKK", 905, 488),
	("KKC", 1020, 320),
	("HKT", 770, 800),
	("HDY", 890, 890)
)
ZOOM_SCALE = 2		# map zoom scaling	