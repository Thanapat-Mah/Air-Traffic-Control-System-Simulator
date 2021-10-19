import pygame
from configuration import COLOR, FONT
from button import MultiStateButton, StatusButton
from information_box import InformationBox

### sidebar at left of screen, display simulation's infomations
class Sidebar:
	def __init__(self, screen_size, toolbar_height, notch_width=20, notch_color=COLOR["black"], width=350,
		background_color=COLOR["black"], font=FONT["roboto_small"], padding=10):
		self.__x = screen_size[0]						# x position of sidebar background, at closing state
		self.__y = 0
		self.__width = width
		self.__height = screen_size[1] - toolbar_height
		self.__is_open = False							# begin with closing state
		self.__notch_width = notch_width
		self.__notch_color = notch_color
		self.__notch_button = MultiStateButton(label_tuple=("<|", "|>"), x=0, y=(self.__height-60)/2, width=40, height=60,
			border_size=0, border_radius=10, background_color=notch_color)
		self.__background_color = background_color
		self.__font = font
		self.__padding = padding
		component_x = self.__x - self.__width + self.__padding
		component_width_space = self.__width - 2*self.__padding
		half_width_space = (component_width_space-padding)/2
		self.__overall_plane_information = InformationBox(x=component_x, y=self.__y+self.__padding,
			width=half_width_space, height=170, topic="Plane", font=self.__font)
		self.__overall_airport_information = InformationBox(x=component_x+half_width_space+self.__padding, y=self.__y+self.__padding,
			width=half_width_space, height=170, topic="Airport", font=self.__font)
		self.__overall_list_box = None
		self.__command_input_box = pygame.Rect((0, 0), (component_width_space, 40))
		self.__command_input_box.bottomleft = (component_x, self.__y+self.__height-self.__padding)
		self.__selected_object_detail = InformationBox(x=component_x, y=self.__command_input_box.topleft[1]-self.__padding-220,
			width=component_width_space, height=220, topic="Details", font=self.__font)
		self.test_button = StatusButton(x=component_x, y=200, width=component_width_space, height=40, code="TG200", detail="Flying")

	# # draw information box including overall plane&airport information, selected object information
	# def draw_information_box(self, display, simulator=None):
	# 	self.__selected_object_detail.draw_information_box(display=display)

	# update simulations information on sidebar
	def update_information(self, overall_plane_information, overall_airport_information, selected_object_detail):
		self.__overall_plane_information.update_content(overall_plane_information)
		self.__overall_airport_information.update_content(overall_airport_information)
		self.__selected_object_detail.update_content(selected_object_detail)

	# draw all components on sidebar
	def draw_sidebar(self, display, simulator=None):
		# change x position when sidebar is open
		if not self.__is_open:
			current_x = self.__x
		else:
			current_x = self.__x - self.__width
			# draw background
			pygame.draw.rect(display, self.__background_color, (current_x, self.__y, self.__width, self.__height))
			# draw information box
			self.__selected_object_detail.draw_information_box(display=display)
			self.__overall_plane_information.draw_information_box(display=display)
			self.__overall_airport_information.draw_information_box(display=display)
			# draw command box
			pygame.draw.rect(display, COLOR["dark_gray"], self.__command_input_box)
			# test
			self.test_button.draw_button(display, True)
		# draw_notch
		self.__notch_button.x = current_x - self.__notch_button.width - self.__notch_width/2
		self.__notch_button.draw_button(display=display)
		pygame.draw.rect(display, self.__notch_color, (current_x - self.__notch_width, self.__y, self.__notch_width, self.__height))
		

	# check sidebar openning/closing
	def check_event(self, event):
		if self.__notch_button.click(event):
			self.__is_open = not self.__is_open
			self.__notch_button.switch_state()