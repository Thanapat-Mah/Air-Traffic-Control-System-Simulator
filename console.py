import pygame
from configuration import COLOR, FONT, ICON_PATH, KEYWORD, FORMAT, OPTIONAL, REQUIRED, SYNTAX, FAIL_RESPONSE
from utilities import Loader
from button import MultiStateButton
from command_input import CommandInput

### console for input command, show response and notify collision detection
class Console:
	def __init__(self, x, y, width, height, border_radius=10, background_color=COLOR["transparance_black"],
		font=FONT["consolas_small"], user_text_prefix=">"):
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
		self.__text_spacing = {
			"user": 10,
			"success_response": 0,
			"fail_response": 0,
			"warning": 10
		}
		self.__user_text_prefix = user_text_prefix
		self.__syntax = SYNTAX
		self.__command_log = [{"success_response": "Type something in!"}]
		self.__command_input = CommandInput(x=25, y=self.__height-40, width=self.__width-80, height=30, font=self.__font)
		self.__command_input_text = ""
		self.__formatted_input = []
		loader = Loader()
		self.__help_button = MultiStateButton(x=self.__width-40, y=self.__y+self.__height-40, width=30, height=30,
			label_tuple=("", ""), icon_tuple=loader.load_icons(30, ICON_PATH["help_inactive"], ICON_PATH["help_active"]),
			border_radius=15)
		self.__is_help_open = False 	# open status of commnand help

	# pop out formatted input (return value and clear value)
	def pop_formatted_input(self):
		tmp = []
		if len(self.__formatted_input) > 0:
			tmp = self.__formatted_input.copy()
			self.__formatted_input.clear()
		return(tmp)

	# handle incoming command input, check for command validity and save formatted command
	def handle_input(self):
		self.__formatted_input = []
		if self.__command_input_text != "":
			self.__command_log.append({"user": f"{self.__user_text_prefix} {self.__command_input_text}"})
			# tokenize input
			input_tokens = self.__command_input_text.split()
			input_syntax = False
			invalid_command = False
			invalid_syntax = False
			# check for keyword
			for input_token in input_tokens:
				for command_syntax in self.__syntax:
					if input_token == command_syntax[KEYWORD]:
						input_syntax = command_syntax
			# if there is no keyword (command) in input, respond with invalid command
			if not input_syntax:
				invalid_command = True
				# print("no command(keyword)")
			# else, check for syntax
			else:
				# check if input exceed the number of token in correct syntax format
				if len(input_tokens) > len(input_syntax[FORMAT]):
					invalid_syntax = True
					# print("exceed")
				# else, process command input token by token
				else:
					for i in range(len(input_syntax[FORMAT])):
						# extract token from input and correct syntax
						input_token = ""
						if i < len(input_tokens):
							input_token = input_tokens[i]
						command_token = input_syntax[FORMAT][i]
						if command_token == KEYWORD:
							# check if keyword is in wrong order
							if input_token != input_syntax["keyword"]:
								invalid_syntax = True
								# print("wrong order")
							# else, collect keyword to formatted input
							else:
								self.__formatted_input.insert(0, input_token)
						else:
							# check if required parameter is missing
							if command_token == REQUIRED:
								if input_token == "":
									invalid_syntax = True
									# print("required missing")
							# check for optional parameter..., maybe no need to check
							# collect parameter to formatted input
							self.__formatted_input.append(input_token)
			# if something is invalid, clear formatted input and send fail response
			if invalid_command:
				self.__formatted_input.clear()
				self.__command_log.append({"fail_response": FAIL_RESPONSE["invalid_command"]})
			elif invalid_syntax:
				self.__formatted_input.clear()
				self.__command_log.append({"fail_response": FAIL_RESPONSE["invalid_syntax"]})
			else:
				self.__command_log.append({"success_response": "keyword and syntax is pass!"})
			# clear input text after process
			self.__command_input_text = ""

	# handle incoming response from PlaneManager
	def handle_response(self, responses):
		for response in responses:
			self.__command_log.append(response)

	# check for clicking on command input box or help button
	def check_event(self, event):
		self.__command_input.check_clicking(event, parent_surface_position=(self.__x, self.__y))
		input_text = self.__command_input.check_input(event)
		if input_text != "":
			self.__command_input_text = input_text
			self.handle_input()
		if self.__help_button.click(event):
			self.__is_help_open = not self.__is_help_open
			self.__help_button.switch_state()
			self.__command_log.append({"warning": f"now help opening is {self.__is_help_open}"})

	# draw console including command log, command input and help button
	def draw_console(self, display):
		# draw transparent background
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
		# draw console surface
		display.blit(self.__background_surface, (self.__x, self.__y))
		# draw help button
		self.__help_button.draw_button(display)