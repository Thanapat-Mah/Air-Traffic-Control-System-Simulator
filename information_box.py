import pygame
from configuration import FONT, COLOR

### static information box for display overall and specific object information on sidebar
class InformationBox:
	def __init__(self, x, y, width, height, border_radius=10, topic="topic", content=[""], padding=10, content_padding=5,
		font=FONT["roboto_normal"], text_color=COLOR["white"], background_color=COLOR["dark_gray"]):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height
		self.__border_radius = border_radius
		self.__topic = topic
		self.__content = content
		self.__padding = padding
		self.__content_padding = content_padding
		self.__font = font
		self.__text_color = text_color
		self.__background_color = background_color

	# return four corner point position
	def get_corner_point(self, index=0):
		corner_point = (
			(self.__x, self.__y),								# top left
			(self.__x+self.__width, self.__y),					# top right
			(self.__x, self.__y+self.__height),					# bottom left
			(self.__x+self.__width, self.__y+self.__height)		# bottom right
			)
		corner_point = corner_point[index]
		return(corner_point)

	# set content in box
	def set_content(self, new_content):
		self.__content = new_content

	# draw information box on screen
	def draw_information_box(self, display):
		# draw background box
		pygame.draw.rect(display, self.__background_color, (self.__x, self.__y, self.__width, self.__height),
			border_radius=self.__border_radius)
		# draw_topic
		topic_surface = self.__font.render(self.__topic, True, self.__text_color)
		x_topic = (self.__width - topic_surface.get_size()[0])/2
		display.blit(topic_surface, (self.__x+x_topic, self.__y+self.__padding))
		# draw content line by line
		if self.__content != None:
			y_position = self.__y + topic_surface.get_size()[1] + self.__padding*2
			for line in self.__content:
				content_surface = self.__font.render(line, True, self.__text_color)
				display.blit(content_surface, (self.__x+self.__padding, y_position))
				y_position += content_surface.get_size()[1] + self.__content_padding