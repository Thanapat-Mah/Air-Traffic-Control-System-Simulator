import pygame
from screen import Screen
# from font import Font
from toolbar import Toolbar

def play_game(screen):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			else:
				toolbar.check_event(event)

		# update screen to next frame
		screen.update_screen(toolbar=toolbar)
		# text_surface = Font.roboto_normal.render('Speed 900 km/h', True, (0, 255, 0))
		# screen.display.blit(text_surface, (0, 0))
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	pygame.init()

	screen = Screen(fullscreen=True)
	toolbar = Toolbar(screen_size=screen.get_size(), height=60)

	play_game(screen)