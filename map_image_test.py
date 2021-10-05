#### elemet rotation
# l = [1, 2, 3]

# tmp = l.pop()
# l.insert(0, tmp)

# print(l)



#### state
# class State:
# 	def __init__(self, label, value):
# 		self.label = label
# 		self.value = value		

# is_play_list = [State('Playing', True), State('Paused', False)]
# speed_list = [State('Slow', 300), State('Normal', 200), State('Fast', 100)]


#### image
import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

source_image = pygame.image.load('thailand_map.png')
image = pygame.transform.scale(source_image, (500, 500))

zoom_scale = 2
scale = 1
zoom = False
print([a*scale for a in image.get_size()])

top_left_point = (0, 0)
circle_position = (100, 100)



run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			# zoom in
			if pygame.mouse.get_pressed()[0]:
				zoom = True
				scale = zoom_scale
				tmp = tuple(int(a*zoom_scale) for a in image.get_size())
				image = pygame.transform.scale(source_image, tmp)
				# top_left_point = pygame.mouse.get_pos()
			# zoom out
			elif pygame.mouse.get_pressed()[2]:
				zoom = False
				scale = 1
				tmp = tuple(int(a/zoom_scale) for a in image.get_size())
				image = pygame.transform.scale(source_image, tmp)

	# fill background
	win.fill((255, 255, 255))

	# draw map
	win.blit(image, top_left_point)

	# draw airport
	circle_x = top_left_point[0] + circle_position[0]
	circle_y = top_left_point[1] + circle_position[1]
	pygame.draw.circle(win, (0, 255, 0), (circle_x*scale, circle_y*scale), 10)

	pygame.display.update()

pygame.quit()



# #### edit tuple
# class Airport:
# 	def __init__(self, x):
# 		self.x = x

# t = (Airport(0), Airport(1))
# for a in t:
# 	print(a.x)

# print('edit')

# for a in t:
# 	a.x = 555

# for a in t:
# 	print(a.x)

# l = []
# print(dir(l))