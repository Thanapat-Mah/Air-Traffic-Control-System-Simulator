import pygame
from color import Color
from font import Font

### screen of program, adjust and display component.
class Screen:
	def __init__(self, fullscreen=False, width=1500, height=750, background_color=Color.dark_gray, text_background_color=Color.black, text_color=Color.white, font=Font.roboto_normal):
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
		self.display = pygame.display.set_mode((self.__width, self.__height))
		self.__text_background_color = text_background_color
		self.__text_color = text_color
		self.__font = font

	# return the size of screen in format (width, height)
	def get_size(self):
		return((self.__width, self.__height))

	# refresh plain color background
	def refresh_background(self):
		self.display.fill(self.__background_color)

	# draw name of simulation
	def draw_name(self, display, name):
		padding = 10
		text_surface = self.__font.render(name, True, self.__text_color)
		text_size = text_surface.get_size()
		pygame.draw.rect(display, self.__text_background_color,
			((self.__width-text_size[0])/2-padding, 0, text_size[0]+padding*2, text_size[1]+padding*2),
			border_bottom_left_radius=10, border_bottom_right_radius=10)
		display.blit(text_surface, ((self.__width-text_size[0])/2, padding))

	# update screen by re-draw every components
	def update_screen(self, simulator=None, map=None, airport=None, sidebar=None, toolbar=None):
		self.refresh_background()
		map.draw_map(self.display)
		airport.draw_airport(self.display)
		toolbar.draw_toolbar(self.display, simulated_datetime=simulator.get_simulated_datetime())
		sidebar.draw_sidebar(self.display)
		self.draw_name(self.display, name=simulator.get_name())
		
