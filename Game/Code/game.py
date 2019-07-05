import pygame
import random
import sys

def main():

	FPS = 60

	"""Stop timer conditions"""
	alive = True
	boss = True
	pause = False
	quit = False

	x=10
	y=285
	w=30
	h=30
	g=1
	r=5
	v=0
	s=2.5

	while not quit:

		pygame.init()
		screen=pygame.display.set_mode((800,600))
		pygame.display.set_caption("Game")

		pygame.time.delay(50)
		stop_condition = None

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				stop_condition = "quit"
				quit = True

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			x -= s
		if keys[pygame.K_RIGHT]:
			x += s
		if keys[pygame.K_DOWN]:
			v -= s
		v += g

		y -= v

		screen.fill((0,0,0))

		pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h))

		pygame.display.update()


	return stop_condition




if __name__ == '__main__':
	main()