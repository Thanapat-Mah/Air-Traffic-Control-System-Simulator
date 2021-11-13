import pygame
from configuration import COLOR, FONT, ICON_PATH
from button import ExitButton, MultiStateButton
from utilities import Loader

### toolbar at bottom side of screen, provide tool for modify simulation behavior
class Toolbar:
	def __init__(self, screen_size, simulator, height=50, background_color=COLOR["black"], font=FONT["roboto_normal"], datetime_color=COLOR["white"]):
		self.__x = 0
		self.__y = screen_size[1] - height	# adjust position to buttom of screen
		self.__width = screen_size[0]
		self.__height = height
		self.__background_color = background_color
		self.__font = font
		self.__datetime_color = datetime_color
		# initiate control button
		button_y_padding = 10
		loader = Loader()
		self.__play_pause_button = MultiStateButton(label_tuple=("Playing", "Paused"),
			icon_tuple=loader.load_icons(self.__height-button_y_padding*2-12, ICON_PATH["pause"], ICON_PATH["play"]),
			x=220, y=self.__y+button_y_padding, width=120, height=self.__height-button_y_padding*2)
		self.__speed_button = MultiStateButton(label_tuple=("Speed", "Speed", "Speed"),
			icon_tuple=loader.load_icons(self.__height-button_y_padding*2-12, ICON_PATH["speed1"], ICON_PATH["speed2"], ICON_PATH["speed3"]),
			x=350, y=self.__y+button_y_padding, width=150, height=self.__height-button_y_padding*2)
		self.__zoom_button = MultiStateButton(label_tuple=("Zoom", "Zoom"),
			icon_tuple=loader.load_icons(self.__height-button_y_padding*2-12, ICON_PATH["zoom_in"], ICON_PATH["zoom_out"]),
			x=510, y=self.__y+button_y_padding, width=110, height=self.__height-button_y_padding*2)
		self.__exit_button = ExitButton(x=self.__width-90, y=self.__y+button_y_padding, width=80, height=self.__height-button_y_padding*2)

	# getter for toolbar height
	def get_height(self):
		return(self.__height)

	# draw simulated datetime on toolbar
	def draw_datetime(self, display, simulated_datetime):
		text = simulated_datetime.strftime("%d %b %Y | %I:%M %p")
		text_surface = self.__font.render(text, True, self.__datetime_color)
		display.blit(text_surface, (20, self.__y+(self.__height-text_surface.get_size()[1])/2))

	# draw button on toolbar
	def draw_button(self, display):
		self.__play_pause_button.draw_button(display)
		self.__speed_button.draw_button(display)
		self.__zoom_button.draw_button(display)
		self.__exit_button.draw_button(display)

	# draw all componenets on toolbar
	def draw_toolbar(self, display, simulated_datetime):
		# draw background
		pygame.draw.rect(display, self.__background_color, (self.__x, self.__y, self.__width, self.__height))
		# draw components on top of background
		self.draw_datetime(display, simulated_datetime)
		self.draw_button(display)

	# check event on toolbar
	def check_event(self, event, simulator):
		if self.__play_pause_button.click(event):
			self.__play_pause_button.switch_state()
			simulator.update_state("is_play")
		elif self.__speed_button.click(event):
			self.__speed_button.switch_state()
			simulator.update_state("time_period")
		elif self.__zoom_button.click(event):
			self.__zoom_button.switch_state()
			simulator.update_state("is_zoom")
		self.__exit_button.click(event)