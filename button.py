import pygame
from configuration import COLOR, FONT

### button UI
class Button:
	def __init__(self, x, y, width, height, border_size=3, border_color=COLOR["dark_gray"], border_radius=5,
		background_color=COLOR["black"], text="Button", font=FONT["roboto_normal"], text_color=COLOR["white"]):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.border_size = border_size			# border_size = 0 means no border
		self.border_color = border_color
		self.border_radius = border_radius
		self.background_color = background_color
		self.text = text
		self.font = font
		self.text_color = text_color
		self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)

	# draw button with text
	def draw_button(self, display):
		# adjust hit box and text on button
		self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
		self.text_surface = self.font.render(self.text, True, self.text_color)
		# draw button background and border
		pygame.draw.rect(display, self.background_color, self.hit_box, width=0, border_radius=self.border_radius)
		if self.border_size != 0:
			pygame.draw.rect(display, self.border_color, self.hit_box, width=self.border_size, border_radius=self.border_radius)
		# draw text on center of button
		padding_x = (self.width - self.text_surface.get_size()[0])/2
		padding_y = (self.height - self.text_surface.get_size()[1])/2
		display.blit(self.text_surface, (self.x+padding_x, self.y+padding_y))

	# return True when button is clicked by left mouse button
	def click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:		# left mouse clicked
				if self.hit_box.collidepoint(x, y):
					return(True)
		return(False)

class ExitButton(Button):
	# overide default style of button
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, border_size=0, background_color=COLOR["pink"], text="Exit")

	# quit program when button is clicked by left mouse button
	def click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.hit_box.collidepoint(x, y):
					quit()

class MultiStateButton(Button):
	def __init__(self, label_tuple, icon_tuple=None, *args, **kwargs):
		super(MultiStateButton, self).__init__(*args, **kwargs)
		if icon_tuple == None:
			icon_tuple = tuple(None for i in range(len(label_tuple)))
		if len(label_tuple) != len(icon_tuple):
			return(False)
		# begin at first state, first label and first icon
		self.state = 0
		self.label_tuple = label_tuple
		self.text = label_tuple[0]
		self.icon_tuple = icon_tuple
		self.icon = icon_tuple[0]

	# switch buttons state to next state
	def switch_state(self):
		if self.state == len(self.label_tuple) - 1:
			self.state = 0
		else:
			self.state += 1
		self.text = self.label_tuple[self.state]
		self.icon = self.icon_tuple[self.state]

	def draw_button(self, display):
		# adjust hit box and text on button
		self.hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
		self.text_surface = self.font.render(self.text, True, self.text_color)
		# draw button background and border
		pygame.draw.rect(display, self.background_color, self.hit_box, width=0, border_radius=self.border_radius)
		if self.border_size != 0:
			pygame.draw.rect(display, self.border_color, self.hit_box, width=self.border_size, border_radius=self.border_radius)
		# draw text and icon on center of button
		# if this button have icon
		if self.icon != None:
			text_x = (self.width - self.text_surface.get_size()[0] - self.icon.get_size()[0] - 10)/2
			icon_x = text_x + self.text_surface.get_size()[0] + 10
			icon_y = (self.height - self.icon.get_size()[1])/2
			display.blit(self.icon, (self.x+icon_x, self.y+icon_y))
		# if this button have no icon
		else:
			text_x = (self.width - self.text_surface.get_size()[0])/2
		text_y = (self.height - self.text_surface.get_size()[1])/2
		display.blit(self.text_surface, (self.x+text_x, self.y+text_y))