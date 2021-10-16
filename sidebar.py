import pygame
from button import MultiStateButton
from configuration import COLOR

### sidebar at left of screen, display simulation's infomations
class Sidebar:
	def __init__(self, screen_size, toolbar_height, notch_width=20, notch_color=COLOR["black"], width=250, background_color=COLOR["black"]):
		self.__x = screen_size[0] - notch_width
		self.__y = 0
		self.__width = width
		self.__height = screen_size[1] - toolbar_height
		self.__is_open = False
		self.__notch_width = notch_width
		self.__notch_color = notch_color
		self.__notch_button = MultiStateButton(label_tuple=("<|", "|>"), x=0, y=(self.__height-60)/2, width=40, height=60,
			border_size=0, border_radius=10, background_color=notch_color)
		self.__background_color = background_color

	# draw all components on sidebar
	def draw_sidebar(self, display):
		if self.__is_open:
			# modify position
			current_x = self.__x - self.__width
			self.__notch_button.x = self.__x-self.__notch_width-self.__width-10
			# draw background
			pygame.draw.rect(display, self.__background_color, (current_x+self.__notch_width, self.__y, self.__width, self.__height))
		else:
			# modify position
			current_x = self.__x
			self.__notch_button.x = self.__x-self.__notch_width-10
		# draw notch
		pygame.draw.rect(display, self.__notch_color, (current_x, self.__y, self.__notch_width, self.__height))
		self.__notch_button.draw_button(display=display)

	# check sidebar openning/closing
	def check_event(self, event):
		if self.__notch_button.click(event):
			self.__is_open = not self.__is_open
			self.__notch_button.switch_state()