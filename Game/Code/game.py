import pygame
import random
import string
import time
import namer
import sys

"""
TODO
Detect collisions with missiles for damage
Bosses will be BIG
Melee damage is BIG
"""

hi = 1

class Projectile(object):
	def __init__(self,x,y,safe):
		self.x=x
		self.y=y
		self.colour=(255, 0, 0)
		self.v=15
		self.safe=safe

	def draw(self, screen):
		if self.safe == 1:
			hi = None
			#pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 2)
		elif self.safe == 0:
			pygame.draw.circle(screen, self.colour, (self.x, self.y), 2)



import interMission

def game(screen, levelNum, health, ammunition, Mdamage, Rdamage, fuel, money):

	# Colours
	black = (0, 0, 0)
	white = (255, 255, 255)
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)

	health, ammunition, Mdamage, Rdamage, fuel, money = interMission.interMission(screen, health, ammunition, Mdamage, Rdamage, fuel, money, levelNum-1)
	print("Health = %d\nAmmunition = %d\nMdamage = %d\nRdamage = %d\nFuel = %d\nMoney = %d" %(health, ammunition, Mdamage, Rdamage, fuel, money))
	screen.fill(black)

	missileTimer = 0
	targettedTimer = 0
	waveTimer = 0

	rangeDmg = Rdamage*20
	meleeDmg = Mdamage*60
	ammo = ammunition
	maxFuel = fuel * 100
	currFuel = maxFuel

	reloadCount = 1000
	projectiles = []

	pygame.font.init()
	font = pygame.font.Font(pygame.font.get_default_font(), 30)

	FPS = 60

	maxHealth = 400 * levelNum**2
	currHealth = maxHealth

	playerHealth = health
	playerCurrent = playerHealth

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

	weapon = 0
	switchTimer=10

	gun1=pygame.image.load("../Images/Sprites/main_sprite/gun/gun1.png")
	gun2=pygame.image.load("../Images/Sprites/main_sprite/gun/gun2.png")
	gun3=pygame.image.load("../Images/Sprites/main_sprite/gun/gun3.png")
	spike1=pygame.image.load("../Images/Sprites/main_sprite/spike/spike1.png")
	spike2=pygame.image.load("../Images/Sprites/main_sprite/spike/spike2.png")
	spike3=pygame.image.load("../Images/Sprites/main_sprite/spike/spike3.png")
	currSprite = gun1

	while not quit:
		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0, levelNum, health, ammunition, Mdamage, Rdamage, fuel, money
					quit = True

		if win:
			pygame.time.delay(50)
			wintext = font.render('YOU WIN!', True, white)
			wintext2 = font.render('Press m to return to menu', True, white)
			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return "quit", levelNum, health, ammunition, Mdamage, Rdamage, fuel, money
					quit = True

			if keys[pygame.K_m]:
				money = int(money)
				money += 200
				return "Win", levelNum, health, ammunition, Mdamage, Rdamage, fuel, money

			screen.blit(wintext,(300,200))
			screen.blit(wintext2,(220,300))
			pygame.display.update()

		while pause: 
			pygame.time.delay(50)
			pausetext = font.render('Press space to play', True, white)
			keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0, levelNum, health, ammunition, Mdamage, Rdamage, fuel, money
					quit = True

			if keys[pygame.K_SPACE]:
				pause = False

			screen.blit(pausetext,(300,300))
			pygame.display.update()

		while not pause and not win:

			if currSprite == gun2:
				currSprite = gun3
			if currSprite == gun3:
				currSprite = gun1

			if currSprite == spike2:
				currSprite = spike3
			if currSprite == spike3:
				currSprite = spike1

			pygame.time.delay(50)
			stop_condition = None

			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return 0, levelNum, health, ammunition, Mdamage, Rdamage, fuel, money
					quit = True

			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				x -= s
			if keys[pygame.K_RIGHT]:
				x += s
			if keys[pygame.K_DOWN]:
				if currFuel > 0:
					currFuel -= 5
					v -= r
			v += g
			y -= v

			if keys[pygame.K_q]:
				if weapon == 0:
					currSprite = gun2
					if x > 650:
						currHealth -= meleeDmg
					else:
						playerCurrent -= 1
				if weapon == 1:
					currSprite = spike2
					reloadCount += 2
					if reloadCount > 5 and ammo > 0:
						ammo -= 1
						projectiles.append(Projectile(int(x), int(y), 1))
						reloadCount = 0

			switchTimer += 1
			if keys[pygame.K_TAB]:
				if switchTimer > 5:
					switchTimer=0
					if weapon == 1:
						weapon = 0
						currSprite = gun1
					elif weapon == 0:
						weapon = 1
						currSprite = spike1

			if keys[pygame.K_p]:
				pause = True

			if keys[pygame.K_z]:
				playerCurrent -= 1

			if x < 0 or x > 770 or y < 50 or y > 570 or playerCurrent < 1:
				return 0, levelNum, health, ammunition, Mdamage, Rdamage, fuel, money
				#death screen here
				pygame.QUIT()

			if currHealth < 1:
				win = True
			bossHP = font.render('%d / %d' %(currHealth, maxHealth), True, (120,120,200))
			ammoText = font.render('%d' %(ammo), True, (0,0,0))

			"""Enemy attacks here"""

			if missileTimer > 10:
				missileTimer = 0
				projectiles.append(Projectile(799, random.randrange(1, 549), 0))

			if targettedTimer > 14:
				targettedTimer = 0
				projectiles.append(Projectile(799, int(y), 0))

			if waveTimer > 30:
				waveTimer = 0
				center = random.randrange(100, 450)
				for i in range(8):
					j = (i-4)*10
					projectiles.append(Projectile(799, center + j, 0))

			waveTimer +=1
			targettedTimer += 1
			missileTimer += 1
			spike=pygame.image.load("../Images/Sprites/main_sprite/spike/spike.png")
			spike = pygame.transform.scale(spike, (64,40))
			screen.fill(black)

			currSpriteDisplay = pygame.transform.scale(currSprite, (64,40))
			pygame.draw.rect(screen, red, (0,0,800,50))
			pygame.draw.rect(screen, green, (0,0,currHealth/maxHealth*800,50))
			pygame.draw.rect(screen, red, (0,550,200,50))
			pygame.draw.rect(screen, green, (0,550,playerCurrent/playerHealth*200,50))
			pygame.draw.rect(screen, (100, 100, 100), (750,400,50,200))
			pygame.draw.rect(screen, blue, (750,400,50,currFuel/maxFuel*200))
			screen.blit(currSpriteDisplay, (x, y))
			for projectile in projectiles:
				if projectile.x > 0 and projectile.x < 800 and projectile.safe == 1:
					projectile.x += projectile.v
				elif projectile.x >= 0 and projectile.x <= 800 and projectile.safe == 0:
					projectile.x -= projectile.v
				else:
					projectiles.pop(projectiles.index(projectile))
				projectile.draw(screen)
				if projectile.safe == 1:
					screen.blit(spike, (projectile.x, projectile.y))
					if projectile.x > 700:
						if projectile.y > 200 and projectile.y < 400:
							currHealth -= rangeDmg
							projectiles.pop(projectiles.index(projectile))
				if projectile.safe == 0:
					if projectile.x <= x + 5 and projectile.x >= x-5:
						if projectile.y < y + 5 and projectile.y > y-5:
							playerCurrent -= 1
							projectiles.pop(projectiles.index(projectile))

			screen.blit(ammoText, (10,0))
			screen.blit(bossHP,(350,0))
			pygame.display.update()