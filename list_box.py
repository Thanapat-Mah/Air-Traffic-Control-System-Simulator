import pygame
from configuration import COLOR, FONT
from button import Button, StatusButton
import math

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
		# adjust rect (hit box) of each topic
		topic_height = self.__font.render(self.__menu_topic_tuple[0], True, self.__text_color).get_size()[1]
		self.__menu_topic_rect = (
			pygame.Rect(self.__x, self.__y, int(self.__width/2), topic_height+20),
			pygame.Rect(self.__x+int(self.__width/2), self.__y, int(self.__width/2), topic_height+20)
			)
		self.__selected_topic = self.__menu_topic_tuple[1]
		self.__non_selected_topic_color = non_selected_topic_color
		self.__selected_page = 1
		self.__all_page_count = 1	
		page_number_width = self.__font.render("1/2", True, self.__text_color).get_size()[0]*2
		page_button_y = self.__y+self.__height-40
		self.__switch_page_button = (
			Button(x=self.__x+int((self.__width-page_number_width)/2)-40, y=page_button_y, width=40, height=30,text="<<",
				font=self.__font, background_color=self.__background_color, border_color=self.__text_color, border_size=1),
			Button(x=self.__x+int((self.__width+page_number_width)/2), y=page_button_y, width=40, height=30, text=">>",
				font=self.__font, background_color=self.__background_color, border_color=self.__text_color, border_size=1)
			)		
		# calculate button per page
		self.__status_button_padding = 10
		self.__status_button_height = 40
		status_button_height_space = page_button_y - (self.__menu_topic_rect[0].bottomleft[1])
		self.__status_button_per_page = math.floor(status_button_height_space/(self.__status_button_height+self.__status_button_padding))
		self.__status_button_list = []

	def update_button(self, airport_status_list=None, plane_manager=None):
		# choose status button between flight list and airport list
		if self.__selected_topic == self.__menu_topic_tuple[0]:
			pass
		elif self.__selected_topic == self.__menu_topic_tuple[1]:
			status_list = airport_status_list
		# adjust selected page and all page count according to status_list
		self.__all_page_count = math.ceil(len(status_list)/self.__status_button_per_page)
		while (self.__selected_page != 1) and (self.__selected_page > self.__all_page_count):
			self.__selected_page -= 1
		# create status button only those which will be displayed
		first_displayed_index = (self.__selected_page-1)*self.__status_button_per_page
		displayed = status_list[first_displayed_index : first_displayed_index + self.__status_button_per_page]
		self.__status_button_list = []
		status_button_y = self.__menu_topic_rect[0].bottomleft[1] + self.__status_button_padding
		for item in displayed:
			self.__status_button_list.append(
				StatusButton(x=self.__x+self.__status_button_padding, y=status_button_y,
					width=self.__width-2*self.__status_button_padding, height=self.__status_button_height,
					code=item["code"], detail=item["detail"])
				)
			status_button_y += self.__status_button_height + self.__status_button_padding

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
		# draw status button
		for status_button in self.__status_button_list:
			status_button.draw_button(display)
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
						self.__selected_page = 1
		# check for change page
		if self.__switch_page_button[0].click(event):
			if self.__selected_page > 1:
				self.__selected_page -= 1
		elif self.__switch_page_button[1].click(event):
			if self.__selected_page < self.__all_page_count:
				self.__selected_page += 1