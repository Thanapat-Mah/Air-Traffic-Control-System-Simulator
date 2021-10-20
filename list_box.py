import pygame
from configuration import COLOR, FONT
from button import Button

### list box for contain clickable status box on sidebar
class ListBox:
	def __init__(self, x, y, width, height, border_radius=10, font=FONT["roboto_small"], text_color=COLOR["white"],
		background_color=COLOR["dark_gray"], menu_topic_tuple=("Flight List", "Airport List"), non_selected_topic_color=COLOR["black"]):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__font = font
		self.__text_color = text_color
		self.__background_color = background_color
		self.__menu_topic_tuple = menu_topic_tuple
		topic_height = font.render(menu_topic_tuple[0], True, text_color).get_size()[1]
		self.__menu_topic_rect = (
			pygame.Rect(x, y, int(width/2), topic_height+20),
			pygame.Rect(x+int(width/2), y, int(width/2), topic_height+20)
			)
		self.__selected_topic = menu_topic_tuple[0]
		self.__non_selected_topic_color = non_selected_topic_color
		self.__selected_page = 1
		self.__all_page_count = 1
		self.__button_per_page = 3		
		page_number_width = font.render("1/2", True, text_color).get_size()[0]*2
		self.__switch_page_button = (
			Button(x=x+int((width-page_number_width)/2)-40, y=y+height-40, width=40, height=30,text="<<",
				font=font, background_color=background_color, border_color=text_color, border_size=1),
			Button(x=x+int((width+page_number_width)/2), y=y+height-40, width=40, height=30, text=">>",
				font=font, background_color=background_color, border_color=text_color, border_size=1)
			)
		self.__status_button_list = []

	def update_button(self, airport_manager=None, plane_manager=None):
		pass

	def draw_button(self):
		pass

	def draw_list_box(self, display):
		# draw background of list box
		pygame.draw.rect(display, self.__background_color, (self.__x, self.__y, self.__width, self.__height), border_radius=self.__border_radius)
		# draw topic
		for count in range(0, len(self.__menu_topic_tuple)):
			if self.__menu_topic_tuple[count] != self.__selected_topic:
				# non_selected topic rect
				pygame.draw.rect(display, self.__non_selected_topic_color, self.__menu_topic_rect[count])
				topic_text_color = self.__background_color
			else:
				topic_text_color = self.__text_color			
			# topic text
			topic_text_surface = self.__font.render(self.__menu_topic_tuple[count], True, topic_text_color)
			topic_x = self.__x + count*self.__width/2 + (self.__width/2-topic_text_surface.get_size()[0])/2
			display.blit(topic_text_surface, (topic_x, self.__y+10))
		# page number
		page_text_surface = self.__font.render(f"{self.__selected_page}/{self.__all_page_count}", True, self.__text_color)
		left_switch_button = self.__switch_page_button[0]
		display.blit(page_text_surface,
			(self.__x+(self.__width-page_text_surface.get_size()[0])/2,
			left_switch_button.y+(left_switch_button.height-page_text_surface.get_size()[1])/2))
		# switch page button
		for button in self.__switch_page_button:
			button.draw_button(display)
		

	def check_event(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				# check for change topic
				for count in range(0, len(self.__menu_topic_tuple)):
					if self.__menu_topic_rect[count].collidepoint(x, y):
						self.__selected_topic = self.__menu_topic_tuple[count]
		# check for change page
		if self.__switch_page_button[0].click(event):
			self.__selected_page -= 1
		elif self.__switch_page_button[1].click(event):
			self.__selected_page += 1