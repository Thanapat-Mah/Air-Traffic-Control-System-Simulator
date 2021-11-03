import pygame
from configuration import COLOR, FONT, KEYWORD, FORMAT, OPTIONAL, REQUIRED, SYNTAX
from button import MultiStateButton
from command_input import CommandInput

### console for input command, show response and notify collision detection
class Console:
	def __init__(self, x, y, width, height, border_radius=10, background_color=COLOR["transparance_black"],
		font=FONT["consolas_normal"], user_text_prefix=">"):
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
			"success_response": 0,
			"fail_response": 0,
			"warning": 10
		}
		self.__command_log = [{"success_response": "Type something in!"}]
		self.__syntax = SYNTAX
		self.__command_input = CommandInput(x=25, y=self.__height-40, width=self.__width-40, height=30, font=self.__font)
		self.__command_input_text = ""
		self.__help_button = None 		# MultiStateButton()

	# handle incoming command input
	def handle_input(self):
		if self.__command_input_text != "":
			self.__command_log.append({"user": f"{self.__user_text_prefix} {self.__command_input_text}"})
			self.__command_log.append({"fail_response": "Can't process command yet"})
			self.__command_input_text = ""
		l = []
		l.append(["generate"])
		l.append(["generate", "A320", "BKK", "CNX"])
		l.append(["takeoff", "TG001"])
		l.append(["hold", "TG001"])
		l.append(["continue", "TG001"])
		l.append(["altitude", "TG001", "30000"])
		return(l[1])

	# check for clicking on command input box or help button
	def check_event(self, event):
		self.handle_input()
		self.__command_input.check_clicking(event, parent_surface_position=(self.__x, self.__y))
		input_text = self.__command_input.check_input(event)
		if input_text != "":
			self.__command_input_text = input_text

	# draw console including command log, command input and help button
	def draw_console(self, display):
		pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)

		# draw command log
		text_y = 10
		for log in self.__command_log:
			for key in log:
				# render log text
				text = log[key]
				text_surface = self.__font.render(text, True, self.__text_color[key])
				# spacing this line text
				text_y += self.__text_spacing[key]
				# if text is exceed the area of console, remove oldest current log
				if text_y > (self.__height-40-text_surface.get_size()[1]):
					self.__command_log = self.__command_log[1:]
				else:
					# draw text on surface
					self.__background_surface.blit(text_surface, (10, text_y))
				# spacing next line text
				text_y += text_surface.get_size()[1]
		# draw command input box
		prefix_surface = self.__font.render(self.__user_text_prefix, True, self.__text_color["user"])
		self.__background_surface.blit(prefix_surface, (10, self.__height-35))
		self.__command_input.draw_command_input(display=self.__background_surface)
		display.blit(self.__background_surface, (self.__x, self.__y))