import pygame
from configuration import COLOR, FONT

### command input box for receive command text input from user
class CommandInput:
	def __init__(self, x, y, width, height, border_radius=5, border_size=2, background_color=COLOR["dark_gray"],
		typing_background_color=COLOR["black"], font=FONT["consolas_small"], text_color=COLOR["white"]):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__border_size = border_size
		self.__background_color = background_color
		self.__typing_background_color = typing_background_color
		self.__font = font
		self.__text_color = text_color
		self.__placeholder_text = "Command..."
		self.__input_buffer = ""
		self.__is_typing = False
		self.__hit_box = pygame.Rect(self.__x, self.__y, self.__width, self.__height)
		self.__background_surface = pygame.Surface((self.__width, self.__height), pygame.SRCALPHA)

	# check for clicking on command input box
	def check_clicking(self, event, parent_surface_position):
		x, y = pygame.mouse.get_pos()
		x -= parent_surface_position[0]
		y -= parent_surface_position[1]
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.__hit_box.collidepoint(x, y):
					self.__is_typing = True
				else:
					self.__is_typing = False

	# return input buffer after user press enter
	def check_input(self, event):
		if self.__is_typing and (event.type == pygame.KEYDOWN):
			# check for backspace
			if event.key == pygame.K_BACKSPACE:
				if len(self.__input_buffer) > 0:
					self.__input_buffer = self.__input_buffer[:-1]
			# check for enter
			elif event.key == pygame.K_RETURN:
				input_text = self.__input_buffer
				self.__input_buffer = ""
				return(input_text)
			# anything else count as input, collect them
			else:
				self.__input_buffer += event.unicode
		return("")

	# draw command input box and buffer if it available
	def draw_command_input(self, display):
		# choose color and border width, up to current is_typing value		
		if self.__is_typing or self.__input_buffer != "":
			background_color = self.__typing_background_color
			border_size = self.__border_size
			# draw rounded rect on its surface
			pygame.draw.rect(self.__background_surface, self.__typing_background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)
			# draw rounded rect border on its surface
			pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(),
				width=self.__border_size, border_radius=self.__border_radius)
			# draw input buffer text
			input_buffer_surface = self.__font.render(self.__input_buffer, True, self.__text_color)
			input_buffer_y = (self.__background_surface.get_size()[1] - input_buffer_surface.get_size()[1])/2
			self.__background_surface.blit(input_buffer_surface, (10, input_buffer_y))
		else:
			# draw rounded rect on its surface
			pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)
			# draw placeholder
			placeholder_surface = self.__font.render(self.__placeholder_text, True, self.__text_color)
			placeholder_y = (self.__background_surface.get_size()[1] - placeholder_surface.get_size()[1])/2
			self.__background_surface.blit(placeholder_surface, (10, placeholder_y))
		# draw its surface on display
		display.blit(self.__background_surface, (self.__x, self.__y))