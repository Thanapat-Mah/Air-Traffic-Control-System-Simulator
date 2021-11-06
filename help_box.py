import pygame
from configuration import COLOR, FONT, HELP_PATH
from utilities import Loader
from button import Button

### help box displaying multiple picture
class HelpBox:
	def __init__(self, x, y, width, height, border_radius=10, background_color=COLOR["transparance_black"],
		topic="Command Help", font=FONT["roboto_small"], text_color=COLOR["white"]):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
		self.__topic = topic
		self.__font = font
		self.__text_color = text_color
		loader = Loader()
		self.__contents = loader.load_icons(self.__width, *(HELP_PATH[key] for key in HELP_PATH))
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
		# can switch page only when it is opened
		if is_open:
			# check for change page
			if self.__switch_page_button[0].click(event):
				if self.__selected_page > 1:
					self.__selected_page -= 1
			elif self.__switch_page_button[1].click(event):
				if self.__selected_page < self.__all_page_count:
					self.__selected_page += 1

	# draw help box
	def draw_help_box(self, display, is_open=False):
		# draw only help box is open
		if is_open:
			# draw transparent background
			pygame.draw.rect(self.__background_surface, self.__background_color, self.__background_surface.get_rect(), border_radius=self.__border_radius)
			# draw topic
			topic_surface = self.__font.render(self.__topic, True, self.__text_color)
			topic_x = (self.__width - topic_surface.get_size()[0])/2
			self.__background_surface.blit(topic_surface, (topic_x, 20))
			# draw content
			content_surface = self.__contents[self.__selected_page-1]
			content_x = (self.__width - content_surface.get_size()[0])/2
			content_y = 40 + topic_surface.get_size()[1]
			self.__background_surface.blit(content_surface, (content_x, content_y))
			# draw background surface
			display.blit(self.__background_surface, (self.__x, self.__y))
			# draw page number
			page_text_surface = self.__font.render(f"{self.__selected_page}/{self.__all_page_count}", True, self.__text_color)
			left_switch_button = self.__switch_page_button[0]
			display.blit(page_text_surface,
				(self.__x+(self.__width-page_text_surface.get_size()[0])/2,
				left_switch_button.y+(left_switch_button.height-page_text_surface.get_size()[1])/2))
			# draw switch page button
			for button in self.__switch_page_button:
				button.draw_button(display=display)