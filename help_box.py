import pygame
from configuration import COLOR, FONT, HELP_PATH
from utilities import Loader
from button import Button

### help box displaying multiple picture
class HelpBox:
	def __init__(self, x, y, width, height, border_radius=10, background_color=COLOR["transparance_black"],
		font=FONT["consolas_small"], text_color=COLOR["white"]):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
		self.__font = font
		self.__text_color = text_color
		loader = Loader()
		self.__contents = loader.load_icons(self.__width-50, *(HELP_PATH[key] for key in HELP_PATH))
		self.__selected_page = 1
		self.__all_page_count = len(self.__contents)
		page_number_width = self.__font.render("1/2", True, self.__text_color).get_size()[0]*2
		page_button_y = self.__y+self.__height-40
		self.__switch_page_button = (
			Button(x=self.__x+int((self.__width-page_number_width)/2)-40, y=page_button_y, width=40, height=30,text="<<",
				font=self.__font, background_color=self.__background_color, border_color=self.__text_color, border_size=1),
			Button(x=self.__x+int((self.__width+page_number_width)/2), y=page_button_y, width=40, height=30, text=">>",
				font=self.__font, background_color=self.__background_color, border_color=self.__text_color, border_size=1)
			)

	# check for page switching
	def check_event(self, event, is_open=False):
		pass

	# draw help box
	def draw_help_box(self, display, is_open=False):
		# draw transparent background
		pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)

		display.blit(self.__background_surface, (self.__x, self.__y))