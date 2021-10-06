import pygame

def adjust_size(icon, height_limit):
	width, height = icon.get_size()
	scale = height_limit/height
	return(pygame.transform.scale(icon, (int(width*scale), int(height*scale))))

# load icons used in button
def load_icons(height_limit, *name):
	icons_tuple = tuple(adjust_size(pygame.image.load("assets/icons/"+n), height_limit) for n in name)
	return(icons_tuple)