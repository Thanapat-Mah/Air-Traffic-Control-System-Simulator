import pygame
from color import Color
from font import Font
from button import Button
from button import QuitButton
from button import MultiStateButton
from icon_loader import *

### toolbar at bottom side of screen, provide tool for modify simulation behavior
class Toolbar:
	def __init__(self, screen_size, simulator, height=80, background_color=Color.black, font=Font.roboto_normal, datetime_color=Color.white):
		self.__x = 0
		self.__y = screen_size[1] - height	# adjust position to buttom of screen
		self.__width = screen_size[0]
		self.__height = height
		self.__background_color = background_color
		self.__font = font
		self.__datetime_color = datetime_color
		# initiate play-pause button
		button_y_padding = 15
		self.__play_pause_button = MultiStateButton(label_tuple=tuple(state[0] for state in simulator.get_state("play_pause")),
			icon_tuple=load_icons(25, "icon_paused.png", "icon_playing.png"),
			x=290, y=self.__y+button_y_padding, width=150, height=self.__height-button_y_padding*2)
		self.__speed_button = MultiStateButton(label_tuple=tuple(state[0] for state in simulator.get_state("speed")),
			icon_tuple=load_icons(25, "icon_speed_1.png", "icon_speed_2.png", "icon_speed_3.png"),
			x=450, y=self.__y+button_y_padding, width=180, height=self.__height-button_y_padding*2)
		self.__zoom_button = MultiStateButton(label_tuple=tuple(state[0] for state in simulator.get_state("zoomed")),
			icon_tuple=load_icons(25, "icon_zoom_in.png", "icon_zoom_out.png"),
			x=640, y=self.__y+button_y_padding, width=130, height=self.__height-button_y_padding*2)
		self.__quit_button = QuitButton(x=self.__width-120, y=self.__y+button_y_padding, width=100, height=self.__height-button_y_padding*2)

	# getter for toolbar's height
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
		self.__quit_button.draw_button(display)

	# draw all componenets on toolbar
	def draw_toolbar(self, display, simulated_datetime):
		# draw background
		pygame.draw.rect(display, self.__background_color, (self.__x, self.__y, self.__width, self.__height))
		self.draw_datetime(display, simulated_datetime)
		self.draw_button(display)

	# check event on toolbar
	def check_event(self, event, simulator):
		if self.__play_pause_button.click(event):
			self.__play_pause_button.switch_state()
			simulator.update_state("play_pause")
		elif self.__speed_button.click(event):
			self.__speed_button.switch_state()
			simulator.update_state("speed")
		elif self.__zoom_button.click(event):
			self.__zoom_button.switch_state()
			simulator.update_state("zoomed")
		self.__quit_button.click(event)
