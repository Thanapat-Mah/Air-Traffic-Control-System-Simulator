import pygame
from color import Color

### screen of program, adjust and display component.
class Screen:
	def __init__(self, fullscreen=False, width=1500, height=750, background_color=Color.dark_gray):
		self.fullscreen = fullscreen
		# if fullsreen, adjust width and height to fit user's display size
		if fullscreen:
			info_object = pygame.display.Info()
			self.width = info_object.current_w
			self.height = info_object.current_h
		else:
			self.width = width
			self.height = height
		self.background_color = background_color
		self.display = pygame.display.set_mode((self.width, self.height))

	# refresh plain color background
	def refresh_background(self):
		self.display.fill(self.background_color)

	# update screen by re-draw every components
	def update_screen(self):
		self.refresh_background()