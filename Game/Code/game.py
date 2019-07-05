import pygame
import random
import sys

def game():

	# Colours
	black = (0, 0, 0)
	white = (255, 255, 255)
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)

	pygame.font.init()
	font = pygame.font.Font(pygame.font.get_default_font(), 30)

	FPS = 60

	maxHealth = 600
	currHealth = 600

	playerHealth = 20
	playerCurrent = 4

	"""Player Stats"""
	#import from player class generated by the main menu, shop purchases
	Health = 20
	Speed = 5
	Gun = 10
	Knife = 5


	"""Stop timer conditions"""
	win = False
	pause = True
	quit = False

	x=20
	y=275
	w=30
	h=30
	g=1
	r=2.5
	v=0
	s=Speed

	pygame.init()
	screen=pygame.display.set_mode((800,600))
	pygame.display.set_caption("Game")


	while not quit:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					stop_condition = "quit"
					quit = True

		if win:
			pygame.time.delay(50)
			wintext = font.render('YOU WIN!', True, white)
			wintext2 = font.render('Press m to return to menu', True, white)
			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return("quit")
					quit = True

			if keys[pygame.K_m]:
				return("win")

			screen.blit(wintext,(300,200))
			screen.blit(wintext2,(220,300))
			pygame.display.update()

		while pause: 
			pygame.time.delay(50)
			pausetext = font.render('Press space to play', True, white)
			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					stop_condition = "quit"
					quit = True

			if keys[pygame.K_SPACE]:
				pause = False

			screen.blit(pausetext,(300,300))
			pygame.display.update()

		while not pause and not win:

			pygame.time.delay(50)
			stop_condition = None

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return("quit")
					quit = True

			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				x -= s
			if keys[pygame.K_RIGHT]:
				x += s
			if keys[pygame.K_DOWN]:
				v -= r
			v += g

			y -= v


			if keys[pygame.K_q]:
				currHealth -= Gun

			if keys[pygame.K_p]:
				pause = True

			if keys[pygame.K_z]:
				playerCurrent -= 1

			if x < 0 or x > 770 or y < 50 or y > 570 or playerCurrent < 1:
				return(0)
				#death screen here
				pygame.QUIT()

			if currHealth < 1:
				win = True
			bossHP = font.render('%d / %d' %(currHealth, maxHealth), True, (120,120,200))

			screen.fill(black)

			pygame.draw.rect(screen, red, (0,0,800,50))
			pygame.draw.rect(screen, green, (0,0,currHealth/maxHealth*800,50))
			pygame.draw.rect(screen, red, (0,550,200,50))
			pygame.draw.rect(screen, green, (0,550,playerCurrent/playerHealth*200,50))
			pygame.draw.rect(screen, blue, (x, y, w, h))

			screen.blit(bossHP,(350,0))

			pygame.display.update()