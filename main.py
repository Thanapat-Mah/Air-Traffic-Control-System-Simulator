import pygame
from screen import Screen

def play_game(screen):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# update screen to next frame
		screen.update_screen()
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	pygame.init()

	screen = Screen()

	play_game(screen)