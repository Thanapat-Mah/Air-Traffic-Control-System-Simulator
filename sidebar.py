import pygame
from configuration import COLOR, FONT
from button import MultiStateButton, StatusButton
from information_box import InformationBox
from list_box import ListBox

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
		self.__notch_button = MultiStateButton(
			label_tuple=("<|", "|>"), x=0, y=(self.__height-60)/2, width=40, height=60,
			border_size=0, border_radius=10, background_color=notch_color
			)
		self.__background_color = background_color
		self.__font = font
		self.__padding = padding
		# align and create components on sidebar
		component_x = self.__x - self.__width + self.__padding
		component_width_space = self.__width - 2*self.__padding
		half_width_space = (component_width_space-padding)/2
		self.__overall_plane_information = InformationBox(
			x=component_x, y=self.__y+self.__padding, width=half_width_space, height=170, topic="Plane", font=self.__font
			)
		self.__overall_airport_information = InformationBox(
			x=component_x+half_width_space+self.__padding, y=self.__y+self.__padding,
			width=half_width_space, height=170, topic="Airport", font=self.__font
			)
		self.__command_input_box = pygame.Rect((0, 0), (component_width_space, 40))
		self.__command_input_box.bottomleft = (component_x, self.__y+self.__height-self.__padding)
		self.__selected_object_detail = InformationBox(
			x=component_x, y=self.__command_input_box.topleft[1]-self.__padding-220,
			width=component_width_space, height=220, topic="Details", font=self.__font
			)
		list_box_y = self.__overall_plane_information.get_corner_point(2)[1]+padding
		list_box_height = self.__selected_object_detail.get_corner_point(0)[1] - list_box_y - padding
		self.__overall_list_box = ListBox(x=component_x, y=list_box_y, width=component_width_space, height=list_box_height)

	# update simulations information on sidebar
	def update_information(self, plane_information, airport_information, selected_object_detail):		
		# update plane information
		overall_plane_information = []
		plane_status_list = []
		for key in plane_information:
			overall_plane_information.append(f"{key}: {len(plane_information[key])}")
			for plane in plane_information[key]:
				plane_status_list.append({"code": plane, "detail": key})
		# update airport information
		overall_airport_information = []		
		airport_status_list = []
		for key in airport_information:
			overall_airport_information.append(f"{key}: {len(airport_information[key])}")
			for airport in airport_information[key]:
				airport_status_list.append({"code": airport, "detail": key})
		# update content in each components
		self.__overall_plane_information.update_content(new_content=overall_plane_information)
		self.__overall_airport_information.update_content(new_content=overall_airport_information)
		self.__overall_list_box.update_button(airport_status_list=airport_status_list, plane_status_list=plane_status_list)
		self.__selected_object_detail.update_content(new_content=selected_object_detail)

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
			# draw list box
			self.__overall_list_box.draw_list_box(display=display, simulator=simulator)
			# draw command box
			pygame.draw.rect(display, COLOR["dark_gray"], self.__command_input_box)
		# draw_notch
		self.__notch_button.x = current_x - self.__notch_button.width - self.__notch_width/2
		self.__notch_button.draw_button(display=display)
		pygame.draw.rect(display, self.__notch_color, (current_x - self.__notch_width, self.__y, self.__notch_width, self.__height))
		
	# check sidebar openning/closing
	def check_event(self, event):
		if self.__notch_button.click(event=event):
			self.__is_open = not self.__is_open
			self.__notch_button.switch_state()
		if self.__is_open:
			self.__overall_list_box.check_event(event=event)
		
	# check if user select (click) status button in list box, return empty string or selected object code
	def check_selection(self, event):
		selected_object_code = ""
		if self.__is_open:
			selected_object_code = self.__overall_list_box.check_selection(event=event)
		return(selected_object_code)