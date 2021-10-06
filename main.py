import pygame
from screen import Screen
from font import Font
from color import Color
from toolbar import Toolbar
from sidebar import Sidebar

def simulate(screen, toolbar, sidebar):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			else:
				toolbar.check_event(event)

		# update screen to next frame
		screen.update_screen(toolbar=toolbar, sidebar=sidebar)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	pygame.init()

	screen = Screen(fullscreen=True)
	toolbar = Toolbar(screen_size=screen.get_size())
	sidebar = Sidebar(screen_size=screen.get_size(), toolbar_height=toolbar.get_height())

	simulate(screen, toolbar, sidebar)