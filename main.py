import pygame
from configuration import MAP_PATH
from screen import Screen
from toolbar import Toolbar
from sidebar import Sidebar
from simulator import Simulator
from map import Map  
from airport import Airport, AirportManager


def simulate(screen, toolbar, sidebar, airport_manager, map_, simulator):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			else:
				toolbar.check_event(event, simulator)
				sidebar.check_event(event)
				map_.check_event(event, simulator)

		# update screen to next frame
		simulator.tick_time()
		screen.update_screen(simulator=simulator, toolbar=toolbar, sidebar=sidebar, airport_manager=airport_manager, map_=map_)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	pygame.init()
	screen = Screen(fullscreen=True)
	simulator = Simulator(name="Air Traffic Control SysStem Simulator")
	toolbar = Toolbar(screen_size=screen.get_size(), simulator=simulator)
	sidebar = Sidebar(screen_size=screen.get_size(), toolbar_height=toolbar.get_height())
	map_ = Map(image_path=MAP_PATH, screen_size=screen.get_size())
	airport_manager = AirportManager(screen_size=screen.get_size())
	simulate(screen, toolbar, sidebar, airport_manager, map_, simulator)