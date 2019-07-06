import pygame
import random
import sys
import string
import time
import namer

"""
TODO
Detect collisions with missiles for damage
Bosses will be BIG
Melee damage is BIG
"""

class Projectile(object):
	def __init__(self,x,y,colour,safe):
		self.x=x
		self.y=y
		self.colour=colour
		self.v=25
		self.safe=safe

	def draw(self, screen):
		pygame.draw.circle(screen, self.colour, (self.x, self.y), 2)



import interMission

def game(levelNum, health, ammunition, Mdamage, Rdamage, fuel, money):

	missileTimer = 0
	targettedTimer = 0
	waveTimer = 0

	rangeDmg = 20
	meleeDmg = 80

	ammo = 20
	reloadCount = 1000
	projectiles = []

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

	playerHealth = 40
	playerCurrent = 40

	maxFuel = 1000
	fuel = 1000

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

	health, ammunition, Mdamage, Rdamage, fuel, money = interMission.interMission(screen, health, ammunition, Mdamage, Rdamage, fuel, money, levelNum-1)
	print("Health = %d\nAmmunition = %d\nMdamage = %d\nRdamage = %d\nFuel = %d\nMoney = %d" %(health, ammunition, Mdamage, Rdamage, fuel, money))

	while not quit:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0
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
				return("Win")

			screen.blit(wintext,(300,200))
			screen.blit(wintext2,(220,300))
			pygame.display.update()

		while pause: 
			pygame.time.delay(50)
			pausetext = font.render('Press space to play', True, white)
			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0
					quit = True

			if keys[pygame.K_SPACE]:
				pause = False

			screen.blit(pausetext,(300,300))
			pygame.display.update()

		while not pause and not win:

			pygame.time.delay(50)
			stop_condition = None

			for projectile in projectiles:
				if projectile.x > 0 and projectile.x < 800 and projectile.safe == 1:
					projectile.x += projectile.v
				elif projectile.x >= 0 and projectile.x <= 800 and projectile.safe == 0:
					projectile.x -= projectile.v
				else:
					projectiles.pop(projectiles.index(projectile))

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0
					quit = True

			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				x -= s
			if keys[pygame.K_RIGHT]:
				x += s
			if keys[pygame.K_DOWN]:
				if fuel > 0:
					fuel -= 5
					v -= r
			v += g

			y -= v

			if keys[pygame.K_w]:
				reloadCount += 2
				if reloadCount > 5 and ammo > 0:
					ammo -= 1
					projectiles.append(Projectile(int(x), int(y), blue, 1))
					reloadCount = 0


			if keys[pygame.K_q]:
				currHealth -= Gun

			if keys[pygame.K_p]:
				pause = True

			if keys[pygame.K_z]:
				playerCurrent -= 1

			if x < 0 or x > 770 or y < 50 or y > 570 or playerCurrent < 1:
				return 0
				#death screen here
				pygame.QUIT()

			if currHealth < 1:
				win = True
			bossHP = font.render('%d / %d' %(currHealth, maxHealth), True, (120,120,200))
			ammoText = font.render('%d' %(ammo), True, (0,0,0))

			"""Enemy attacks here"""

			if missileTimer > 10:
				missileTimer = 0
				projectiles.append(Projectile(799, random.randrange(1, 549), red, 0))

			if targettedTimer > 14:
				targettedTimer = 0
				projectiles.append(Projectile(799, int(y), red, 0))

			if waveTimer > 30:
				waveTimer = 0
				center = random.randrange(100, 450)
				for i in range(8):
					j = (i-4)*10
					projectiles.append(Projectile(799, center + j, red, 0))

			waveTimer +=1
			targettedTimer += 1
			missileTimer += 1
			screen.fill(black)

			pygame.draw.rect(screen, red, (0,0,800,50))
			pygame.draw.rect(screen, green, (0,0,currHealth/maxHealth*800,50))
			pygame.draw.rect(screen, red, (0,550,200,50))
			pygame.draw.rect(screen, green, (0,550,playerCurrent/playerHealth*200,50))
			pygame.draw.rect(screen, (100, 100, 100), (750,400,50,200))
			pygame.draw.rect(screen, blue, (750,400,50,fuel/maxFuel*200))
			pygame.draw.rect(screen, blue, (x, y, w, h))
			for p in projectiles:
				p.draw(screen)

			screen.blit(ammoText, (10,0))
			screen.blit(bossHP,(350,0))
			pygame.display.update()
game()