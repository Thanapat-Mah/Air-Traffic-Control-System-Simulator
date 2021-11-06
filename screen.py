import pygame
from configuration import COLOR, FONT
from utilities import Converter, Converter

### screen of program, adjust and display components.
class Screen:
	def __init__(self, fullscreen=False, width=1500, height=750, background_color=COLOR["dark_gray"], text_background_color=COLOR["black"], text_color=COLOR["white"], font=FONT["roboto_normal"]):
		self.__fullscreen = fullscreen
		# if fullsreen, adjust width and height to fit user's display size
		if fullscreen:
			info_object = pygame.display.Info()
			self.__width = info_object.current_w
			self.__height = info_object.current_h
		else:
			self.__width = width
			self.__height = height
		self.__background_color = background_color
		self.__display = pygame.display.set_mode((self.__width, self.__height))
		self.__text_background_color = text_background_color
		self.__text_color = text_color
		self.__font = font

	# return the size of screen in format (width, height)
	def get_size(self):
		return((self.__width, self.__height))

	# refresh plain color background
	def refresh_background(self):
		#self.__display.fill(self.__background_color)
		pass

	# draw name of simulation
	def draw_name(self, name):
		padding = 10
		text_surface = self.__font.render(name, True, self.__text_color)
		text_size = text_surface.get_size()
		pygame.draw.rect(self.__display, self.__text_background_color,
			((self.__width-text_size[0])/2-padding, 0, text_size[0]+padding*2, text_size[1]+padding*2),
			border_bottom_left_radius=10, border_bottom_right_radius=10)
		self.__display.blit(text_surface, ((self.__width-text_size[0])/2, padding))

	# update screen by re-draw every components
	def update_screen(self, simulator, map_, airport_manager, sidebar, toolbar, plane_manager, collision_detector, console, help_box):
		self.refresh_background()
		converter = Converter(screen_size=(self.__width, self.__height), map_=map_, simulator=simulator)
		map_.draw_map(self.__display)
		airport_manager.draw_all_airport(self.__display, converter=converter)
		plane_manager.draw_all_plane(self.__display, converter=converter)
		toolbar.draw_toolbar(self.__display, simulated_datetime=simulator.get_simulated_datetime())
		sidebar.draw_sidebar(self.__display, simulator=simulator, collision_detector=collision_detector)
		self.draw_name(name=simulator.get_name())
		console.draw_console(self.__display)
		help_box.draw_help_box(self.__display, is_open=console.get_is_help_open())