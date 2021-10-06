import pygame
from color import Color
from font import Font

### button UI
class Button:
	def __init__(self, x, y, width, height, border_size=2, border_color=Color.light_gray, border_radius=5,
		background_color=Color.dark_gray, text="Button", font=Font.roboto_normal, text_color=Color.white):
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

class QuitButton(Button):
	# overide default style of button
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, border_size=0, background_color=Color.pink, text="Exit")

	# return True when button is clicked by left mouse button
	def click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self.hit_box.collidepoint(x, y):
					quit()

class MultiStateButton(Button):
	def __init__(self, icon_tuple, *args, **kwargs):
		super(MultiStateButton, self).__init__(*args, **kwargs)
		self.icon_tuple = icon_tuple