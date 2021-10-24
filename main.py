import pygame
from configuration import MAP_PATH, PLANE_PATH
from screen import Screen
from toolbar import Toolbar
from sidebar import Sidebar
from simulator import Simulator
from map import Map
from airport import AirportManager
from plane import PlaneManager

def simulate(screen, toolbar, sidebar, airport_manager, map_, simulator,plane_manager):
	run = True
	while run:
		# check for every event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			else:
				simulator.check_selection(event, plane_manager=plane_manager, airport_manager=airport_manager, sidebar=sidebar)
				toolbar.check_event(event, simulator=simulator)
				sidebar.check_event(event)
				map_.check_event(event, simulator=simulator)

		# update screen to next frame
		plane_manager.generate_new_plane(airport_manager=airport_manager)
		simulator.update_simulator(airport_manager=airport_manager, plane_manager=plane_manager, sidebar=sidebar)
		screen.update_screen(simulator=simulator, toolbar=toolbar, sidebar=sidebar, airport_manager=airport_manager, map_=map_, plane_manager = plane_manager)
		pygame.display.update()

	pygame.quit()
	
if __name__ == "__main__":
	pygame.init()
	screen = Screen(fullscreen=True)
	simulator = Simulator(name="Air Traffic Control System Simulator")
	toolbar = Toolbar(screen_size=screen.get_size(), simulator=simulator)
	sidebar = Sidebar(screen_size=screen.get_size(), toolbar_height=toolbar.get_height())
	map_ = Map(image_path=MAP_PATH, screen_size=screen.get_size())
	airport_manager = AirportManager()
	plane_manager = PlaneManager(image_path=PLANE_PATH)
	simulate(screen, toolbar, sidebar, airport_manager, map_, simulator, plane_manager)
