import pygame

pygame.init()

class Plane:
	def __init__(self, text='capybara', x=0, y=100, speed=10):
		self.text = text
		self.x = x
		self.y = y
		self.speed = speed
		self.color = (255, 255, 255)

	def draw(self, win):
		# myfont = pygame.font.SysFont('comicsans', 30)
		myfont = pygame.font.Font('fonts/wakandaforever-regular.ttf', 30)
		text_surface = myfont.render(self.text, 1, self.color)
		win.blit(text_surface, (self.x, self.y))

	def update_position(self):
		self.x += self.speed

p1 = Plane()

period = 1000
win = pygame.display.set_mode((500, 300))
time = 0
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:
				p1.color = (255, 0, 0)
				x, y = pygame.mouse.get_pos()
				p1.x, p1.y = x, y
			elif pygame.mouse.get_pressed()[2]:
				p1.color = (0, 255, 0)
	
	if time%period == 0:
		p1.update_position()	

	time += 1
	
	win.fill((0, 0, 0))
	p1.draw(win)
	pygame.time.delay(1)
	pygame.display.update()

pygame.quit()