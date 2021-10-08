import pygame
from screen import Screen
from font import Font
from color import Color
from toolbar import Toolbar
from sidebar import Sidebar
from simulator import Simulator
from map import Map


def simulate(screen, toolbar, sidebar, map, simulator):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			else:
				toolbar.check_event(event, simulator)
				sidebar.check_event(event)
				map.check_event(event, simulator)

		# update screen to next frame
		simulator.tick_time()
		screen.update_screen(simulator=simulator, toolbar=toolbar, sidebar=sidebar, map=map)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	pygame.init()

	screen = Screen(fullscreen=True)
	simulator = Simulator(name="Air Traffic Control System Simulator")
	toolbar = Toolbar(screen_size=screen.get_size(), simulator=simulator)
	sidebar = Sidebar(screen_size=screen.get_size(), toolbar_height=toolbar.get_height())
	map = Map(image_path="assets\images\map_full_size.png", screen_size=screen.get_size())
	simulate(screen, toolbar, sidebar, map, simulator)