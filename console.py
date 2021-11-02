import pygame
from configuration import COLOR, FONT, KEYWORD, FORMAT, OPTIONAL, REQUIRED, SYNTAX
from button import MultiStateButton
from command_input import CommandInput

### console for input command, show response and notify collision detection
class Console:
	def __init__(self, x, y, width, height, border_radius=10, background_color=COLOR["transparance_black"],
		font=FONT["roboto_normal"], user_text_prefix=">"):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
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
		self.__command_input = CommandInput(x=10, y=self.__height-40, width=self.__width/2, height=30)
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

	# draw console including command log, command input and help button
	def draw_console(self, display):
		pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)
		
		text = "> TG001 Capybara 555555555555555555555555555555555555555555555555555555555555555555555 bara"
		text_surface = self.__font.render(text, True, self.__text_color["user"])
		self.__background_surface.blit(text_surface, (50, 50))
		# draw command input box
		self.__command_input.draw_command_input(display=self.__background_surface)
		display.blit(self.__background_surface, (self.__x, self.__y))