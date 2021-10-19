import pygame

### list box for contain clickable status box on sidebar
class ListBox:
	def __init__(self, x, y, width, height, border_radius, font, text_color, background_color, menu_topic_tuple):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__font = font
		self.__text_color = text_color
		self.__background_color = background_color
		self.__menu_topic_tuple = __menu_topic_tuple
		self.__menu_topic_rect = None
		self.__selected_topic = ""
		self.__selected_page = 0
		# self.__switch_page_button = tuple(Button())
		self.__status_button_list = []

	def update_button(self):
		pass

	def draw_button(self):
		pass

	def draw_list_box(self):
		pass

	def check_event(self):
		pass