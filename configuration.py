### constant value
# pygame.font.Font object in specific font and size
import pygame
pygame.font.init()
FONT = {
	"roboto_normal": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 18),
	"roboto_small": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 14),
	"roboto_large": pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24),
	"bebasneue_normal": pygame.font.Font('assets/fonts/BebasNeue-Regular.ttf', 22),
	"bebasneue_small": pygame.font.Font('assets/fonts/BebasNeue-Regular.ttf', 16),
	"consolas_small": pygame.font.Font('assets/fonts/CONSOLA.TTF', 14)
}
# RGB code for every color used in program
COLOR = {
	"black": (28, 28, 28),
	"transparance_black": (28, 28, 28, int(255*0.8)),
	"dark_gray": (57, 62, 70),
	"light_gray": (194, 194, 194),
	"white": (255, 255, 255),
	"pink": (255, 82, 96),
	"red": (197, 0, 0),
	"transparance_red": (197, 0, 0, int(255*0.5)),
	"green": (63, 181, 61)
}
MAP_PATH = "assets/images/map_full_size.png"
PLANE_PATH = "assets/images/plane.png"
AIRPORT_PATH = "assets/images/airport.png"
MAP_TOP_LEFT_DEGREE = (21.755940, 85.028580)		# decimal degree position of top left corner of map image
MAP_BOTTOM_RIGHT_DEGREE = (3.614883, 118.405937)	# decimal degree position of bottom right corner of map image
ICON_PATH = {
	"pause": "assets/icons/icon_paused.png",
	"play": "assets/icons/icon_playing.png",
	"speed1": "assets/icons/icon_speed_1.png",
	"speed2": "assets/icons/icon_speed_2.png",
	"speed3": "assets/icons/icon_speed_3.png",
	"zoom_in": "assets/icons/icon_zoom_in.png",
	"zoom_out": "assets/icons/icon_zoom_out.png",
	"magnifier": "assets/icons/icon_magnifier.png",
	"help_active": "assets/icons/help_active.png",
	"help_inactive": "assets/icons/help_inactive.png"
}
HELP_PATH = {
	"command_generate": "assets/images/help/command_generate.png",
	"command_takeoff": "assets/images/help/command_takeoff.png",
	"command_hold": "assets/images/help/command_hold.png",
	"command_continue": "assets/images/help/command_continue.png",
	"command_altitude": "assets/images/help/command_altitude.png"
}


### simulations data setting
# airport name, IATA code and location
AIRPORTS = (
	("Chiang Mai International Airport", "CNX", 18.767750, 98.964000),
    ("Suvarnabhumi Airport", "BKK", 13.690000, 100.750111),
    ("Khon Kaen Airport", "KKC", 16.465417, 102.787361),
    ("Phuket International Airport", "HKT", 8.110722, 98.306944),
    ("Hat Yai International Airport", "HDY", 6.936417, 100.393389)
)
# airline IATA code and full name
AIRLINES = (
	("FD", "Thai AirAsia"),
	("TG", "Thai Airways Insternational")
)
# plane model information model code, model, max seat, average speed, altitude range
PLANE_INFORMATIONS = (
	("A320", "Airbus A320-200", 180, 863, (29000, 39000)),
	("B787", "Boeing 787-9", 236, 903, (35000, 43000))
)
ZOOM_SCALE = 2.5 # map zoom scaling

ROC = 3500/60 	 # rate of climbing 3500 ft/min
ROT = 3 		 # rate of turn 3 degree / second
ACCELERATE = 6 	 #accelerate when taking off and landing (m/s^2)
PLNAE_PHASE = {
	"waiting":"Waiting",
	"takingoff":"Taking-off",
	"climbing":"Climbing",
	"cruising":"Cruising",
	"descending":"Descending",
	"landing":"Landing",
	"holding":"Holding"
}
FAIL_RESPONSE = {
	"invalid_command": "Invalid command, please try again",
	"invalid_syntax": "Invalid syntax, please try again",
	"invalid_flight_code": "Invalid flight code, please try again",
	"invalid_value": "Invalid value, please try again",
	"can_not_command": "Can not command, please try again"
}
# command syntax
KEYWORD = "keyword"
FORMAT = "format"
OPTIONAL = "optional"
REQUIRED = "require"
SYNTAX = [
	# generate A320, BKK, CNX
	{KEYWORD: "generate",
	FORMAT: [KEYWORD, OPTIONAL, OPTIONAL, OPTIONAL]},
	# TG001 takeoff
	{KEYWORD: "takeoff",
	FORMAT: [REQUIRED, KEYWORD]},
	# TG001 hold
	{KEYWORD: "hold",
	FORMAT: [REQUIRED, KEYWORD]},
	# TG001 continue
	{KEYWORD: "continue",
	FORMAT: [REQUIRED, KEYWORD]},
	# TG001 altitude 30000
	{KEYWORD: "altitude",
	FORMAT: [REQUIRED, KEYWORD, REQUIRED]},
]