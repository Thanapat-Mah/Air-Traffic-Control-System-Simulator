import pygame

### RGB code for every color used in program
class Color:
	black = (28, 28, 28)
	dark_gray = (57, 62, 70)
	light_gray = (194, 194, 194)
	white = (255, 255, 255)
	pink = (255, 82, 96)

pygame.font.init()
### pygame.font.Font object in specific font and size
class Font:
	roboto_normal = pygame.font.Font('assets/fonts/Roboto-Regular.ttf', 24)