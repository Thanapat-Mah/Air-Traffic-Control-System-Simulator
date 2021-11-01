import pygame
from configuration import COLOR, FONT, KEYWORD, FORMAT, OPTIONAL, REQUIRED, SYNTAX
from button import MultiStateButton

### console for input command, show response and notify collision detection
class Console:
	def __init__(self, x, y, width, height, border_radius=5, background_color=COLOR["black"], background_alpha=50,
		font=FONT["roboto_normal"], user_text_prefix=">"):
		self._x = x
		self._y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__background_alpha = background_alpha
		self.__font = font
		self.__text_color = {
			"user": COLOR["white"],
			"success_response": COLOR["green"],
			"fail_response": COLOR["pink"],
			"warning": COLOR["pink"]
		}
		self.__user_text_prefix = user_text_prefix
		self.__text_spacing = {
			"user": 10,
			"success_response": 5,
			"fail_response": 5,
			"warning": 10
		}
		self.__command_log = [{"success_response": "Initailizing..."}]
		self.__syntax = SYNTAX
		self.__command_input = None 	# CommandInput()
		self.__help_button = None 		# MultiStateButton()

	### mock method
	def mock_handle_input(self):
		l = []
		l.append(["generate"])
		l.append(["generate", "A320", "BKK", "CNX"])
		l.append(["takeoff", "TG001"])
		l.append(["hold", "TG001"])
		l.append(["continue", "TG001"])
		l.append(["altitude", "TG001", "30000"])
		return(l[1])

	def mock_check_clicking(self):
		return(False)