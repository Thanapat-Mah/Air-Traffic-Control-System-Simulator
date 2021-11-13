import pygame
from configuration import COLOR, FONT, ICON_PATH
from utilities import Loader

### button UI
class Button:
	def __init__(self, x, y, width, height, border_size=2, border_color=COLOR["dark_gray"], border_radius=5,
		background_color=COLOR["black"], text="Button", font=FONT["roboto_normal"], text_color=COLOR["white"]):
		self._x = x
		self._y = y
		self._width = width
		self._height = height
		self._border_size = border_size			# border_size = 0 means no border
		self._border_color = border_color
		self._border_radius = border_radius
		self._background_color = background_color
		self._text = text
		self._font = font
		self._text_color = text_color
		self._hit_box = pygame.Rect(self._x, self._y, self._width, self._height)

	def get_y(self):
		return(self._y)

	def get_width(self):
		return(self._width)

	def get_height(self):
		return(self._height)

	def set_x(self, new_x):
		self._x = new_x

	def set_background_color(self, new_background_color):
		self._background_color = new_background_color

	# draw button with text
	def draw_button(self, display):
		# adjust hit box and text on button
		self._hit_box = pygame.Rect(self._x, self._y, self._width, self._height)
		self._text_surface = self._font.render(self._text, True, self._text_color)
		# draw button background and border
		pygame.draw.rect(display, self._background_color, self._hit_box, width=0, border_radius=self._border_radius)
		if self._border_size != 0:
			pygame.draw.rect(display, self._border_color, self._hit_box, width=self._border_size, border_radius=self._border_radius)
		# draw text on center of button
		padding_x = (self._width - self._text_surface.get_size()[0])/2
		padding_y = (self._height - self._text_surface.get_size()[1])/2
		display.blit(self._text_surface, (self._x+padding_x, self._y+padding_y))

	# return True when button is clicked by left mouse button
	def click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:		# left mouse clicked
				if self._hit_box.collidepoint(x, y):
					return(True)
		return(False)

### Exit button used to close the simulator and close program
class ExitButton(Button):
	# overide default style of button
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, border_size=0, background_color=COLOR["pink"], text="Exit")

	# quit program when button is clicked by left mouse button
	def click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				if self._hit_box.collidepoint(x, y):
					quit()

### button with many state with icon
class MultiStateButton(Button):
	def __init__(self, label_tuple, icon_tuple=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if icon_tuple == None:
			icon_tuple = tuple(None for i in range(len(label_tuple)))
		if len(label_tuple) != len(icon_tuple):
			return(False)
		# begin at first state, first label and first icon
		self._state = 0
		self._label_tuple = label_tuple
		self._text = label_tuple[0]
		self._icon_tuple = icon_tuple
		self._icon = icon_tuple[0]

	# switch buttons state to next state
	def switch_state(self):
		if self._state == len(self._label_tuple) - 1:
			self._state = 0
		else:
			self._state += 1
		self._text = self._label_tuple[self._state]
		self._icon = self._icon_tuple[self._state]

	def draw_button(self, display):
		# adjust hit box and text on button
		self._hit_box = pygame.Rect(self._x, self._y, self._width, self._height)
		self._text_surface = self._font.render(self._text, True, self._text_color)
		# if button have only icon, do not draw button background and border
		if self._text != "":
			# draw button background and border
			pygame.draw.rect(display, self._background_color, self._hit_box, width=0, border_radius=self._border_radius)
			if self._border_size != 0:
				pygame.draw.rect(display, self._border_color, self._hit_box, width=self._border_size, border_radius=self._border_radius)
		# draw text and icon on center of button
		# if this button have icon
		if self._icon != None:
			text_x = (self._width - self._text_surface.get_size()[0] - self._icon.get_size()[0] - 10)/2
			icon_x = text_x + self._text_surface.get_size()[0] + 10
			icon_y = (self._height - self._icon.get_size()[1])/2
			display.blit(self._icon, (self._x+icon_x, self._y+icon_y))
		# if this button have no icon
		else:
			text_x = (self._width - self._text_surface.get_size()[0])/2
		text_y = (self._height - self._text_surface.get_size()[1])/2
		display.blit(self._text_surface, (self._x+text_x, self._y+text_y))

### clickable status button for plane and airport on list box on sidebar
class StatusButton(Button):
	def __init__(self, code, detail, icon=Loader.load_image(image_path=ICON_PATH["magnifier"], size=(20, 20)),
		selected_background_color=COLOR["black"], collision_color=COLOR["red"], *args, **kwargs):
		super().__init__(font=FONT["roboto_small"], background_color=COLOR["dark_gray"],
			border_color=COLOR["white"], border_size=1, *args, **kwargs)
		self._code = code
		self._detail = detail
		self._icon = icon
		self._selected_background_color = selected_background_color
		self._collision_color = collision_color
		self._text = str(self._code) + " | " + str(self._detail)

	def get_code(self):
		return(self._code)

	# draw button with fix icon at left
	def draw_button(self, display, is_selected=False, is_collide=False):
		# adjust hit box and text on button
		self._hit_box = pygame.Rect(self._x, self._y, self._width, self._height)
		self._text_surface = self._font.render(self._text, True, self._text_color)
		# draw button background and border
		drawing_background_color = self._background_color
		drawing_border_color = self._border_color
		# check if this button is collide
		if is_collide:
			drawing_background_color = self._collision_color
			drawing_border_color = self._collision_color
		# check if this button is selected
		if is_selected:
			drawing_background_color = self._selected_background_color
		# draw background
		pygame.draw.rect(display, drawing_background_color, self._hit_box, width=0, border_radius=self._border_radius)
		# draw border
		if self._border_size != 0:
			pygame.draw.rect(display, drawing_border_color, self._hit_box, width=self._border_size, border_radius=self._border_radius)
		# draw text on left of button
		padding = (self._height - self._text_surface.get_size()[1])/2
		display.blit(self._text_surface, (self._x+padding, self._y+padding))
		# draw icon on right of button		
		icon_x = self._x + self._width - self._icon.get_size()[0] - padding
		icon_y = self._y + (self._height-self._icon.get_size()[1])/2
		display.blit(self._icon, (icon_x, icon_y))

	def click(self, event):
		if super().click(event):
			return(self._code)
		else:
			return("")